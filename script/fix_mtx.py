#!/usr/bin/env python3
#
# Harano Aji Fonts generator
# https://github.com/trueroad/HaranoAjiFonts-generator
#
# fix_mtx.py:
#   Fix hmtx and vmtx tables according to changed glyphs.
#
# Copyright (C) 2020 Masamichi Hosoda.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#

import sys
from typing import Optional
import xml.etree.ElementTree as ET

import load_table

########################################################################

def main() -> None:
    if len(sys.argv) <= 3:
        print("Usage: fix_mtx.py letter_face.tbl " \
              "INPUT.{h|v}mtx.ttx OUTPUT.{h|v}mtx.ttx")
        sys.exit(1)

    table_filename: str = sys.argv[1]
    input_filename: str = sys.argv[2]
    output_filename: str = sys.argv[3]

    table: dict[str, tuple[float, float, float, float]] = \
        load_table.load_letter_face_as_dict(table_filename)

    tree: ET.ElementTree = ET.parse(input_filename)
    root: ET.Element = tree.getroot()

    name: Optional[str]
    hmtx: ET.Element
    for hmtx in root.findall("./hmtx/mtx"):
        name = hmtx.get("name")
        if name is None:
            continue
        if name in table:
            print("hmtx {}".format(name))
            lsb_str: Optional[str] = hmtx.get("lsb")
            if lsb_str is None:
                continue
            lsb: int = int(lsb_str)
            x_min: float
            x_min, _, _, _ = table[name]
            new_lsb: int = int(x_min)
            if lsb != new_lsb:
                hmtx.set("lsb", str(new_lsb))
                print("  LSB {} -> {}".format(lsb, new_lsb))

    ascender: int = 880

    vmtx: ET.Element
    for vmtx in root.findall("./vmtx/mtx"):
        name = vmtx.attrib["name"]
        if name is None:
            continue
        if name in table:
            print("vmtx {}".format(name))
            tsb_str: Optional[str] = vmtx.get("tsb")
            if tsb_str is None:
                continue
            tsb: int = int(tsb_str)
            y_max: float
            _, _, _, y_max = table[name]
            new_tsb: int = int(ascender - y_max)
            if tsb != new_tsb:
                vmtx.set("tsb", str(new_tsb))
                print("  TSB {} -> {}".format(tsb, new_tsb))

    ET.indent(tree, '  ')
    tree.write(output_filename)


if __name__ == '__main__':
    main()
