#!/usr/bin/env python3
#
# Harano Aji Fonts generator
# https://github.com/trueroad/HaranoAjiFonts-generator
#
# make_adjust_center.py:
#   read hmtx.ttx and create adjustment parameters.
#
# Copyright (C) 2020 Yukimasa Morimi.
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

def adjust_type(cid):
    return 'c'

def adjust(cid, name, source_width, output_width):
    t = adjust_type(cid)
    if t == "l":
        print("{}\t{}\t{}\t{}\t{}\t{}".format(name, output_width, 0, 0, 1, 1))
    elif t == "c":
        dx = (output_width - source_width) // 2
        print("{}\t{}\t{}\t{}\t{}\t{}".format(name, output_width, dx, 0, 1, 1))
    elif t == "r":
        dx = (output_width - source_width)
        print("{}\t{}\t{}\t{}\t{}\t{}".format(name, output_width, dx, 0, 1, 1))
    else:
        print("# {}".format(name))

def load_table(file):
    table = {}
    with open(file, "r") as f:
        for line in f:
            if line.startswith('#'):
                continue
            cid = line.split()
            if len(cid) == 2:
                table[int(cid[0])] = int(cid[1])
    return table

def load_hmtx(root):
    hmtx = {}
    for mtx in root.findall("./hmtx/mtx"):
        name = mtx.attrib["name"]
        width = int(mtx.attrib["width"])
        hmtx[name] = width
    return hmtx

########################################################################

if len(sys.argv) <= 3:
    print("Usage: make_adjust_center.py table.tbl Source._h_m_t_x.ttx hmtx.ttx > adjust.tbl")
    exit(1)

table_filename = sys.argv[1]
source_filename = sys.argv[2]
output_filename = sys.argv[3]

table = load_table(table_filename)

source_tree = ET.parse(source_filename)
source_root = source_tree.getroot()
source_hmtx = load_hmtx(source_root)

output_tree = ET.parse(output_filename)
output_root = output_tree.getroot()
output_hmtx = load_hmtx(output_root)

print("# name width x-trans y-trans x-scale y-scale")

for source_name, source_width in source_hmtx.items():
    if source_name.startswith("cid"):
        source_cid = int(source_name[3:])
        if source_cid in table:
            output_cid = table[source_cid]
            output_name = "aji{:05}".format(output_cid)
            if output_name in output_hmtx:
                output_width = output_hmtx[output_name]
                if source_width != output_width:
                    adjust(output_cid, output_name, source_width, output_width)
