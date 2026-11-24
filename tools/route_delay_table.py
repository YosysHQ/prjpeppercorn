#!/usr/bin/env python3
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

import math
import os
import statistics
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gatemate"))
from timing import decompress_timing

DELAY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "delay")
MODES = [f"{t}_{p}" for t in ("best", "typ", "worst") for p in ("lpr", "eco", "spd")]


# Worse of rise and fall max
def pick(d):
    return max(d.rise.max, d.fall.max)


# NC for dly files
def connected(d):
    return d.rise.min != 123456


def sb_value(t, src):
    arr = t.SB_del_tile_arr
    return statistics.median(pick(arr[a][b][c][p][d][src])
                             for a in range(4) for b in range(8) for c in range(4) for p in range(12)
                             for d in range(1, 5) if connected(arr[a][b][c][p][d][src]))


def im_value(t, path, inputs):
    arr = t.IM_del_tile_arr
    return statistics.median(pick(arr[path][x][y][p][i])
                             for x in range(8) for y in range(8) for p in range(8) for i in inputs
                             if connected(arr[path][x][y][p][i]))


def analyse(path):
    t = decompress_timing(path)
    r = {}
    r["span20"] = sb_value(t, 7)
    r["im_in"] = im_value(t, 0, range(4))
    r["im_pin"] = im_value(t, 1, range(4))
    r["neighbour"] = 10 + r["im_in"] + r["im_pin"]
    r["tile20"] = r["span20"] / 20
    # rounded down so estimate stays below cheapest route
    r["est_b"] = math.floor(r["tile20"])
    r["est_a"] = math.floor((r["neighbour"] - r["tile20"]) / 10) * 10
    return r


COLUMNS = ["im_in", "im_pin", "span20", "neighbour", "tile20", "est_a", "est_b"]


def main():
    widths = [10] + [max(7, len(c)) for c in COLUMNS]
    print(" ".join(h.rjust(w) for h, w in zip(["mode"] + COLUMNS, widths)))
    for mode in MODES:
        path = os.path.join(DELAY_DIR, f"cc_{mode}_dly.dly")
        if not os.path.exists(path):
            sys.exit(f"missing {path}")
        r = analyse(path)
        print(" ".join([mode.ljust(widths[0])] + [f"{r[c]:.1f}".rjust(w) for c, w in zip(COLUMNS, widths[1:])]))


if __name__ == "__main__":
    main()
