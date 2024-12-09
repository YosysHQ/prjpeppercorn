from enum import Enum

def max_row():
    return 131

def max_col():
    return 163

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

def is_cpe(x,y):
    return x>=1 and x<=160 and y>=1 and y<=128

def is_outmux(x,y):
    return is_cpe(x,y) and (x+1) % 2 == (y+1) % 2

def is_edge_left(x,y):
    return x==-2 and y>=1 and y<=130

def is_edge_right(x,y):
    return x==max_col() and y>=1 and y<=128

def is_edge_bottom(x,y):
    return y==-2 and x>=-1 and x<=162

def is_edge_top(x,y):
    return y==max_row() and x>=1 and x<=162

def is_edge_io(x,y):
    if (y==-2 and x>=5 and x<=40): # GPIO_S3
        return True
    if (y==-2 and x>=57 and x<=92):  # GPIO_S1
        return True
    if (y==-2 and x>=101 and x<=136): # GPIO_S2
        return True
    if (x==-2 and y>=25 and y<=60): # GPIO_W1
        return True
    if (x==-2 and y>=69 and y<=104): # GPIO_W2
        return True
    if (x==max_col() and y>=25 and y<=50): # GPIO_E1
        return True
    if (x==max_col() and y>=69 and y<=104): # GPIO_E2
        return True
    if (y==max_row() and x>=57 and x<=92): # GPIO_N1
        return True
    if (y==max_row() and x>=101 and x<=136): # GPIO_N2
        return True

def is_gpio(x,y):
    if is_edge_io(x,y):
        if (y==-2 or y==max_row()):
            return x % 2==1
        if (x==-2 or x==max_col()):
            return y % 2==1
    return False

def get_tile_type_list():
    return [ "CPE_BIG", "CPE_SML", "CPE",
             "SB_BIG", "SB_SML",
             "GPIO_T", "EDGE_IO_T", "EDGE_T",
             "GPIO_B", "EDGE_IO_B", "EDGE_B",
             "GPIO_L", "EDGE_IO_L", "EDGE_L",
             "GPIO_R", "EDGE_IO_R", "EDGE_R",
             "NONE" ]

class PinType(Enum):
    INPUT = 0
    OUTPUT = 1
    INOUT = 2


CPE_PINS = {
    "RAM_I1" : PinType.INPUT,
    "RAM_I2" : PinType.INPUT,
    "IN1" : PinType.INPUT,
    "IN2" : PinType.INPUT,
    "IN3" : PinType.INPUT,
    "IN4" : PinType.INPUT,
    "IN5" : PinType.INPUT,
    "IN6" : PinType.INPUT,
    "IN7" : PinType.INPUT,
    "IN8" : PinType.INPUT,
    "CLK" : PinType.INPUT,
    "EN" : PinType.INPUT,
    "SR" : PinType.INPUT,
    "CINX" : PinType.INPUT,
    "PINX" : PinType.INPUT,
    "CINY1" : PinType.INPUT,
    "PINY1" : PinType.INPUT,
    "CINY2" : PinType.INPUT,
    "PINY2" : PinType.INPUT,
    "OUT1" : PinType.OUTPUT,
    "OUT2" : PinType.OUTPUT,
    "RAM_O1" : PinType.OUTPUT,
    "RAM_O2" : PinType.OUTPUT,
    "COUTX" : PinType.OUTPUT,
    "POUTX" : PinType.OUTPUT,
    "COUTY1" : PinType.OUTPUT,
    "POUTY1" : PinType.OUTPUT,
    "COUTY2" : PinType.OUTPUT,
    "POUTY2" : PinType.OUTPUT
}

def get_groups_for_type(type):
    groups = []
    def create_group(name, type):
        groups.append({"name":name, "type":type})
    if type.startswith("CPE"):
        # CPE
        for p in range(12):
            create_group(f"INMUX_P{p+1:02d}", "INMUX")
            if "_" in type and p>7: # OUTMUX only on CPE_BIG and CPE_SML
                create_group(f"OUTMUX_P{p+1:02d}", "OUTMUX")
    if "BIG" in type:
        # SB_BIG
        for p in range(12):
            create_group(f"SB_BIG_P{p+1:02d}", "SB_BIG")
    if "SML" in type:
        # SB_SML
        for p in range(12):
            create_group(f"SB_SML_P{p+1:02d}", "SB_SML")
    #if "GPIO" in type:
    #    # GPIO
    #if "EDGE_IO" in type:
    #    # EDGE_IO
    return groups

def get_bels_for_type(type):
    if type.startswith("CPE"):
        return [{"name":"CPE", "type":"CPE", "z":0}]
    return []

def get_bel_pins(bel):
    if bel == "CPE":
        return CPE_PINS.items()
    return []


def get_endpoints_for_type(type):
    wires = []
    def create_wire(name, type):
        wires.append({"name":name, "type":type})
    if type.startswith("CPE"):
        # CPE
        create_wire("CPE.IN1", type="CPE_WIRE_L")
        create_wire("CPE.IN2", type="CPE_WIRE_L")
        create_wire("CPE.IN3", type="CPE_WIRE_L")
        create_wire("CPE.IN4", type="CPE_WIRE_L")
        create_wire("CPE.IN5", type="CPE_WIRE_L")
        create_wire("CPE.IN6", type="CPE_WIRE_L")
        create_wire("CPE.IN7", type="CPE_WIRE_L")
        create_wire("CPE.IN8", type="CPE_WIRE_L")
        create_wire("CPE.CLK", type="CPE_WIRE_L")
        create_wire("CPE.EN", type="CPE_WIRE_L")
        create_wire("CPE.SR", type="CPE_WIRE_L")

        create_wire("CPE.RAM_I2", type="CPE_WIRE_L")
        create_wire("CPE.RAM_I1", type="CPE_WIRE_L")
        create_wire("CPE.CINX", type="CPE_WIRE_L")
        create_wire("CPE.PINX", type="CPE_WIRE_L")

        create_wire("CPE.CINY1", type="CPE_WIRE_B")
        create_wire("CPE.PINY1", type="CPE_WIRE_B")
        create_wire("CPE.CINY2", type="CPE_WIRE_B")
        create_wire("CPE.PINY2", type="CPE_WIRE_B")

        create_wire("CPE.OUT2", type="CPE_WIRE_R")
        create_wire("CPE.OUT1", type="CPE_WIRE_R")
        
        create_wire("CPE.RAM_O2", type="CPE_WIRE_R")
        create_wire("CPE.RAM_O1", type="CPE_WIRE_R")
        create_wire("CPE.COUTX", type="CPE_WIRE_R")
        create_wire("CPE.POUTX", type="CPE_WIRE_R")

        create_wire("CPE.COUTY1", type="CPE_WIRE_T")
        create_wire("CPE.POUTY1", type="CPE_WIRE_T")
        create_wire("CPE.COUTY2", type="CPE_WIRE_T")
        create_wire("CPE.POUTY2", type="CPE_WIRE_T")

        for p in range(12):
            plane = f"{p+1:02d}"
            for i in range(8):
                create_wire(f"INMUX.P{plane}.D{i}", type="INMUX_WIRE")
            create_wire(f"INMUX.P{plane}.Y", type="INMUX_WIRE")
            if "_" in type and p>7: # OUTMUX only on CPE_BIG and CPE_SML
                for i in range(4):
                    create_wire(f"OUTMUX.P{plane}.D{i}", type="OUTMUX_WIRE")
                create_wire(f"OUTMUX.P{plane}.Y", type="OUTMUX_WIRE")

    if "BIG" in type:
        # SB_BIG
        for p in range(12):
            plane = f"{p+1:02d}"
            create_wire(f"SB_BIG.P{plane}.D0", type="SB_BIG_WIRE")
            for i in range(4):
                create_wire(f"SB_BIG.P{plane}.D2_{i+1}", type="SB_BIG_WIRE")
                create_wire(f"SB_BIG.P{plane}.D3_{i+1}", type="SB_BIG_WIRE")
                create_wire(f"SB_BIG.P{plane}.D4_{i+1}", type="SB_BIG_WIRE")
                create_wire(f"SB_BIG.P{plane}.D5_{i+1}", type="SB_BIG_WIRE")
                create_wire(f"SB_BIG.P{plane}.D6_{i+1}", type="SB_BIG_WIRE")
                create_wire(f"SB_BIG.P{plane}.D7_{i+1}", type="SB_BIG_WIRE")
                create_wire(f"SB_BIG.P{plane}.Y{i+1}", type="SB_BIG_WIRE")

            create_wire(f"SB_BIG.P{plane}.YDIAG", type="SB_BIG_WIRE")
            create_wire(f"SB_BIG.P{plane}.X34", type="SB_BIG_WIRE")
            create_wire(f"SB_BIG.P{plane}.X14", type="SB_BIG_WIRE")
            create_wire(f"SB_BIG.P{plane}.X12", type="SB_BIG_WIRE")
            create_wire(f"SB_BIG.P{plane}.X23", type="SB_BIG_WIRE")

    if "SML" in type:
        # SB_SML
        for p in range(12):
            plane = f"{p+1:02d}"
            create_wire(f"SB_SML.P{plane}.D0", type="SB_SML_WIRE")
            for i in range(4):
                create_wire(f"SB_SML.P{plane}.D2_{i+1}", type="SB_SML_WIRE")
                create_wire(f"SB_SML.P{plane}.D3_{i+1}", type="SB_SML_WIRE")
                create_wire(f"SB_SML.P{plane}.Y{i+1}", type="SB_SML_WIRE")

            create_wire(f"SB_SML.P{plane}.YDIAG", type="SB_SML_WIRE")
            create_wire(f"SB_SML.P{plane}.X34", type="SB_SML_WIRE")
            create_wire(f"SB_SML.P{plane}.X14", type="SB_SML_WIRE")
            create_wire(f"SB_SML.P{plane}.X12", type="SB_SML_WIRE")
            create_wire(f"SB_SML.P{plane}.X23", type="SB_SML_WIRE")
    #if "GPIO" in type:
    #    # GPIO
    #if "EDGE_IO" in type:
    #    # EDGE_IO
    return wires

def get_mux_connections_for_type(type):
    muxes = []
    def create_pip(src, dst, bits, value):
        mux = dst.replace(".","_") + "_MUX"
        muxes.append({"src":src, "dst":dst, "mux":mux, "bits":bits, "value": value})

    if type.startswith("CPE"):
        # CPE
        for p in range(12):
            plane = f"{p+1:02d}"
            for i in range(8):
                create_pip(f"INMUX.P{plane}.D{i}", f"INMUX.P{plane}.Y", 3, i)
            if "_" in type and p>7: # OUTMUX only on CPE_BIG and CPE_SML
                for i in range(4):
                    create_pip(f"OUTMUX.P{plane}.D{i}", f"OUTMUX.P{plane}.Y", 2, i)

    if "BIG" in type:
        # SB_BIG
        for p in range(12):
            plane = f"{p+1:02d}"
            # Per Y output mux
            for i in range(4):
                create_pip(f"SB_BIG.P{plane}.D0",       f"SB_BIG.P{plane}.Y{i+1}", 3, 0)
                create_pip(f"SB_BIG.P{plane}.YDIAG",    f"SB_BIG.P{plane}.Y{i+1}", 3, 1)
                create_pip(f"SB_BIG.P{plane}.D2_{i+1}", f"SB_BIG.P{plane}.Y{i+1}", 3, 2)
                create_pip(f"SB_BIG.P{plane}.D3_{i+1}", f"SB_BIG.P{plane}.Y{i+1}", 3, 3)
                create_pip(f"SB_BIG.P{plane}.D4_{i+1}", f"SB_BIG.P{plane}.Y{i+1}", 3, 4)
                create_pip(f"SB_BIG.P{plane}.D5_{i+1}", f"SB_BIG.P{plane}.Y{i+1}", 3, 5)
                create_pip(f"SB_BIG.P{plane}.D6_{i+1}", f"SB_BIG.P{plane}.Y{i+1}", 3, 6)
                create_pip(f"SB_BIG.P{plane}.D7_{i+1}", f"SB_BIG.P{plane}.Y{i+1}", 3, 7)

            # YDIAG output mux
            create_pip(f"SB_BIG.P{plane}.Y1",  f"SB_BIG.P{plane}.YDIAG", 3, 0)
            create_pip(f"SB_BIG.P{plane}.Y2",  f"SB_BIG.P{plane}.YDIAG", 3, 1)
            create_pip(f"SB_BIG.P{plane}.Y3",  f"SB_BIG.P{plane}.YDIAG", 3, 2)
            create_pip(f"SB_BIG.P{plane}.Y4",  f"SB_BIG.P{plane}.YDIAG", 3, 3)
            create_pip(f"SB_BIG.P{plane}.X34", f"SB_BIG.P{plane}.YDIAG", 3, 4)
            create_pip(f"SB_BIG.P{plane}.X14", f"SB_BIG.P{plane}.YDIAG", 3, 5)
            create_pip(f"SB_BIG.P{plane}.X12", f"SB_BIG.P{plane}.YDIAG", 3, 6)
            create_pip(f"SB_BIG.P{plane}.X23", f"SB_BIG.P{plane}.YDIAG", 3, 7)
    if "SML" in type:
        # SB_SML
        for p in range(12):
            plane = f"{p+1:02d}"
            # Per Y output mux
            for i in range(4):
                create_pip(f"SB_SML.P{plane}.D0",       f"SB_SML.P{plane}.Y{i+1}", 2, 0)
                create_pip(f"SB_SML.P{plane}.YDIAG",    f"SB_SML.P{plane}.Y{i+1}", 2, 1)
                create_pip(f"SB_SML.P{plane}.D2_{i+1}", f"SB_SML.P{plane}.Y{i+1}", 2, 2)
                create_pip(f"SB_SML.P{plane}.D3_{i+1}", f"SB_SML.P{plane}.Y{i+1}", 2, 3)

            # YDIAG output mux
            create_pip(f"SB_SML.P{plane}.Y1",  f"SB_SML.P{plane}.YDIAG", 3, 0)
            create_pip(f"SB_SML.P{plane}.Y2",  f"SB_SML.P{plane}.YDIAG", 3, 1)
            create_pip(f"SB_SML.P{plane}.Y3",  f"SB_SML.P{plane}.YDIAG", 3, 2)
            create_pip(f"SB_SML.P{plane}.Y4",  f"SB_SML.P{plane}.YDIAG", 3, 3)
            create_pip(f"SB_SML.P{plane}.X34", f"SB_SML.P{plane}.YDIAG", 3, 4)
            create_pip(f"SB_SML.P{plane}.X14", f"SB_SML.P{plane}.YDIAG", 3, 5)
            create_pip(f"SB_SML.P{plane}.X12", f"SB_SML.P{plane}.YDIAG", 3, 6)
            create_pip(f"SB_SML.P{plane}.X23", f"SB_SML.P{plane}.YDIAG", 3, 7)

    #if "GPIO" in type:
    #    # GPIO
    #if "EDGE_IO" in type:
    #    # EDGE_IO
    return muxes

def get_tile_type(x,y):
    if is_cpe(x,y): # core section
        if is_sb_big(x,y): 
            return "CPE_BIG" # CPE + SB_BIG + INMUX + OUTMUX
        elif is_sb_sml(x,y):
            return "CPE_SML" # CPE + SB_SML + INMUX + OUTMUX
        else:
            return "CPE" # CPE + INMUX
    elif is_sb_big(x,y):
        return "SB_BIG" # SB_BIG
    elif is_sb_sml(x,y):
        return "SB_SML" # SB_SML
    elif is_edge_top(x,y):
        if is_gpio(x,y):
            return "GPIO_T" # GPIO + EDGE_IO + EDGE_T
        elif is_edge_io(x,y):
            return "EDGE_IO_T" # EDGE_IO + EDGE_T
        else:
            return "EDGE_T" # EDGE_T
    elif is_edge_bottom(x,y):
        if is_gpio(x,y):
            return "GPIO_B" # GPIO + EDGE_IO + EDGE_B
        elif is_edge_io(x,y):
            return "EDGE_IO_B" # EDGE_IO + EDGE_B
        else:
            return "EDGE_B" # EDGE_B
    elif is_edge_left(x,y):
        if is_gpio(x,y):
            return "GPIO_L" # GPIO + EDGE_IO + EDGE_L
        elif is_edge_io(x,y):
            return "EDGE_IO_L" # EDGE_IO + EDGE_L
        else:
            return "EDGE_L" # EDGE_L
    elif is_edge_right(x,y):
        if is_gpio(x,y):
            return "GPIO_R" # GPIO + EDGE_IO + EDGE_R
        elif is_edge_io(x,y):
            return "EDGE_IO_R" # EDGE_IO + EDGE_R
        else:
            return "EDGE_R" # EDGE_R
    else:
        return "NONE"

def get_connections():
    conn = dict()
    def create_conn(src_x,src_y, src, dst_x, dst_y, dst):
        key_val = f"{src_x}/{src_y}/{src}"
        key = {
            "x" : src_x,
            "y" : src_y,
            "w" : src
        }
        item = {
            "x" : dst_x,
            "y" : dst_y,
            "w" : dst
        }
        if key_val not in conn:
            conn[key_val] = list()
            conn[key_val].append(key)
        conn[key_val].append(item)

    for y in range(-2, max_row()+1):
        for x in range(-2, max_col()+1):
            if is_cpe(x,y):
                create_conn(x,y,"INMUX.P01.Y", x,y,"CPE.IN1")
                create_conn(x,y,"INMUX.P02.Y", x,y,"CPE.IN2")
                create_conn(x,y,"INMUX.P03.Y", x,y,"CPE.IN3")
                create_conn(x,y,"INMUX.P04.Y", x,y,"CPE.IN4")
                create_conn(x,y,"INMUX.P05.Y", x,y,"CPE.IN5")
                create_conn(x,y,"INMUX.P06.Y", x,y,"CPE.IN6")
                create_conn(x,y,"INMUX.P07.Y", x,y,"CPE.IN7")
                create_conn(x,y,"INMUX.P08.Y", x,y,"CPE.IN8")
                create_conn(x,y,"INMUX.P09.Y", x,y,"CPE.CLK")
                create_conn(x,y,"INMUX.P10.Y", x,y,"CPE.EN")
                create_conn(x,y,"INMUX.P11.Y", x,y,"CPE.SR")

                if is_cpe(x,y-1):
                    create_conn(x,y-1,"CPE.COUTY1", x,y,"CPE.CINY1")
                    create_conn(x,y-1,"CPE.COUTY2", x,y,"CPE.CINY2")
                    create_conn(x,y-1,"CPE.POUTY1", x,y,"CPE.PINY1")
                    create_conn(x,y-1,"CPE.POUTY2", x,y,"CPE.PINY2")
                if is_cpe(x-1,y):
                    create_conn(x-1,y,"CPE.COUTX", x,y,"CPE.CINX")
                    create_conn(x-1,y,"CPE.POUTX", x,y,"CPE.PINX")


    return conn.items()
