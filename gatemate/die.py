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

from enum import Enum
from dataclasses import dataclass

PLL_X_POS = 33
PLL_Y_POS = 131
SERDES_X_POS = 1
SERDES_Y_POS = 121
CTRL_X_POS = -2
CTRL_Y_POS = -2
RAM_INPUT = 0
RAM_OUTPUT = 1

def max_row():
    return 131

def max_col():
    return 163

def num_rows():
    return max_row() + 3

def num_cols():
    return max_col() + 3

def is_sb(x,y):
    if (x>=-1 and x<=162 and y>=-1 and y<=130):
        return (x+1) % 2 == (y+1) % 2
    return False

def is_sb_big(x,y):
    if (x>=-1 and x<=162 and y>=-1 and y<=130):
        if (x+1) % 2 == 1 and (y+1) % 2 == 1:
            return False if (x+1) % 4 == (y+1) % 4 else True
        if (x+1) % 2 == 0 and (y+1) % 2 == 0:
            return False if (x+1) % 4 != (y+1) % 4 else True
    return False

def is_sb_sml(x,y):
    if (x>=-1 and x<=162 and y>=-1 and y<=130):
        if (x+1) % 2 == 1 and (y+1) % 2 == 1:
            return True if (x+1) % 4 == (y+1) % 4 else False
        if (x+1) % 2 == 0 and (y+1) % 2 == 0:
            return True if (x+1) % 4 != (y+1) % 4 else False
    return False

def get_sb_type(x,y):
    return "SB_BIG" if is_sb_big(x,y) else "SB_SML"

def is_cpe(x,y):
    return x>=1 and x<=160 and y>=1 and y<=128

def is_outmux(x,y):
    return is_cpe(x,y) and (x+1) % 2 == (y+1) % 2

def is_edge_left(x,y):
    return x==-2 and y>=1 and y<=128

def is_edge_right(x,y):
    return x==max_col() and y>=1 and y<=128

def is_edge_bottom(x,y):
    return y==-2 and x>=1 and x<=160

def is_edge_top(x,y):
    return y==max_row() and x>=28 and x<=160

def is_edge_io(x,y):
    if (y==-2 and x>=5 and x<=40): # IO Bank S3/WA
        return True
    if (y==-2 and x>=57 and x<=92):  # IO Bank S1/WB
        return True
    if (y==-2 and x>=101 and x<=136): # IO Bank S2/WC
        return True
    if (x==-2 and y>=25 and y<=60): # IO Bank W1/SA
        return True
    if (x==-2 and y>=69 and y<=104): # IO Bank W2/SB
        return True
    if (x==max_col() and y>=25 and y<=60): # IO Bank E1/NA
        return True
    if (x==max_col() and y>=69 and y<=104): # IO Bank E2/NB
        return True
    if (y==max_row() and x>=57 and x<=92): # IO Bank N1/EA
        return True
    if (y==max_row() and x>=101 and x<=136): # IO Bank N2/EB
        return True

def is_ram(x,y):
    return x in [33,65,97,129] and y in [1,17,33,49,65,81,97,113]

def get_full_tile_loc_str(x,y):
    tile_x = ((x-1)+16) % 8 + 1
    tile_y = ((y-1)+16) % 8 + 1
    tile   = ((((x+16-1) // 8)+2) % 4) + 1

    return f"t{tile}_x{tile_x}_y{tile_y}"

def get_tile_loc_str(x,y):
    tile_x = ((x-1)+16) % 8 + 1
    tile_y = ((y-1)+16) % 8 + 1

    return f"x{tile_x}_y{tile_y}"

@dataclass
class IOName:
    bank : str
    port : str
    num  : int

def get_io_name(x,y):
    if (y==-2 and x>=5 and x<=40): # IO Bank S3/WA
        x-=5
        return IOName("S3", "A" if x % 4==0 else "B", x//4)
    if (y==-2 and x>=57 and x<=92):  # IO Bank S1/WB
        x-=57
        return IOName("S1", "A" if x % 4==0 else "B", x//4)
    if (y==-2 and x>=101 and x<=136): # IO Bank S2/WC
        x-=101
        return IOName("S2", "A" if x % 4==0 else "B", x//4)
    if (x==-2 and y>=25 and y<=60): # IO Bank W1/SA
        y-=25
        return IOName("W1", "A" if y % 4==0 else "B", y//4)
    if (x==-2 and y>=69 and y<=104): # IO Bank W2/SB
        y-=69
        return IOName("W2", "A" if y % 4==0 else "B", y//4)
    if (x==max_col() and y>=25 and y<=60): # IO Bank E1/NA
        y-=25
        return IOName("E1", "A" if y % 4==0 else "B", y//4)
    if (x==max_col() and y>=69 and y<=104): # IO Bank E2/NB
        y-=69
        return IOName("E2", "A" if y % 4==0 else "B", y//4)
    if (y==max_row() and x>=57 and x<=92): # IO Bank N1/EA
        x-=57
        return IOName("N1", "A" if x % 4==0 else "B", x//4)
    if (y==max_row() and x>=101 and x<=136): # IO Bank N2/EB
        x-=101
        return IOName("N2", "A" if x % 4==0 else "B", x//4)

def is_gpio(x,y):
    if is_edge_io(x,y):
        if (y==-2 or y==max_row()):
            return x % 2==1
        if (x==-2 or x==max_col()):
            return y % 2==1
    return False

def is_pll(x,y):
    return x==PLL_X_POS and y==PLL_Y_POS

def is_serdes(x,y):
    return x==SERDES_X_POS and y==SERDES_Y_POS

def is_cfg_ctrl(x,y):
    return x==CTRL_X_POS and y==CTRL_Y_POS

def base_loc(x,y):
    return (((x-1) & ~1) + 1, ((y-1) & ~1) + 1)

class PinType(Enum):
    INPUT = 0
    OUTPUT = 1
    INOUT = 2

@dataclass(eq=True, order=True)
class Primitive:
    name : str
    type : str
    z    : int

@dataclass(eq=True, order=True)
class Pin:
    name : str
    dir  : PinType
    wire_type : str
    use_alias_conn: bool = False

@dataclass(eq=True, order=True)
class PinConstr:
    name : str
    rel_x : int
    rel_y : int
    output: int
    pin_num : int

@dataclass(eq=True, order=True)
class Group:
    name : str
    type : str

@dataclass(eq=True, order=True)
class Endpoint:
    name : str
    type : str

@dataclass(eq=True, order=True)
class MUX:
    src : str
    dst : str
    name : str
    bits : int
    value : int
    invert: bool
    visible: bool
    config: bool
    delay: str

@dataclass
class Location:
    x : int
    y : int
    z : int

@dataclass(eq=True, order=True)
class Connection:
    x : int
    y : int
    name : str
    delay: str

@dataclass(eq=True, order=True)
class TileInfo:
    die : int
    bit_x : int
    bit_y : int
    tile_x : int
    tile_y : int
    prim_index : int

PRIMITIVES_PINS = {
    "CPE_LT_U": [
        Pin("IN1"    ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("IN2"    ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("IN3"    ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("IN4"    ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("OUT"    ,PinType.OUTPUT, "CPE_WIRE", True),
    ],
    "CPE_FF_U": [
        Pin("DIN"    ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("CLK"    ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("EN"     ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("SR"     ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("DOUT"   ,PinType.OUTPUT, "CPE_WIRE", True),
    ],
    "CPE_RAMIO_U": [
        Pin("RAM_I"  ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("I"      ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("OUT"    ,PinType.OUTPUT, "CPE_WIRE", True),
        Pin("RAM_O"  ,PinType.OUTPUT, "CPE_WIRE", True),
    ],
    "CPE_LT_L": [
        Pin("IN1"    ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("IN2"    ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("IN3"    ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("IN4"    ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("OUT"    ,PinType.OUTPUT, "CPE_WIRE", True),
    ],
    "CPE_FF_L": [
        Pin("DIN"    ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("CLK"    ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("EN"     ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("SR"     ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("DOUT"   ,PinType.OUTPUT, "CPE_WIRE", True),
    ],
    "CPE_RAMIO_L": [
        Pin("RAM_I"  ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("I"      ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("OUT"    ,PinType.OUTPUT, "CPE_WIRE", True),
        Pin("RAM_O"  ,PinType.OUTPUT, "CPE_WIRE", True),
    ],
    "CPE_LT_FULL": [
        Pin("IN1"    ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("IN2"    ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("IN3"    ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("IN4"    ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("IN5"    ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("IN6"    ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("IN7"    ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("IN8"    ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("OUT1"   ,PinType.OUTPUT, "CPE_WIRE", True),
        Pin("OUT2"   ,PinType.OUTPUT, "CPE_WIRE", True),
    ],

    "CPE_LINES": [
        Pin("CINX"   ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("PINX"   ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("CINY1"  ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("PINY1"  ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("CINY2"  ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("PINY2"  ,PinType.INPUT,  "CPE_WIRE", True),
        Pin("COUTX"  ,PinType.OUTPUT, "CPE_WIRE", True),
        Pin("POUTX"  ,PinType.OUTPUT, "CPE_WIRE", True),
        Pin("COUTY1" ,PinType.OUTPUT, "CPE_WIRE", True),
        Pin("POUTY1" ,PinType.OUTPUT, "CPE_WIRE", True),
        Pin("COUTY2" ,PinType.OUTPUT, "CPE_WIRE", True),
        Pin("POUTY2" ,PinType.OUTPUT, "CPE_WIRE", True),
    ],

    "GPIO" : [
        Pin("IN1"   , PinType.OUTPUT,"GPIO_WIRE"),
        Pin("IN2"   , PinType.OUTPUT,"GPIO_WIRE"),
        Pin("OUT1"  , PinType.INPUT, "GPIO_WIRE"),
        Pin("OUT2"  , PinType.INPUT, "GPIO_WIRE"),
        Pin("OUT3"  , PinType.INPUT, "GPIO_WIRE"),
        Pin("OUT4"  , PinType.INPUT, "GPIO_WIRE"),
        Pin("DDR"   , PinType.INPUT, "GPIO_WIRE"),
        # Reset is global but no control over it
        #Pin("RESET" , PinType.INPUT, "GPIO_WIRE"),
        Pin("CLOCK1", PinType.INPUT, "GPIO_WIRE"),
        Pin("CLOCK2", PinType.INPUT, "GPIO_WIRE"),
        Pin("CLOCK3", PinType.INPUT, "GPIO_WIRE"),
        Pin("CLOCK4", PinType.INPUT, "GPIO_WIRE"),
        # PAD wires
        Pin("I",      PinType.INPUT, "GPIO_WIRE"),
        Pin("O",      PinType.OUTPUT,"GPIO_WIRE"),
        Pin("IO",     PinType.INOUT, "GPIO_WIRE"),
        # LVDS PAD wires
        Pin("I_P",    PinType.INPUT, "GPIO_WIRE"),
        Pin("I_N",    PinType.INPUT, "GPIO_WIRE"),
        Pin("O_P",    PinType.OUTPUT,"GPIO_WIRE"),
        Pin("O_N",    PinType.OUTPUT,"GPIO_WIRE"),
        Pin("IO_P",   PinType.INOUT, "GPIO_WIRE"),
        Pin("IO_N",   PinType.INOUT, "GPIO_WIRE"),
    ],
    "CLKIN" : [
        Pin("CLK0"     , PinType.INPUT, "CLKIN_WIRE"),
        Pin("CLK1"     , PinType.INPUT, "CLKIN_WIRE"),
        Pin("CLK2"     , PinType.INPUT, "CLKIN_WIRE"),
        Pin("CLK3"     , PinType.INPUT, "CLKIN_WIRE"),
        Pin("SER_CLK"  , PinType.INPUT, "CLKIN_WIRE"),
        Pin("CLK_REF0" , PinType.OUTPUT,"CLKIN_WIRE"),
        Pin("CLK_REF1" , PinType.OUTPUT,"CLKIN_WIRE"),
        Pin("CLK_REF2" , PinType.OUTPUT,"CLKIN_WIRE"),
        Pin("CLK_REF3" , PinType.OUTPUT,"CLKIN_WIRE"),
    ],
    "GLBOUT" : [
        Pin("CLK0_0"       , PinType.INPUT, "GLBOUT_WIRE"),
        Pin("CLK90_0"      , PinType.INPUT, "GLBOUT_WIRE"),
        Pin("CLK180_0"     , PinType.INPUT, "GLBOUT_WIRE"),
        Pin("CLK270_0"     , PinType.INPUT, "GLBOUT_WIRE"),
        Pin("CLK_REF_OUT0" , PinType.INPUT, "GLBOUT_WIRE"),
        Pin("USR_GLB0"     , PinType.INPUT, "GLBOUT_WIRE"),
        Pin("USR_FB0"      , PinType.INPUT, "GLBOUT_WIRE"),
        Pin("CLK_FB0"      , PinType.OUTPUT,"GLBOUT_WIRE"),
        Pin("GLB0"         , PinType.OUTPUT,"GLBOUT_WIRE"),
        Pin("CLK0_1"       , PinType.INPUT, "GLBOUT_WIRE"),
        Pin("CLK90_1"      , PinType.INPUT, "GLBOUT_WIRE"),
        Pin("CLK180_1"     , PinType.INPUT, "GLBOUT_WIRE"),
        Pin("CLK270_1"     , PinType.INPUT, "GLBOUT_WIRE"),
        Pin("CLK_REF_OUT1" , PinType.INPUT, "GLBOUT_WIRE"),
        Pin("USR_GLB1"     , PinType.INPUT, "GLBOUT_WIRE"),
        Pin("USR_FB1"      , PinType.INPUT, "GLBOUT_WIRE"),
        Pin("CLK_FB1"      , PinType.OUTPUT,"GLBOUT_WIRE"),
        Pin("GLB1"         , PinType.OUTPUT,"GLBOUT_WIRE"),
        Pin("CLK0_2"       , PinType.INPUT, "GLBOUT_WIRE"),
        Pin("CLK90_2"      , PinType.INPUT, "GLBOUT_WIRE"),
        Pin("CLK180_2"     , PinType.INPUT, "GLBOUT_WIRE"),
        Pin("CLK270_2"     , PinType.INPUT, "GLBOUT_WIRE"),
        Pin("CLK_REF_OUT2" , PinType.INPUT, "GLBOUT_WIRE"),
        Pin("USR_GLB2"     , PinType.INPUT, "GLBOUT_WIRE"),
        Pin("USR_FB2"      , PinType.INPUT, "GLBOUT_WIRE"),
        Pin("CLK_FB2"      , PinType.OUTPUT,"GLBOUT_WIRE"),
        Pin("GLB2"         , PinType.OUTPUT,"GLBOUT_WIRE"),
        Pin("CLK0_3"       , PinType.INPUT, "GLBOUT_WIRE"),
        Pin("CLK90_3"      , PinType.INPUT, "GLBOUT_WIRE"),
        Pin("CLK180_3"     , PinType.INPUT, "GLBOUT_WIRE"),
        Pin("CLK270_3"     , PinType.INPUT, "GLBOUT_WIRE"),
        Pin("CLK_REF_OUT3" , PinType.INPUT, "GLBOUT_WIRE"),
        Pin("USR_GLB3"     , PinType.INPUT, "GLBOUT_WIRE"),
        Pin("USR_FB3"      , PinType.INPUT, "GLBOUT_WIRE"),
        Pin("CLK_FB3"      , PinType.OUTPUT,"GLBOUT_WIRE"),
        Pin("GLB3"         , PinType.OUTPUT,"GLBOUT_WIRE"),
    ],
    "PLL" : [
        Pin("CLK_REF",             PinType.INPUT, "PLL_WIRE"),
        Pin("USR_CLK_REF",         PinType.INPUT, "PLL_WIRE"),
        Pin("USR_SEL_A_B",         PinType.INPUT, "PLL_WIRE"),
        Pin("CLK_FEEDBACK",        PinType.INPUT, "PLL_WIRE"),
        Pin("USR_LOCKED_STDY_RST", PinType.INPUT, "PLL_WIRE"),
        Pin("CLK0",                PinType.OUTPUT,"PLL_WIRE"),
        Pin("CLK90",               PinType.OUTPUT,"PLL_WIRE"),
        Pin("CLK180",              PinType.OUTPUT,"PLL_WIRE"),
        Pin("CLK270",              PinType.OUTPUT,"PLL_WIRE"),
        Pin("CLK_REF_OUT",         PinType.OUTPUT,"PLL_WIRE"),
        Pin("USR_PLL_LOCKED_STDY", PinType.OUTPUT,"PLL_WIRE"),
        Pin("USR_PLL_LOCKED",      PinType.OUTPUT,"PLL_WIRE"),
    ],
    "USR_RSTN" : [
        Pin("USR_RSTN", PinType.OUTPUT,"USR_RSTN_WIRE"),
    ],
    "CFG_CTRL" : [
        Pin("DATA[7]", PinType.INPUT,"CFG_CTRL_WIRE"),
        Pin("DATA[6]", PinType.INPUT,"CFG_CTRL_WIRE"),
        Pin("DATA[5]", PinType.INPUT,"CFG_CTRL_WIRE"),
        Pin("DATA[4]", PinType.INPUT,"CFG_CTRL_WIRE"),
        Pin("DATA[3]", PinType.INPUT,"CFG_CTRL_WIRE"),
        Pin("DATA[2]", PinType.INPUT,"CFG_CTRL_WIRE"),
        Pin("DATA[1]", PinType.INPUT,"CFG_CTRL_WIRE"),
        Pin("DATA[0]", PinType.INPUT,"CFG_CTRL_WIRE"),
        Pin("CLK", PinType.INPUT,"CFG_CTRL_WIRE"),
        Pin("EN", PinType.INPUT,"CFG_CTRL_WIRE"),
        Pin("VALID", PinType.INPUT,"CFG_CTRL_WIRE"),
        Pin("RECFG", PinType.INPUT,"CFG_CTRL_WIRE"),
    ],
    "RAM" : [
        Pin("C_ADDRA[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("C_ADDRA[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("C_ADDRA[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("C_ADDRA[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("C_ADDRA[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("C_ADDRA[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("C_ADDRA[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("C_ADDRA[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("C_ADDRB[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("C_ADDRB[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("C_ADDRB[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("C_ADDRB[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("C_ADDRB[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("C_ADDRB[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("C_ADDRB[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("C_ADDRB[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("CLKA[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("CLKA[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("ENA[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("ENA[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("GLWEA[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("GLWEA[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[8]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[9]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[10]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[11]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[12]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[13]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[14]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0[15]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[8]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[9]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[10]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[11]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[12]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[13]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[14]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA0X[15]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[8]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[9]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[10]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[11]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[12]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[13]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[14]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[15]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[16]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[17]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[18]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[19]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[8]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[9]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[10]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[11]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[12]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[13]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[14]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[15]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[16]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[17]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[18]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[19]", PinType.INPUT,"RAM_WIRE"),
        Pin("CLKA[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("CLKA[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("ENA[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("ENA[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("GLWEA[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("GLWEA[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[8]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[9]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[10]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[11]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[12]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[13]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[14]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1[15]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[8]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[9]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[10]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[11]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[12]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[13]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[14]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRA1X[15]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[20]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[21]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[22]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[23]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[24]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[25]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[26]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[27]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[28]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[29]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[30]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[31]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[32]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[33]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[34]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[35]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[36]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[37]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[38]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIA[39]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[20]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[21]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[22]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[23]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[24]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[25]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[26]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[27]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[28]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[29]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[30]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[31]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[32]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[33]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[34]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[35]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[36]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[37]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[38]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEA[39]", PinType.INPUT,"RAM_WIRE"),
        Pin("CLKB[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("CLKB[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("ENB[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("ENB[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("GLWEB[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("GLWEB[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[8]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[9]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[10]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[11]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[12]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[13]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[14]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0[15]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[8]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[9]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[10]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[11]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[12]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[13]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[14]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB0X[15]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[8]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[9]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[10]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[11]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[12]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[13]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[14]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[15]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[16]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[17]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[18]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[19]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[8]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[9]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[10]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[11]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[12]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[13]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[14]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[15]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[16]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[17]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[18]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[19]", PinType.INPUT,"RAM_WIRE"),
        Pin("CLKB[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("CLKB[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("ENB[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("ENB[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("GLWEB[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("GLWEB[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[8]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[9]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[10]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[11]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[12]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[13]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[14]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1[15]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[0]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[1]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[2]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[3]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[4]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[5]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[6]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[7]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[8]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[9]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[10]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[11]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[12]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[13]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[14]", PinType.INPUT,"RAM_WIRE"),
        Pin("ADDRB1X[15]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[20]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[21]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[22]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[23]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[24]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[25]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[26]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[27]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[28]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[29]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[30]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[31]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[32]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[33]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[34]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[35]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[36]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[37]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[38]", PinType.INPUT,"RAM_WIRE"),
        Pin("DIB[39]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[20]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[21]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[22]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[23]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[24]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[25]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[26]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[27]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[28]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[29]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[30]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[31]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[32]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[33]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[34]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[35]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[36]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[37]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[38]", PinType.INPUT,"RAM_WIRE"),
        Pin("WEB[39]", PinType.INPUT,"RAM_WIRE"),
        Pin("F_RSTN", PinType.INPUT,"RAM_WIRE"),
        Pin("DOA[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[4]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[4]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[5]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[5]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[6]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[6]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[7]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[7]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[8]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[8]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[9]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[9]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[10]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[10]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[11]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[11]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[12]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[12]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[13]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[13]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[14]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[14]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[15]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[15]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[16]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[16]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[17]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[17]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[18]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[18]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[19]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[19]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[20]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[20]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[21]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[21]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[22]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[22]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[23]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[23]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[24]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[24]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[25]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[25]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[26]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[26]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[27]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[27]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[28]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[28]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[29]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[29]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[30]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[30]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[31]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[31]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[32]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[32]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[33]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[33]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[34]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[34]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[35]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[35]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[36]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[36]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[37]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[37]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[38]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[38]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOA[39]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOAX[39]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("CLOCKA[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("CLOCKA[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("CLOCKA[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("CLOCKA[4]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[4]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[4]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[5]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[5]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[6]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[6]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[7]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[7]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[8]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[8]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[9]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[9]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[10]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[10]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[11]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[11]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[12]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[12]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[13]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[13]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[14]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[14]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[15]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[15]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[16]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[16]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[17]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[17]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[18]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[18]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[19]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[19]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[20]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[20]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[21]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[21]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[22]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[22]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[23]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[23]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[24]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[24]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[25]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[25]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[26]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[26]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[27]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[27]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[28]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[28]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[29]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[29]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[30]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[30]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[31]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[31]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[32]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[32]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[33]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[33]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[34]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[34]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[35]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[35]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[36]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[36]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[37]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[37]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[38]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[38]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOB[39]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("DOBX[39]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("CLOCKB[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("CLOCKB[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("CLOCKB[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("CLOCKB[4]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC1B_ERRA[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC1B_ERRA[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC1B_ERRA[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC1B_ERRA[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC1B_ERRB[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC1B_ERRB[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC1B_ERRB[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC1B_ERRB[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC2B_ERRA[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC2B_ERRA[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC2B_ERRA[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC2B_ERRA[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC2B_ERRB[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC2B_ERRB[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC2B_ERRB[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("ECC2B_ERRB[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("F_FULL[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("F_FULL[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("F_EMPTY[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("F_EMPTY[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("F_AL_FULL[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("F_AL_FULL[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("F_AL_EMPTY[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("F_AL_EMPTY[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ERR[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ERR[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ERR[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ERR[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[4]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[4]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[5]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[5]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[6]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[6]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[7]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[7]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[8]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[8]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[9]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[9]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[10]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[10]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[11]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[11]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[12]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[12]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[13]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[13]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[14]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[14]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDR[15]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FWR_ADDRX[15]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[0]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[1]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[2]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[3]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[4]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[4]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[5]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[5]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[6]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[6]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[7]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[7]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[8]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[8]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[9]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[9]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[10]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[10]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[11]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[11]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[12]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[12]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[13]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[13]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[14]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[14]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDR[15]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("FRD_ADDRX[15]", PinType.OUTPUT,"RAM_WIRE"),
        Pin("CLOCK1", PinType.INPUT,"RAM_WIRE"),
        Pin("CLOCK2", PinType.INPUT,"RAM_WIRE"),
        Pin("CLOCK3", PinType.INPUT,"RAM_WIRE"),
        Pin("CLOCK4", PinType.INPUT,"RAM_WIRE"),
    ],
    "SERDES" : [
        Pin("TX_DETECT_RX_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("PLL_RESET_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_CLK_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CLK_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_CLK_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_WE_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_EN_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_RESET_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_PCS_RESET_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_PMA_RESET_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_PRBS_FORCE_ERR_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_POLARITY_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_8B10B_EN_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_RESET_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_PMA_RESET_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_EQA_RESET_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_CDR_RESET_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_PCS_RESET_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_BUF_RESET_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_PRBS_CNT_RESET_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_EN_EI_DETECTOR_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_COMMA_DETECT_EN_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_SLIDE_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_POLARITY_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_8B10B_EN_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_MCOMMA_ALIGN_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_PCOMMA_ALIGN_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_NOT_IN_TABLE_O[7]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_NOT_IN_TABLE_O[6]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_NOT_IN_TABLE_O[5]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_NOT_IN_TABLE_O[4]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_NOT_IN_TABLE_O[3]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_NOT_IN_TABLE_O[2]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_NOT_IN_TABLE_O[1]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_NOT_IN_TABLE_O[0]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_COMMA_O[7]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_COMMA_O[6]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_COMMA_O[5]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_COMMA_O[4]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_COMMA_O[3]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_COMMA_O[2]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_COMMA_O[1]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_COMMA_O[0]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_ADDR_I[7]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_ADDR_I[6]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_ADDR_I[5]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_ADDR_I[4]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_ADDR_I[3]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_ADDR_I[2]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_ADDR_I[1]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_ADDR_I[0]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_IS_K_I[7]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_IS_K_I[6]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_IS_K_I[5]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_IS_K_I[4]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_IS_K_I[3]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_IS_K_I[2]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_IS_K_I[1]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_IS_K_I[0]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_8B10B_BYPASS_I[7]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_8B10B_BYPASS_I[6]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_8B10B_BYPASS_I[5]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_8B10B_BYPASS_I[4]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_8B10B_BYPASS_I[3]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_8B10B_BYPASS_I[2]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_8B10B_BYPASS_I[1]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_8B10B_BYPASS_I[0]", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_8B10B_BYPASS_I[7]", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_8B10B_BYPASS_I[6]", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_8B10B_BYPASS_I[5]", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_8B10B_BYPASS_I[4]", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_8B10B_BYPASS_I[3]", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_8B10B_BYPASS_I[2]", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_8B10B_BYPASS_I[1]", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_8B10B_BYPASS_I[0]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPMODE_I[7]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPMODE_I[6]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPMODE_I[5]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPMODE_I[4]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPMODE_I[3]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPMODE_I[2]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPMODE_I[1]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPMODE_I[0]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPVAL_I[7]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPVAL_I[6]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPVAL_I[5]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPVAL_I[4]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPVAL_I[3]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPVAL_I[2]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPVAL_I[1]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_CHAR_DISPVAL_I[0]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[63]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[62]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[61]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[60]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[59]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[58]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[57]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[56]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[55]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[54]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[53]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[52]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[51]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[50]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[49]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[48]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[47]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[46]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[45]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[44]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[43]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[42]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[41]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[40]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[39]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[38]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[37]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[36]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[35]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[34]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[33]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[32]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[31]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[30]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[29]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[28]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[27]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[26]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[25]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[24]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[23]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[22]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[21]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[20]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[19]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[18]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[17]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[16]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[15]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[14]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[13]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[12]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[11]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[10]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[9]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[8]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[7]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[6]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[5]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[4]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[3]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[2]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[1]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_DATA_I[0]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[15]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[14]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[13]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[12]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[11]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[10]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[9]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[8]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[7]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[6]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[5]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[4]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[3]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[2]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[1]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DO_O[0]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[15]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[14]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[13]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[12]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[11]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[10]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[9]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[8]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[7]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[6]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[5]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[4]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[3]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[2]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[1]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_DI_I[0]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[15]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[14]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[13]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[12]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[11]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[10]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[9]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[8]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[7]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[6]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[5]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[4]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[3]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[2]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[1]", PinType.INPUT,"SERDES_WIRE"),
        Pin("REGFILE_MASK_I[0]", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_K_O[7]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_K_O[6]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_K_O[5]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_K_O[4]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_K_O[3]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_K_O[2]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_K_O[1]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CHAR_IS_K_O[0]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DISP_ERR_O[7]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DISP_ERR_O[6]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DISP_ERR_O[5]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DISP_ERR_O[4]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DISP_ERR_O[3]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DISP_ERR_O[2]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DISP_ERR_O[1]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DISP_ERR_O[0]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[63]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[62]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[61]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[60]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[59]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[58]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[57]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[56]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[55]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[54]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[53]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[52]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[51]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[50]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[49]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[48]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[47]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[46]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[45]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[44]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[43]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[42]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[41]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[40]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[39]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[38]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[37]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[36]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[35]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[34]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[33]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[32]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[31]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[30]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[29]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[28]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[27]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[26]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[25]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[24]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[23]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[22]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[21]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[20]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[19]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[18]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[17]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[16]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[15]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[14]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[13]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[12]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[11]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[10]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[9]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[8]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[7]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[6]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[5]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[4]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[3]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[2]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[1]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_DATA_O[0]", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("TX_DETECT_RX_DONE_O", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("TX_DETECT_RX_PRESENT_O", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_CLK_O", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("PLL_CLK_O", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("TX_BUF_ERR_O", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("TX_RESET_DONE_O", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("REGFILE_RDY_O", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_PRBS_ERR_O", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_BUF_ERR_O", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_BYTE_IS_ALIGNED_O", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_BYTE_REALIGN_O", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_RESET_DONE_O", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("RX_EI_EN_O", PinType.OUTPUT,"SERDES_WIRE"),
        Pin("LOOPBACK_I[2]", PinType.INPUT,"SERDES_WIRE"),
        Pin("LOOPBACK_I[1]", PinType.INPUT,"SERDES_WIRE"),
        Pin("LOOPBACK_I[0]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_PRBS_SEL_I[2]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_PRBS_SEL_I[1]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_PRBS_SEL_I[0]", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_PRBS_SEL_I[2]", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_PRBS_SEL_I[1]", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_PRBS_SEL_I[0]", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_POWER_DOWN_N_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("RX_POWER_DOWN_N_I", PinType.INPUT,"SERDES_WIRE"),
        Pin("TX_ELEC_IDLE_I", PinType.INPUT,"SERDES_WIRE"),
    ],
}

def get_groups_for_type(type):
    groups = []
    def create_group(name, type):
        groups.append(Group(name,type))

    if "CPE" in type:
        # CPE
        for p in range(1,13):
            create_group(f"IM_P{p:02d}", "IM")
            if "OM" in type and p>=9:
                create_group(f"OM_P{p:02d}", "OM")
    if "SB_BIG" in type:
        # SB_BIG
        for p in range(1,13):
            create_group(f"SB_BIG_P{p:02d}", "SB_BIG")
    if "SB_SML" in type:
        # SB_SML
        for p in range(1,13):
            create_group(f"SB_SML_P{p:02d}", "SB_SML")
    #if "GPIO" in type:
    #    # GPIO
    if "IOES" in type:
        # IOES
        create_group("IOES", "IOES")
    if "LES" in type:
        # LES
        create_group("LES", "LES")
    if "RES" in type:
        # RES
        create_group("RES", "RES")
    if "TES" in type:
        # TES
        create_group("TES", "TES")
    if "BES" in type:
        # BES
        create_group("BES", "BES")
    return groups

def get_primitives_for_type(type):
    primitives = []
    if "CPE" in type:
        primitives.append(Primitive("CPE_LT_U","CPE_LT_U",0))
        primitives.append(Primitive("CPE_LT_L","CPE_LT_L",1))
        primitives.append(Primitive("CPE_FF_U","CPE_FF_U",2))
        primitives.append(Primitive("CPE_FF_L","CPE_FF_L",3))
        primitives.append(Primitive("CPE_RAMIO_U","CPE_RAMIO_U",4))
        primitives.append(Primitive("CPE_RAMIO_L","CPE_RAMIO_L",5))
        primitives.append(Primitive("CPE_LINES","CPE_LINES",6))
        primitives.append(Primitive("CPE_LT_FULL","CPE_LT_FULL",7))
    if "RAM" in type:
        primitives.append(Primitive("RAM","RAM",8))
    if "SERDES" in type:
        primitives.append(Primitive("SERDES","SERDES",8))
    if "GPIO" in type:
        primitives.append(Primitive("GPIO","GPIO",0))
    if "PLL" in type:
        primitives.append(Primitive("CLKIN","CLKIN",0))
        primitives.append(Primitive("GLBOUT","GLBOUT",1))
        primitives.append(Primitive("PLL0","PLL",2))
        primitives.append(Primitive("PLL1","PLL",3))
        primitives.append(Primitive("PLL2","PLL",4))
        primitives.append(Primitive("PLL3","PLL",5))
    if "CFG_CTRL" in type:
        primitives.append(Primitive("CFG_CTRL","CFG_CTRL",8))
        primitives.append(Primitive("USR_RSTN","USR_RSTN",9))
    return primitives

def get_primitive_pins(bel):
    return PRIMITIVES_PINS[bel]

def get_pins_constraint(type_name, prim_name, prim_type):
    val = []
    if prim_type=="USR_RSTN":
        val.append(PinConstr("USR_RSTN", -CTRL_X_POS+1, -CTRL_Y_POS+66, RAM_INPUT, 2))
    elif prim_type=="CFG_CTRL":
        val.append(PinConstr("DATA[7]", -CTRL_X_POS+1, -CTRL_Y_POS+16, RAM_OUTPUT, 1))
        val.append(PinConstr("DATA[6]", -CTRL_X_POS+1, -CTRL_Y_POS+15, RAM_OUTPUT, 1))
        val.append(PinConstr("DATA[5]", -CTRL_X_POS+1, -CTRL_Y_POS+14, RAM_OUTPUT, 1))
        val.append(PinConstr("DATA[4]", -CTRL_X_POS+1, -CTRL_Y_POS+13, RAM_OUTPUT, 1))
        val.append(PinConstr("DATA[3]", -CTRL_X_POS+1, -CTRL_Y_POS+12, RAM_OUTPUT, 1))
        val.append(PinConstr("DATA[2]", -CTRL_X_POS+1, -CTRL_Y_POS+11, RAM_OUTPUT, 1))
        val.append(PinConstr("DATA[1]", -CTRL_X_POS+1, -CTRL_Y_POS+10, RAM_OUTPUT, 1))
        val.append(PinConstr("DATA[0]", -CTRL_X_POS+1, -CTRL_Y_POS+ 9, RAM_OUTPUT, 1))
        val.append(PinConstr("CLK",-CTRL_X_POS+1, -CTRL_Y_POS+6, RAM_OUTPUT, 1))
        val.append(PinConstr("EN",-CTRL_X_POS+1, -CTRL_Y_POS+7, RAM_OUTPUT, 1))
        val.append(PinConstr("VALID",-CTRL_X_POS+1, -CTRL_Y_POS+8, RAM_OUTPUT, 1))
        val.append(PinConstr("RECFG",-CTRL_X_POS+1, -CTRL_Y_POS+5, RAM_OUTPUT, 1))
    elif prim_type=="RAM":
        val.append(PinConstr("C_ADDRA[0]", -3, 2, RAM_OUTPUT, 1))
        val.append(PinConstr("C_ADDRA[1]", -3, 2, RAM_OUTPUT, 2))
        val.append(PinConstr("C_ADDRA[2]", -3, 3, RAM_OUTPUT, 1))
        val.append(PinConstr("C_ADDRA[3]", -3, 3, RAM_OUTPUT, 2))
        val.append(PinConstr("C_ADDRA[4]", -3, 4, RAM_OUTPUT, 1))
        val.append(PinConstr("C_ADDRA[5]", -3, 4, RAM_OUTPUT, 2))
        val.append(PinConstr("C_ADDRA[6]", -3, 5, RAM_OUTPUT, 1))
        val.append(PinConstr("C_ADDRA[7]", -3, 5, RAM_OUTPUT, 2))
        val.append(PinConstr("C_ADDRB[0]", 2, 2, RAM_OUTPUT, 1))
        val.append(PinConstr("C_ADDRB[1]", 2, 2, RAM_OUTPUT, 2))
        val.append(PinConstr("C_ADDRB[2]", 2, 3, RAM_OUTPUT, 1))
        val.append(PinConstr("C_ADDRB[3]", 2, 3, RAM_OUTPUT, 2))
        val.append(PinConstr("C_ADDRB[4]", 2, 4, RAM_OUTPUT, 1))
        val.append(PinConstr("C_ADDRB[5]", 2, 4, RAM_OUTPUT, 2))
        val.append(PinConstr("C_ADDRB[6]", 2, 5, RAM_OUTPUT, 1))
        val.append(PinConstr("C_ADDRB[7]", 2, 5, RAM_OUTPUT, 2))
        val.append(PinConstr("CLKA[0]", -6, 0, RAM_OUTPUT, 1))
        val.append(PinConstr("CLKA[1]", -3, 0, RAM_OUTPUT, 1))
        val.append(PinConstr("ENA[0]", -6, 1, RAM_OUTPUT, 1))
        val.append(PinConstr("ENA[1]", -3, 1, RAM_OUTPUT, 1))
        val.append(PinConstr("GLWEA[0]", -6, 0, RAM_OUTPUT, 2))
        val.append(PinConstr("GLWEA[1]", -3, 0, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRA0[0]", -5, 0, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA0[1]", -5, 0, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRA0[2]", -5, 1, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA0[3]", -5, 1, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRA0[4]", -5, 2, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA0[5]", -5, 2, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRA0[6]", -5, 3, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA0[7]", -5, 3, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRA0[8]", -5, 4, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA0[9]", -5, 4, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRA0[10]", -5, 5, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA0[11]", -5, 5, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRA0[12]", -5, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA0[13]", -5, 6, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRA0[14]", -5, 7, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA0[15]", -5, 7, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRA0X[0]", -5, 0, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA0X[1]", -4, 0, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA0X[2]", -5, 1, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA0X[3]", -4, 1, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA0X[4]", -5, 2, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA0X[5]", -4, 2, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA0X[6]", -5, 3, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA0X[7]", -4, 3, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA0X[8]", -5, 4, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA0X[9]", -4, 4, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA0X[10]", -5, 5, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA0X[11]", -4, 5, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA0X[12]", -6, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA0X[13]", -5, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA0X[14]", -6, 7, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA0X[15]", -5, 7, RAM_OUTPUT, 1))
        val.append(PinConstr("DIA[0]", -1, 0, RAM_OUTPUT, 1))
        val.append(PinConstr("DIA[1]", -1, 0, RAM_OUTPUT, 2))
        val.append(PinConstr("DIA[2]", -1, 1, RAM_OUTPUT, 1))
        val.append(PinConstr("DIA[3]", -1, 1, RAM_OUTPUT, 2))
        val.append(PinConstr("DIA[4]", -1, 2, RAM_OUTPUT, 1))
        val.append(PinConstr("DIA[5]", -1, 2, RAM_OUTPUT, 2))
        val.append(PinConstr("DIA[6]", -1, 3, RAM_OUTPUT, 1))
        val.append(PinConstr("DIA[7]", -1, 3, RAM_OUTPUT, 2))
        val.append(PinConstr("DIA[8]", -1, 4, RAM_OUTPUT, 1))
        val.append(PinConstr("DIA[9]", -1, 4, RAM_OUTPUT, 2))
        val.append(PinConstr("DIA[10]", -1, 5, RAM_OUTPUT, 1))
        val.append(PinConstr("DIA[11]", -1, 5, RAM_OUTPUT, 2))
        val.append(PinConstr("DIA[12]", -1, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("DIA[13]", -1, 6, RAM_OUTPUT, 2))
        val.append(PinConstr("DIA[14]", -1, 7, RAM_OUTPUT, 1))
        val.append(PinConstr("DIA[15]", -1, 7, RAM_OUTPUT, 2))
        val.append(PinConstr("DIA[16]", -3, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("DIA[17]", -3, 6, RAM_OUTPUT, 2))
        val.append(PinConstr("DIA[18]", -3, 7, RAM_OUTPUT, 1))
        val.append(PinConstr("DIA[19]", -3, 7, RAM_OUTPUT, 2))
        val.append(PinConstr("WEA[0]", -2, 0, RAM_OUTPUT, 1))
        val.append(PinConstr("WEA[1]", -2, 0, RAM_OUTPUT, 2))
        val.append(PinConstr("WEA[2]", -2, 1, RAM_OUTPUT, 1))
        val.append(PinConstr("WEA[3]", -2, 1, RAM_OUTPUT, 2))
        val.append(PinConstr("WEA[4]", -2, 2, RAM_OUTPUT, 1))
        val.append(PinConstr("WEA[5]", -2, 2, RAM_OUTPUT, 2))
        val.append(PinConstr("WEA[6]", -2, 3, RAM_OUTPUT, 1))
        val.append(PinConstr("WEA[7]", -2, 3, RAM_OUTPUT, 2))
        val.append(PinConstr("WEA[8]", -2, 4, RAM_OUTPUT, 1))
        val.append(PinConstr("WEA[9]", -2, 4, RAM_OUTPUT, 2))
        val.append(PinConstr("WEA[10]", -2, 5, RAM_OUTPUT, 1))
        val.append(PinConstr("WEA[11]", -2, 5, RAM_OUTPUT, 2))
        val.append(PinConstr("WEA[12]", -2, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("WEA[13]", -2, 6, RAM_OUTPUT, 2))
        val.append(PinConstr("WEA[14]", -2, 7, RAM_OUTPUT, 1))
        val.append(PinConstr("WEA[15]", -2, 7, RAM_OUTPUT, 2))
        val.append(PinConstr("WEA[16]", -4, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("WEA[17]", -4, 6, RAM_OUTPUT, 2))
        val.append(PinConstr("WEA[18]", -4, 7, RAM_OUTPUT, 1))
        val.append(PinConstr("WEA[19]", -4, 7, RAM_OUTPUT, 2))
        val.append(PinConstr("CLKA[2]", -6, 8, RAM_OUTPUT, 1))
        val.append(PinConstr("CLKA[3]", -3, 8, RAM_OUTPUT, 1))
        val.append(PinConstr("ENA[2]", -6, 9, RAM_OUTPUT, 1))
        val.append(PinConstr("ENA[3]", -3, 9, RAM_OUTPUT, 1))
        val.append(PinConstr("GLWEA[2]", -6, 8, RAM_OUTPUT, 2))
        val.append(PinConstr("GLWEA[3]", -3, 8, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRA1[0]", -5, 8, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA1[1]", -5, 8, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRA1[2]", -5, 9, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA1[3]", -5, 9, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRA1[4]", -5, 10, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA1[5]", -5, 10, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRA1[6]", -5, 11, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA1[7]", -5, 11, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRA1[8]", -5, 12, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA1[9]", -5, 12, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRA1[10]", -5, 13, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA1[11]", -5, 13, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRA1[12]", -5, 14, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA1[13]", -5, 14, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRA1[14]", -5, 15, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA1[15]", -5, 15, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRA1X[0]", -5, 8, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA1X[1]", -4, 8, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA1X[2]", -5, 9, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA1X[3]", -4, 9, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA1X[4]", -5, 10, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA1X[5]", -4, 10, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA1X[6]", -5, 11, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA1X[7]", -4, 11, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA1X[8]", -5, 12, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA1X[9]", -4, 12, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA1X[10]", -5, 13, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA1X[11]", -4, 13, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA1X[12]", -6, 14, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA1X[13]", -5, 14, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA1X[14]", -6, 15, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRA1X[15]", -5, 15, RAM_OUTPUT, 1))
        val.append(PinConstr("DIA[20]", -1, 8, RAM_OUTPUT, 1))
        val.append(PinConstr("DIA[21]", -1, 8, RAM_OUTPUT, 2))
        val.append(PinConstr("DIA[22]", -1, 9, RAM_OUTPUT, 1))
        val.append(PinConstr("DIA[23]", -1, 9, RAM_OUTPUT, 2))
        val.append(PinConstr("DIA[24]", -1, 10, RAM_OUTPUT, 1))
        val.append(PinConstr("DIA[25]", -1, 10, RAM_OUTPUT, 2))
        val.append(PinConstr("DIA[26]", -1, 11, RAM_OUTPUT, 1))
        val.append(PinConstr("DIA[27]", -1, 11, RAM_OUTPUT, 2))
        val.append(PinConstr("DIA[28]", -1, 12, RAM_OUTPUT, 1))
        val.append(PinConstr("DIA[29]", -1, 12, RAM_OUTPUT, 2))
        val.append(PinConstr("DIA[30]", -1, 13, RAM_OUTPUT, 1))
        val.append(PinConstr("DIA[31]", -1, 13, RAM_OUTPUT, 2))
        val.append(PinConstr("DIA[32]", -1, 14, RAM_OUTPUT, 1))
        val.append(PinConstr("DIA[33]", -1, 14, RAM_OUTPUT, 2))
        val.append(PinConstr("DIA[34]", -1, 15, RAM_OUTPUT, 1))
        val.append(PinConstr("DIA[35]", -1, 15, RAM_OUTPUT, 2))
        val.append(PinConstr("DIA[36]", -3, 14, RAM_OUTPUT, 1))
        val.append(PinConstr("DIA[37]", -3, 14, RAM_OUTPUT, 2))
        val.append(PinConstr("DIA[38]", -3, 15, RAM_OUTPUT, 1))
        val.append(PinConstr("DIA[39]", -3, 15, RAM_OUTPUT, 2))
        val.append(PinConstr("WEA[20]", -2, 8, RAM_OUTPUT, 1))
        val.append(PinConstr("WEA[21]", -2, 8, RAM_OUTPUT, 2))
        val.append(PinConstr("WEA[22]", -2, 9, RAM_OUTPUT, 1))
        val.append(PinConstr("WEA[23]", -2, 9, RAM_OUTPUT, 2))
        val.append(PinConstr("WEA[24]", -2, 10, RAM_OUTPUT, 1))
        val.append(PinConstr("WEA[25]", -2, 10, RAM_OUTPUT, 2))
        val.append(PinConstr("WEA[26]", -2, 11, RAM_OUTPUT, 1))
        val.append(PinConstr("WEA[27]", -2, 11, RAM_OUTPUT, 2))
        val.append(PinConstr("WEA[28]", -2, 12, RAM_OUTPUT, 1))
        val.append(PinConstr("WEA[29]", -2, 12, RAM_OUTPUT, 2))
        val.append(PinConstr("WEA[30]", -2, 13, RAM_OUTPUT, 1))
        val.append(PinConstr("WEA[31]", -2, 13, RAM_OUTPUT, 2))
        val.append(PinConstr("WEA[32]", -2, 14, RAM_OUTPUT, 1))
        val.append(PinConstr("WEA[33]", -2, 14, RAM_OUTPUT, 2))
        val.append(PinConstr("WEA[34]", -2, 15, RAM_OUTPUT, 1))
        val.append(PinConstr("WEA[35]", -2, 15, RAM_OUTPUT, 2))
        val.append(PinConstr("WEA[36]", -4, 14, RAM_OUTPUT, 1))
        val.append(PinConstr("WEA[37]", -4, 14, RAM_OUTPUT, 2))
        val.append(PinConstr("WEA[38]", -4, 15, RAM_OUTPUT, 1))
        val.append(PinConstr("WEA[39]", -4, 15, RAM_OUTPUT, 2))
        val.append(PinConstr("CLKB[0]", 2, 0, RAM_OUTPUT, 1))
        val.append(PinConstr("CLKB[1]", 5, 0, RAM_OUTPUT, 1))
        val.append(PinConstr("ENB[0]", 2, 1, RAM_OUTPUT, 1))
        val.append(PinConstr("ENB[1]", 5, 1, RAM_OUTPUT, 1))
        val.append(PinConstr("GLWEB[0]", 2, 0, RAM_OUTPUT, 2))
        val.append(PinConstr("GLWEB[1]", 5, 0, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRB0[0]", 4, 0, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB0[1]", 4, 0, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRB0[2]", 4, 1, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB0[3]", 4, 1, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRB0[4]", 4, 2, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB0[5]", 4, 2, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRB0[6]", 4, 3, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB0[7]", 4, 3, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRB0[8]", 4, 4, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB0[9]", 4, 4, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRB0[10]", 4, 5, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB0[11]", 4, 5, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRB0[12]", 4, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB0[13]", 4, 6, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRB0[14]", 4, 7, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB0[15]", 4, 7, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRB0X[0]", 3, 0, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB0X[1]", 4, 0, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB0X[2]", 3, 1, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB0X[3]", 4, 1, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB0X[4]", 3, 2, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB0X[5]", 4, 2, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB0X[6]", 3, 3, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB0X[7]", 4, 3, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB0X[8]", 3, 4, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB0X[9]", 4, 4, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB0X[10]", 3, 5, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB0X[11]", 4, 5, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB0X[12]", 4, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB0X[13]", 5, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB0X[14]", 4, 7, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB0X[15]", 5, 7, RAM_OUTPUT, 1))
        val.append(PinConstr("DIB[0]", 1, 0, RAM_OUTPUT, 1))
        val.append(PinConstr("DIB[1]", 1, 0, RAM_OUTPUT, 2))
        val.append(PinConstr("DIB[2]", 1, 1, RAM_OUTPUT, 1))
        val.append(PinConstr("DIB[3]", 1, 1, RAM_OUTPUT, 2))
        val.append(PinConstr("DIB[4]", 1, 2, RAM_OUTPUT, 1))
        val.append(PinConstr("DIB[5]", 1, 2, RAM_OUTPUT, 2))
        val.append(PinConstr("DIB[6]", 1, 3, RAM_OUTPUT, 1))
        val.append(PinConstr("DIB[7]", 1, 3, RAM_OUTPUT, 2))
        val.append(PinConstr("DIB[8]", 1, 4, RAM_OUTPUT, 1))
        val.append(PinConstr("DIB[9]", 1, 4, RAM_OUTPUT, 2))
        val.append(PinConstr("DIB[10]", 1, 5, RAM_OUTPUT, 1))
        val.append(PinConstr("DIB[11]", 1, 5, RAM_OUTPUT, 2))
        val.append(PinConstr("DIB[12]", 1, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("DIB[13]", 1, 6, RAM_OUTPUT, 2))
        val.append(PinConstr("DIB[14]", 1, 7, RAM_OUTPUT, 1))
        val.append(PinConstr("DIB[15]", 1, 7, RAM_OUTPUT, 2))
        val.append(PinConstr("DIB[16]", 3, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("DIB[17]", 3, 6, RAM_OUTPUT, 2))
        val.append(PinConstr("DIB[18]", 3, 7, RAM_OUTPUT, 1))
        val.append(PinConstr("DIB[19]", 3, 7, RAM_OUTPUT, 2))
        val.append(PinConstr("WEB[0]", 0, 0, RAM_OUTPUT, 1))
        val.append(PinConstr("WEB[1]", 0, 0, RAM_OUTPUT, 2))
        val.append(PinConstr("WEB[2]", 0, 1, RAM_OUTPUT, 1))
        val.append(PinConstr("WEB[3]", 0, 1, RAM_OUTPUT, 2))
        val.append(PinConstr("WEB[4]", 0, 2, RAM_OUTPUT, 1))
        val.append(PinConstr("WEB[5]", 0, 2, RAM_OUTPUT, 2))
        val.append(PinConstr("WEB[6]", 0, 3, RAM_OUTPUT, 1))
        val.append(PinConstr("WEB[7]", 0, 3, RAM_OUTPUT, 2))
        val.append(PinConstr("WEB[8]", 0, 4, RAM_OUTPUT, 1))
        val.append(PinConstr("WEB[9]", 0, 4, RAM_OUTPUT, 2))
        val.append(PinConstr("WEB[10]", 0, 5, RAM_OUTPUT, 1))
        val.append(PinConstr("WEB[11]", 0, 5, RAM_OUTPUT, 2))
        val.append(PinConstr("WEB[12]", 0, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("WEB[13]", 0, 6, RAM_OUTPUT, 2))
        val.append(PinConstr("WEB[14]", 0, 7, RAM_OUTPUT, 1))
        val.append(PinConstr("WEB[15]", 0, 7, RAM_OUTPUT, 2))
        val.append(PinConstr("WEB[16]", 2, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("WEB[17]", 2, 6, RAM_OUTPUT, 2))
        val.append(PinConstr("WEB[18]", 2, 7, RAM_OUTPUT, 1))
        val.append(PinConstr("WEB[19]", 2, 7, RAM_OUTPUT, 2))
        val.append(PinConstr("CLKB[2]", 2, 8, RAM_OUTPUT, 1))
        val.append(PinConstr("CLKB[3]", 5, 8, RAM_OUTPUT, 1))
        val.append(PinConstr("ENB[2]", 2, 9, RAM_OUTPUT, 1))
        val.append(PinConstr("ENB[3]", 5, 9, RAM_OUTPUT, 1))
        val.append(PinConstr("GLWEB[2]", 2, 8, RAM_OUTPUT, 2))
        val.append(PinConstr("GLWEB[3]", 5, 8, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRB1[0]", 4, 8, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB1[1]", 4, 8, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRB1[2]", 4, 9, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB1[3]", 4, 9, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRB1[4]", 4, 10, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB1[5]", 4, 10, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRB1[6]", 4, 11, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB1[7]", 4, 11, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRB1[8]", 4, 12, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB1[9]", 4, 12, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRB1[10]", 4, 13, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB1[11]", 4, 13, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRB1[12]", 4, 14, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB1[13]", 4, 14, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRB1[14]", 4, 15, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB1[15]", 4, 15, RAM_OUTPUT, 2))
        val.append(PinConstr("ADDRB1X[0]", 3, 8, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB1X[1]", 4, 8, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB1X[2]", 3, 9, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB1X[3]", 4, 9, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB1X[4]", 3, 10, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB1X[5]", 4, 10, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB1X[6]", 3, 11, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB1X[7]", 4, 11, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB1X[8]", 3, 12, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB1X[9]", 4, 12, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB1X[10]", 3, 13, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB1X[11]", 4, 13, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB1X[12]", 4, 14, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB1X[13]", 5, 14, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB1X[14]", 4, 15, RAM_OUTPUT, 1))
        val.append(PinConstr("ADDRB1X[15]", 5, 15, RAM_OUTPUT, 1))
        val.append(PinConstr("DIB[20]", 1, 8, RAM_OUTPUT, 1))
        val.append(PinConstr("DIB[21]", 1, 8, RAM_OUTPUT, 2))
        val.append(PinConstr("DIB[22]", 1, 9, RAM_OUTPUT, 1))
        val.append(PinConstr("DIB[23]", 1, 9, RAM_OUTPUT, 2))
        val.append(PinConstr("DIB[24]", 1, 10, RAM_OUTPUT, 1))
        val.append(PinConstr("DIB[25]", 1, 10, RAM_OUTPUT, 2))
        val.append(PinConstr("DIB[26]", 1, 11, RAM_OUTPUT, 1))
        val.append(PinConstr("DIB[27]", 1, 11, RAM_OUTPUT, 2))
        val.append(PinConstr("DIB[28]", 1, 12, RAM_OUTPUT, 1))
        val.append(PinConstr("DIB[29]", 1, 12, RAM_OUTPUT, 2))
        val.append(PinConstr("DIB[30]", 1, 13, RAM_OUTPUT, 1))
        val.append(PinConstr("DIB[31]", 1, 13, RAM_OUTPUT, 2))
        val.append(PinConstr("DIB[32]", 1, 14, RAM_OUTPUT, 1))
        val.append(PinConstr("DIB[33]", 1, 14, RAM_OUTPUT, 2))
        val.append(PinConstr("DIB[34]", 1, 15, RAM_OUTPUT, 1))
        val.append(PinConstr("DIB[35]", 1, 15, RAM_OUTPUT, 2))
        val.append(PinConstr("DIB[36]", 3, 14, RAM_OUTPUT, 1))
        val.append(PinConstr("DIB[37]", 3, 14, RAM_OUTPUT, 2))
        val.append(PinConstr("DIB[38]", 3, 15, RAM_OUTPUT, 1))
        val.append(PinConstr("DIB[39]", 3, 15, RAM_OUTPUT, 2))
        val.append(PinConstr("WEB[20]", 0, 8, RAM_OUTPUT, 1))
        val.append(PinConstr("WEB[21]", 0, 8, RAM_OUTPUT, 2))
        val.append(PinConstr("WEB[22]", 0, 9, RAM_OUTPUT, 1))
        val.append(PinConstr("WEB[23]", 0, 9, RAM_OUTPUT, 2))
        val.append(PinConstr("WEB[24]", 0, 10, RAM_OUTPUT, 1))
        val.append(PinConstr("WEB[25]", 0, 10, RAM_OUTPUT, 2))
        val.append(PinConstr("WEB[26]", 0, 11, RAM_OUTPUT, 1))
        val.append(PinConstr("WEB[27]", 0, 11, RAM_OUTPUT, 2))
        val.append(PinConstr("WEB[28]", 0, 12, RAM_OUTPUT, 1))
        val.append(PinConstr("WEB[29]", 0, 12, RAM_OUTPUT, 2))
        val.append(PinConstr("WEB[30]", 0, 13, RAM_OUTPUT, 1))
        val.append(PinConstr("WEB[31]", 0, 13, RAM_OUTPUT, 2))
        val.append(PinConstr("WEB[32]", 0, 14, RAM_OUTPUT, 1))
        val.append(PinConstr("WEB[33]", 0, 14, RAM_OUTPUT, 2))
        val.append(PinConstr("WEB[34]", 0, 15, RAM_OUTPUT, 1))
        val.append(PinConstr("WEB[35]", 0, 15, RAM_OUTPUT, 2))
        val.append(PinConstr("WEB[36]", 2, 14, RAM_OUTPUT, 1))
        val.append(PinConstr("WEB[37]", 2, 14, RAM_OUTPUT, 2))
        val.append(PinConstr("WEB[38]", 2, 15, RAM_OUTPUT, 1))
        val.append(PinConstr("WEB[39]", 2, 15, RAM_OUTPUT, 2))
        val.append(PinConstr("F_RSTN", -6, 2, RAM_OUTPUT, 2))
        val.append(PinConstr("DOA[0]", -1, 0, RAM_INPUT, 1))
        val.append(PinConstr("DOAX[0]", -2, 0, RAM_INPUT, 2))
        val.append(PinConstr("DOA[1]", -1, 0, RAM_INPUT, 2))
#        val.append(PinConstr("DOAX[1]", -1, 0, RAM_INPUT, 2))
        val.append(PinConstr("DOA[2]", -1, 1, RAM_INPUT, 1))
        val.append(PinConstr("DOAX[2]", -2, 1, RAM_INPUT, 2))
        val.append(PinConstr("DOA[3]", -1, 1, RAM_INPUT, 2))
#        val.append(PinConstr("DOAX[3]", -1, 1, RAM_INPUT, 2))
        val.append(PinConstr("DOA[4]", -1, 2, RAM_INPUT, 1))
        val.append(PinConstr("DOAX[4]", -2, 2, RAM_INPUT, 2))
        val.append(PinConstr("DOA[5]", -1, 2, RAM_INPUT, 2))
#        val.append(PinConstr("DOAX[5]", -1, 2, RAM_INPUT, 2))
        val.append(PinConstr("DOA[6]", -1, 3, RAM_INPUT, 1))
        val.append(PinConstr("DOAX[6]", -2, 3, RAM_INPUT, 2))
        val.append(PinConstr("DOA[7]", -1, 3, RAM_INPUT, 2))
#        val.append(PinConstr("DOAX[7]", -1, 3, RAM_INPUT, 2))
        val.append(PinConstr("DOA[8]", -1, 4, RAM_INPUT, 1))
        val.append(PinConstr("DOAX[8]", -2, 4, RAM_INPUT, 2))
        val.append(PinConstr("DOA[9]", -1, 4, RAM_INPUT, 2))
#        val.append(PinConstr("DOAX[9]", -1, 4, RAM_INPUT, 2))
        val.append(PinConstr("DOA[10]", -1, 5, RAM_INPUT, 1))
        val.append(PinConstr("DOAX[10]", -2, 5, RAM_INPUT, 2))
        val.append(PinConstr("DOA[11]", -1, 5, RAM_INPUT, 2))
#        val.append(PinConstr("DOAX[11]", -1, 5, RAM_INPUT, 2))
        val.append(PinConstr("DOA[12]", -1, 6, RAM_INPUT, 1))
        val.append(PinConstr("DOAX[12]", -2, 6, RAM_INPUT, 2))
        val.append(PinConstr("DOA[13]", -1, 6, RAM_INPUT, 2))
#        val.append(PinConstr("DOAX[13]", -1, 6, RAM_INPUT, 2))
        val.append(PinConstr("DOA[14]", -1, 7, RAM_INPUT, 1))
        val.append(PinConstr("DOAX[14]", -2, 7, RAM_INPUT, 2))
        val.append(PinConstr("DOA[15]", -1, 7, RAM_INPUT, 2))
#        val.append(PinConstr("DOAX[15]", -1, 7, RAM_INPUT, 2))
        val.append(PinConstr("DOA[16]", -3, 6, RAM_INPUT, 1))
        val.append(PinConstr("DOAX[16]", -4, 6, RAM_INPUT, 2))
        val.append(PinConstr("DOA[17]", -3, 6, RAM_INPUT, 2))
#        val.append(PinConstr("DOAX[17]", -3, 6, RAM_INPUT, 2))
        val.append(PinConstr("DOA[18]", -3, 7, RAM_INPUT, 1))
        val.append(PinConstr("DOAX[18]", -4, 7, RAM_INPUT, 2))
        val.append(PinConstr("DOA[19]", -3, 7, RAM_INPUT, 2))
#        val.append(PinConstr("DOAX[19]", -3, 7, RAM_INPUT, 2))
        val.append(PinConstr("DOA[20]", -1, 8, RAM_INPUT, 1))
        val.append(PinConstr("DOAX[20]", -2, 8, RAM_INPUT, 2))
        val.append(PinConstr("DOA[21]", -1, 8, RAM_INPUT, 2))
#        val.append(PinConstr("DOAX[21]", -1, 8, RAM_INPUT, 2))
        val.append(PinConstr("DOA[22]", -1, 9, RAM_INPUT, 1))
        val.append(PinConstr("DOAX[22]", -2, 9, RAM_INPUT, 2))
        val.append(PinConstr("DOA[23]", -1, 9, RAM_INPUT, 2))
#        val.append(PinConstr("DOAX[23]", -1, 9, RAM_INPUT, 2))
        val.append(PinConstr("DOA[24]", -1, 10, RAM_INPUT, 1))
        val.append(PinConstr("DOAX[24]", -2, 10, RAM_INPUT, 2))
        val.append(PinConstr("DOA[25]", -1, 10, RAM_INPUT, 2))
#        val.append(PinConstr("DOAX[25]", -1, 10, RAM_INPUT, 2))
        val.append(PinConstr("DOA[26]", -1, 11, RAM_INPUT, 1))
        val.append(PinConstr("DOAX[26]", -2, 11, RAM_INPUT, 2))
        val.append(PinConstr("DOA[27]", -1, 11, RAM_INPUT, 2))
#        val.append(PinConstr("DOAX[27]", -1, 11, RAM_INPUT, 2))
        val.append(PinConstr("DOA[28]", -1, 12, RAM_INPUT, 1))
        val.append(PinConstr("DOAX[28]", -2, 12, RAM_INPUT, 2))
        val.append(PinConstr("DOA[29]", -1, 12, RAM_INPUT, 2))
#        val.append(PinConstr("DOAX[29]", -1, 12, RAM_INPUT, 2))
        val.append(PinConstr("DOA[30]", -1, 13, RAM_INPUT, 1))
        val.append(PinConstr("DOAX[30]", -2, 13, RAM_INPUT, 2))
        val.append(PinConstr("DOA[31]", -1, 13, RAM_INPUT, 2))
#        val.append(PinConstr("DOAX[31]", -1, 13, RAM_INPUT, 2))
        val.append(PinConstr("DOA[32]", -1, 14, RAM_INPUT, 1))
        val.append(PinConstr("DOAX[32]", -2, 14, RAM_INPUT, 2))
        val.append(PinConstr("DOA[33]", -1, 14, RAM_INPUT, 2))
#        val.append(PinConstr("DOAX[33]", -1, 14, RAM_INPUT, 2))
        val.append(PinConstr("DOA[34]", -1, 15, RAM_INPUT, 1))
        val.append(PinConstr("DOAX[34]", -2, 15, RAM_INPUT, 2))
        val.append(PinConstr("DOA[35]", -1, 15, RAM_INPUT, 2))
#        val.append(PinConstr("DOAX[35]", -1, 15, RAM_INPUT, 2))
        val.append(PinConstr("DOA[36]", -3, 14, RAM_INPUT, 1))
        val.append(PinConstr("DOAX[36]", -4, 14, RAM_INPUT, 2))
        val.append(PinConstr("DOA[37]", -3, 14, RAM_INPUT, 2))
#        val.append(PinConstr("DOAX[37]", -3, 14, RAM_INPUT, 2))
        val.append(PinConstr("DOA[38]", -3, 15, RAM_INPUT, 1))
        val.append(PinConstr("DOAX[38]", -4, 15, RAM_INPUT, 2))
        val.append(PinConstr("DOA[39]", -3, 15, RAM_INPUT, 2))
#        val.append(PinConstr("DOAX[39]", -3, 15, RAM_INPUT, 2))
        val.append(PinConstr("CLOCKA[1]", -3, 10, RAM_INPUT, 1))
        val.append(PinConstr("CLOCKA[2]", -3, 11, RAM_INPUT, 1))
        val.append(PinConstr("CLOCKA[3]", -3, 12, RAM_INPUT, 1))
        val.append(PinConstr("CLOCKA[4]", -3, 13, RAM_INPUT, 1))
        val.append(PinConstr("DOB[0]", 1, 0, RAM_INPUT, 1))
        val.append(PinConstr("DOBX[0]", 0, 0, RAM_INPUT, 2))
        val.append(PinConstr("DOB[1]", 1, 0, RAM_INPUT, 2))
#        val.append(PinConstr("DOBX[1]", 1, 0, RAM_INPUT, 2))
        val.append(PinConstr("DOB[2]", 1, 1, RAM_INPUT, 1))
        val.append(PinConstr("DOBX[2]", 0, 1, RAM_INPUT, 2))
        val.append(PinConstr("DOB[3]", 1, 1, RAM_INPUT, 2))
#        val.append(PinConstr("DOBX[3]", 1, 1, RAM_INPUT, 2))
        val.append(PinConstr("DOB[4]", 1, 2, RAM_INPUT, 1))
        val.append(PinConstr("DOBX[4]", 0, 2, RAM_INPUT, 2))
        val.append(PinConstr("DOB[5]", 1, 2, RAM_INPUT, 2))
#        val.append(PinConstr("DOBX[5]", 1, 2, RAM_INPUT, 2))
        val.append(PinConstr("DOB[6]", 1, 3, RAM_INPUT, 1))
        val.append(PinConstr("DOBX[6]", 0, 3, RAM_INPUT, 2))
        val.append(PinConstr("DOB[7]", 1, 3, RAM_INPUT, 2))
#        val.append(PinConstr("DOBX[7]", 1, 3, RAM_INPUT, 2))
        val.append(PinConstr("DOB[8]", 1, 4, RAM_INPUT, 1))
        val.append(PinConstr("DOBX[8]", 0, 4, RAM_INPUT, 2))
        val.append(PinConstr("DOB[9]", 1, 4, RAM_INPUT, 2))
#        val.append(PinConstr("DOBX[9]", 1, 4, RAM_INPUT, 2))
        val.append(PinConstr("DOB[10]", 1, 5, RAM_INPUT, 1))
        val.append(PinConstr("DOBX[10]", 0, 5, RAM_INPUT, 2))
        val.append(PinConstr("DOB[11]", 1, 5, RAM_INPUT, 2))
#        val.append(PinConstr("DOBX[11]", 1, 5, RAM_INPUT, 2))
        val.append(PinConstr("DOB[12]", 1, 6, RAM_INPUT, 1))
        val.append(PinConstr("DOBX[12]", 0, 6, RAM_INPUT, 2))
        val.append(PinConstr("DOB[13]", 1, 6, RAM_INPUT, 2))
#        val.append(PinConstr("DOBX[13]", 1, 6, RAM_INPUT, 2))
        val.append(PinConstr("DOB[14]", 1, 7, RAM_INPUT, 1))
        val.append(PinConstr("DOBX[14]", 0, 7, RAM_INPUT, 2))
        val.append(PinConstr("DOB[15]", 1, 7, RAM_INPUT, 2))
#        val.append(PinConstr("DOBX[15]", 1, 7, RAM_INPUT, 2))
        val.append(PinConstr("DOB[16]", 3, 6, RAM_INPUT, 1))
        val.append(PinConstr("DOBX[16]", 2, 6, RAM_INPUT, 2))
        val.append(PinConstr("DOB[17]", 3, 6, RAM_INPUT, 2))
#        val.append(PinConstr("DOBX[17]", 3, 6, RAM_INPUT, 2))
        val.append(PinConstr("DOB[18]", 3, 7, RAM_INPUT, 1))
        val.append(PinConstr("DOBX[18]", 2, 7, RAM_INPUT, 2))
        val.append(PinConstr("DOB[19]", 3, 7, RAM_INPUT, 2))
#        val.append(PinConstr("DOBX[19]", 3, 7, RAM_INPUT, 2))
        val.append(PinConstr("DOB[20]", 1, 8, RAM_INPUT, 1))
        val.append(PinConstr("DOBX[20]", 0, 8, RAM_INPUT, 2))
        val.append(PinConstr("DOB[21]", 1, 8, RAM_INPUT, 2))
#        val.append(PinConstr("DOBX[21]", 1, 8, RAM_INPUT, 2))
        val.append(PinConstr("DOB[22]", 1, 9, RAM_INPUT, 1))
        val.append(PinConstr("DOBX[22]", 0, 9, RAM_INPUT, 2))
        val.append(PinConstr("DOB[23]", 1, 9, RAM_INPUT, 2))
#        val.append(PinConstr("DOBX[23]", 1, 9, RAM_INPUT, 2))
        val.append(PinConstr("DOB[24]", 1, 10, RAM_INPUT, 1))
        val.append(PinConstr("DOBX[24]", 0, 10, RAM_INPUT, 2))
        val.append(PinConstr("DOB[25]", 1, 10, RAM_INPUT, 2))
#        val.append(PinConstr("DOBX[25]", 1, 10, RAM_INPUT, 2))
        val.append(PinConstr("DOB[26]", 1, 11, RAM_INPUT, 1))
        val.append(PinConstr("DOBX[26]", 0, 11, RAM_INPUT, 2))
        val.append(PinConstr("DOB[27]", 1, 11, RAM_INPUT, 2))
#        val.append(PinConstr("DOBX[27]", 1, 11, RAM_INPUT, 2))
        val.append(PinConstr("DOB[28]", 1, 12, RAM_INPUT, 1))
        val.append(PinConstr("DOBX[28]", 0, 12, RAM_INPUT, 2))
        val.append(PinConstr("DOB[29]", 1, 12, RAM_INPUT, 2))
#        val.append(PinConstr("DOBX[29]", 1, 12, RAM_INPUT, 2))
        val.append(PinConstr("DOB[30]", 1, 13, RAM_INPUT, 1))
        val.append(PinConstr("DOBX[30]", 0, 13, RAM_INPUT, 2))
        val.append(PinConstr("DOB[31]", 1, 13, RAM_INPUT, 2))
#        val.append(PinConstr("DOBX[31]", 1, 13, RAM_INPUT, 2))
        val.append(PinConstr("DOB[32]", 1, 14, RAM_INPUT, 1))
        val.append(PinConstr("DOBX[32]", 0, 14, RAM_INPUT, 2))
        val.append(PinConstr("DOB[33]", 1, 14, RAM_INPUT, 2))
#        val.append(PinConstr("DOBX[33]", 1, 14, RAM_INPUT, 2))
        val.append(PinConstr("DOB[34]", 1, 15, RAM_INPUT, 1))
        val.append(PinConstr("DOBX[34]", 0, 15, RAM_INPUT, 2))
        val.append(PinConstr("DOB[35]", 1, 15, RAM_INPUT, 2))
#        val.append(PinConstr("DOBX[35]", 1, 15, RAM_INPUT, 2))
        val.append(PinConstr("DOB[36]", 3, 14, RAM_INPUT, 1))
        val.append(PinConstr("DOBX[36]", 2, 14, RAM_INPUT, 2))
        val.append(PinConstr("DOB[37]", 3, 14, RAM_INPUT, 2))
#        val.append(PinConstr("DOBX[37]", 3, 14, RAM_INPUT, 2))
        val.append(PinConstr("DOB[38]", 3, 15, RAM_INPUT, 1))
        val.append(PinConstr("DOBX[38]", 2, 15, RAM_INPUT, 2))
        val.append(PinConstr("DOB[39]", 3, 15, RAM_INPUT, 2))
#        val.append(PinConstr("DOBX[39]", 3, 15, RAM_INPUT, 2))
        val.append(PinConstr("CLOCKB[1]", 2, 10, RAM_INPUT, 2))
        val.append(PinConstr("CLOCKB[2]", 2, 11, RAM_INPUT, 2))
        val.append(PinConstr("CLOCKB[3]", 2, 12, RAM_INPUT, 2))
        val.append(PinConstr("CLOCKB[4]", 2, 13, RAM_INPUT, 2))
        val.append(PinConstr("ECC1B_ERRA[0]", -4, 0, RAM_INPUT, 1))
        val.append(PinConstr("ECC1B_ERRA[1]", -4, 8, RAM_INPUT, 1))
        val.append(PinConstr("ECC1B_ERRA[2]", 5, 0, RAM_INPUT, 1))
        val.append(PinConstr("ECC1B_ERRA[3]", 5, 8, RAM_INPUT, 1))
        val.append(PinConstr("ECC1B_ERRB[0]", -4, 1, RAM_INPUT, 1))
        val.append(PinConstr("ECC1B_ERRB[1]", -4, 9, RAM_INPUT, 1))
        val.append(PinConstr("ECC1B_ERRB[2]", 5, 1, RAM_INPUT, 1))
        val.append(PinConstr("ECC1B_ERRB[3]", 5, 9, RAM_INPUT, 1))
        val.append(PinConstr("ECC2B_ERRA[0]", -4, 0, RAM_INPUT, 2))
        val.append(PinConstr("ECC2B_ERRA[1]", -4, 8, RAM_INPUT, 2))
        val.append(PinConstr("ECC2B_ERRA[2]", 5, 0, RAM_INPUT, 2))
        val.append(PinConstr("ECC2B_ERRA[3]", 5, 8, RAM_INPUT, 2))
        val.append(PinConstr("ECC2B_ERRB[0]", -4, 1, RAM_INPUT, 2))
        val.append(PinConstr("ECC2B_ERRB[1]", -4, 9, RAM_INPUT, 2))
        val.append(PinConstr("ECC2B_ERRB[2]", 5, 1, RAM_INPUT, 2))
        val.append(PinConstr("ECC2B_ERRB[3]", 5, 9, RAM_INPUT, 2))
        val.append(PinConstr("F_FULL[0]", -4, 10, RAM_INPUT, 2))
        val.append(PinConstr("F_FULL[1]", -4, 12, RAM_INPUT, 2))
        val.append(PinConstr("F_EMPTY[0]", -4, 10, RAM_INPUT, 1))
        val.append(PinConstr("F_EMPTY[1]", -4, 13, RAM_INPUT, 2))
        val.append(PinConstr("F_AL_FULL[0]", -4, 11, RAM_INPUT, 2))
        val.append(PinConstr("F_AL_FULL[1]", -4, 12, RAM_INPUT, 1))
        val.append(PinConstr("F_AL_EMPTY[0]", -4, 11, RAM_INPUT, 1))
        val.append(PinConstr("F_AL_EMPTY[1]", -4, 13, RAM_INPUT, 1))
        val.append(PinConstr("FWR_ERR[0]", -4, 4, RAM_INPUT, 1))
        val.append(PinConstr("FWR_ERR[1]", -4, 5, RAM_INPUT, 1))
        val.append(PinConstr("FRD_ERR[0]", -4, 4, RAM_INPUT, 2))
        val.append(PinConstr("FRD_ERR[1]", -4, 5, RAM_INPUT, 2))
        val.append(PinConstr("FWR_ADDR[0]", -6, 8, RAM_INPUT, 1))
        val.append(PinConstr("FWR_ADDRX[0]", -5, 8, RAM_INPUT, 1))
        val.append(PinConstr("FWR_ADDR[1]", -6, 8, RAM_INPUT, 2))
        val.append(PinConstr("FWR_ADDRX[1]", -5, 8, RAM_INPUT, 2))
        val.append(PinConstr("FWR_ADDR[2]", -6, 9, RAM_INPUT, 1))
        val.append(PinConstr("FWR_ADDRX[2]", -5, 9, RAM_INPUT, 1))
        val.append(PinConstr("FWR_ADDR[3]", -6, 9, RAM_INPUT, 2))
        val.append(PinConstr("FWR_ADDRX[3]", -5, 9, RAM_INPUT, 2))
        val.append(PinConstr("FWR_ADDR[4]", -6, 10, RAM_INPUT, 1))
        val.append(PinConstr("FWR_ADDRX[4]", -5, 10, RAM_INPUT, 1))
        val.append(PinConstr("FWR_ADDR[5]", -6, 10, RAM_INPUT, 2))
        val.append(PinConstr("FWR_ADDRX[5]", -5, 10, RAM_INPUT, 2))
        val.append(PinConstr("FWR_ADDR[6]", -6, 11, RAM_INPUT, 1))
        val.append(PinConstr("FWR_ADDRX[6]", -5, 11, RAM_INPUT, 1))
        val.append(PinConstr("FWR_ADDR[7]", -6, 11, RAM_INPUT, 2))
        val.append(PinConstr("FWR_ADDRX[7]", -5, 11, RAM_INPUT, 2))
        val.append(PinConstr("FWR_ADDR[8]", -6, 12, RAM_INPUT, 1))
        val.append(PinConstr("FWR_ADDRX[8]", -5, 12, RAM_INPUT, 1))
        val.append(PinConstr("FWR_ADDR[9]", -6, 12, RAM_INPUT, 2))
        val.append(PinConstr("FWR_ADDRX[9]", -5, 12, RAM_INPUT, 2))
        val.append(PinConstr("FWR_ADDR[10]", -6, 13, RAM_INPUT, 1))
        val.append(PinConstr("FWR_ADDRX[10]", -5, 13, RAM_INPUT, 1))
        val.append(PinConstr("FWR_ADDR[11]", -6, 13, RAM_INPUT, 2))
        val.append(PinConstr("FWR_ADDRX[11]", -5, 13, RAM_INPUT, 2))
        val.append(PinConstr("FWR_ADDR[12]", -6, 14, RAM_INPUT, 1))
        val.append(PinConstr("FWR_ADDRX[12]", -5, 14, RAM_INPUT, 1))
        val.append(PinConstr("FWR_ADDR[13]", -6, 14, RAM_INPUT, 2))
        val.append(PinConstr("FWR_ADDRX[13]", -5, 14, RAM_INPUT, 2))
        val.append(PinConstr("FWR_ADDR[14]", -6, 15, RAM_INPUT, 1))
        val.append(PinConstr("FWR_ADDRX[14]", -5, 15, RAM_INPUT, 1))
        val.append(PinConstr("FWR_ADDR[15]", -6, 15, RAM_INPUT, 2))
        val.append(PinConstr("FWR_ADDRX[15]", -5, 15, RAM_INPUT, 2))
        val.append(PinConstr("FRD_ADDR[0]", -6, 0, RAM_INPUT, 1))
        val.append(PinConstr("FRD_ADDRX[0]", -5, 0, RAM_INPUT, 1))
        val.append(PinConstr("FRD_ADDR[1]", -6, 0, RAM_INPUT, 2))
        val.append(PinConstr("FRD_ADDRX[1]", -5, 0, RAM_INPUT, 2))
        val.append(PinConstr("FRD_ADDR[2]", -6, 1, RAM_INPUT, 1))
        val.append(PinConstr("FRD_ADDRX[2]", -5, 1, RAM_INPUT, 1))
        val.append(PinConstr("FRD_ADDR[3]", -6, 1, RAM_INPUT, 2))
        val.append(PinConstr("FRD_ADDRX[3]", -5, 1, RAM_INPUT, 2))
        val.append(PinConstr("FRD_ADDR[4]", -6, 2, RAM_INPUT, 1))
        val.append(PinConstr("FRD_ADDRX[4]", -5, 2, RAM_INPUT, 1))
        val.append(PinConstr("FRD_ADDR[5]", -6, 2, RAM_INPUT, 2))
        val.append(PinConstr("FRD_ADDRX[5]", -5, 2, RAM_INPUT, 2))
        val.append(PinConstr("FRD_ADDR[6]", -6, 3, RAM_INPUT, 1))
        val.append(PinConstr("FRD_ADDRX[6]", -5, 3, RAM_INPUT, 1))
        val.append(PinConstr("FRD_ADDR[7]", -6, 3, RAM_INPUT, 2))
        val.append(PinConstr("FRD_ADDRX[7]", -5, 3, RAM_INPUT, 2))
        val.append(PinConstr("FRD_ADDR[8]", -6, 4, RAM_INPUT, 1))
        val.append(PinConstr("FRD_ADDRX[8]", -5, 4, RAM_INPUT, 1))
        val.append(PinConstr("FRD_ADDR[9]", -6, 4, RAM_INPUT, 2))
        val.append(PinConstr("FRD_ADDRX[9]", -5, 4, RAM_INPUT, 2))
        val.append(PinConstr("FRD_ADDR[10]", -6, 5, RAM_INPUT, 1))
        val.append(PinConstr("FRD_ADDRX[10]", -5, 5, RAM_INPUT, 1))
        val.append(PinConstr("FRD_ADDR[11]", -6, 5, RAM_INPUT, 2))
        val.append(PinConstr("FRD_ADDRX[11]", -5, 5, RAM_INPUT, 2))
        val.append(PinConstr("FRD_ADDR[12]", -6, 6, RAM_INPUT, 1))
        val.append(PinConstr("FRD_ADDRX[12]", -5, 6, RAM_INPUT, 1))
        val.append(PinConstr("FRD_ADDR[13]", -6, 6, RAM_INPUT, 2))
        val.append(PinConstr("FRD_ADDRX[13]", -5, 6, RAM_INPUT, 2))
        val.append(PinConstr("FRD_ADDR[14]", -6, 7, RAM_INPUT, 1))
        val.append(PinConstr("FRD_ADDRX[14]", -5, 7, RAM_INPUT, 1))
        val.append(PinConstr("FRD_ADDR[15]", -6, 7, RAM_INPUT, 2))
        val.append(PinConstr("FRD_ADDRX[15]", -5, 7, RAM_INPUT, 2))
    elif prim_type=="SERDES":
        val.append(PinConstr("TX_DETECT_RX_I", 6, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("PLL_RESET_I", 6, 5, RAM_OUTPUT, 2))
        val.append(PinConstr("REGFILE_CLK_I", 6, 5, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_CLK_I", 6, 4, RAM_OUTPUT, 2))
        val.append(PinConstr("RX_CLK_I", 6, 4, RAM_OUTPUT, 1))
        val.append(PinConstr("REGFILE_WE_I", 6, 3, RAM_OUTPUT, 2))
        val.append(PinConstr("REGFILE_EN_I", 6, 3, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_RESET_I", 6, 2, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_PCS_RESET_I", 6, 2, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_PMA_RESET_I", 6, 1, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_PRBS_FORCE_ERR_I", 6, 1, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_POLARITY_I", 6, 0, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_8B10B_EN_I", 6, 0, RAM_OUTPUT, 1))
        val.append(PinConstr("RX_RESET_I", 7, 6, RAM_OUTPUT, 2))
        val.append(PinConstr("RX_PMA_RESET_I", 7, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("RX_EQA_RESET_I", 7, 5, RAM_OUTPUT, 2))
        val.append(PinConstr("RX_CDR_RESET_I", 7, 5, RAM_OUTPUT, 1))
        val.append(PinConstr("RX_PCS_RESET_I", 7, 4, RAM_OUTPUT, 2))
        val.append(PinConstr("RX_BUF_RESET_I", 7, 4, RAM_OUTPUT, 1))
        val.append(PinConstr("RX_PRBS_CNT_RESET_I", 7, 3, RAM_OUTPUT, 2))
        val.append(PinConstr("RX_EN_EI_DETECTOR_I", 7, 3, RAM_OUTPUT, 1))
        val.append(PinConstr("RX_COMMA_DETECT_EN_I", 7, 2, RAM_OUTPUT, 2))
        val.append(PinConstr("RX_SLIDE_I", 7, 2, RAM_OUTPUT, 1))
        val.append(PinConstr("RX_POLARITY_I", 7, 1, RAM_OUTPUT, 2))
        val.append(PinConstr("RX_8B10B_EN_I", 7, 1, RAM_OUTPUT, 1))
        val.append(PinConstr("RX_MCOMMA_ALIGN_I", 7, 0, RAM_OUTPUT, 2))
        val.append(PinConstr("RX_PCOMMA_ALIGN_I", 7, 0, RAM_OUTPUT, 1))
        val.append(PinConstr("RX_NOT_IN_TABLE_O[7]", 8, 7, RAM_INPUT, 1))
        val.append(PinConstr("RX_NOT_IN_TABLE_O[6]", 8, 7, RAM_INPUT, 2))
        val.append(PinConstr("RX_NOT_IN_TABLE_O[5]", 9, 7, RAM_INPUT, 1))
        val.append(PinConstr("RX_NOT_IN_TABLE_O[4]", 9, 7, RAM_INPUT, 2))
        val.append(PinConstr("RX_NOT_IN_TABLE_O[3]", 10, 7, RAM_INPUT, 1))
        val.append(PinConstr("RX_NOT_IN_TABLE_O[2]", 10, 7, RAM_INPUT, 2))
        val.append(PinConstr("RX_NOT_IN_TABLE_O[1]", 11, 7, RAM_INPUT, 1))
        val.append(PinConstr("RX_NOT_IN_TABLE_O[0]", 11, 7, RAM_INPUT, 2))
        val.append(PinConstr("RX_CHAR_IS_COMMA_O[7]", 12, 7, RAM_INPUT, 1))
        val.append(PinConstr("RX_CHAR_IS_COMMA_O[6]", 12, 7, RAM_INPUT, 2))
        val.append(PinConstr("RX_CHAR_IS_COMMA_O[5]", 13, 7, RAM_INPUT, 1))
        val.append(PinConstr("RX_CHAR_IS_COMMA_O[4]", 13, 7, RAM_INPUT, 2))
        val.append(PinConstr("RX_CHAR_IS_COMMA_O[3]", 14, 7, RAM_INPUT, 1))
        val.append(PinConstr("RX_CHAR_IS_COMMA_O[2]", 14, 7, RAM_INPUT, 2))
        val.append(PinConstr("RX_CHAR_IS_COMMA_O[1]", 15, 7, RAM_INPUT, 1))
        val.append(PinConstr("RX_CHAR_IS_COMMA_O[0]", 15, 7, RAM_INPUT, 2))
        val.append(PinConstr("REGFILE_ADDR_I[7]", 8, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("REGFILE_ADDR_I[6]", 8, 6, RAM_OUTPUT, 2))
        val.append(PinConstr("REGFILE_ADDR_I[5]", 9, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("REGFILE_ADDR_I[4]", 9, 6, RAM_OUTPUT, 2))
        val.append(PinConstr("REGFILE_ADDR_I[3]", 10, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("REGFILE_ADDR_I[2]", 10, 6, RAM_OUTPUT, 2))
        val.append(PinConstr("REGFILE_ADDR_I[1]", 11, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("REGFILE_ADDR_I[0]", 11, 6, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_CHAR_IS_K_I[7]", 12, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_CHAR_IS_K_I[6]", 12, 6, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_CHAR_IS_K_I[5]", 13, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_CHAR_IS_K_I[4]", 13, 6, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_CHAR_IS_K_I[3]", 14, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_CHAR_IS_K_I[2]", 14, 6, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_CHAR_IS_K_I[1]", 15, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_CHAR_IS_K_I[0]", 15, 6, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_8B10B_BYPASS_I[7]", 8, 5, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_8B10B_BYPASS_I[6]", 8, 5, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_8B10B_BYPASS_I[5]", 9, 5, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_8B10B_BYPASS_I[4]", 9, 5, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_8B10B_BYPASS_I[3]", 10, 5, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_8B10B_BYPASS_I[2]", 10, 5, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_8B10B_BYPASS_I[1]", 11, 5, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_8B10B_BYPASS_I[0]", 11, 5, RAM_OUTPUT, 2))
        val.append(PinConstr("RX_8B10B_BYPASS_I[7]", 12, 5, RAM_OUTPUT, 1))
        val.append(PinConstr("RX_8B10B_BYPASS_I[6]", 12, 5, RAM_OUTPUT, 2))
        val.append(PinConstr("RX_8B10B_BYPASS_I[5]", 13, 5, RAM_OUTPUT, 1))
        val.append(PinConstr("RX_8B10B_BYPASS_I[4]", 13, 5, RAM_OUTPUT, 2))
        val.append(PinConstr("RX_8B10B_BYPASS_I[3]", 14, 5, RAM_OUTPUT, 1))
        val.append(PinConstr("RX_8B10B_BYPASS_I[2]", 14, 5, RAM_OUTPUT, 2))
        val.append(PinConstr("RX_8B10B_BYPASS_I[1]", 15, 5, RAM_OUTPUT, 1))
        val.append(PinConstr("RX_8B10B_BYPASS_I[0]", 15, 5, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_CHAR_DISPMODE_I[7]", 8, 4, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_CHAR_DISPMODE_I[6]", 8, 4, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_CHAR_DISPMODE_I[5]", 9, 4, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_CHAR_DISPMODE_I[4]", 9, 4, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_CHAR_DISPMODE_I[3]", 10, 4, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_CHAR_DISPMODE_I[2]", 10, 4, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_CHAR_DISPMODE_I[1]", 11, 4, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_CHAR_DISPMODE_I[0]", 11, 4, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_CHAR_DISPVAL_I[7]", 12, 4, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_CHAR_DISPVAL_I[6]", 12, 4, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_CHAR_DISPVAL_I[5]", 13, 4, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_CHAR_DISPVAL_I[4]", 13, 4, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_CHAR_DISPVAL_I[3]", 14, 4, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_CHAR_DISPVAL_I[2]", 14, 4, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_CHAR_DISPVAL_I[1]", 15, 4, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_CHAR_DISPVAL_I[0]", 15, 4, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[63]", 8, 3, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[62]", 8, 3, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[61]", 9, 3, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[60]", 9, 3, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[59]", 10, 3, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[58]", 10, 3, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[57]", 11, 3, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[56]", 11, 3, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[55]", 12, 3, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[54]", 12, 3, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[53]", 13, 3, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[52]", 13, 3, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[51]", 14, 3, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[50]", 14, 3, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[49]", 15, 3, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[48]", 15, 3, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[47]", 8, 2, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[46]", 8, 2, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[45]", 9, 2, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[44]", 9, 2, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[43]", 10, 2, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[42]", 10, 2, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[41]", 11, 2, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[40]", 11, 2, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[39]", 12, 2, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[38]", 12, 2, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[37]", 13, 2, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[36]", 13, 2, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[35]", 14, 2, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[34]", 14, 2, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[33]", 15, 2, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[32]", 15, 2, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[31]", 8, 1, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[30]", 8, 1, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[29]", 9, 1, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[28]", 9, 1, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[27]", 10, 1, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[26]", 10, 1, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[25]", 11, 1, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[24]", 11, 1, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[23]", 12, 1, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[22]", 12, 1, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[21]", 13, 1, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[20]", 13, 1, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[19]", 14, 1, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[18]", 14, 1, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[17]", 15, 1, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[16]", 15, 1, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[15]", 8, 0, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[14]", 8, 0, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[13]", 9, 0, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[12]", 9, 0, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[11]", 10, 0, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[10]", 10, 0, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[9]", 11, 0, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[8]", 11, 0, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[7]", 12, 0, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[6]", 12, 0, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[5]", 13, 0, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[4]", 13, 0, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[3]", 14, 0, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[2]", 14, 0, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_DATA_I[1]", 15, 0, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_DATA_I[0]", 15, 0, RAM_OUTPUT, 2))
        val.append(PinConstr("REGFILE_DO_O[15]", 16, 7, RAM_INPUT, 1))
        val.append(PinConstr("REGFILE_DO_O[14]", 16, 7, RAM_INPUT, 2))
        val.append(PinConstr("REGFILE_DO_O[13]", 17, 7, RAM_INPUT, 1))
        val.append(PinConstr("REGFILE_DO_O[12]", 17, 7, RAM_INPUT, 2))
        val.append(PinConstr("REGFILE_DO_O[11]", 18, 7, RAM_INPUT, 1))
        val.append(PinConstr("REGFILE_DO_O[10]", 18, 7, RAM_INPUT, 2))
        val.append(PinConstr("REGFILE_DO_O[9]", 19, 7, RAM_INPUT, 1))
        val.append(PinConstr("REGFILE_DO_O[8]", 19, 7, RAM_INPUT, 2))
        val.append(PinConstr("REGFILE_DO_O[7]", 20, 7, RAM_INPUT, 1))
        val.append(PinConstr("REGFILE_DO_O[6]", 20, 7, RAM_INPUT, 2))
        val.append(PinConstr("REGFILE_DO_O[5]", 21, 7, RAM_INPUT, 1))
        val.append(PinConstr("REGFILE_DO_O[4]", 21, 7, RAM_INPUT, 2))
        val.append(PinConstr("REGFILE_DO_O[3]", 22, 7, RAM_INPUT, 1))
        val.append(PinConstr("REGFILE_DO_O[2]", 22, 7, RAM_INPUT, 2))
        val.append(PinConstr("REGFILE_DO_O[1]", 23, 7, RAM_INPUT, 1))
        val.append(PinConstr("REGFILE_DO_O[0]", 23, 7, RAM_INPUT, 2))
        val.append(PinConstr("REGFILE_DI_I[15]", 16, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("REGFILE_DI_I[14]", 16, 6, RAM_OUTPUT, 2))
        val.append(PinConstr("REGFILE_DI_I[13]", 17, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("REGFILE_DI_I[12]", 17, 6, RAM_OUTPUT, 2))
        val.append(PinConstr("REGFILE_DI_I[11]", 18, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("REGFILE_DI_I[10]", 18, 6, RAM_OUTPUT, 2))
        val.append(PinConstr("REGFILE_DI_I[9]", 19, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("REGFILE_DI_I[8]", 19, 6, RAM_OUTPUT, 2))
        val.append(PinConstr("REGFILE_DI_I[7]", 20, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("REGFILE_DI_I[6]", 20, 6, RAM_OUTPUT, 2))
        val.append(PinConstr("REGFILE_DI_I[5]", 21, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("REGFILE_DI_I[4]", 21, 6, RAM_OUTPUT, 2))
        val.append(PinConstr("REGFILE_DI_I[3]", 22, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("REGFILE_DI_I[2]", 22, 6, RAM_OUTPUT, 2))
        val.append(PinConstr("REGFILE_DI_I[1]", 23, 6, RAM_OUTPUT, 1))
        val.append(PinConstr("REGFILE_DI_I[0]", 23, 6, RAM_OUTPUT, 2))
        val.append(PinConstr("REGFILE_MASK_I[15]", 16, 5, RAM_OUTPUT, 1))
        val.append(PinConstr("REGFILE_MASK_I[14]", 16, 5, RAM_OUTPUT, 2))
        val.append(PinConstr("REGFILE_MASK_I[13]", 17, 5, RAM_OUTPUT, 1))
        val.append(PinConstr("REGFILE_MASK_I[12]", 17, 5, RAM_OUTPUT, 2))
        val.append(PinConstr("REGFILE_MASK_I[11]", 18, 5, RAM_OUTPUT, 1))
        val.append(PinConstr("REGFILE_MASK_I[10]", 18, 5, RAM_OUTPUT, 2))
        val.append(PinConstr("REGFILE_MASK_I[9]", 19, 5, RAM_OUTPUT, 1))
        val.append(PinConstr("REGFILE_MASK_I[8]", 19, 5, RAM_OUTPUT, 2))
        val.append(PinConstr("REGFILE_MASK_I[7]", 20, 5, RAM_OUTPUT, 1))
        val.append(PinConstr("REGFILE_MASK_I[6]", 20, 5, RAM_OUTPUT, 2))
        val.append(PinConstr("REGFILE_MASK_I[5]", 21, 5, RAM_OUTPUT, 1))
        val.append(PinConstr("REGFILE_MASK_I[4]", 21, 5, RAM_OUTPUT, 2))
        val.append(PinConstr("REGFILE_MASK_I[3]", 22, 5, RAM_OUTPUT, 1))
        val.append(PinConstr("REGFILE_MASK_I[2]", 22, 5, RAM_OUTPUT, 2))
        val.append(PinConstr("REGFILE_MASK_I[1]", 23, 5, RAM_OUTPUT, 1))
        val.append(PinConstr("REGFILE_MASK_I[0]", 23, 5, RAM_OUTPUT, 2))
        val.append(PinConstr("RX_CHAR_IS_K_O[7]", 16, 4, RAM_INPUT, 1))
        val.append(PinConstr("RX_CHAR_IS_K_O[6]", 16, 4, RAM_INPUT, 2))
        val.append(PinConstr("RX_CHAR_IS_K_O[5]", 17, 4, RAM_INPUT, 1))
        val.append(PinConstr("RX_CHAR_IS_K_O[4]", 17, 4, RAM_INPUT, 2))
        val.append(PinConstr("RX_CHAR_IS_K_O[3]", 18, 4, RAM_INPUT, 1))
        val.append(PinConstr("RX_CHAR_IS_K_O[2]", 18, 4, RAM_INPUT, 2))
        val.append(PinConstr("RX_CHAR_IS_K_O[1]", 19, 4, RAM_INPUT, 1))
        val.append(PinConstr("RX_CHAR_IS_K_O[0]", 19, 4, RAM_INPUT, 2))
        val.append(PinConstr("RX_DISP_ERR_O[7]", 20, 4, RAM_INPUT, 1))
        val.append(PinConstr("RX_DISP_ERR_O[6]", 20, 4, RAM_INPUT, 2))
        val.append(PinConstr("RX_DISP_ERR_O[5]", 21, 4, RAM_INPUT, 1))
        val.append(PinConstr("RX_DISP_ERR_O[4]", 21, 4, RAM_INPUT, 2))
        val.append(PinConstr("RX_DISP_ERR_O[3]", 22, 4, RAM_INPUT, 1))
        val.append(PinConstr("RX_DISP_ERR_O[2]", 22, 4, RAM_INPUT, 2))
        val.append(PinConstr("RX_DISP_ERR_O[1]", 23, 4, RAM_INPUT, 1))
        val.append(PinConstr("RX_DISP_ERR_O[0]", 23, 4, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[63]", 16, 3, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[62]", 16, 3, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[61]", 17, 3, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[60]", 17, 3, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[59]", 18, 3, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[58]", 18, 3, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[57]", 19, 3, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[56]", 19, 3, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[55]", 20, 3, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[54]", 20, 3, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[53]", 21, 3, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[52]", 21, 3, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[51]", 22, 3, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[50]", 22, 3, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[49]", 23, 3, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[48]", 23, 3, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[47]", 16, 2, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[46]", 16, 2, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[45]", 17, 2, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[44]", 17, 2, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[43]", 18, 2, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[42]", 18, 2, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[41]", 19, 2, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[40]", 19, 2, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[39]", 20, 2, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[38]", 20, 2, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[37]", 21, 2, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[36]", 21, 2, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[35]", 22, 2, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[34]", 22, 2, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[33]", 23, 2, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[32]", 23, 2, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[31]", 16, 1, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[30]", 16, 1, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[29]", 17, 1, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[28]", 17, 1, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[27]", 18, 1, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[26]", 18, 1, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[25]", 19, 1, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[24]", 19, 1, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[23]", 20, 1, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[22]", 20, 1, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[21]", 21, 1, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[20]", 21, 1, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[19]", 22, 1, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[18]", 22, 1, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[17]", 23, 1, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[16]", 23, 1, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[15]", 16, 0, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[14]", 16, 0, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[13]", 17, 0, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[12]", 17, 0, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[11]", 18, 0, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[10]", 18, 0, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[9]", 19, 0, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[8]", 19, 0, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[7]", 20, 0, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[6]", 20, 0, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[5]", 21, 0, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[4]", 21, 0, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[3]", 22, 0, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[2]", 22, 0, RAM_INPUT, 2))
        val.append(PinConstr("RX_DATA_O[1]", 23, 0, RAM_INPUT, 1))
        val.append(PinConstr("RX_DATA_O[0]", 23, 0, RAM_INPUT, 2))
        val.append(PinConstr("TX_DETECT_RX_DONE_O", 24, 6, RAM_INPUT, 2))
        val.append(PinConstr("TX_DETECT_RX_PRESENT_O", 24, 6, RAM_INPUT, 1))
        val.append(PinConstr("RX_CLK_O", 24, 5, RAM_INPUT, 2))
        val.append(PinConstr("PLL_CLK_O", 24, 5, RAM_INPUT, 1))
        val.append(PinConstr("TX_BUF_ERR_O", 24, 4, RAM_INPUT, 2))
        val.append(PinConstr("TX_RESET_DONE_O", 24, 4, RAM_INPUT, 1))
        val.append(PinConstr("REGFILE_RDY_O", 24, 3, RAM_INPUT, 2))
        val.append(PinConstr("RX_PRBS_ERR_O", 24, 3, RAM_INPUT, 1))
        val.append(PinConstr("RX_BUF_ERR_O", 24, 2, RAM_INPUT, 2))
        val.append(PinConstr("RX_BYTE_IS_ALIGNED_O", 24, 2, RAM_INPUT, 1))
        val.append(PinConstr("RX_BYTE_REALIGN_O", 24, 1, RAM_INPUT, 2))
        val.append(PinConstr("RX_RESET_DONE_O", 24, 1, RAM_INPUT, 1))
        val.append(PinConstr("RX_EI_EN_O", 24, 0, RAM_INPUT, 2))
        val.append(PinConstr("LOOPBACK_I[2]", 25, 5, RAM_OUTPUT, 1))
        val.append(PinConstr("LOOPBACK_I[1]", 25, 5, RAM_OUTPUT, 2))
        val.append(PinConstr("LOOPBACK_I[0]", 25, 4, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_PRBS_SEL_I[2]", 25, 3, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_PRBS_SEL_I[1]", 25, 3, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_PRBS_SEL_I[0]", 25, 2, RAM_OUTPUT, 2))
        val.append(PinConstr("RX_PRBS_SEL_I[2]", 25, 1, RAM_OUTPUT, 1))
        val.append(PinConstr("RX_PRBS_SEL_I[1]", 25, 1, RAM_OUTPUT, 2))
        val.append(PinConstr("RX_PRBS_SEL_I[0]", 25, 0, RAM_OUTPUT, 2))
        val.append(PinConstr("TX_POWER_DOWN_N_I", 25, 4, RAM_OUTPUT, 1))
        val.append(PinConstr("RX_POWER_DOWN_N_I", 25, 2, RAM_OUTPUT, 1))
        val.append(PinConstr("TX_ELEC_IDLE_I", 25, 0, RAM_OUTPUT, 1))
    elif prim_type=="GPIO":
        if "LES" in type_name:
            val.append(PinConstr("OUT4", 3, 1, RAM_OUTPUT, 2))
            val.append(PinConstr("OUT3", 3, 1, RAM_OUTPUT, 1))
            val.append(PinConstr("OUT2", 3, 0, RAM_OUTPUT, 2))
            val.append(PinConstr("OUT1", 3, 0, RAM_OUTPUT, 1))
        if "RES" in type_name:
            val.append(PinConstr("OUT1", -3, 0, RAM_OUTPUT, 1))
            val.append(PinConstr("OUT2", -3, 0, RAM_OUTPUT, 2))
            val.append(PinConstr("OUT3", -3, 1, RAM_OUTPUT, 1))
            val.append(PinConstr("OUT4", -3, 1, RAM_OUTPUT, 2))
        if "TES" in type_name:
            val.append(PinConstr("OUT1", 0, -3, RAM_OUTPUT, 1))
            val.append(PinConstr("OUT2", 0, -3, RAM_OUTPUT, 2))
            val.append(PinConstr("OUT3", 1, -3, RAM_OUTPUT, 1))
            val.append(PinConstr("OUT4", 1, -3, RAM_OUTPUT, 2))
        if "BES" in type_name:
            val.append(PinConstr("OUT4", 1, 3, RAM_OUTPUT, 2))
            val.append(PinConstr("OUT3", 1, 3, RAM_OUTPUT, 1))
            val.append(PinConstr("OUT2", 0, 3, RAM_OUTPUT, 2))
            val.append(PinConstr("OUT1", 0, 3, RAM_OUTPUT, 1))
    elif prim_type=="PLL":
        pll_num = int(prim_name[3])
        
        val.append(PinConstr("USR_CLK_REF", -PLL_X_POS+1, -PLL_Y_POS+124 - pll_num, RAM_OUTPUT, 1))
        val.append(PinConstr("USR_LOCKED_STDY_RST", -PLL_X_POS+1, -PLL_Y_POS+120 - pll_num, RAM_OUTPUT, 1))
        val.append(PinConstr("USR_SEL_A_B", -PLL_X_POS+1, -PLL_Y_POS+116 - pll_num, RAM_OUTPUT, 1))

        val.append(PinConstr("USR_PLL_LOCKED", -PLL_X_POS+1, -PLL_Y_POS+128 - pll_num, RAM_INPUT, 2))
        val.append(PinConstr("USR_PLL_LOCKED_STDY", -PLL_X_POS+1, -PLL_Y_POS+124 - pll_num, RAM_INPUT, 2))

        val.append(PinConstr("CLK0", -PLL_X_POS+39 + pll_num * 4, -PLL_Y_POS+128, RAM_INPUT, 1))
        val.append(PinConstr("CLK90", -PLL_X_POS+40 + pll_num * 4, -PLL_Y_POS+128, RAM_INPUT, 1))
        val.append(PinConstr("CLK180", -PLL_X_POS+41 + pll_num * 4, -PLL_Y_POS+128, RAM_INPUT, 1))
        val.append(PinConstr("CLK270", -PLL_X_POS+42 + pll_num * 4, -PLL_Y_POS+128, RAM_INPUT, 1))
    elif prim_type=="GLBOUT":
        val.append(PinConstr("USR_GLB0", -PLL_X_POS+1, -PLL_Y_POS+128, RAM_OUTPUT, 1))
        val.append(PinConstr("USR_GLB1", -PLL_X_POS+1, -PLL_Y_POS+127, RAM_OUTPUT, 1))
        val.append(PinConstr("USR_GLB2", -PLL_X_POS+1, -PLL_Y_POS+126, RAM_OUTPUT, 1))
        val.append(PinConstr("USR_GLB3", -PLL_X_POS+1, -PLL_Y_POS+125, RAM_OUTPUT, 1))
        val.append(PinConstr("USR_FB0", -PLL_X_POS+1, -PLL_Y_POS+128, RAM_OUTPUT, 2))
        val.append(PinConstr("USR_FB1", -PLL_X_POS+1, -PLL_Y_POS+127, RAM_OUTPUT, 2))
        val.append(PinConstr("USR_FB2", -PLL_X_POS+1, -PLL_Y_POS+126, RAM_OUTPUT, 2))
        val.append(PinConstr("USR_FB3", -PLL_X_POS+1, -PLL_Y_POS+125, RAM_OUTPUT, 2))

    return val

def get_pin_connection_name(prim, pin):
    if prim.type == "CPE_LT_U":
        match pin.name:
            case "OUT":
                return "CPE.COMBOUT2_int"
            case "IN1":
                return "CPE.IN1_int"
            case "IN2":
                return "CPE.IN2_int"
            case "IN3":
                return "CPE.IN3_int"
            case "IN4":
                return "CPE.IN4_int"
            case _:
                return f"CPE.{pin.name}"
    elif prim.type == "CPE_FF_U":
        match pin.name:
            case "DIN":
                return "CPE.DIN2_int"
            case "DOUT":
                return "CPE.DOUT2_int"
            case _:
                return f"CPE.{pin.name}"
    elif prim.type == "CPE_RAMIO_U":
        match pin.name:
            case "OUT":
                return "CPE.OUT2"
            case "RAM_O":
                return "CPE.RAM_O2"
            case "RAM_I":
                return "CPE.RAM_I2"
            case "I":
                return "CPE.OUT2_int"
            case _:
                return f"CPE.{pin.name}"
    elif prim.type == "CPE_LT_L":
        match pin.name:
            case "OUT":
                return "CPE.COMBOUT1_int"
            case "IN1":
                return "CPE.IN5_int"
            case "IN2":
                return "CPE.IN6_int"
            case "IN3":
                return "CPE.IN7_int"
            case "IN4":
                return "CPE.IN8_int"
            case _:
                return f"CPE.{pin.name}"
    elif prim.type == "CPE_LT_FULL":
        match pin.name:
            case "OUT1":
                return "CPE.COMBOUT1_int"
            case "OUT2":
                return "CPE.COMBOUT2_int"
            case "IN1":
                return "CPE.IN1_int"
            case "IN2":
                return "CPE.IN2_int"
            case "IN3":
                return "CPE.IN3_int"
            case "IN4":
                return "CPE.IN4_int"
            case "IN5":
                return "CPE.IN5_int"
            case "IN6":
                return "CPE.IN6_int"
            case "IN7":
                return "CPE.IN7_int"
            case "IN8":
                return "CPE.IN8_int"
            case _:
                return f"CPE.{pin.name}"
    elif prim.type == "CPE_FF_L":
        match pin.name:
            case "DIN":
                return "CPE.DIN1_int"
            case "DOUT":
                return "CPE.DOUT1_int"
            case _:
                return f"CPE.{pin.name}"
    elif prim.type == "CPE_RAMIO_L":
        match pin.name:
            case "OUT":
                return "CPE.OUT1"
            case "RAM_O":
                return "CPE.RAM_O1"
            case "RAM_I":
                return "CPE.RAM_I1"
            case "I":
                return "CPE.OUT1_int"
            case _:
                return f"CPE.{pin.name}"
    elif prim.type == "CPE_LINES":
        match pin.name:
            case _:
                return f"CPE.{pin.name}"
    return f"{prim.name}.{pin.name}"

def get_endpoints_for_type(type):
    wires = []
    def create_wire(name, type):
        wires.append(Endpoint(name,type))

    for prim in get_primitives_for_type(type):
        for pin in get_primitive_pins(prim.type):
            if not pin.use_alias_conn:
                create_wire(f"{prim.name}.{pin.name}", type=f"{pin.wire_type}")

    if "CPE" in type:
        create_wire("CPE.RAM_I1" , type="CPE_WIRE_L")
        create_wire("CPE.RAM_I2" , type="CPE_WIRE_L")
        create_wire("CPE.IN1"    , type="CPE_WIRE_L")
        create_wire("CPE.IN2"    , type="CPE_WIRE_L")
        create_wire("CPE.IN3"    , type="CPE_WIRE_L")
        create_wire("CPE.IN4"    , type="CPE_WIRE_L")
        create_wire("CPE.IN5"    , type="CPE_WIRE_L")
        create_wire("CPE.IN6"    , type="CPE_WIRE_L")
        create_wire("CPE.IN7"    , type="CPE_WIRE_L")
        create_wire("CPE.IN8"    , type="CPE_WIRE_L")
        create_wire("CPE.IN1_int", type="CPE_WIRE_INT")
        create_wire("CPE.IN2_int", type="CPE_WIRE_INT")
        create_wire("CPE.IN3_int", type="CPE_WIRE_INT")
        create_wire("CPE.IN4_int", type="CPE_WIRE_INT")
        create_wire("CPE.IN5_int", type="CPE_WIRE_INT")
        create_wire("CPE.IN6_int", type="CPE_WIRE_INT")
        create_wire("CPE.IN7_int", type="CPE_WIRE_INT")
        create_wire("CPE.IN8_int", type="CPE_WIRE_INT")
        create_wire("CPE.OUT1_int", type="CPE_WIRE_INT")
        create_wire("CPE.OUT2_int", type="CPE_WIRE_INT")
        create_wire("CPE.COMBOUT1_int", type="CPE_WIRE_INT")
        create_wire("CPE.COMBOUT2_int", type="CPE_WIRE_INT")
        create_wire("CPE.DIN1_int", type="CPE_WIRE_INT")
        create_wire("CPE.DIN2_int", type="CPE_WIRE_INT")
        create_wire("CPE.DOUT1_int", type="CPE_WIRE_INT")
        create_wire("CPE.DOUT2_int", type="CPE_WIRE_INT")
        create_wire("CPE.CLK"    , type="CPE_WIRE_L")
        create_wire("CPE.EN"     , type="CPE_WIRE_L")
        create_wire("CPE.SR"     , type="CPE_WIRE_L")
        create_wire("CPE.OUT1"   , type="CPE_WIRE_B")
        create_wire("CPE.OUT2"   , type="CPE_WIRE_B")
        create_wire("CPE.RAM_O1" , type="CPE_WIRE_B")
        create_wire("CPE.RAM_O2" , type="CPE_WIRE_B")
        create_wire("CPE.CINX"   , type="CPE_WIRE_L")
        create_wire("CPE.PINX"   , type="CPE_WIRE_L")
        create_wire("CPE.CINY1"  , type="CPE_WIRE_B")
        create_wire("CPE.PINY1"  , type="CPE_WIRE_B")
        create_wire("CPE.CINY2"  , type="CPE_WIRE_B")
        create_wire("CPE.PINY2"  , type="CPE_WIRE_B")
        create_wire("CPE.COUTX"  , type="CPE_WIRE_B")
        create_wire("CPE.POUTX"  , type="CPE_WIRE_B")
        create_wire("CPE.COUTY1" , type="CPE_WIRE_T")
        create_wire("CPE.POUTY1" , type="CPE_WIRE_T")
        create_wire("CPE.COUTY2" , type="CPE_WIRE_T")
        create_wire("CPE.POUTY2" , type="CPE_WIRE_T")
        for p in range(1,13):
            plane = f"{p:02d}"
            for i in range(8):
                create_wire(f"IM.P{plane}.D{i}", type="IM_WIRE")
            create_wire(f"IM.P{plane}.Y", type="IM_WIRE")
            if "OM" in type and p>=9:
                for i in range(4):
                    create_wire(f"OM.P{plane}.D{i}", type="OM_WIRE")
                create_wire(f"OM.P{plane}.Y", type="OM_WIRE")

    if "SB_BIG" in type:
        for p in range(1,13):
            plane = f"{p:02d}"
            create_wire(f"SB_BIG.P{plane}.D0", type="SB_BIG_WIRE")
            for i in range(1,5):
                create_wire(f"SB_BIG.P{plane}.D2_{i}", type="SB_BIG_WIRE")
                create_wire(f"SB_BIG.P{plane}.D3_{i}", type="SB_BIG_WIRE")
                create_wire(f"SB_BIG.P{plane}.D4_{i}", type="SB_BIG_WIRE")
                create_wire(f"SB_BIG.P{plane}.D5_{i}", type="SB_BIG_WIRE")
                create_wire(f"SB_BIG.P{plane}.D6_{i}", type="SB_BIG_WIRE")
                create_wire(f"SB_BIG.P{plane}.D7_{i}", type="SB_BIG_WIRE")
                create_wire(f"SB_BIG.P{plane}.Y{i}", type="SB_BIG_WIRE")

            create_wire(f"SB_BIG.P{plane}.YDIAG", type="SB_BIG_WIRE")
            create_wire(f"SB_BIG.P{plane}.X34", type="SB_BIG_WIRE")
            create_wire(f"SB_BIG.P{plane}.X14", type="SB_BIG_WIRE")
            create_wire(f"SB_BIG.P{plane}.X12", type="SB_BIG_WIRE")
            create_wire(f"SB_BIG.P{plane}.X23", type="SB_BIG_WIRE")

            for i in range(1,5):
                create_wire(f"SB_DRIVE.P{plane}.D{i}.IN", type="SB_DRIVE_WIRE")
                create_wire(f"SB_DRIVE.P{plane}.D{i}.OUT", type="SB_DRIVE_WIRE")
                create_wire(f"SB_DRIVE.P{plane}.D{i}.OUT_NOINV", type="SB_DRIVE_INT_WIRE")

    if "SB_SML" in type:
        for p in range(1,13):
            plane = f"{p:02d}"
            create_wire(f"SB_SML.P{plane}.D0", type="SB_SML_WIRE")
            for i in range(1,5):
                create_wire(f"SB_SML.P{plane}.D2_{i}", type="SB_SML_WIRE")
                create_wire(f"SB_SML.P{plane}.D3_{i}", type="SB_SML_WIRE")
                create_wire(f"SB_SML.P{plane}.Y{i}", type="SB_SML_WIRE")
                create_wire(f"SB_SML.P{plane}.Y{i}_int", type="SB_SML_WIRE")

            create_wire(f"SB_SML.P{plane}.YDIAG", type="SB_SML_WIRE")
            create_wire(f"SB_SML.P{plane}.YDIAG_int", type="SB_SML_WIRE")
            create_wire(f"SB_SML.P{plane}.X34", type="SB_SML_WIRE")
            create_wire(f"SB_SML.P{plane}.X14", type="SB_SML_WIRE")
            create_wire(f"SB_SML.P{plane}.X12", type="SB_SML_WIRE")
            create_wire(f"SB_SML.P{plane}.X23", type="SB_SML_WIRE")

    if "IOES" in type:
        create_wire("IOES.IO_IN1", type="IOES_WIRE")
        create_wire("IOES.IO_IN2", type="IOES_WIRE")
        for p in range(1,13):
            plane = f"{p:02d}"
            create_wire(f"IOES.SB_IN_{plane}", type="IOES_WIRE")
            create_wire(f"IOES.ALTIN_{plane}", type="IOES_WIRE")

    if "LES" in type:
        for p in range(1,9):
            create_wire(f"LES.SB_Y3.P{p}", type="LES_WIRE")
            create_wire(f"LES.MDIE1.P{p}", type="LES_WIRE")
        for i in range(4):
            create_wire(f"LES.CLOCK{i}", type="LES_WIRE")
        create_wire("LES.CPE_CINX", type="LES_WIRE")
        create_wire("LES.CPE_PINX", type="LES_WIRE")
        # Internal wires
        create_wire("LES.SB_Y3_SEL1_int", type="LES_INT_WIRE")
        create_wire("LES.MDIE1_SEL1_int", type="LES_INT_WIRE")
        create_wire("LES.CLOCK_SEL1_int", type="LES_INT_WIRE")
        create_wire("LES.SB_Y3_SEL2_int", type="LES_INT_WIRE")
        create_wire("LES.MDIE1_SEL2_int", type="LES_INT_WIRE")
        create_wire("LES.CLOCK_SEL2_int", type="LES_INT_WIRE")

    if "BES" in type:
        for p in range(1,9):
            create_wire(f"BES.SB_Y4.P{p}", type="BES_WIRE")
            create_wire(f"BES.MDIE2.P{p}", type="BES_WIRE")
        for i in range(4):
            create_wire(f"BES.CLOCK{i}", type="BES_WIRE")
        create_wire("BES.P_CINY1", type="BES_WIRE")
        create_wire("BES.P_PINY1", type="BES_WIRE")
        create_wire("BES.P_CINY2", type="BES_WIRE")
        create_wire("BES.P_PINY2", type="BES_WIRE")
        create_wire("BES.CPE_CINY1", type="BES_WIRE")
        create_wire("BES.CPE_PINY1", type="BES_WIRE")
        create_wire("BES.CPE_CINY2", type="BES_WIRE")
        create_wire("BES.CPE_PINY2", type="BES_WIRE")
        # Internal wires
        create_wire("BES.SB_Y4_SEL1_int", type="BES_INT_WIRE")
        create_wire("BES.MDIE2_SEL1_int", type="BES_INT_WIRE")
        create_wire("BES.CLOCK_SEL1_int", type="BES_INT_WIRE")
        create_wire("BES.SB_Y4_SEL2_int", type="BES_INT_WIRE")
        create_wire("BES.MDIE2_SEL2_int", type="BES_INT_WIRE")
        create_wire("BES.CLOCK_SEL2_int", type="BES_INT_WIRE")
        create_wire("BES.SB_Y4_SEL3_int", type="BES_INT_WIRE")
        create_wire("BES.MDIE2_SEL3_int", type="BES_INT_WIRE")
        create_wire("BES.CLOCK_SEL3_int", type="BES_INT_WIRE")
        create_wire("BES.SB_Y4_SEL4_int", type="BES_INT_WIRE")
        create_wire("BES.MDIE2_SEL4_int", type="BES_INT_WIRE")
        create_wire("BES.CLOCK_SEL4_int", type="BES_INT_WIRE")
        create_wire("BES.CPE_CINY1_int", type="BES_INT_WIRE")
        create_wire("BES.CPE_PINY1_int", type="BES_INT_WIRE")
        create_wire("BES.CPE_CINY2_int", type="BES_INT_WIRE")
        create_wire("BES.CPE_PINY2_int", type="BES_INT_WIRE")

    if "RES" in type:
        create_wire("RES.CPE_RAM_O1", type="RES_WIRE")
        create_wire("RES.CPE_RAM_O2", type="RES_WIRE")
        create_wire("RES.CPE_COUTX", type="RES_WIRE")
        create_wire("RES.CPE_POUTX", type="RES_WIRE")
        for p in range(1,9):
            create_wire(f"RES.SB_Y1.P{p}", type="RES_WIRE")
            create_wire(f"RES.MDIE1.P{p}", type="RES_WIRE")
        for i in range(4):
            create_wire(f"RES.CLOCK{i}", type="RES_WIRE")
        # Internal wires
        create_wire("RES.SIG_SEL1_int", type="RES_INT_WIRE")
        create_wire("RES.SIG_SEL2_int", type="RES_INT_WIRE")
        create_wire("RES.SIG_SEL3_int", type="RES_INT_WIRE")
        create_wire("RES.SIG_SEL4_int", type="RES_INT_WIRE")

    if "TES" in type:
        create_wire("TES.CPE_RAM_O1", type="TES_WIRE")
        create_wire("TES.CPE_RAM_O2", type="TES_WIRE")
        create_wire("TES.CPE_COUTY1", type="TES_WIRE")
        create_wire("TES.CPE_POUTY1", type="TES_WIRE")
        create_wire("TES.CPE_COUTY2", type="TES_WIRE")
        create_wire("TES.CPE_POUTY2", type="TES_WIRE")
        for p in range(1,9):
            create_wire(f"TES.SB_Y2.P{p}", type="TES_WIRE")
            create_wire(f"TES.MDIE2.P{p}", type="TES_WIRE")
        for i in range(4):
            create_wire(f"TES.CLOCK{i}", type="TES_WIRE")
        # Internal wires
        create_wire("TES.SIG_SEL1_int", type="TES_INT_WIRE")
        create_wire("TES.SIG_SEL2_int", type="TES_INT_WIRE")
        create_wire("TES.SIG_SEL3_int", type="TES_INT_WIRE")
        create_wire("TES.SIG_SEL4_int", type="TES_INT_WIRE")

    return wires

def get_mux_connections_for_type(type):
    muxes = []
    def create_mux(src, dst, bits, value, invert, name = None, visible = True, config = False, delay = ""):
        name = dst if name is None else name
        muxes.append(MUX(src, dst, name, bits, value, invert, visible, config, delay))

    if "CPE" in type:
        # CPE
        for i in range(1,9):
            create_mux(f"CPE.IN{i}", f"CPE.IN{i}_int", 0, 0, False, None, False)
        create_mux("CPE.PINY1", "CPE.IN2_int", 1, 1, False, "CPE.C_I1")
        create_mux("CPE.CINX",  "CPE.IN4_int", 1, 1, False, "CPE.C_I2")
        create_mux("CPE.PINY1", "CPE.IN6_int", 1, 1, False, "CPE.C_I3")
        create_mux("CPE.PINX",  "CPE.IN8_int", 1, 1, False, "CPE.C_I4")
        for p in range(1,13):
            plane = f"{p:02d}"
            for i in range(8):
                create_mux(f"IM.P{plane}.D{i}", f"IM.P{plane}.Y", 3, i, True, f"IM.P{plane}")
            if "OM" in type and p>=9:
                for i in range(4):
                    create_mux(f"OM.P{plane}.D{i}", f"OM.P{plane}.Y", 2, i, True, f"OM.P{plane}")
        create_mux("CPE.DOUT1_int",    "CPE.OUT1_int", 2, 0, False, "CPE.C_O1")
        create_mux("CPE.COMBOUT1_int", "CPE.OUT1_int", 2, 3, False, "CPE.C_O1")
        create_mux("CPE.COMBOUT1_int", "CPE.DIN1_int",1, 0, False, visible=False)

        create_mux("CPE.DOUT2_int",    "CPE.OUT2_int", 2, 0, False, "CPE.C_O2")
        create_mux("CPE.COMBOUT2_int", "CPE.OUT2_int", 2, 3, False, "CPE.C_O2")
        create_mux("CPE.COMBOUT2_int", "CPE.DIN2_int",1, 1, False, "CPE.C_2D_IN")

        # Virtual connections
        create_mux("CPE.OUT1_int",    "CPE.OUT1", 1, 0, False, visible=False)
        create_mux("CPE.OUT2_int",    "CPE.OUT2", 1, 0, False, visible=False)

    if "SB_BIG" in type:
        # SB_BIG
        for p in range(1,13):
            delay = f"sb_del_t1_x1_y1"
            plane = f"{p:02d}"
            # Per Y output mux
            for i in range(1,5):
                create_mux(f"SB_BIG.P{plane}.D0",     f"SB_BIG.P{plane}.Y{i}", 3, 0, True, delay="del_dummy")
                create_mux(f"SB_BIG.P{plane}.YDIAG",  f"SB_BIG.P{plane}.Y{i}", 3, 1, True, delay=f"{delay}_p{p}_d1_s1")
                create_mux(f"SB_BIG.P{plane}.D2_{i}", f"SB_BIG.P{plane}.Y{i}", 3, 2, True, delay="del_dummy")
                create_mux(f"SB_BIG.P{plane}.D3_{i}", f"SB_BIG.P{plane}.Y{i}", 3, 3, True, delay="del_dummy")
                create_mux(f"SB_BIG.P{plane}.D4_{i}", f"SB_BIG.P{plane}.Y{i}", 3, 4, True, delay="del_dummy")
                create_mux(f"SB_BIG.P{plane}.D5_{i}", f"SB_BIG.P{plane}.Y{i}", 3, 5, True, delay="del_dummy")
                create_mux(f"SB_BIG.P{plane}.D6_{i}", f"SB_BIG.P{plane}.Y{i}", 3, 6, True, delay="del_dummy")
                create_mux(f"SB_BIG.P{plane}.D7_{i}", f"SB_BIG.P{plane}.Y{i}", 3, 7, True, delay="del_dummy")

            # YDIAG output mux
            create_mux(f"SB_BIG.P{plane}.Y1",  f"SB_BIG.P{plane}.YDIAG", 3, 0, True, delay=f"{delay}_p{p}_d0_s0")
            create_mux(f"SB_BIG.P{plane}.Y2",  f"SB_BIG.P{plane}.YDIAG", 3, 1, True, delay=f"{delay}_p{p}_d0_s1")
            create_mux(f"SB_BIG.P{plane}.Y3",  f"SB_BIG.P{plane}.YDIAG", 3, 2, True, delay=f"{delay}_p{p}_d0_s2")
            create_mux(f"SB_BIG.P{plane}.Y4",  f"SB_BIG.P{plane}.YDIAG", 3, 3, True, delay=f"{delay}_p{p}_d0_s3")
            create_mux(f"SB_BIG.P{plane}.X34", f"SB_BIG.P{plane}.YDIAG", 3, 4, True, delay="del_dummy")
            create_mux(f"SB_BIG.P{plane}.X14", f"SB_BIG.P{plane}.YDIAG", 3, 5, True, delay="del_dummy")
            create_mux(f"SB_BIG.P{plane}.X12", f"SB_BIG.P{plane}.YDIAG", 3, 6, True, delay="del_dummy")
            create_mux(f"SB_BIG.P{plane}.X23", f"SB_BIG.P{plane}.YDIAG", 3, 7, True, delay="del_dummy")

            for i in range(1,5):
                create_mux(f"SB_DRIVE.P{plane}.D{i}.IN", f"SB_DRIVE.P{plane}.D{i}.OUT", 1, 1, True, f"SB_DRIVE.P{plane}.D{i}", delay="del_sb_drv")
                create_mux(f"SB_DRIVE.P{plane}.D{i}.IN", f"SB_DRIVE.P{plane}.D{i}.OUT_NOINV", 1, 1, False, f"SB_DRIVE.P{plane}.D{i}", delay="del_sb_drv")

    if "SB_SML" in type:
        # SB_SML
        for p in range(1,13):
            delay = f"sb_del_t1_x1_y1"
            plane = f"{p:02d}"
            # Per Y output mux
            for i in range(1,5):
                create_mux(f"SB_SML.P{plane}.D0",       f"SB_SML.P{plane}.Y{i}_int", 2, 0, False, f"SB_SML.P{plane}.Y{i}", delay="del_dummy")
                create_mux(f"SB_SML.P{plane}.YDIAG_int",f"SB_SML.P{plane}.Y{i}_int", 2, 1, False, f"SB_SML.P{plane}.Y{i}", delay=f"{delay}_p{p}_d1_s1")
                create_mux(f"SB_SML.P{plane}.D2_{i}",   f"SB_SML.P{plane}.Y{i}_int", 2, 2, False, f"SB_SML.P{plane}.Y{i}", delay="del_dummy")
                create_mux(f"SB_SML.P{plane}.D3_{i}",   f"SB_SML.P{plane}.Y{i}_int", 2, 3, False, f"SB_SML.P{plane}.Y{i}", delay="del_dummy")

            # YDIAG output mux
            create_mux(f"SB_SML.P{plane}.Y1_int", f"SB_SML.P{plane}.YDIAG_int", 3, 0, False, f"SB_SML.P{plane}.YDIAG", delay=f"{delay}_p{p}_d0_s0")
            create_mux(f"SB_SML.P{plane}.Y2_int", f"SB_SML.P{plane}.YDIAG_int", 3, 1, False, f"SB_SML.P{plane}.YDIAG", delay=f"{delay}_p{p}_d0_s1")
            create_mux(f"SB_SML.P{plane}.Y3_int", f"SB_SML.P{plane}.YDIAG_int", 3, 2, False, f"SB_SML.P{plane}.YDIAG", delay=f"{delay}_p{p}_d0_s2")
            create_mux(f"SB_SML.P{plane}.Y4_int", f"SB_SML.P{plane}.YDIAG_int", 3, 3, False, f"SB_SML.P{plane}.YDIAG", delay=f"{delay}_p{p}_d0_s3")
            create_mux(f"SB_SML.P{plane}.X34",    f"SB_SML.P{plane}.YDIAG_int", 3, 4, False, f"SB_SML.P{plane}.YDIAG", delay="del_dummy")
            create_mux(f"SB_SML.P{plane}.X14",    f"SB_SML.P{plane}.YDIAG_int", 3, 5, False, f"SB_SML.P{plane}.YDIAG", delay="del_dummy")
            create_mux(f"SB_SML.P{plane}.X12",    f"SB_SML.P{plane}.YDIAG_int", 3, 6, False, f"SB_SML.P{plane}.YDIAG", delay="del_dummy")
            create_mux(f"SB_SML.P{plane}.X23",    f"SB_SML.P{plane}.YDIAG_int", 3, 7, False, f"SB_SML.P{plane}.YDIAG", delay="del_dummy")

            create_mux(f"SB_SML.P{plane}.Y1_int",    f"SB_SML.P{plane}.Y1",    1, 1, True, f"SB_SML.P{plane}.Y1_INT", False, delay="del_dummy")
            create_mux(f"SB_SML.P{plane}.Y2_int",    f"SB_SML.P{plane}.Y2",    1, 1, True, f"SB_SML.P{plane}.Y2_INT", False, delay="del_dummy")
            create_mux(f"SB_SML.P{plane}.Y3_int",    f"SB_SML.P{plane}.Y3",    1, 1, True, f"SB_SML.P{plane}.Y3_INT", False, delay="del_dummy")
            create_mux(f"SB_SML.P{plane}.Y4_int",    f"SB_SML.P{plane}.Y4",    1, 1, True, f"SB_SML.P{plane}.Y4_INT", False, delay="del_dummy")
            create_mux(f"SB_SML.P{plane}.YDIAG_int", f"SB_SML.P{plane}.YDIAG", 1, 1, True, f"SB_SML.P{plane}.YDIAG_INT", False, delay="del_dummy")

    #if "GPIO" in type:
    #    # GPIO
    if "IOES" in type:
        # IOES
        for p in range(1,13):
            plane = f"{p:02d}"
            io_in = 1 if p % 2 else 2
            create_mux(f"IOES.IO_IN{io_in}", f"IOES.SB_IN_{plane}", 1, 0, False)
            create_mux(f"IOES.ALTIN_{plane}", f"IOES.SB_IN_{plane}", 1, 1, False)

    if "LES" in type:
        for p in range(1,9):
            create_mux(f"LES.SB_Y3.P{p}", "LES.SB_Y3_SEL1_int", 3, p-1, False, "LES.SB_Y3_SEL1", delay="del_dummy")
            create_mux(f"LES.MDIE1.P{p}", "LES.MDIE1_SEL1_int", 3, p-1, False, "LES.MDIE1_SEL1", delay="del_dummy")
            create_mux(f"LES.SB_Y3.P{p}", "LES.SB_Y3_SEL2_int", 3, p-1, False, "LES.SB_Y3_SEL2", delay="del_dummy")
            create_mux(f"LES.MDIE1.P{p}", "LES.MDIE1_SEL2_int", 3, p-1, False, "LES.MDIE1_SEL2", delay="del_dummy")
        for i in range(4):
            create_mux(f"LES.CLOCK{i}", "LES.CLOCK_SEL1_int", 2, i, False, "LES.CLOCK_SEL1", delay="del_dummy")
            create_mux(f"LES.CLOCK{i}", "LES.CLOCK_SEL2_int", 2, i, False, "LES.CLOCK_SEL2", delay="del_dummy")

        create_mux("LES.SB_Y3_SEL1_int", "LES.CPE_CINX", 2, 1, False, "LES.CINX_SEL", delay="del_left_SB_couty2")
        create_mux("LES.MDIE1_SEL1_int", "LES.CPE_CINX", 2, 2, False, "LES.CINX_SEL", delay="del_left_couty2")
        create_mux("LES.CLOCK_SEL1_int", "LES.CPE_CINX", 2, 3, False, "LES.CINX_SEL", delay="del_left_glb_couty2")

        create_mux("LES.SB_Y3_SEL2_int", "LES.CPE_PINX", 2, 1, False, "LES.PINX_SEL", delay="del_left_SB_pouty2")
        create_mux("LES.MDIE1_SEL2_int", "LES.CPE_PINX", 2, 2, False, "LES.PINX_SEL", delay="del_left_pouty2")
        create_mux("LES.CLOCK_SEL2_int", "LES.CPE_PINX", 2, 3, False, "LES.PINX_SEL", delay="del_left_glb_pouty2")

    if "BES" in type:
        for p in range(1,9):
            create_mux(f"BES.SB_Y4.P{p}", "BES.SB_Y4_SEL1_int", 3, p-1, False, "BES.SB_Y4_SEL1", delay="del_dummy")
            create_mux(f"BES.MDIE2.P{p}", "BES.MDIE2_SEL1_int", 3, p-1, False, "BES.MDIE2_SEL1", delay="del_dummy")
            create_mux(f"BES.SB_Y4.P{p}", "BES.SB_Y4_SEL2_int", 3, p-1, False, "BES.SB_Y4_SEL2", delay="del_dummy")
            create_mux(f"BES.MDIE2.P{p}", "BES.MDIE2_SEL2_int", 3, p-1, False, "BES.MDIE2_SEL2", delay="del_dummy")
            create_mux(f"BES.SB_Y4.P{p}", "BES.SB_Y4_SEL3_int", 3, p-1, False, "BES.SB_Y4_SEL3", delay="del_dummy")
            create_mux(f"BES.MDIE2.P{p}", "BES.MDIE2_SEL3_int", 3, p-1, False, "BES.MDIE2_SEL3", delay="del_dummy")
            create_mux(f"BES.SB_Y4.P{p}", "BES.SB_Y4_SEL4_int", 3, p-1, False, "BES.SB_Y4_SEL4", delay="del_dummy")
            create_mux(f"BES.MDIE2.P{p}", "BES.MDIE2_SEL4_int", 3, p-1, False, "BES.MDIE2_SEL4", delay="del_dummy")
        for i in range(4):
            create_mux(f"BES.CLOCK{i}", "BES.CLOCK_SEL1_int", 2, i, False, "BES.CLOCK_SEL1", delay="del_dummy")
            create_mux(f"BES.CLOCK{i}", "BES.CLOCK_SEL2_int", 2, i, False, "BES.CLOCK_SEL2", delay="del_dummy")
            create_mux(f"BES.CLOCK{i}", "BES.CLOCK_SEL3_int", 2, i, False, "BES.CLOCK_SEL3", delay="del_dummy")
            create_mux(f"BES.CLOCK{i}", "BES.CLOCK_SEL4_int", 2, i, False, "BES.CLOCK_SEL4", delay="del_dummy")

        create_mux("BES.SB_Y4_SEL1_int", "BES.CPE_CINY1_int", 2, 1, False, "BES.CINY1_SEL", delay="del_bot_SB_couty2")
        create_mux("BES.MDIE2_SEL1_int", "BES.CPE_CINY1_int", 2, 2, False, "BES.CINY1_SEL", delay="del_bot_couty2")
        create_mux("BES.CLOCK_SEL1_int", "BES.CPE_CINY1_int", 2, 3, False, "BES.CINY1_SEL", delay="del_bot_glb_couty2")
        create_mux("BES.SB_Y4_SEL2_int", "BES.CPE_PINY1_int", 2, 1, False, "BES.PINY1_SEL", delay="del_bot_SB_pouty2")
        create_mux("BES.MDIE2_SEL2_int", "BES.CPE_PINY1_int", 2, 2, False, "BES.PINY1_SEL", delay="del_bot_pouty2")
        create_mux("BES.CLOCK_SEL2_int", "BES.CPE_PINY1_int", 2, 3, False, "BES.PINY1_SEL", delay="del_bot_glb_pouty2")
        create_mux("BES.SB_Y4_SEL3_int", "BES.CPE_CINY2_int", 2, 1, False, "BES.CINY2_SEL", delay="del_bot_SB_couty2")
        create_mux("BES.MDIE2_SEL3_int", "BES.CPE_CINY2_int", 2, 2, False, "BES.CINY2_SEL", delay="del_bot_couty2")
        create_mux("BES.CLOCK_SEL3_int", "BES.CPE_CINY2_int", 2, 3, False, "BES.CINY2_SEL", delay="del_bot_glb_couty2")
        create_mux("BES.SB_Y4_SEL4_int", "BES.CPE_PINY2_int", 2, 1, False, "BES.PINY2_SEL", delay="del_bot_SB_pouty2")
        create_mux("BES.MDIE2_SEL4_int", "BES.CPE_PINY2_int", 2, 2, False, "BES.PINY2_SEL", delay="del_bot_pouty2")
        create_mux("BES.CLOCK_SEL4_int", "BES.CPE_PINY2_int", 2, 3, False, "BES.PINY2_SEL", delay="del_bot_glb_pouty2")

        create_mux("BES.CPE_CINY1_int", "BES.CPE_CINY1",      1, 0, False, "BES.P_CINY1", delay="del_dummy")
        create_mux("BES.P_CINY1",       "BES.CPE_CINY1",      1, 1, False, "BES.P_CINY1", delay="del_dummy")
        create_mux("BES.CPE_PINY1_int", "BES.CPE_PINY1",      1, 0, False, "BES.P_PINY1", delay="del_dummy")
        create_mux("BES.P_PINY1",       "BES.CPE_PINY1",      1, 1, False, "BES.P_PINY1", delay="del_dummy")
        create_mux("BES.CPE_CINY2_int", "BES.CPE_CINY2",      1, 0, False, "BES.P_CINY2", delay="del_dummy")
        create_mux("BES.P_CINY2",       "BES.CPE_CINY2",      1, 1, False, "BES.P_CINY2", delay="del_dummy")
        create_mux("BES.CPE_PINY2_int", "BES.CPE_PINY2",      1, 0, False, "BES.P_PINY2", delay="del_dummy")
        create_mux("BES.P_PINY2",       "BES.CPE_PINY2",      1, 1, False, "BES.P_PINY2", delay="del_dummy")

    if "RES" in type:
        for sel in range(4):
            create_mux("RES.CPE_RAM_O1", f"RES.SIG_SEL{sel+1}_int", 3, 0, False, f"RES.SIG_SEL{sel+1}", delay="del_dummy")
            create_mux("RES.CPE_RAM_O2", f"RES.SIG_SEL{sel+1}_int", 3, 1, False, f"RES.SIG_SEL{sel+1}", delay="del_dummy")
            create_mux("RES.CPE_COUTX",  f"RES.SIG_SEL{sel+1}_int", 3, 2, False, f"RES.SIG_SEL{sel+1}", delay="del_dummy")
            create_mux("RES.CPE_POUTX",  f"RES.SIG_SEL{sel+1}_int", 3, 3, False, f"RES.SIG_SEL{sel+1}", delay="del_dummy")
            for i in range(4):
                create_mux(f"RES.CLOCK{i}", f"RES.SIG_SEL{sel+1}_int", 3, 4 + i, False, f"RES.SIG_SEL{sel+1}", delay="del_dummy")

        for p in range(1,9):
            create_mux(f"RES.SB_Y1.P{p}", f"RES.MDIE1.P{p}", 1, 0, False, f"RES.SEL_MDIE{p}", delay="del_dummy")
            sel = (p - 1) // 2 + 1
            create_mux(f"RES.SIG_SEL{sel}_int", f"RES.MDIE1.P{p}", 1, 1, False, f"RES.SEL_MDIE{p}", delay="del_dummy")

    if "TES" in type:
        for sel in range(4):
            create_mux("TES.CPE_RAM_O1", f"TES.SIG_SEL{sel+1}_int", 3, 0, False, f"TES.SIG_SEL{sel+1}", delay="del_dummy")
            create_mux("TES.CPE_RAM_O2", f"TES.SIG_SEL{sel+1}_int", 3, 1, False, f"TES.SIG_SEL{sel+1}", delay="del_dummy")
            create_mux("TES.CPE_COUTY1", f"TES.SIG_SEL{sel+1}_int", 3, 2, False, f"TES.SIG_SEL{sel+1}", delay="del_dummy")
            create_mux("TES.CPE_POUTY1", f"TES.SIG_SEL{sel+1}_int", 3, 3, False, f"TES.SIG_SEL{sel+1}", delay="del_dummy")
            create_mux("TES.CPE_COUTY2", f"TES.SIG_SEL{sel+1}_int", 3, 4, False, f"TES.SIG_SEL{sel+1}", delay="del_dummy")
            create_mux("TES.CPE_POUTY2", f"TES.SIG_SEL{sel+1}_int", 3, 5, False, f"TES.SIG_SEL{sel+1}", delay="del_dummy")
            clk = 0 if sel < 2 else 2
            create_mux(f"TES.CLOCK{clk+0}", f"TES.SIG_SEL{sel+1}_int", 3, 6, False, f"TES.SIG_SEL{sel+1}", delay="del_dummy")
            create_mux(f"TES.CLOCK{clk+1}", f"TES.SIG_SEL{sel+1}_int", 3, 7, False, f"TES.SIG_SEL{sel+1}", delay="del_dummy")

        for p in range(1,9):
            create_mux(f"TES.SB_Y2.P{p}", f"TES.MDIE2.P{p}", 1, 0, False, f"TES.SEL_MDIE{p}", delay="del_dummy")
            sel = (p - 1) // 2 + 1
            create_mux(f"TES.SIG_SEL{sel}_int", f"TES.MDIE2.P{p}", 1, 1, False, f"TES.SEL_MDIE{p}", delay="del_dummy")

    if "PLL" in type:
        create_mux("PLL1.CLK0",   "GLBOUT.CLK0_1",   1, 0, False, visible=False, delay="del_dummy")
        create_mux("PLL2.CLK0",   "GLBOUT.CLK0_2",   1, 0, False, visible=False, delay="del_dummy")
        create_mux("PLL3.CLK0",   "GLBOUT.CLK0_3",   1, 0, False, visible=False, delay="del_dummy")

        create_mux("PLL0.CLK90",  "GLBOUT.CLK90_0",  1, 0, False, visible=False, delay="del_dummy")
        create_mux("PLL2.CLK90",  "GLBOUT.CLK90_2",  1, 0, False, visible=False, delay="del_dummy")
        create_mux("PLL3.CLK90",  "GLBOUT.CLK90_3",  1, 0, False, visible=False, delay="del_dummy")

        create_mux("PLL0.CLK180", "GLBOUT.CLK180_0", 1, 0, False, visible=False, delay="del_dummy")
        create_mux("PLL1.CLK180", "GLBOUT.CLK180_1", 1, 0, False, visible=False, delay="del_dummy")
        create_mux("PLL3.CLK180", "GLBOUT.CLK180_3", 1, 0, False, visible=False, delay="del_dummy")

        create_mux("PLL0.CLK270", "GLBOUT.CLK270_0", 1, 0, False, visible=False, delay="del_dummy")
        create_mux("PLL1.CLK270", "GLBOUT.CLK270_1", 1, 0, False, visible=False, delay="del_dummy")
        create_mux("PLL2.CLK270", "GLBOUT.CLK270_2", 1, 0, False, visible=False, delay="del_dummy")

        for i in range(0,4):
            create_mux(f"CLKIN.CLK_REF{i}",   f"PLL{i}.CLK_REF",        1, 0, False, visible=False, delay="del_dummy")
            
            create_mux(f"PLL{i}.CLK0",        f"GLBOUT.CLK0_{i}",       1, 0, False, visible=False, delay="del_dummy")
            create_mux(f"PLL{i}.CLK90",       f"GLBOUT.CLK90_{i}",      1, 0, False, visible=False, delay="del_dummy")
            create_mux(f"PLL{i}.CLK180",      f"GLBOUT.CLK180_{i}",     1, 0, False, visible=False, delay="del_dummy")
            create_mux(f"PLL{i}.CLK270",      f"GLBOUT.CLK270_{i}",     1, 0, False, visible=False, delay="del_dummy")
            create_mux(f"PLL{i}.CLK_REF_OUT", f"GLBOUT.CLK_REF_OUT{i}", 1, 0, False, visible=False, delay="del_dummy")

            create_mux(f"GLBOUT.CLK_FB{i}",   f"PLL{i}.CLK_FEEDBACK",   1, 0, False, visible=False, delay="del_dummy")
        
            create_mux(f"CLKIN.CLK_REF{i}",   f"GLBOUT.CLK_REF_OUT{i}", 1, 0, False, f"PLL{i}.USR_CLK_OUT", config=True, delay="del_dummy")
            create_mux(f"PLL{i}.USR_CLK_REF", f"GLBOUT.CLK_REF_OUT{i}", 1, 1, False, f"PLL{i}.USR_CLK_OUT", config=True, delay="del_dummy")

    return muxes

def get_tile_types(x,y):
    val = list()
    if is_cpe(x,y):
        val.append("CPE")
        val.append("IM")
        if is_outmux(x,y):
            val.append("OM")

    if is_sb_big(x,y):
        val.append("SB_BIG")
    if is_sb_sml(x,y):
        val.append("SB_SML")
    if is_gpio(x,y):
        val.append("GPIO")
    if is_edge_io(x,y):
        val.append("IOES")
    if is_edge_top(x,y):
        val.append("TES")
    if is_edge_bottom(x,y):
        val.append("BES")
    if is_edge_left(x,y):
        val.append("LES")
    if is_edge_right(x,y):
        val.append("RES")
    if is_pll(x,y):
        val.append("PLL")
    if is_serdes(x,y):
        val.append("SERDES")
    if is_cfg_ctrl(x,y):
        val.append("CFG_CTRL")
    if is_ram(x,y):
        val.append("RAM")
    return val

def get_tile_type(x,y):
    val = get_tile_types(x,y)
    if not val:
        val.append("NONE")
    return "_".join(val)

def get_tile_type_list():
    tt = set()
    for y in range(-2, max_row()+1):
        for x in range(-2, max_col()+1):
            tt.add(get_tile_type(x,y))

    return tt

def get_bitstream_tile(x, y):
    # Edge blocks are bit bigger
    if x == -2:
        x += 1
    if x == max_col():
        x -= 1
    if y == -2:
        y += 1
    if y == max_row():
        y -= 1
    return (x + 1) // 2, (y + 1) // 2

def get_tile_info(d,x,y):
    bx, by = get_bitstream_tile(x,y)
    pos = 0
    if is_cpe(x,y):
        pos = ((x+1) % 2) * 2 + ((y+1) % 2) + 1
    if is_edge_top(x,y):
        pos = (x - 1) % 2 + 1
    if is_edge_bottom(x,y):
        pos = (x - 1) % 2 + 1
    if is_edge_left(x,y):
        pos = (y - 1) % 2 + 1
    if is_edge_right(x,y):
        pos = (y - 1) % 2 + 1
    tile_x = ((x-1)+16) % 8
    tile_y = ((y-1)+16) % 8
    return TileInfo(d, bx, by, tile_x, tile_y, pos)

def alt_plane(dir,plane):
    alt = [[5, 6, 7, 8, 1, 2, 3, 4,11,12, 9,10],
           [9,10,11,12, 9,10,11,12,12,11,10, 9]]
    return alt[dir][plane-1]

def prev_plane(p):
    return (p-2) % 12 + 1

def next_plane(p):
    return p % 12 + 1

class Die:
    def __init__(self, name : str, die_x : int, die_y : int):
        self.name = name
        self.die_x = die_x
        self.die_y = die_y
        self.debug_conn = False
        self.offset_x = die_x * num_cols()
        self.offset_y = die_y * num_rows()
        self.io_pad_names = dict()
        self.gpio_to_loc = dict()
        self.conn = dict()
        self.rev_conn = dict()
        self.ddr_i = dict()
        for y in range(-2, max_row()+1):
            for x in range(-2, max_col()+1):
                if is_gpio(x,y):
                    io = get_io_name(x,y)
                    if io.bank not in self.io_pad_names:
                        self.io_pad_names[io.bank] = dict()
                    if io.port not in self.io_pad_names[io.bank]:
                        self.io_pad_names[io.bank][io.port] = dict()
                    if io.num not in self.io_pad_names[io.bank][io.port]:
                        self.io_pad_names[io.bank][io.port][io.num] = dict()
                    self.gpio_to_loc[f"GPIO_{io.bank}_{io.port}[{io.num}]"]  = Location(x, y, 0)
                    self.io_pad_names[io.bank][io.port][io.num] = Location(x, y, 0)

    def create_conn(self, src_x,src_y, src, dst_x, dst_y, dst, delay=""):
        key_val = f"{src_x + self.offset_x}/{src_y + self.offset_y}/{src}"
        key  = Connection(src_x + self.offset_x, src_y + self.offset_y, src, "")
        item = Connection(dst_x + self.offset_x, dst_y + self.offset_y, dst, delay)
        if key_val not in self.conn:
            self.conn[key_val] = list()
            self.conn[key_val].append(key)
        self.conn[key_val].append(item)
        if "CPE.RAM_I" in dst:
            rev_key_val = f"{dst_x + self.offset_x}/{dst_y + self.offset_y}/{dst}"
            if rev_key_val not in self.rev_conn:
                self.rev_conn[rev_key_val] = list()
                self.rev_conn[rev_key_val].append(item)
            self.rev_conn[rev_key_val].append(key)
        if self.debug_conn:
            print(f"({src_x + self.offset_x},{src_y}) {src} => ({dst_x + self.offset_x},{dst_y + self.offset_y}) {dst}")

    def get_connections_for(self, src_x,src_y, src):
        key_val = f"{src_x + self.offset_x}/{src_y + self.offset_y}/{src}"
        if key_val in self.conn:
            return self.conn[key_val]
        return list()

    def get_connections_to(self, dst_x, dst_y, dst):
        rev_key_val = f"{dst_x + self.offset_x}/{dst_y + self.offset_y}/{dst}"
        if rev_key_val in self.rev_conn:
            return self.rev_conn[rev_key_val]
        return list()

    def create_cpe(self, x,y):
        delay = f"im_{get_tile_loc_str(x,y)}"
        self.create_conn(x,y,"IM.P01.Y", x,y,"CPE.IN1", f"{delay}_p1_d0_path2") # TODO: fix, d0 used only
        self.create_conn(x,y,"IM.P02.Y", x,y,"CPE.IN2", f"{delay}_p2_d0_path2")
        self.create_conn(x,y,"IM.P03.Y", x,y,"CPE.IN3", f"{delay}_p3_d0_path2")
        self.create_conn(x,y,"IM.P04.Y", x,y,"CPE.IN4", f"{delay}_p4_d0_path2")
        self.create_conn(x,y,"IM.P05.Y", x,y,"CPE.IN5", f"{delay}_p5_d0_path2")
        self.create_conn(x,y,"IM.P06.Y", x,y,"CPE.IN6", f"{delay}_p6_d0_path2")
        self.create_conn(x,y,"IM.P07.Y", x,y,"CPE.IN7", f"{delay}_p7_d0_path2")
        self.create_conn(x,y,"IM.P08.Y", x,y,"CPE.IN8", f"{delay}_p8_d0_path2")
        self.create_conn(x,y,"IM.P09.Y", x,y,"CPE.CLK", f"{delay}_p9_d0_path2")
        self.create_conn(x,y,"IM.P10.Y", x,y,"CPE.EN", f"{delay}_p10_d0_path2")
        self.create_conn(x,y,"IM.P11.Y", x,y,"CPE.SR", f"{delay}_p11_d0_path2")
        if is_cpe(x,y-1):
            self.create_conn(x,y-1,"CPE.COUTY1", x,y,"CPE.CINY1")
            self.create_conn(x,y-1,"CPE.COUTY2", x,y,"CPE.CINY2")
            self.create_conn(x,y-1,"CPE.POUTY1", x,y,"CPE.PINY1")
            self.create_conn(x,y-1,"CPE.POUTY2", x,y,"CPE.PINY2")
        if is_cpe(x-1,y):
            self.create_conn(x-1,y,"CPE.COUTX", x,y,"CPE.CINX")
            self.create_conn(x-1,y,"CPE.POUTX", x,y,"CPE.PINX")

    def create_inmux(self, x,y):
        for p in range(1,13):
            plane = f"{p:02d}"

            # D0 - D3 are from nearby SBs
            offset = 2 if is_sb(x,y) else 1
            delay = f"im_{get_tile_loc_str(x,y)}_p{p}"
            self.create_conn(x-offset,y,f"{get_sb_type(x-offset,y)}.P{plane}.Y1", x,y,f"IM.P{plane}.D0", f"{delay}_d0_path1")
            self.create_conn(x,y-offset,f"{get_sb_type(x,y-offset)}.P{plane}.Y2", x,y,f"IM.P{plane}.D1", f"{delay}_d1_path1")
            self.create_conn(x+offset,y,f"{get_sb_type(x+offset,y)}.P{plane}.Y3", x,y,f"IM.P{plane}.D2", f"{delay}_d2_path1")
            self.create_conn(x,y+offset,f"{get_sb_type(x,y+offset)}.P{plane}.Y4", x,y,f"IM.P{plane}.D3", f"{delay}_d3_path1")

            # D4 and D5 are from diagonal INMUX
            if is_cpe(x-1,y-1):
                self.create_conn(x-1,y-1,f"IM.P{plane}.Y", x,y,f"IM.P{plane}.D4", f"{delay}_d4_path1")
            if is_cpe(x+1,y+1):
                self.create_conn(x+1,y+1,f"IM.P{plane}.Y", x,y,f"IM.P{plane}.D5", f"{delay}_d5_path1")

            # D6 and D7 are from alternate planes
            alt = f"{alt_plane(0,p):02d}"
            self.create_conn(x,y,f"IM.P{alt}.Y", x,y,f"IM.P{plane}.D6", f"{delay}_d6_path1")
            alt = f"{alt_plane(1,p):02d}"
            self.create_conn(x,y,f"IM.P{alt}.Y", x,y,f"IM.P{plane}.D7", f"{delay}_d7_path1")

    def create_sb(self, x,y):
        x_0,y_0 = base_loc(x,y)
        sb_type = get_sb_type(x,y)

        for p in range(1,13):
            plane = f"{p:02d}"
            delay = f"sb_del_{get_full_tile_loc_str(x,y)}"
            # Handling input D0
            if is_cpe(x,y):
                # Core section SBs are connected to CPE
                if p < 9:
                    # planes 1..8
                    x_cpe = x_0 + (1 if (p-1) & 2 else 0)
                    y_cpe = y_0 + (1 if (p-1) & 1 else 0)
                    # alternate patterns for lower-left SB(1,1) and upper-right SB(2,2)
                    out = [ 2, 1, 2, 1, 1, 2, 1, 2] if x & 1 else [ 1, 2, 1, 2, 2, 1, 2, 1]
                    self.create_conn(x_cpe,y_cpe,f"CPE.OUT{out[p-1]}", x,y,f"{sb_type}.P{plane}.D0", f"{delay}_p{p}_d0_s0")
                else:
                    # planes 9..12
                    self.create_conn(x,y,f"OM.P{plane}.Y", x,y,f"{sb_type}.P{plane}.D0", f"{delay}_p{p}_d0_s0")
            # Handling GPIO connections is done in create_io
            # Handling inputs D2_* till D7_*
            distances = [2, 4, 8, 12, 16, 20] if is_sb_big(x,y) else [2, 4]
            for i,distance in enumerate(distances):
                for direction in range(4):
                    sb_x, sb_y = x, y
                    match direction:
                        case 0 :
                            sb_x -= distance
                        case 1 :
                            sb_y -= distance
                        case 2 :
                            sb_x += distance
                        case 3 :
                            sb_y += distance
                    if is_sb(sb_x,sb_y):
                        src  = f"{get_sb_type(sb_x,sb_y)}.P{plane}.Y{direction+1}"
                        # Long distance signals are coming from SB_DRIVE
                        if distance > 4:
                            t1x, t1y = (sb_x+16-1) // 8, (sb_y+16-1) // 8
                            t2x, t2y = (x+16-1) // 8, (y+16-1) // 8
                            # depending on distance there are additional inverters
                            # that signal is passing through each 8x8 tile
                            dist = abs(t1x-t2x) + abs(t1y-t2y)
                            if dist % 2 == 1:
                                src = f"SB_DRIVE.P{plane}.D{direction+1}.OUT"
                            else:
                                src = f"SB_DRIVE.P{plane}.D{direction+1}.OUT_NOINV"
                        self.create_conn(sb_x,sb_y, src, x,y,f"{get_sb_type(x,y)}.P{plane}.D{i+2}_{direction+1}", f"{delay}_p{p}_d{direction+1}_s{i+2}")

            if is_sb_big(x,y):
                for direction in range(4):
                    self.create_conn(x,y, f"{get_sb_type(x,y)}.P{plane}.Y{direction+1}", x,y,f"SB_DRIVE.P{plane}.D{direction+1}.IN", delay="del_dummy")

            # Diagonal inputs
            # X12 and X34 on edges are unconnected
            if is_sb(x-1,y-1):
                self.create_conn(x-1,y-1,f"{get_sb_type(x-1,y-1)}.P{plane}.YDIAG", x,y,f"{get_sb_type(x,y)}.P{plane}.X12", f"{delay}_p{p}_d0_s6")
            if is_sb(x+1,y+1):
                self.create_conn(x+1,y+1,f"{get_sb_type(x+1,y+1)}.P{plane}.YDIAG", x,y,f"{get_sb_type(x,y)}.P{plane}.X34", f"{delay}_p{p}_d0_s4")
            self.create_conn(x,y,f"{get_sb_type(x,y)}.P{prev_plane(p):02d}.YDIAG", x,y,f"{get_sb_type(x,y)}.P{plane}.X14", f"{delay}_p{p}_d0_s5")
            self.create_conn(x,y,f"{get_sb_type(x,y)}.P{next_plane(p):02d}.YDIAG", x,y,f"{get_sb_type(x,y)}.P{plane}.X23", f"{delay}_p{p}_d0_s7")

    def create_outmux(self, x,y):
        x_0,y_0 = base_loc(x,y)
        for p in range(9,13):
            plane = f"{p:02d}"
            # alternating patters depending of plane and outmux position
            outputs = [2, 2, 1, 1] if p % 2 == x & 1 else [1, 1, 2, 2]
            delay = f"om_{get_tile_loc_str(x,y)}"
            self.create_conn(x_0,   y_0,   f"CPE.OUT{outputs[0]}", x,y, f"OM.P{plane}.D0", f"{delay}_p{p}_d0")
            self.create_conn(x_0,   y_0+1, f"CPE.OUT{outputs[1]}", x,y, f"OM.P{plane}.D1", f"{delay}_p{p}_d1")
            self.create_conn(x_0+1, y_0,   f"CPE.OUT{outputs[2]}", x,y, f"OM.P{plane}.D2", f"{delay}_p{p}_d2")
            self.create_conn(x_0+1, y_0+1, f"CPE.OUT{outputs[3]}", x,y, f"OM.P{plane}.D3", f"{delay}_p{p}_d3")

    def get_pin_real_name(self, prim_name, pin):
        prim_type = prim_name
        num = 0
        if prim_name.startswith("PLL"):
            num = int(prim_name[3]) + 2
            prim_type = "PLL"
        prim = Primitive(prim_name, prim_type, num)
        return get_pin_connection_name(prim, Pin(pin,PinType.INPUT,"",False))

    def create_ram_io_conn(self, prim_name, prim_type, loc_x, loc_y):
        for c in get_pins_constraint(get_tile_type(loc_x,loc_y),prim_name, prim_type):
            name = self.get_pin_real_name(prim_name, c.name)
            if c.output == RAM_OUTPUT:
                self.create_conn(loc_x + c.rel_x, loc_y + c.rel_y, f"CPE.RAM_O{c.pin_num}", loc_x, loc_y, f"{name}")
            else:
                self.create_conn(loc_x, loc_y, f"{name}", loc_x + c.rel_x, loc_y + c.rel_y, f"CPE.RAM_I{c.pin_num}", delay="del_special_RAM_I")

    def create_io(self, x,y):
        cpe_x, cpe_y = gpio_x, gpio_y = sb_x, sb_y = x, y
        alt = False
        if is_edge_left(sb_x,sb_y):
            output = "Y3"
            cpe_x += 3
            if is_sb(sb_x+1,sb_y):
                sb_x += 1
            else:
                sb_x += 2
                gpio_y -= 1
                alt = True
        elif is_edge_right(sb_x,sb_y):
            output = "Y1"
            cpe_x -= 3
            if is_sb(sb_x-1,sb_y):
                sb_x -= 1
                gpio_y -= 1
                alt = True
            else:
                sb_x -= 2
        elif is_edge_bottom(sb_x,sb_y):
            output = "Y4"
            cpe_y += 3
            if is_sb(sb_x,sb_y+1):
                sb_y += 1
            else:
                sb_y += 2
                gpio_x -= 1
                alt = True
        else:
            output = "Y2"
            cpe_y -= 3
            if is_sb(sb_x,sb_y-1):
                sb_y -= 1
                gpio_x -= 1
                alt = True
            else:
                sb_y -= 2

        for p in range(1,13):
            plane = f"{p:02d}"
            self.create_conn(sb_x,sb_y,f"{get_sb_type(sb_x,sb_y)}.P{plane}.{output}", x,y, f"IOES.ALTIN_{plane}")
            self.create_conn(x,y, f"IOES.SB_IN_{plane}", sb_x,sb_y,f"{get_sb_type(sb_x,sb_y)}.P{plane}.D0")
        self.create_conn(gpio_x,gpio_y,"GPIO.IN1", x,y, "IOES.IO_IN1")
        self.create_conn(gpio_x,gpio_y,"GPIO.IN2", x,y, "IOES.IO_IN2")

        if not alt:
            self.create_ram_io_conn("GPIO", "GPIO", x, y)
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB0", gpio_x, gpio_y, "GPIO.CLOCK1", "del_GLBOUT_IO_SEL")
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB1", gpio_x, gpio_y, "GPIO.CLOCK2", "del_GLBOUT_IO_SEL")
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB2", gpio_x, gpio_y, "GPIO.CLOCK3", "del_GLBOUT_IO_SEL")
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB3", gpio_x, gpio_y, "GPIO.CLOCK4", "del_GLBOUT_IO_SEL")

    def create_pll(self):
        # GPIO_W2_A[8]  CLK0
        # GPIO_W2_A[7]  CLK1
        # GPIO_W2_A[6]  CLK2
        # GPIO_W2_A[5]  CLK3
        # SER_CLK       SER_CLK
        # GPIO_S3_B[8]  SPI_CLK
        # GPIO_S3_A[5]  JTAG_CLK
        loc = self.gpio_to_loc["GPIO_W2_A[8]"]
        self.create_conn(loc.x, loc.y, "GPIO.IN1", PLL_X_POS, PLL_Y_POS, "CLKIN.CLK0")
        loc = self.gpio_to_loc["GPIO_W2_A[7]"]
        self.create_conn(loc.x, loc.y, "GPIO.IN1", PLL_X_POS, PLL_Y_POS, "CLKIN.CLK1")
        loc = self.gpio_to_loc["GPIO_W2_A[6]"]
        self.create_conn(loc.x, loc.y, "GPIO.IN1", PLL_X_POS, PLL_Y_POS, "CLKIN.CLK2")
        loc = self.gpio_to_loc["GPIO_W2_A[5]"]
        self.create_conn(loc.x, loc.y, "GPIO.IN1", PLL_X_POS, PLL_Y_POS, "CLKIN.CLK3")

        self.create_ram_io_conn("GLBOUT", "GLBOUT", PLL_X_POS, PLL_Y_POS)

        self.create_ram_io_conn("PLL0", "PLL", PLL_X_POS, PLL_Y_POS)
        self.create_ram_io_conn("PLL1", "PLL", PLL_X_POS, PLL_Y_POS)
        self.create_ram_io_conn("PLL2", "PLL", PLL_X_POS, PLL_Y_POS)
        self.create_ram_io_conn("PLL3", "PLL", PLL_X_POS, PLL_Y_POS)

    def global_mesh(self):
        def global_mesh_conn(x,y,inp):
            for p in range(1,13):
                plane = f"{p:02d}"
                if is_sb_big(x,y):
                    # Clock#1: p1, p5,p9
                    # Clock#2: p2, p6,p10
                    # Clock#3: p3, p7,p11
                    # Clock#4: p4, p8,p12
                    self.create_conn(PLL_X_POS, PLL_Y_POS, f"GLBOUT.GLB{(p-1) & 3}", x,y,f"SB_BIG.P{plane}.{inp}", "del_GLBOUT_sb_big")

        # Connecting Global Mesh signals to Switch Boxes
        # Left edge
        for y in range(0,130+1):
            x = 2 - (y % 4)
            global_mesh_conn(x,y,"D7_1")
        global_mesh_conn(-1,-1,"D7_1")

        # Bottom edge
        for x in range(0,162+1):
            y = 2 - (x % 4)
            global_mesh_conn(x,y,"D7_2")
        global_mesh_conn(-1,-1,"D7_2")

        # Right edge
        for y in range(0,130+1):
            x = 2 - (y % 4) + 160
            global_mesh_conn(x,y,"D7_3")
        global_mesh_conn(159,-1,"D7_3")

        # Top edge
        for x in range(0,162+1):
            y = 2 - (x % 4) + 128
            global_mesh_conn(x,y,"D7_4")
        global_mesh_conn(-1,127,"D7_4")

        # Connecting Global Mesh signals to CPEs
        #for m in range (0,3+1):
        #    for n in range (0,7+1):
        #        x0 = 33 + m * 32
        #        y0 = 1 + n * 16
        #        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB0", x0 - 3, y0 + 10 , "CPE.RAM_I1")
        #        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB1", x0 - 3, y0 + 11 , "CPE.RAM_I1")
        #        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB2", x0 - 3, y0 + 12 , "CPE.RAM_I1")
        #        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB3", x0 - 3, y0 + 13 , "CPE.RAM_I1")
#
        #        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB0", x0 + 2, y0 + 10 , "CPE.RAM_I2")
        #        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB1", x0 + 2, y0 + 11 , "CPE.RAM_I2")
        #        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB2", x0 + 2, y0 + 12 , "CPE.RAM_I2")
        #        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB3", x0 + 2, y0 + 13 , "CPE.RAM_I2")

    def edge_select(self):
        # Left edge
        for y in range(1,128+1):
            self.create_conn(-2, y, "LES.CPE_CINX", 1, y ,"CPE.CINX")
            self.create_conn(-2, y, "LES.CPE_PINX", 1, y ,"CPE.PINX")

            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB0", -2, y, "LES.CLOCK0")
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB1", -2, y, "LES.CLOCK1")
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB2", -2, y, "LES.CLOCK2")
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB3", -2, y, "LES.CLOCK3")

            for p in range(1,9):
                plane = f"{p:02d}"
                sb_x = -1 if y % 2==1 else 0
                self.create_conn(sb_x, y, f"{get_sb_type(sb_x,y)}.P{plane}.Y3", -2, y, f"LES.SB_Y3.P{p}")

        # Bottom edge
        for x in range(1,160+1):
            self.create_conn(x, -2, "BES.CPE_CINY1", x, 1 ,"CPE.CINY1")
            self.create_conn(x, -2, "BES.CPE_PINY1", x, 1 ,"CPE.PINY1")
            self.create_conn(x, -2, "BES.CPE_CINY2", x, 1 ,"CPE.CINY2")
            self.create_conn(x, -2, "BES.CPE_PINY2", x, 1 ,"CPE.PINY2")
            if x>1:
                self.create_conn(x-1, -2, "BES.CPE_CINY1", x, -2 ,"BES.P_CINY1")
                self.create_conn(x-1, -2, "BES.CPE_PINY1", x, -2 ,"BES.P_PINY1")
                self.create_conn(x-1, -2, "BES.CPE_CINY2", x, -2 ,"BES.P_CINY2")
                self.create_conn(x-1, -2, "BES.CPE_PINY2", x, -2 ,"BES.P_PINY2")

            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB0", x, -2, "BES.CLOCK0")
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB1", x, -2, "BES.CLOCK1")
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB2", x, -2, "BES.CLOCK2")
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB3", x, -2, "BES.CLOCK3")

            for p in range(1,9):
                plane = f"{p:02d}"
                sb_y = -1 if x % 2==1 else 0
                self.create_conn(x, sb_y, f"{get_sb_type(x,sb_y)}.P{plane}.Y4", x, -2, f"BES.SB_Y4.P{p}")

        # Right edge
        for y in range(1,128+1):
            self.create_conn(160, y, "CPE.RAM_O1", 163, y ,"RES.CPE_RAM_O1")
            self.create_conn(160, y, "CPE.RAM_O2", 163, y ,"RES.CPE_RAM_O2")
            self.create_conn(160, y, "CPE.COUTX", 163, y ,"RES.CPE_COUTX")
            self.create_conn(160, y, "CPE.POUTX", 163, y ,"RES.CPE_POUTX")

            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB0", 163, y, "RES.CLOCK0")
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB1", 163, y, "RES.CLOCK1")
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB2", 163, y, "RES.CLOCK2")
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB3", 163, y, "RES.CLOCK3")

            for p in range(1,9):
                plane = f"{p:02d}"
                sb_x = 161 if y % 2==1 else 162
                self.create_conn(sb_x, y, f"{get_sb_type(sb_x,y)}.P{plane}.Y1", 163, y, f"RES.SB_Y1.P{p}")

        # Top edge
        for x in range(28,160+1):
            self.create_conn(x, 128 ,"CPE.RAM_O1", x, 131, "TES.CPE_RAM_O1")
            self.create_conn(x, 128 ,"CPE.RAM_O2", x, 131, "TES.CPE_RAM_O2")
            self.create_conn(x, 128 ,"CPE.COUTY1", x, 131, "TES.CPE_COUTY1")
            self.create_conn(x, 128 ,"CPE.POUTY1", x, 131, "TES.CPE_POUTY1")
            self.create_conn(x, 128 ,"CPE.COUTY2", x, 131, "TES.CPE_COUTY2")
            self.create_conn(x, 128 ,"CPE.POUTY2", x, 131, "TES.CPE_POUTY2")

            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB0", x, 131, "TES.CLOCK0")
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB1", x, 131, "TES.CLOCK1")
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB2", x, 131, "TES.CLOCK2")
            self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB3", x, 131, "TES.CLOCK3")

            for p in range(1,9):
                plane = f"{p:02d}"
                sb_y = 129 if x % 2==1 else 130
                self.create_conn(x, sb_y, f"{get_sb_type(x,sb_y)}.P{plane}.Y2", x, 131, f"TES.SB_Y2.P{p}")

    def connect_ddr_i(self, x, y, out, bank):
        for port in ['A','B']:
            for num in range(0,9):
                loc = self.io_pad_names[bank][port][num]
                self.create_conn(x, y , f"CPE.RAM_O{out}", loc.x, loc.y, "GPIO.DDR")
        self.ddr_i[bank] = Location(x+self.offset_x,y+self.offset_y,2-out)

    def misc_connections(self):
        self.create_ram_io_conn("CFG_CTRL", "CFG_CTRL", CTRL_X_POS, CTRL_Y_POS)
        self.create_ram_io_conn("USR_RSTN", "USR_RSTN", CTRL_X_POS, CTRL_Y_POS)

        self.connect_ddr_i(97,128,1,'N1')
        self.connect_ddr_i(97,128,2,'N2')
        self.connect_ddr_i(160,65,1,'E1')
        self.connect_ddr_i(160,65,2,'E2')
        self.connect_ddr_i(1,65,1,'W1')
        self.connect_ddr_i(1,65,2,'W2')
        self.connect_ddr_i(97,1,1,'S1')
        self.connect_ddr_i(97,1,2,'S2')
        self.connect_ddr_i(49,1,1,'S3')

    def create_serdes(self, x, y):
        self.create_ram_io_conn("SERDES", "SERDES", x, y)

    def create_ram(self, x, y):
        self.create_ram_io_conn("RAM", "RAM", x, y)
        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB0", x, y, "RAM.CLOCK1")
        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB1", x, y, "RAM.CLOCK2")
        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB2", x, y, "RAM.CLOCK3")
        self.create_conn(PLL_X_POS, PLL_Y_POS, "GLBOUT.GLB3", x, y, "RAM.CLOCK4")

    def create_in_die_connections(self, conn):
        self.conn = conn
        for y in range(-2, max_row()+1):
            for x in range(-2, max_col()+1):
                if is_cpe(x,y):
                    self.create_cpe(x,y)
                    self.create_inmux(x,y)
                    if is_outmux(x,y):
                        self.create_outmux(x,y)
                if is_sb(x,y):
                    self.create_sb(x,y)
                if is_edge_io(x,y):
                    self.create_io(x,y)
                if is_ram(x,y):
                    self.create_ram(x,y)
                if is_serdes(x,y):
                    self.create_serdes(x,y)
        self.create_pll()
        self.global_mesh()
        self.edge_select()
        self.misc_connections()
