import argparse
import sys
import os
import die

consts = set()

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-yosys', dest='yosys', type=str,
					help="Yosys share directory", default="/usr/local/share/yosys")
parser.add_argument('-o', '--outfile', dest='outfile', type=argparse.FileType('w'),
                    help="output HTML file")

def export_name(name,fout):
    if name not in consts:
        print(f"X({name})", file=fout)
        consts.add(name)
    else:
        print(f"//X({name})", file=fout)

def parse_line(item,fout):
    line = item.strip().split(" ")
    if line[0] == "module":
        name = line[1].split("(")[0]
        print(f"// primitive {name}", file=fout)
        export_name(name, fout)
    elif line[0] == "parameter":
        name = line[1]
        if name.startswith("["):
            name = line[2]
        export_name(name, fout)
    elif line[0] in ["input", "output" ,"inout"]:
        items = " ".join(line[1:]).strip().split(",")
        for it in items:
            name = it.split(" ")[-1].strip()
            if len(name)>0:
                export_name(name, fout)
    elif line[0].startswith("endmodule"):
        print(file=fout)

def main(argv):
    args = parser.parse_args(argv[1:])
    fout = args.outfile

    print("// autogenerated items", file=fout)
    with open(os.path.join(args.yosys, "gatemate", "cells_sim.v"), "r") as f:
        for item in f:
            parse_line(item,fout)
    with open(os.path.join(args.yosys, "gatemate", "cells_bb.v"), "r") as f:
        for item in f:
            parse_line(item,fout)

    for name,v in die.PRIMITIVES_PINS.items():
        print(f"// hardware primitive {name}", file=fout)
        export_name(name, fout)
        print(f"// {name} pins", file=fout)
        for pin in v:
            export_name(pin.name, fout)
        print(file=fout)

    print("// end of autogenerated items", file=fout)
    print(file=fout)

if __name__ == "__main__":
    main(sys.argv)
