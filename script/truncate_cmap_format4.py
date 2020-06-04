#!/usr/bin/env python3
#
# Harano Aji Fonts generator
# https://github.com/trueroad/HaranoAjiFonts-generator
#
# truncate_cmap_format4.py:
#   Truncate cmap table format 4 subtable.
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
        print("Usage: truncate_cmap_format4.py " \
              "INPUT.cmap.ttx OUTPUT.cmap.ttx")
        exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    tree = ET.parse(input_filename)
    root = tree.getroot()

    for format4 in root.findall("./cmap/cmap_format_4"):
        removes = []
        for map in format4.findall("./map"):
            code = int(map.attrib["code"], 0)
            # CJK Unified Ideographs U+4E00..U+9FFF
            # CJK Compatibility Ideographs U+F900..U+FAFF
            if (0x4e00 <= code and code <= 0x9fff) or \
               (0xf900 <= code and code <= 0xfaff):
                removes.append(map)

        for r in removes:
            format4.remove (r)

    tree.write(output_filename)

if __name__ == "__main__":
    main ()
