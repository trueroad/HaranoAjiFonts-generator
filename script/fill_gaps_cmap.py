#!/usr/bin/env python3
#
# Harano Aji Fonts generator
# https://github.com/trueroad/HaranoAjiFonts-generator
#
# fill_gaps_cmap.py:
#   Fill the gaps in the cmap table to reduce the size of format 4.
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
import xml.etree.ElementTree as ET

def main ():
    if len(sys.argv) <= 2:
        print("Usage: fill_gaps_cmap.py " \
              "INPUT.cmap.ttx OUTPUT.cmap.ttx")
        exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    tree = ET.parse(input_filename)
    root = tree.getroot()

    # Fill the gaps for format 4
    for format4 in root.findall("./cmap/cmap_format_4"):
        codes = []
        for map in format4.findall("./map"):
            code = int(map.attrib["code"], 0)
            codes.append(code)
        codes.sort()

        before = -9999
        for code in codes:
            if code == (before + 2):
                element = ET.SubElement(format4, "map")
                element.set("code", "0x{:x}".format(code - 1))
                element.set("name", ".notdef")
            before = code

    # Format 12 for Unicode BMP must be same as format 4
    for format12 in root.findall("./cmap/cmap_format_12"):
        codes = []
        for map in format12.findall("./map"):
            code = int(map.attrib["code"], 0)
            if code < 0x10000:
                codes.append(code)
        codes.sort()

        before = -9999
        for code in codes:
            if code == (before + 2):
                element = ET.SubElement(format12, "map")
                element.set("code", "0x{:x}".format(code - 1))
                element.set("name", ".notdef")
            before = code

    tree.write(output_filename)

if __name__ == "__main__":
    main ()
