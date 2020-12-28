#!/usr/bin/env python3

#
# Harano Aji Fonts generator
# https://github.com/trueroad/HaranoAjiFonts-generator
#
# add_gsub_single_table.py:
#   Add GSUB single substitution table.
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

def create_lookup (root):
    ll = root.find ("./GSUB/LookupList")
    max_index = 0
    for l in ll.findall ("./Lookup"):
        index = int (l.attrib["index"])
        if (max_index < index):
            max_index = index

    new_l = ET.SubElement (ll, "Lookup")
    new_l.attrib["index"] = str (max_index + 1)
    new_lt = ET.SubElement (new_l, "LookupType")
    new_lt.attrib["value"] = "1"
    new_lf = ET.SubElement (new_l, "LookupFlag")
    new_lf.attrib["value"] = "0"
    new_ss = ET.SubElement (new_l, "SingleSubst")
    new_ss.attrib["Format"] = "2"
    new_ss.attrib["index"] = "0"

    return (max_index + 1)

def create_feature_record (root, tag, lookup_index):
    fl = root.find ("./GSUB/FeatureList")
    max_index = 0
    for fr in fl.findall ("./FeatureRecord"):
        index = int (fr.attrib["index"])
        if (max_index < index):
            max_index = index

    new_fr = ET.SubElement (fl, "FeatureRecord")
    new_fr.attrib["index"] = str (max_index + 1)
    new_ft = ET.SubElement (new_fr, "FeatureTag")
    new_ft.attrib["value"] = tag
    new_f = ET.SubElement (new_fr, "Feature")
    new_lli = ET.SubElement (new_f, "LookupListIndex")
    new_lli.attrib["index"] = "0"
    new_lli.attrib["value"] = str (lookup_index)

    return (max_index + 1)

def main ():
    if len (sys.argv) != 4:
        print ("Usage: add_gsub_single_table.py FEATURE " \
               "INPUT_GSUB.ttx OUTPUT_GSUB.ttx")
        exit (1)

    feature = sys.argv[1]
    input_filename = sys.argv[2]
    output_filename = sys.argv[3]

    tree = ET.parse (input_filename)
    root = tree.getroot ()

    lookup_index = create_lookup (root)

    xpath = "./GSUB/ScriptList/ScriptRecord/Script/DefaultLangSys"
    for ls in root.findall (xpath):
        index = create_feature_record (root, feature, lookup_index)
        new_fi = ET.SubElement (ls, "FeatureIndex")
        new_fi.attrib["value"] = str (index)

    xpath = "./GSUB/ScriptList/ScriptRecord/Script/LangSysRecord/LangSys"
    for ls in root.findall (xpath):
        index = create_feature_record (root, feature, lookup_index)
        new_fi = ET.SubElement (ls, "FeatureIndex")
        new_fi.attrib["value"] = str (index)

    tree.write (output_filename)

if __name__ == "__main__":
    main ()
