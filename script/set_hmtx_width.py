#!/usr/bin/env python3
#
# Harano Aji Fonts generator
# https://github.com/trueroad/HaranoAjiFonts-generator
#
# set_hmtx_width.py:
#   Set hmtx width for pwid glyphs.
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

def load_table(file):
    table = {}
    with open(file, "r") as f:
        for line in f:
            if line.startswith('#'):
                continue
            items = line.split()
            name = items[0]
            width = int(items[1])
            table[name] = width
    return table

########################################################################

if len(sys.argv) <= 3:
    print("Usage: set_hmtx_width.py width.tbl " \
          "INPUT.hmtx.ttx OUTPUT.hmtx.ttx")
    exit(1)

table_filename = sys.argv[1]
input_filename = sys.argv[2]
output_filename = sys.argv[3]

table = load_table(table_filename)

tree = ET.parse(input_filename)
root = tree.getroot()

for hmtx in root.findall("./hmtx/mtx"):
    name = hmtx.attrib["name"]
    if name in table:
        print("hmtx {}".format(name))
        width = int(hmtx.attrib["width"])
        new_width = table[name]
        if width != new_width:
            hmtx.attrib["width"] = str(new_width)
            print("  Width {} -> {}".format(width, new_width))

tree.write(output_filename)
