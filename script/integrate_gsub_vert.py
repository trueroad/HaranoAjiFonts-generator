#!/usr/bin/env python3

#
# Harano Aji Fonts generator
# https://github.com/trueroad/HaranoAjiFonts-generator
#
# integrate_gsub_vert.py:
#   Integrate GSUB vert lookup tables.
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

def get_max_index (root):
    for elem_lookup_list in root.findall ("./GSUB/LookupList"):
        i = 0
        for l in elem_lookup_list.findall ("./Lookup"):
            index = int (l.attrib["index"])
            if i != index:
                print ("Lookup index error: index {}, expected {}". \
                       format (index, i))
                exit (1);
            i += 1

    return i - 1

def get_vrt2_index (root):
    vrt2 = set ()

    for feature_record in root.findall ("./GSUB/FeatureList/FeatureRecord"):
        if feature_record.find ("./FeatureTag[@value='vrt2']") is not None:
            for lookup_list_index in \
                feature_record.findall ("./Feature/LookupListIndex"):
                vrt2.add (int (lookup_list_index.attrib["value"]))

    return vrt2

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

def get_single_substs (root, index):
    substs = []

    xpath = "./GSUB/LookupList/Lookup[@index='" + str (index) \
        + "']/SingleSubst/Substitution"
    for elem in root.findall (xpath):
        substs.append ((elem.attrib["in"], elem.attrib["out"]))

    return substs

def add_single_substs (root, index, substs):
    ss = root.find ("./GSUB/LookupList/Lookup[@index='" + str (index) \
                    + "']/SingleSubst")
    for (name_in, name_out) in substs:
        new_elem = ET.SubElement (ss, "Substitution")
        new_elem.attrib["in"] = name_in
        new_elem.attrib["out"] = name_out

def main ():
    if len (sys.argv) != 3:
        print ("Usage: integrate_gsub_vert.py INPUT_GSUB.ttx OUTPUT_GSUB.ttx")
        exit (1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    tree = ET.parse (input_filename)
    root = tree.getroot ()

    max_index = get_max_index (root)
    print ("max lookup table index: {}".format (max_index))
    vrt2_index = get_vrt2_index (root)
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
            substs += get_single_substs (root, j)

        print ("substs: {}".format (substs))
        add_single_substs (root, i, substs)

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

    if get_max_index (root) !=  max_index:
        print ("max lookup index error")
        exit (1)

    tree.write (output_filename)

if __name__ == "__main__":
    main ()
