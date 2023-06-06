#!/usr/bin/env python3

#
# Harano Aji Fonts generator
# https://github.com/trueroad/HaranoAjiFonts-generator
#
# add_gsub_single.py:
#   Add GSUB single substitution.
#
# Copyright (C) 2020, 2022 Masamichi Hosoda.
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

import load_table
import gsub


def main ():
    if len (sys.argv) != 5:
        print ("Usage: add_gsub_single.py FEATURE INPUT_TABLE.tbl " \
               "INPUT_GSUB.ttx OUTPUT_GSUB.ttx")
        exit (1)

    feature = sys.argv[1]
    table_filename = sys.argv[2]
    input_filename = sys.argv[3]
    output_filename = sys.argv[4]

    table = load_table.load_gsub_single_table(table_filename)

    tree = ET.parse (input_filename)
    root = tree.getroot ()

    indexes = gsub.get_gsub_lookup_indexes(root, feature)
    print ("{} lookup table index: {}".format (feature, indexes))

    for index in indexes:
        gsub.add_gsub_single_substs(root, index, table)

    ET.indent(tree, '  ')
    tree.write (output_filename)

if __name__ == "__main__":
    main ()
