#
#  prjpeppercorn -- GateMate FPGAs Bitstream Documentation and Tools
#
#  Copyright (C) 2024  The Project Peppercorn Authors.
#
#  Permission to use, copy, modify, and/or distribute this software for any
#  purpose with or without fee is hereby granted, provided that the above
#  copyright notice and this permission notice appear in all copies.
#
#  THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
#  WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
#  MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
#  ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
#  WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
#  ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
#  OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

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

@dataclass
class Tentry_rec:
    pins: Tpin_pair
    entry_no: int


@dataclass
class Tdel_entry:
    key: int
    edge1: int
    edge2: int
    time1: T_delay_tri
    time2: T_delay_tri


@dataclass
class TRAM_del_rec:
    iopath: List[Tentry_rec]
    setuphold: List[Tentry_rec]
    width: List[Tentry_rec]
    del_entry: List[Tdel_entry]


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
    
@dataclass
class Tdel_rec_tri:
    val: T_delay_tri
    conf_mux: int
    name: str
    x: int
    y: int

    @staticmethod
    def from_bytes(mv: memoryview, offset: int) -> ('Tdel_rec_tri', int):
        val = T_delay_tri.from_bytes(mv[offset:offset+12])
        offset += 12

        conf_mux = struct.unpack_from('<i', mv, offset)[0]
        offset += 4

        strlen = mv[offset]
        offset += 1
        name = mv[offset:offset + strlen].decode('ascii')
        offset += 23

        x, y = struct.unpack_from('<2i', mv, offset)
        offset += 8

        return Tdel_rec_tri(val, conf_mux, name, x, y), offset


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

@dataclass
class ExtraTimingDelays:
    skew_report_del: int
    fix_skew_del: int
    del_rec_0: Tdel_rec
    del_min_route_SB: Tdel_rec
    del_violation_common: Tdel_rec_tri
    del_dummy: Tdel_rec
    del_Hold_D_L: Tdel_rec_tri
    del_Hold_RAM: Tdel_rec_tri
    del_Setup_D_L: Tdel_rec_tri
    del_Setup_RAM: Tdel_rec_tri
    del_Hold_SN_RN: Tdel_rec_tri
    del_Setup_SN_RN: Tdel_rec_tri
    del_Hold_RN_SN: Tdel_rec_tri
    del_Setup_RN_SN: Tdel_rec_tri
    del_bot_couty2: Tdel_rec
    del_bot_glb_couty2: Tdel_rec
    del_bot_SB_couty2: Tdel_rec
    del_bot_pouty2: Tdel_rec
    del_bot_glb_pouty2: Tdel_rec
    del_bot_SB_pouty2: Tdel_rec
    del_left_couty2: Tdel_rec
    del_left_glb_couty2: Tdel_rec
    del_left_SB_couty2: Tdel_rec
    del_left_pouty2: Tdel_rec
    del_left_glb_pouty2: Tdel_rec
    del_left_SB_pouty2: Tdel_rec
    del_inp: List[Tdel_rec]
    del_CPE_out_mux: List[Tdel_rec]
    del_CPE_CP_Q: Tdel_rec
    del_CPE_S_Q: Tdel_rec
    del_CPE_R_Q: Tdel_rec
    del_CPE_D_Q: Tdel_rec
    del_RAM_CLK_DO: Tdel_rec
    del_GLBOUT_sb_big: Tdel_rec
    del_sb_drv: Tdel_rec
    del_CP_carry_path: Tdel_rec
    del_CP_prop_path: Tdel_rec
    del_special_RAM_I: Tdel_rec
    del_RAMO_xOBF: Tdel_rec
    del_GLBOUT_IO_SEL: Tdel_rec
    del_IO_SEL_Q_out: Tdel_rec
    del_IO_SEL_Q_in: Tdel_rec
    in_delayline_per_stage: Tdel_rec
    out_delayline_per_stage: Tdel_rec
    del_IBF: Tdel_rec
    del_OBF: Tdel_rec
    del_r_OBF: Tdel_rec
    del_TOBF_ctrl: Tdel_rec
    del_LVDS_IBF: Tdel_rec
    del_LVDS_OBF: Tdel_rec
    del_LVDS_r_OBF: Tdel_rec
    del_LVDS_TOBF_ctrl: Tdel_rec
    del_CP_clkin: Tdel_rec
    del_CP_enin: Tdel_rec
    del_preplace: Tdel_rec
    del_CPE_timing_mod: List[Tdel_rec]

    @staticmethod
    def from_bytes(mv: memoryview, offset: int) -> ('ExtraTimingDelays', int):
        skew_report_del, fix_skew_del = struct.unpack_from('<2i', mv, offset)
        offset += 8

        del_rec_0, offset = Tdel_rec.from_bytes(mv, offset)
        del_min_route_SB, offset = Tdel_rec.from_bytes(mv, offset)
        del_violation_common, offset = Tdel_rec_tri.from_bytes(mv, offset)
        del_dummy, offset = Tdel_rec.from_bytes(mv, offset)

        del_Hold_D_L, offset = Tdel_rec_tri.from_bytes(mv, offset)
        del_Hold_RAM, offset = Tdel_rec_tri.from_bytes(mv, offset)
        del_Setup_D_L, offset = Tdel_rec_tri.from_bytes(mv, offset)
        del_Setup_RAM, offset = Tdel_rec_tri.from_bytes(mv, offset)
        del_Hold_SN_RN, offset = Tdel_rec_tri.from_bytes(mv, offset)
        del_Setup_SN_RN, offset = Tdel_rec_tri.from_bytes(mv, offset)
        del_Hold_RN_SN, offset = Tdel_rec_tri.from_bytes(mv, offset)
        del_Setup_RN_SN, offset = Tdel_rec_tri.from_bytes(mv, offset)

        del_bot_couty2, offset = Tdel_rec.from_bytes(mv, offset)
        del_bot_glb_couty2, offset = Tdel_rec.from_bytes(mv, offset)
        del_bot_SB_couty2, offset = Tdel_rec.from_bytes(mv, offset)
        del_bot_pouty2, offset = Tdel_rec.from_bytes(mv, offset)
        del_bot_glb_pouty2, offset = Tdel_rec.from_bytes(mv, offset)
        del_bot_SB_pouty2, offset = Tdel_rec.from_bytes(mv, offset)
        del_left_couty2, offset = Tdel_rec.from_bytes(mv, offset)
        del_left_glb_couty2, offset = Tdel_rec.from_bytes(mv, offset)
        del_left_SB_couty2, offset = Tdel_rec.from_bytes(mv, offset)
        del_left_pouty2, offset = Tdel_rec.from_bytes(mv, offset)
        del_left_glb_pouty2, offset = Tdel_rec.from_bytes(mv, offset)
        del_left_SB_pouty2, offset = Tdel_rec.from_bytes(mv, offset)

        del_inp = []
        for _ in range(8):
            rec, offset = Tdel_rec.from_bytes(mv, offset)
            del_inp.append(rec)

        del_CPE_out_mux = []
        for _ in range(4):
            rec, offset = Tdel_rec.from_bytes(mv, offset)
            del_CPE_out_mux.append(rec)

        del_CPE_CP_Q, offset = Tdel_rec.from_bytes(mv, offset)
        del_CPE_S_Q, offset = Tdel_rec.from_bytes(mv, offset)
        del_CPE_R_Q, offset = Tdel_rec.from_bytes(mv, offset)
        del_CPE_D_Q, offset = Tdel_rec.from_bytes(mv, offset)

        del_RAM_CLK_DO, offset = Tdel_rec.from_bytes(mv, offset)
        del_GLBOUT_sb_big, offset = Tdel_rec.from_bytes(mv, offset)
        del_sb_drv, offset = Tdel_rec.from_bytes(mv, offset)

        del_CP_carry_path, offset = Tdel_rec.from_bytes(mv, offset)
        del_CP_prop_path, offset = Tdel_rec.from_bytes(mv, offset)

        del_special_RAM_I, offset = Tdel_rec.from_bytes(mv, offset)
        del_RAMO_xOBF, offset = Tdel_rec.from_bytes(mv, offset)

        del_GLBOUT_IO_SEL, offset = Tdel_rec.from_bytes(mv, offset)
        del_IO_SEL_Q_out, offset = Tdel_rec.from_bytes(mv, offset)
        del_IO_SEL_Q_in, offset = Tdel_rec.from_bytes(mv, offset)

        in_delayline_per_stage, offset = Tdel_rec.from_bytes(mv, offset)
        out_delayline_per_stage, offset = Tdel_rec.from_bytes(mv, offset)

        del_IBF, offset = Tdel_rec.from_bytes(mv, offset)
        del_OBF, offset = Tdel_rec.from_bytes(mv, offset)
        del_r_OBF, offset = Tdel_rec.from_bytes(mv, offset)
        del_TOBF_ctrl, offset = Tdel_rec.from_bytes(mv, offset)

        del_LVDS_IBF, offset = Tdel_rec.from_bytes(mv, offset)
        del_LVDS_OBF, offset = Tdel_rec.from_bytes(mv, offset)
        del_LVDS_r_OBF, offset = Tdel_rec.from_bytes(mv, offset)
        del_LVDS_TOBF_ctrl, offset = Tdel_rec.from_bytes(mv, offset)

        del_CP_clkin, offset = Tdel_rec.from_bytes(mv, offset)
        del_CP_enin, offset = Tdel_rec.from_bytes(mv, offset)
        del_preplace, offset = Tdel_rec.from_bytes(mv, offset)

        del_CPE_timing_mod = []
        for _ in range(42):
            rec, offset = Tdel_rec.from_bytes(mv, offset)
            del_CPE_timing_mod.append(rec)

        return ExtraTimingDelays(
            skew_report_del, fix_skew_del,
            del_rec_0, del_min_route_SB,
            del_violation_common, del_dummy,
            del_Hold_D_L, del_Hold_RAM, del_Setup_D_L, del_Setup_RAM,
            del_Hold_SN_RN, del_Setup_SN_RN, del_Hold_RN_SN, del_Setup_RN_SN,
            del_bot_couty2, del_bot_glb_couty2, del_bot_SB_couty2,
            del_bot_pouty2, del_bot_glb_pouty2, del_bot_SB_pouty2,
            del_left_couty2, del_left_glb_couty2, del_left_SB_couty2,
            del_left_pouty2, del_left_glb_pouty2, del_left_SB_pouty2,
            del_inp, del_CPE_out_mux,
            del_CPE_CP_Q, del_CPE_S_Q, del_CPE_R_Q, del_CPE_D_Q,
            del_RAM_CLK_DO, del_GLBOUT_sb_big, del_sb_drv,
            del_CP_carry_path, del_CP_prop_path,
            del_special_RAM_I, del_RAMO_xOBF,
            del_GLBOUT_IO_SEL, del_IO_SEL_Q_out, del_IO_SEL_Q_in,
            in_delayline_per_stage, out_delayline_per_stage,
            del_IBF, del_OBF, del_r_OBF, del_TOBF_ctrl,
            del_LVDS_IBF, del_LVDS_OBF, del_LVDS_r_OBF, del_LVDS_TOBF_ctrl,
            del_CP_clkin, del_CP_enin, del_preplace,
            del_CPE_timing_mod
        ), offset

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
    offset += 2 # alignment added
    for _ in range(101):
        entry, offset = read_Tdel_entry_from_bytes(mv, offset)
        del_entry.append(entry)

    return TRAM_del_rec(iopath, setuphold, width, del_entry), offset

def read_IO_SEL_io_coef_from_bytes(mv: memoryview, offset: int) -> (list, int):
    result = []
    for i1 in range(4):  # [1..4]
        row = []
        for i2 in range(27):  # [1..27]
            value = struct.unpack_from('<d', mv, offset)[0]  # '<d' = little-endian double
            offset += 8
            row.append(value)
        result.append(row)
    return result, offset

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
    IO_SEL_io_coef: list[list[float]]
    timing_delays: ExtraTimingDelays

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
        io_sel_coef, offset = read_IO_SEL_io_coef_from_bytes(data, offset)
        timing_delays, offset = ExtraTimingDelays.from_bytes(data, offset)
        return Tdel_all_rec(sb_del_tile_arr, im, om, cpe, sb_del_rim, edge, io_sel, clkin, glbout, pll_del, fpga_ram_del_1, fpga_ram_del_2, fpga_ram_del_3,io_sel_coef, timing_delays)


def decompress_timing(input_path) -> 'Tdel_all_rec':
    with open(input_path, 'rb') as f_in:
        compressed_data = f_in.read()
    try:
        decompressed_data = zlib.decompress(compressed_data)
    except zlib.error as e:
        print(f"Decompression failed: {e}")
        return
    
    return Tdel_all_rec.from_bytes(decompressed_data)

# Example usage
#decompress_timing("cc_best_eco_dly.dly")
#decompress_timing("cc_best_lpr_dly.dly")
#decompress_timing("cc_best_spd_dly.dly")
#
#decompress_timing("cc_typ_eco_dly.dly")
#decompress_timing("cc_typ_lpr_dly.dly")
#decompress_timing("cc_typ_spd_dly.dly")
#
#decompress_timing("cc_worst_eco_dly.dly")
#decompress_timing("cc_worst_lpr_dly.dly")
#decompress_timing("cc_worst_spd_dly.dly")
