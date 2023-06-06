#!/usr/bin/env python3

#
# Harano Aji Fonts generator
# https://github.com/trueroad/HaranoAjiFonts-generator
#
# integrate_gsub_vert.py:
#   Integrate GSUB vert lookup tables.
#
# Copyright (C) 2020, 2023 Masamichi Hosoda.
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

import pprint
import sys
import xml.etree.ElementTree as ET

import gsub

def get_vert_index (root, vrt2_index):
    vert = set ()

    for feature_record in root.findall ("./GSUB/FeatureList/FeatureRecord"):
        if feature_record.find ("./FeatureTag[@value='vert']") is not None:
            v = set ()
            for lookup_list_index in \
                feature_record.findall ("./Feature/LookupListIndex"):
                v.add (int (lookup_list_index.attrib["value"]))
            if vrt2_index in v:
                print ("found vrt2 index {} in vert indexes {}".\
                       format (vrt2_index, v))
                if len (vert) != 0 and v != vert:
                    print ("different vert indexes {} and {} with same vrt2".\
                           format (vert, v))
                    exit (1)
                vert = v
            else:
                print ("not found vrt2 index {} in vert index {}".\
                       format (vrt2_index, v))

    return vert

def main ():
    if len (sys.argv) != 3:
        print ("Usage: integrate_gsub_vert.py INPUT_GSUB.ttx OUTPUT_GSUB.ttx")
        exit (1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    tree = ET.parse (input_filename)
    root = tree.getroot ()

    max_index = gsub.get_gsub_lookup_index_max(root)
    print ("max lookup table index: {}".format (max_index))
    vrt2_index = gsub.get_gsub_lookup_indexes(root, 'vrt2')
    print ("vrt2 lookup table index: {}".format (vrt2_index))

    integrate = {}

    for i in vrt2_index:
        vert_index = get_vert_index (root, i)
        print ("vert lookup table index: {}".format (vert_index))
        vert_index.remove (i)
        integrate[i] = vert_index

    for i in integrate:
        print ("Integrating: vert/vrt2 index {} <- vert index {}...".\
               format (i, integrate[i]))

        substs = []
        for j in integrate[i]:
            substs += gsub.get_gsub_single_substs(root, j)

        print("substs:")
        pprint.pprint(substs)
        gsub.add_gsub_single_substs(root, i, substs)

    remove_index = set ()

    for i in integrate:
        for j in integrate[i]:
            print ("Removing: vert lookup list index {}".format (j))
            remove_index.add (j)
            xpath = "./GSUB/FeatureList/FeatureRecord" + \
                "/FeatureTag[@value='vert']/../Feature"
            for elem_feature in root.findall (xpath):
                for elem in elem_feature.findall \
                    ("./LookupListIndex[@value='" + str (j) + "']"):
                    elem_feature.remove (elem)

    for i in remove_index:
        print ("Removing: lookup table index {}".format (i))
        for elem_lookup_list in root.findall ("./GSUB/LookupList"):
            xpath = "./Lookup[@index='" + str (i) + "']"
            for elem in elem_lookup_list.findall (xpath):
                elem_lookup_list.remove (elem)

    remove_index = sorted (remove_index)
    for i in reversed (remove_index):
        if i == max_index:
            max_index -= 1
            remove_index.remove (i)

    for i in reversed (remove_index):
        for renum_index in range (i + 1, max_index + 1):
            print ("renumbering lookup index {} to {}".\
                   format (renum_index, renum_index - 1))
            xpath = "./GSUB/LookupList/Lookup[@index='" + \
                str (renum_index) + "']"
            for l in root.findall (xpath):
                l.attrib["index"] = str (renum_index - 1)

            xpath = "./GSUB//LookupListIndex[@value='" + \
                str (renum_index) + "']"
            for lli in root.findall (xpath):
                lli.attrib["value"] = str (renum_index - 1)
        max_index -= 1

    if gsub.get_gsub_lookup_index_max(root) !=  max_index:
        print ("max lookup index error")
        exit (1)

    ET.indent(tree, '  ')
    tree.write (output_filename)

if __name__ == "__main__":
    main ()
