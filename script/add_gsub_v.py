#!/usr/bin/env python3

#
# Harano Aji Fonts generator
# https://github.com/trueroad/HaranoAjiFonts-generator
#
# add_gsub_v.py:
#   Add GSUB vert/vrt2 substitution.
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

v_lookup_table = [
    # `〜` U+301C 'WAVE DASH'
    ["aji00665", "aji07894"],
    # `｜` U+FF5C 'Fullwidth Vertical Line Unicode Character'
    ["aji00667", "aji07896"]
    ]

v_add_table = [
    # `‖` U+2016 'DOUBLE VERTICAL LINE'
    ["aji00666", "aji07895"],
    # `°` U+00B0 'DEGREE SIGN'
    ["aji00707", "aji08269"],
    # `′` U+2032 'PRIME'
    ["aji00708", "aji08273"],
    # `″` U+2033 'DOUBLE PRIME'
    ["aji00709", "aji08283"],
    # `✂` U+2702 'BLACK SCISSORS'
    ["aji12176", "aji12178"]
    ]

def get_v_index (root):
    vert = set ()
    vrt2 = set ()

    for feature_record in root.findall ("./GSUB/FeatureList/FeatureRecord"):
        if feature_record.find ("./FeatureTag[@value='vert']") is not None:
            for lookup_list_index in \
                feature_record.findall ("./Feature/LookupListIndex"):
                vert.add (int (lookup_list_index.attrib["value"]))
        if feature_record.find ("./FeatureTag[@value='vrt2']") is not None:
            for lookup_list_index in \
                feature_record.findall ("./Feature/LookupListIndex"):
                vrt2.add (int (lookup_list_index.attrib["value"]))

    return (vert | vrt2)

def is_lookup_single_subst (root, index, name_in, name_out):
    xpath = "./GSUB/LookupList/Lookup[@index='" + str (index) \
        + "']/SingleSubst/Substitution[@in='{}'][@out='{}']" \
        .format (name_in, name_out)
    if root.find (xpath) is not None:
        return True
    return False

def is_lookup_v (root, index):
    for name_in, name_out in v_lookup_table:
        if not is_lookup_single_subst (root, index, name_in, name_out):
            return False
    return True

def add_v_table (root, index):
    ss = root.find ("./GSUB/LookupList/Lookup[@index='" + str (index) \
                    + "']/SingleSubst")
    for name_in, name_out in v_add_table:
        new_elem = ET.SubElement (ss, "Substitution")
        new_elem.attrib["in"] = name_in
        new_elem.attrib["out"] = name_out

def main ():
    if len (sys.argv) != 3:
        print ("Usage: add_gsub_v.py INPUT_GSUB.ttx OUTPUT_GSUB.ttx")
        exit (1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    tree = ET.parse (input_filename)
    root = tree.getroot ()

    v_index = get_v_index (root)
    print ("vert/vrt2 lookup table index: {}".format (v_index))

    target = set ()

    for index in v_index:
        if is_lookup_v (root, index):
            target.add (index)

    print ("target lookup table index: {}".format (target))

    for index in target:
        add_v_table (root, index)

    tree.write (output_filename)

if __name__ == "__main__":
    main ()
