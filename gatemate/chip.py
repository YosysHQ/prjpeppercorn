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
from die import Die
from dataclasses import dataclass
from typing import List, Dict

@dataclass(eq=True, order=True)
class Pad:
    x : int
    y : int
    name : str
    bel : str
    function : str
    bank : int

@dataclass
class Bank:
    die : str
    bank: str

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
                        if pad_name not in not_exist:
                            pads.append(Pad(loc.x + d.offset_x,loc.y + d.offset_y,pad_name,"GPIO","",0))
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
