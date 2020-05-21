#!/usr/bin/env python3
#
# Harano Aji Fonts generator
# https://github.com/trueroad/HaranoAjiFonts-generator
#
# add_cmap_kr.py:
#   Add glyphs to cmap KR (Korean AKR).
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

cmap_add_table = [
    # U+2004 THREE-PER-EM SPACE ->
    #     AKR CID+110 One-third of hangul syllable width
    ["0x2004", "aji00110"],
    # U+2005 FOUR-PER-EM SPACE ->
    #     AKR CID+111 One-fourth of hangul syllable width
    ["0x2005", "aji00111"],
    # U+2006 SIX-PER-EM SPACE ->
    #     AKR CID+112 One-sixth of hangul syllable width
    ["0x2006", "aji00112"],
    # U+2007 FIGURE SPACE -> AKR CID+113 Figure width
    ["0x2007", "aji00113"],
    # U+2009 THIN SPACE ->
    #     AKR CID+114 One-eighth of hangul syllable width
    ["0x2009", "aji00114"],
    # U+200A HAIR SPACE ->
    #     AKR CID+115 One-sixteenth of hangul syllable width
    ["0x200a", "aji00115"],
    # U+3000 FIGURE SPACE -> AKR CID+12105 Hanja width
    ["0x3000", "aji12105"]
    ]

def main ():
    if len(sys.argv) <= 2:
        print("Usage: add_cmap_kr.py " \
              "INPUT.cmap.ttx OUTPUT.cmap.ttx")
        exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    tree = ET.parse(input_filename)
    root = tree.getroot()

    # Add glyphs for format 4
    for format4 in root.findall("./cmap/cmap_format_4"):
        for uc in cmap_add_table:
            element = ET.SubElement(format4, "map")
            element.set("code", uc[0])
            element.set("name", uc[1])

    # Add glyphs for format 12
    for format12 in root.findall("./cmap/cmap_format_12"):
        for uc in cmap_add_table:
            element = ET.SubElement(format12, "map")
            element.set("code", uc[0])
            element.set("name", uc[1])

    tree.write(output_filename)

if __name__ == "__main__":
    main ()
