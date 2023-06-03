#!/usr/bin/env python3

#
# Harano Aji Fonts generator
# https://github.com/trueroad/HaranoAjiFonts-generator
#
# remove_gsub_single.py:
#   Remove GSUB single substitution.
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

def get_gsub_index (root, feature):
    indexes = set ()

    for feature_record in root.findall ("./GSUB/FeatureList/FeatureRecord"):
        if feature_record.find \
           ("./FeatureTag[@value='{}']".format (feature)) is not None:
            for lookup_list_index in \
                feature_record.findall ("./Feature/LookupListIndex"):
                indexes.add (int (lookup_list_index.attrib["value"]))

    return indexes

def remove_single_table (root, index, table):
    ss = root.find ("./GSUB/LookupList/Lookup[@index='" + str (index) \
                    + "']/SingleSubst")
    for name_in, name_out in table:
        elem = ss.find ("./Substitution[@in='" + name_in + "'][@out='" + \
                        name_out + "']")
        if elem != None:
            ss.remove (elem)

def load_table (file):
    table = []
    with open (file, "r") as f:
        for line in f:
            if line.startswith ('#'):
                continue
            items = line.split ()
            table.append ([items[0], items[1]])
    return table

def main ():
    if len (sys.argv) != 5:
        print ("Usage: remove_gsub_single.py FEATURE INPUT_TABLE.tbl " \
               "INPUT_GSUB.ttx OUTPUT_GSUB.ttx")
        exit (1)

    feature = sys.argv[1]
    table_filename = sys.argv[2]
    input_filename = sys.argv[3]
    output_filename = sys.argv[4]

    table = load_table (table_filename)

    tree = ET.parse (input_filename)
    root = tree.getroot ()

    indexes = get_gsub_index (root, feature)
    print ("{} lookup table index: {}".format (feature, indexes))

    for index in indexes:
        remove_single_table (root, index, table)

    ET.indent(tree, '  ')
    tree.write (output_filename)

if __name__ == "__main__":
    main ()
