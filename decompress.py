import zlib
import struct
from dataclasses import dataclass
from typing import List

@dataclass
class T_delay_tri:
    min: int
    typ: int
    max: int

    @staticmethod
    def from_bytes(data: bytes) -> 'T_delay_tri':
        min_val, typ_val, max_val = struct.unpack('<3i', data)
        return T_delay_tri(min_val, typ_val, max_val)

@dataclass
class T_delay:
    rise: T_delay_tri
    fall: T_delay_tri

    @staticmethod
    def from_bytes(data: bytes) -> 'T_delay':
        rise = T_delay_tri.from_bytes(data[:12])
        fall = T_delay_tri.from_bytes(data[12:24])
        return T_delay(rise, fall)

@dataclass
class Tpin_pair:
    i: int
    o_or_clk: int  # Represents either 'o' or 'clk' depending on the boolean case

    @staticmethod
    def from_bytes(data: bytes) -> 'Tpin_pair':
        i_val, o_or_clk_val = struct.unpack('<2h', data)
        return Tpin_pair(i_val, o_or_clk_val)

@dataclass
class Tentry_rec:
    pins: Tpin_pair
    entry_no: int

    @staticmethod
    def from_bytes(data: bytes) -> 'Tentry_rec':
        pins = Tpin_pair.from_bytes(data[:4])
        entry_no = struct.unpack('<h', data[4:6])[0]
        return Tentry_rec(pins, entry_no)

@dataclass
class Tdel_entry:
    key: int
    edge1: int
    edge2: int
    time1: T_delay_tri
    time2: T_delay_tri

    @staticmethod
    def from_bytes(data: bytes) -> 'Tdel_entry':
        key, edge1, edge2 = struct.unpack('<3i', data[:12])
        time1 = T_delay_tri.from_bytes(data[12:24])
        time2 = T_delay_tri.from_bytes(data[24:36])
        return Tdel_entry(key, edge1, edge2, time1, time2)

@dataclass
class TRAM_del_rec:
    iopath: List[Tentry_rec]
    setuphold: List[Tentry_rec]
    width: List[Tentry_rec]
    del_entry: List[Tdel_entry]

    @staticmethod
    def from_bytes(data: bytes) -> 'TRAM_del_rec':
        offset = 0
        iopath = [Tentry_rec.from_bytes(data[offset + i*6:offset + (i+1)*6]) for i in range(3001)]
        offset += 3001 * 6
        setuphold = [Tentry_rec.from_bytes(data[offset + i*6:offset + (i+1)*6]) for i in range(8001)]
        offset += 8001 * 6
        width = [Tentry_rec.from_bytes(data[offset + i*6:offset + (i+1)*6]) for i in range(51)]
        offset += 51 * 6
        del_entry = [Tdel_entry.from_bytes(data[offset + i*36:offset + (i+1)*36]) for i in range(101)]
        return TRAM_del_rec(iopath, setuphold, width, del_entry)

@dataclass
class Tdel_rec:
    val: T_delay
    conf_mux: int
    name: str
    x: int
    y: int
    plane: int
    dir: int
    inv: int
    cnt: int
    con_type: int

    @staticmethod
    def from_bytes(data: memoryview, offset: int) -> ('Tdel_rec', int):
        val = T_delay.from_bytes(data[offset:offset + 24])
        offset += 24

        conf_mux = struct.unpack_from('<i', data, offset)[0]
        offset += 4
        strlen = data[offset]
        offset += 1
        name = data[offset:offset + strlen].decode('ascii')
        offset += 23  # alignment added as well

        x, y, plane, dir, inv, cnt = struct.unpack_from('<6i', data, offset)
        offset += 24

        con_type_val = data[offset]
        offset += 4

        return Tdel_rec(val, conf_mux, name, x, y, plane, dir, inv, cnt, con_type_val), offset

def read_SB_del_tile_arr_from_bytes(mv: memoryview, offset: int) -> (List, int):
    SB_del_tile_arr = []

    for i1 in range(4):  # [1..4]
        level1 = []
        for i2 in range(8):  # [1..8]
            level2 = []
            for i3 in range(4):  # [1..4]
                level3 = []
                for i4 in range(12):  # [1..12]
                    level4 = []
                    for i5 in range(5):  # [0..4]
                        level5 = []
                        for i6 in range(8):  # [0..7]
                            chunk = mv[offset:offset + 24]
                            if len(chunk) < 24:
                                raise EOFError("Unexpected end of data")
                            delay = T_delay.from_bytes(chunk)
                            offset += 24
                            level5.append(delay)
                        level4.append(level5)
                    level3.append(level4)
                level2.append(level3)
            level1.append(level2)
        SB_del_tile_arr.append(level1)

    return SB_del_tile_arr, offset

def read_IM_del_tile_arr_from_bytes(mv: memoryview, offset: int) -> (List, int):
    result = []
    for i1 in range(2):  # [1..2]
        level1 = []
        for i2 in range(8):  # [1..8]
            level2 = []
            for i3 in range(8):  # [1..8]
                level3 = []
                for i4 in range(12):  # [1..12]
                    level4 = []
                    for i5 in range(8):  # [0..7]
                        delay = T_delay.from_bytes(mv[offset:offset+24])
                        offset += 24
                        level4.append(delay)
                    level3.append(level4)
                level2.append(level3)
            level1.append(level2)
        result.append(level1)
    return result, offset

def read_OM_del_tile_arr_from_bytes(mv: memoryview, offset: int) -> (List, int):
    result = []
    for i1 in range(8):  # [1..8]
        level1 = []
        for i2 in range(8):  # [1..8]
            level2 = []
            for i3 in range(4):  # [9..12]
                level3 = []
                for i4 in range(4):  # [0..3]
                    delay = T_delay.from_bytes(mv[offset:offset+24])
                    offset += 24
                    level3.append(delay)
                level2.append(level3)
            level1.append(level2)
        result.append(level1)
    return result, offset

def read_CPE_del_tile_arr_from_bytes(mv: memoryview, offset: int) -> (List, int):
    result = []
    for i1 in range(10):  # [0..9]
        level1 = []
        for i2 in range(19):  # [1..19]
            level2 = []
            for i3 in range(10):  # [1..10]
                rec, offset = Tdel_rec.from_bytes(mv, offset)
                level2.append(rec)
            level1.append(level2)
        result.append(level1)
    return result, offset

def read_SB_del_rim_arr_from_bytes(mv: memoryview, offset: int) -> (List, int):
    result = []
    for i1 in range(165):  # [-2..162]
        level1 = []
        for i2 in range(4):  # [1..4]
            level2 = []
            for i3 in range(12):  # [1..12]
                level3 = []
                for i4 in range(5):  # [0..4]
                    level4 = []
                    for i5 in range(8):  # [0..7]
                        delay = T_delay.from_bytes(mv[offset:offset+24])
                        offset += 24
                        level4.append(delay)
                    level3.append(level4)
                level2.append(level3)
            level1.append(level2)
        result.append(level1)
    return result, offset

def read_Edge_del_arr_from_bytes(mv: memoryview, offset: int) -> (List, int):
    result = []
    for i1 in range(165):  # [-2..162]
        level1 = []
        for i2 in range(4):  # [1..4]
            level2 = []
            for i3 in range(24):  # [1..24]
                level3 = []
                for i4 in range(8):  # [1..8]
                    delay = T_delay.from_bytes(mv[offset:offset+24])
                    offset += 24
                    level3.append(delay)
                level2.append(level3)
            level1.append(level2)
        result.append(level1)
    return result, offset

def read_IO_SEL_del_arr_from_bytes(mv: memoryview, offset: int) -> (List, int):
    result = []
    for i1 in range(11):  # [1..11]
        level1 = []
        for i2 in range(4):  # [1..4]
            delay = T_delay.from_bytes(mv[offset:offset+24])
            offset += 24
            level1.append(delay)
        result.append(level1)
    return result, offset

def read_CLKIN_del_arr_from_bytes(mv: memoryview, offset: int) -> (List, int):
    result = []
    for i1 in range(7):
        level1 = []
        for i2 in range(4):
            delay = T_delay.from_bytes(mv[offset:offset + 24])
            offset += 24
            level1.append(delay)
        result.append(level1)
    return result, offset

def read_GLBOUT_del_arr_from_bytes(mv: memoryview, offset: int) -> (List, int):
    result = []
    for i1 in range(28):
        level1 = []
        for i2 in range(8):
            delay = T_delay.from_bytes(mv[offset:offset + 24])
            offset += 24
            level1.append(delay)
        result.append(level1)
    return result, offset

def read_PLL_del_arr_from_bytes(mv: memoryview, offset: int) -> (List, int):
    result = []
    for i1 in range(7):
        level1 = []
        for i2 in range(6):
            delay = T_delay.from_bytes(mv[offset:offset + 24])
            offset += 24
            level1.append(delay)
        result.append(level1)
    return result, offset

def read_Tentry_rec_from_bytes(data: memoryview, offset: int) -> ('Tentry_rec', int):
    pins_i, pins_val, entry_no = struct.unpack_from('<3h', data, offset)
    return Tentry_rec(Tpin_pair(pins_i, pins_val), entry_no), offset + 6

def read_Tdel_entry_from_bytes(data: memoryview, offset: int) -> ('Tdel_entry', int):
    key, edge1, edge2 = struct.unpack_from('<3i', data, offset)
    time1 = T_delay_tri.from_bytes(data[offset + 12:offset + 24])
    time2 = T_delay_tri.from_bytes(data[offset + 24:offset + 36])
    return Tdel_entry(key, edge1, edge2, time1, time2), offset + 36

def read_TRAM_del_rec_from_bytes(mv: memoryview, offset: int) -> (TRAM_del_rec, int):
    iopath = []
    for _ in range(3001):
        entry, offset = read_Tentry_rec_from_bytes(mv, offset)
        iopath.append(entry)

    setuphold = []
    for _ in range(8001):
        entry, offset = read_Tentry_rec_from_bytes(mv, offset)
        setuphold.append(entry)

    width = []
    for _ in range(51):
        entry, offset = read_Tentry_rec_from_bytes(mv, offset)
        width.append(entry)

    del_entry = []
    for _ in range(101):
        entry, offset = read_Tdel_entry_from_bytes(mv, offset)
        del_entry.append(entry)

    offset += 2 # alignment added
    return TRAM_del_rec(iopath, setuphold, width, del_entry), offset

@dataclass
class Tdel_all_rec:
    SB_del_tile_arr: List[List[List[List[List[List[T_delay]]]]]]
    IM_del_tile_arr: List[List[List[List[List[T_delay]]]]]
    OM_del_tile_arr: List[List[List[List[T_delay]]]]
    CPE_del_tile_arr: List[List[List[Tdel_rec]]]
    SB_del_rim_arr: List[List[List[List[List[T_delay]]]]]
    Edge_del_arr: List[List[List[List[T_delay]]]]
    IO_SEL_del_arr: List[List[T_delay]]
    CLKIN_del_arr: List[List[T_delay]]
    GLBOUT_del_arr: List[List[T_delay]]
    PLL_del_arr: List[List[T_delay]]
    FPGA_ram_del_1: TRAM_del_rec
    FPGA_ram_del_2: TRAM_del_rec
    FPGA_ram_del_3: TRAM_del_rec

    @staticmethod
    def from_bytes(data: bytes) -> 'Tdel_all_rec':
        offset = 0
        sb_del_tile_arr, offset = read_SB_del_tile_arr_from_bytes(data, offset)
        im, offset = read_IM_del_tile_arr_from_bytes(data, offset)
        om, offset = read_OM_del_tile_arr_from_bytes(data, offset)
        cpe, offset = read_CPE_del_tile_arr_from_bytes(data, offset)
        sb_del_rim, offset = read_SB_del_rim_arr_from_bytes(data, offset)
        edge, offset = read_Edge_del_arr_from_bytes(data, offset)
        io_sel, offset = read_IO_SEL_del_arr_from_bytes(data, offset)
        clkin, offset = read_CLKIN_del_arr_from_bytes(data, offset)
        glbout, offset = read_GLBOUT_del_arr_from_bytes(data, offset)
        pll_del, offset = read_PLL_del_arr_from_bytes(data, offset)
        fpga_ram_del_1, offset = read_TRAM_del_rec_from_bytes(data, offset)
        fpga_ram_del_2, offset = read_TRAM_del_rec_from_bytes(data, offset)
        fpga_ram_del_3, offset = read_TRAM_del_rec_from_bytes(data, offset)
        return Tdel_all_rec(sb_del_tile_arr, im, om, cpe, sb_del_rim, edge, io_sel, clkin, glbout, pll_del, fpga_ram_del_1, fpga_ram_del_2, fpga_ram_del_3)


def decompress_file(input_path, output_path):
    with open(input_path, 'rb') as f_in:
        compressed_data = f_in.read()
    try:
        decompressed_data = zlib.decompress(compressed_data)
    except zlib.error as e:
        print(f"Decompression failed: {e}")
        return
    
    all = Tdel_all_rec.from_bytes(decompressed_data)
    #print(all.GLBOUT_del_arr)

    with open(output_path, 'wb') as f_out:
        f_out.write(decompressed_data)

# Example usage
#decompress_file("cc_best_eco_dly.dly", "cc_best_eco_dly.bin")
#decompress_file("cc_best_lpr_dly.dly", "cc_best_lpr_dly.bin")
#decompress_file("cc_best_spd_dly.dly", "cc_best_spd_dly.bin")
#
#decompress_file("cc_typ_eco_dly.dly", "cc_typ_eco_dly.bin")
#decompress_file("cc_typ_lpr_dly.dly", "cc_typ_lpr_dly.bin")
#decompress_file("cc_typ_spd_dly.dly", "cc_typ_spd_dly.bin")
#
#decompress_file("cc_worst_eco_dly.dly", "cc_worst_eco_dly.bin")
#decompress_file("cc_worst_lpr_dly.dly", "cc_worst_lpr_dly.bin")
decompress_file("cc_worst_spd_dly.dly", "cc_worst_spd_dly.bin")
