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

import die
import os
from die import Die
from dataclasses import dataclass
from typing import List, Dict
from timing import decompress_timing

@dataclass(eq=True, order=True)
class Pad:
    x : int
    y : int
    name : str
    bel : str
    function : str
    bank : int
    flags : int

@dataclass
class Bank:
    die : str
    bank: str

@dataclass
class TimingDelay:
    min : int
    max : int

@dataclass
class Chip:
    name : str
    die_width : int
    die_height : int
    dies : Dict[str,Die]
    packages: Dict[str,Dict[str, List[Bank]]]
    not_exist: Dict[str,List[str]]

    def max_row(self):
        return self.die_height * die.num_rows() - 3

    def max_col(self):
        return self.die_width * die.num_cols() - 3

    def get_tile_types(self,x,y):
        x_pos = (x + 2) % die.num_cols() - 2
        y_pos = (y + 2) % die.num_rows() - 2
        return die.get_tile_types(x_pos,y_pos)

    def get_tile_type(self,x,y):
        x_pos = (x + 2) % die.num_cols() - 2
        y_pos = (y + 2) % die.num_rows() - 2
        return die.get_tile_type(x_pos,y_pos)
    
    def get_tile_info(self,x,y):
        x_pos = (x + 2) % die.num_cols() - 2
        y_pos = (y + 2) % die.num_rows() - 2
        x_die = (x + 2) // die.num_cols()
        y_die = (y + 2) // die.num_rows()
        die_num = x_die + y_die * self.die_width
        return die.get_tile_info(die_num, x_pos, y_pos)

    def get_connections(self):
        conn = dict()
        for d in self.dies.values():
            d.create_in_die_connections(conn)
        return conn.items()
    
    def get_packages(self):
        return self.packages

    def get_bank_number(self, bank):
        match bank:
            case 'N1' : return 0
            case 'N2' : return 1
            case 'E1' : return 2
            case 'E2' : return 3
            case 'W1' : return 4
            case 'W2' : return 5
            case 'S1' : return 6
            case 'S2' : return 7
            case 'S3' : return 8
            case _ : return -1

    def get_package_pads(self, package):
        pads = []
        pkg = self.packages[package]
        not_exist = self.not_exist[package]
        for name, banks in pkg.items():
            for bank in banks:
                for p in ["A","B"]:
                    for num in range(9):
                        d = self.dies[bank.die]
                        loc = d.io_pad_names[bank.bank][p][num]
                        pad_name = f"IO_{name}_{p}{num}"
                        flags = 0
                        # mark clock sources
                        if bank.bank == "W2" and p == "A" and num in [5,6,7,8]:
                            flags = 1
                        if pad_name not in not_exist:
                            pads.append(Pad(loc.x + d.offset_x,loc.y + d.offset_y,pad_name,"GPIO","",self.get_bank_number(bank.bank),flags))
        return pads

CCGM1_DEVICES = {
    "CCGM1A1":  Chip("CCGM1A1", 1, 1, {
                    "1A" : Die("1A", 0, 0)
                }, {
                    "FBGA324" : {
                        "EA" : [ Bank("1A", "N1") ],
                        "EB" : [ Bank("1A", "N2") ],
                        "NA" : [ Bank("1A", "E1") ],
                        "NB" : [ Bank("1A", "E2") ],
                        "WA" : [ Bank("1A", "S3") ],
                        "WB" : [ Bank("1A", "S1") ],
                        "WC" : [ Bank("1A", "S2") ],
                        "SA" : [ Bank("1A", "W1") ],
                        "SB" : [ Bank("1A", "W2") ]
                    }
                }, { # non existing pins
                    "FBGA324" : []
                }),
    "CCGM1A2":  Chip("CCGM1A2", 1, 2, {
                    "1A" : Die("1A", 0, 0),
                    "1B" : Die("1B", 0, 1)
                }, {
                    "FBGA324" : {
                        "EA" : [ Bank("1B", "N1") ],
                        "EB" : [ Bank("1B", "N2") ],
                        "NA" : [ Bank("1A", "E1"), Bank("1B", "E1") ],
                        "NB" : [ Bank("1A", "E2") ],
                        "WA" : [ Bank("1A", "S3") ],
                        "WB" : [ Bank("1A", "S1"), Bank("1B", "S1") ],
                        "WC" : [ Bank("1A", "S2") ],
                        "SA" : [ Bank("1A", "W1") ],
                        "SB" : [ Bank("1A", "W2"), Bank("1B", "W2") ]
                    }
                }, { # non existing pins
                    "FBGA324" : []
                }),
    "CCGM1A4":  Chip("CCGM1A4", 2, 2, {
                    "1A" : Die("1A", 0, 0),
                    "1B" : Die("1B", 0, 1),
                    "2A" : Die("2A", 1, 0),
                    "2B" : Die("2B", 1, 1)
                }, {
                    "FBGA324" : {
                        "EA" : [ Bank("1B", "N1") ],
                        "EB" : [ Bank("1B", "N2") ],
                        "NA" : [ Bank("1A", "E1"), Bank("1B", "E1"), Bank("2A", "E1"), Bank("2B", "E1") ],
                        "NB" : [ Bank("2A", "N1"), Bank("2B", "S1") ],
                        "WA" : [ Bank("1A", "S3") ],
                        "WB" : [ Bank("1A", "N1"), Bank("1B", "S1") ],
                        "WC" : [ Bank("1A", "S2") ],
                        "SA" : [ Bank("1A", "W1") ],
                        "SB" : [ Bank("1A", "W2"), Bank("1B", "W2"), Bank("2A", "W2"), Bank("2B", "W2") ]
                    }
                }, { # non existing pins
                    "FBGA324" : [
                                 "IO_SB_A0","IO_SB_B0",
                                 "IO_SB_A1","IO_SB_B1",
                                 "IO_SB_A2","IO_SB_B2",
                                 "IO_SB_A3","IO_SB_B3"
                                ]
                }),
}

def get_all_devices():
    return CCGM1_DEVICES

def get_device(name):
    return CCGM1_DEVICES[name]

def convert_delay(d):
    return TimingDelay(min(d.rise.min, d.fall.min), max(d.rise.max, d.fall.max))

def convert_delay_val(d):
    return TimingDelay(d.min, d.max)

def get_timings(dly_path, name):
    val = dict()
    timing_data = decompress_timing(os.path.join(dly_path, "..", "delay", f"cc_{name}_dly.dly"))
    for i1 in range(4):  # [1..4]
        for i2 in range(8):  # [1..8]
            for i3 in range(4):  # [1..4]
                for i4 in range(12):  # [1..12]
                    for i5 in range(5):  # [0..4]
                        for i6 in range(8):  # [0..7]
                            d = timing_data.SB_del_tile_arr[i1][i2][i3][i4][i5][i6]
                            if d.rise.min == 123456: # not connected
                                continue
                            x = i2+1
                            y = i3+1
                            y = 2*y if (x % 2 == 0) else 2*y-1
                            name = f"sb_del_t{i1+1}_x{x}_y{y}_p{i4+1}_d{i5}_s{i6}"
                            val[name] = convert_delay(d)

    for i1 in range(2):  # [1..2]
        for i2 in range(8):  # [1..8]
            for i3 in range(8):  # [1..8]
                for i4 in range(12):  # [1..12]
                    for i5 in range(8):  # [0..7]
                        d = timing_data.IM_del_tile_arr[i1][i2][i3][i4][i5]
                        if d.rise.min == 123456: # not connected
                            continue
                        name = f"im_x{i2+1}_y{i3+1}_p{i4+1}_d{i5}_path{i1+1}"
                        val[name] = convert_delay(d)

    for i1 in range(8):  # [1..8]
        for i2 in range(8):  # [1..8]
            for i3 in range(4):  # [9..12]
                for i4 in range(4):  # [0..3]
                    d = timing_data.OM_del_tile_arr[i1][i2][i3][i4]
                    if d.rise.min == 123456: # not connected
                        continue
                    name = f"om_x{i1+1}_y{i2+1}_p{i3+9}_d{i4}"
                    val[name] = convert_delay(d)

    for i1 in range(10):  # [0..9]
        for i2 in range(19):  # [1..19]
            for i3 in range(10):  # [1..10]
                d = timing_data.CPE_del_tile_arr[i1][i2][i3]
                if d.val.rise.min == 123456: # not connected
                    continue
                name = f"cpe_func{i1}_i{i2+1}_o{i3+1}"
                val[name] = convert_delay(d.val)

    for i1 in range(165):  # [-2..162]
        for i2 in range(4):  # [1..4]
            for i3 in range(12):  # [1..12]
                for i4 in range(5):  # [0..4]
                    for i5 in range(8):  # [0..7]
                        d = timing_data.SB_del_rim_arr[i1][i2][i3][i4][i5]
                        if d.rise.min == 123456: # not connected
                            continue
                        name = f"sb_rim_xy{i1-2}_s{i2+1}_p{i3+1}_d{i4}_s{i5}"
                        val[name] = convert_delay(d)

    for i1 in range(165):  # [-2..162]
        for i2 in range(4):  # [1..4]
            for i3 in range(24):  # [1..24]
                for i4 in range(8):  # [1..8]
                    d = timing_data.Edge_del_arr[i1][i2][i3][i4]
                    if d.rise.min == 123456: # not connected
                        continue
                    name = f"edge_xy{i1-2}_s{i2+1}_i{i3+1}_o{i4+1}"
                    val[name] = convert_delay(d)

    for i1 in range(11):  # [1..11]
        for i2 in range(4):  # [1..4]
            d = timing_data.IO_SEL_del_arr[i1][i2]
            if d.rise.min == 123456: # not connected
                continue
            name = f"io_sel_i{i1+1}_o{i2+1}"
            val[name] = convert_delay(d)

    for i1 in range(7): # [1..7]
        for i2 in range(4): # [1..4]
            d = timing_data.CLKIN_del_arr[i1][i2]
            if d.rise.min == 123456: # not connected
                continue
            name = f"clkin_i{i1+1}_o{i2+1}"
            val[name] = convert_delay(d)

    for i1 in range(28): # [1..28]
        for i2 in range(8): # [1..8]
            d = timing_data.GLBOUT_del_arr[i1][i2]
            if d.rise.min == 123456: # not connected
                continue
            name = f"glbout_i{i1+1}_o{i2+1}"
            val[name] = convert_delay(d)

    for i1 in range(7): # [1..7]
        for i2 in range(6): # [1..6]
            d = timing_data.PLL_del_arr[i1][i2]
            if d.rise.min == 123456: # not connected
                continue
            name = f"pll_i{i1+1}_o{i2+1}"
            val[name] = convert_delay(d)

    val["del_rec_0"] = convert_delay(timing_data.timing_delays.del_rec_0.val)
    val["del_min_route_SB"] = convert_delay(timing_data.timing_delays.del_min_route_SB.val)
    val["del_violation_common"] = convert_delay_val(timing_data.timing_delays.del_violation_common.val)
    val["del_dummy"] = convert_delay(timing_data.timing_delays.del_dummy.val)
    val["del_Hold_D_L"] = convert_delay_val(timing_data.timing_delays.del_Hold_D_L.val)
    val["del_Setup_D_Ldel_Setup_D_L"] = convert_delay_val(timing_data.timing_delays.del_Setup_D_L.val)
    val["del_Hold_RAM"] = convert_delay_val(timing_data.timing_delays.del_Hold_RAM.val)
    val["del_Setup_RAM"] = convert_delay_val(timing_data.timing_delays.del_Setup_RAM.val)

    val["del_Hold_SN_RN"] = convert_delay_val(timing_data.timing_delays.del_Hold_SN_RN.val)
    val["del_Setup_SN_RN"] = convert_delay_val(timing_data.timing_delays.del_Setup_SN_RN.val)
    val["del_Hold_RN_SN"] = convert_delay_val(timing_data.timing_delays.del_Hold_RN_SN.val)
    val["del_Setup_RN_SN"] = convert_delay_val(timing_data.timing_delays.del_Setup_RN_SN.val)

    val["del_bot_couty2"] = convert_delay(timing_data.timing_delays.del_bot_couty2.val)
    val["del_bot_glb_couty2"] = convert_delay(timing_data.timing_delays.del_bot_glb_couty2.val)
    val["del_bot_SB_couty2"] = convert_delay(timing_data.timing_delays.del_bot_SB_couty2.val)
    val["del_bot_pouty2"] = convert_delay(timing_data.timing_delays.del_bot_pouty2.val)
    val["del_bot_glb_pouty2"] = convert_delay(timing_data.timing_delays.del_bot_glb_pouty2.val)
    val["del_bot_SB_pouty2"] = convert_delay(timing_data.timing_delays.del_bot_SB_pouty2.val)

    val["del_left_couty2"] = convert_delay(timing_data.timing_delays.del_left_couty2.val)
    val["del_left_glb_couty2"] = convert_delay(timing_data.timing_delays.del_left_glb_couty2.val)
    val["del_left_SB_couty2"] = convert_delay(timing_data.timing_delays.del_left_SB_couty2.val)
    val["del_left_pouty2"] = convert_delay(timing_data.timing_delays.del_left_pouty2.val)
    val["del_left_glb_pouty2"] = convert_delay(timing_data.timing_delays.del_left_glb_pouty2.val)
    val["del_left_SB_pouty2"] = convert_delay(timing_data.timing_delays.del_left_SB_pouty2.val)

    val["del_CPE_CP_Q"] = convert_delay(timing_data.timing_delays.del_CPE_CP_Q.val)
    val["del_CPE_S_Q"] = convert_delay(timing_data.timing_delays.del_CPE_S_Q.val)
    val["del_CPE_R_Q"] = convert_delay(timing_data.timing_delays.del_CPE_R_Q.val)
    val["del_CPE_D_Q"] = convert_delay(timing_data.timing_delays.del_CPE_D_Q.val)

    val["del_RAM_CLK_DO"] = convert_delay(timing_data.timing_delays.del_RAM_CLK_DO.val)

    val["del_GLBOUT_sb_big"] = convert_delay(timing_data.timing_delays.del_GLBOUT_sb_big.val)

    val["del_sb_drv"] = convert_delay(timing_data.timing_delays.del_sb_drv.val)

    val["del_CP_carry_path"] = convert_delay(timing_data.timing_delays.del_CP_carry_path.val)
    val["del_CP_prop_path"] = convert_delay(timing_data.timing_delays.del_CP_prop_path.val)


    val["del_special_RAM_I"] = convert_delay(timing_data.timing_delays.del_special_RAM_I.val)
    val["del_RAMO_xOBF"] = convert_delay(timing_data.timing_delays.del_RAMO_xOBF.val)
    val["del_GLBOUT_IO_SEL"] = convert_delay(timing_data.timing_delays.del_GLBOUT_IO_SEL.val)

    val["del_IO_SEL_Q_out"] = convert_delay(timing_data.timing_delays.del_IO_SEL_Q_out.val)
    val["del_IO_SEL_Q_in"] = convert_delay(timing_data.timing_delays.del_IO_SEL_Q_in.val)

    val["in_delayline_per_stage"] = convert_delay(timing_data.timing_delays.in_delayline_per_stage.val)
    val["out_delayline_per_stage"] = convert_delay(timing_data.timing_delays.out_delayline_per_stage.val)

    val["del_IBFdel_IBF"] = convert_delay(timing_data.timing_delays.del_IBF.val)

    val["del_OBF"] = convert_delay(timing_data.timing_delays.del_OBF.val)
    val["del_r_OBF"] = convert_delay(timing_data.timing_delays.del_r_OBF.val)

    val["del_TOBF_ctrl"] = convert_delay(timing_data.timing_delays.del_TOBF_ctrl.val)

    val["del_LVDS_IBF"] = convert_delay(timing_data.timing_delays.del_LVDS_IBF.val)

    val["del_LVDS_OBF"] = convert_delay(timing_data.timing_delays.del_LVDS_OBF.val)
    val["del_ddel_LVDS_r_OBFummy"] = convert_delay(timing_data.timing_delays.del_LVDS_r_OBF.val)

    val["del_LVDS_TOBF_ctrl"] = convert_delay(timing_data.timing_delays.del_LVDS_TOBF_ctrl.val)

    val["del_CP_clkin"] = convert_delay(timing_data.timing_delays.del_CP_clkin.val)
    val["del_CP_enin"] = convert_delay(timing_data.timing_delays.del_CP_enin.val)

    val["del_preplace"] = convert_delay(timing_data.timing_delays.del_preplace.val)

    return val
