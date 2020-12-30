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

def list_feature_lookup (root):
    dic = {}
    max_value = -1
    for fr in root.findall ("./GSUB/FeatureList/FeatureRecord"):
        ft = fr.find ("FeatureTag")
        feature = ft.attrib["value"]
        for lli in fr.findall ("./Feature/LookupListIndex"):
            value = int (lli.attrib["value"])
            if value in dic:
                dic[value] = set (sorted (dic[value] | { feature }))
            else:
                dic[value] = { feature }
            if max_value < value:
                max_value = value

    result = []
    for index in range (0, max_value + 1):
        result.append (dic[index])

    return result

def get_insert_index_before_feature (root, feature):
    lookups = list_feature_lookup (root)
    for index in range (0, len (lookups)):
        if feature in lookups[index]:
            return index

    return -1

def get_insert_index_after_feature (root, feature):
    lookups = list_feature_lookup (root)
    feature_index = -1
    for index in range (0, len (lookups)):
        if feature in lookups[index]:
            feature_index = index

    if feature_index >= 0:
        feature_index += 1

    return feature_index

def insert_lookup (root, insert_index):
    ll = root.find ("./GSUB/LookupList")
    i = 0
    for l in ll.findall ("./Lookup"):
        index = int (l.attrib["index"])
        if i != index:
            print ("Lookup index error: index {}, expected {}". \
                   format (index, i))
            exit (1);
        i += 1;
    print ("max lookup index is {}".format (i - 1))

    if insert_index < 0:
        insert_index = i

    print ("preparing to insert lookup index {}".format (insert_index))
    if i > insert_index:
        for renum_index in reversed (range (insert_index, i)):
            print ("renumbering lookup index {} to {}".\
                   format (renum_index, renum_index + 1))
            l = ll.find ("./Lookup[@index='" + str (renum_index) + "']")
            l.attrib["index"] = str (renum_index + 1)

            xpath = "./GSUB//LookupListIndex[@value='" + \
                str (renum_index) + "']"
            for lli in root.findall (xpath):
                lli.attrib["value"] = str (renum_index + 1)

    print ("inserting lookup index {}".format (insert_index))
    new_l = ET.Element ("Lookup")
    ll.insert (insert_index, new_l)
    new_l.attrib["index"] = str(insert_index)
    new_lt = ET.SubElement (new_l, "LookupType")
    new_lt.attrib["value"] = "1"
    new_lf = ET.SubElement (new_l, "LookupFlag")
    new_lf.attrib["value"] = "0"
    new_ss = ET.SubElement (new_l, "SingleSubst")
    new_ss.attrib["Format"] = "2"
    new_ss.attrib["index"] = "0"

    return insert_index

def append_lookup (root):
    ll = root.find ("./GSUB/LookupList")
    i = 0
    for l in ll.findall ("./Lookup"):
        index = int (l.attrib["index"])
        if i != index:
            print ("Lookup index error: index {}, expected {}". \
                   format (index, i))
            exit (1);
        i += 1;

    new_l = ET.SubElement (ll, "Lookup")
    new_l.attrib["index"] = str (i)
    new_lt = ET.SubElement (new_l, "LookupType")
    new_lt.attrib["value"] = "1"
    new_lf = ET.SubElement (new_l, "LookupFlag")
    new_lf.attrib["value"] = "0"
    new_ss = ET.SubElement (new_l, "SingleSubst")
    new_ss.attrib["Format"] = "2"
    new_ss.attrib["index"] = "0"

    return i

def create_feature_record (root, tag, lookup_index):
    fl = root.find ("./GSUB/FeatureList")
    i = 0
    for fr in fl.findall ("./FeatureRecord"):
        index = int (fr.attrib["index"])
        if i != index:
            print ("FeatureReocrd index error: index {}, expected {}". \
                   format (index, i))
            exit (1);
        i += 1;

    print ("creating feature record index {} that has {} lookup index {}". \
           format (i, tag, lookup_index))
    new_fr = ET.SubElement (fl, "FeatureRecord")
    new_fr.attrib["index"] = str (i)
    new_ft = ET.SubElement (new_fr, "FeatureTag")
    new_ft.attrib["value"] = tag
    new_f = ET.SubElement (new_fr, "Feature")
    new_lli = ET.SubElement (new_f, "LookupListIndex")
    new_lli.attrib["index"] = "0"
    new_lli.attrib["value"] = str (lookup_index)

    return i

def main ():
    if len (sys.argv) != 6:
        print ("Usage: add_gsub_single_table.py {before|after|append}" \
               + " EXISTING_FEATURE \\")
        print ("           NEW_FEATURE INPUT_GSUB.ttx OUTPUT_GSUB.ttx")
        exit (1)

    position_reference = sys.argv[1]
    existing_feature = sys.argv[2]
    feature = sys.argv[3]
    input_filename = sys.argv[4]
    output_filename = sys.argv[5]

    tree = ET.parse (input_filename)
    root = tree.getroot ()

    lookups = list_feature_lookup (root)
    for index in range (0, len (lookups)):
        print ("lookup index {}: {}".format (index, lookups[index]))
    print ("")

    lookup_index = -1
    if position_reference == "after":
        print ("inserting {} after {}".format (feature, existing_feature))
        lookup_index = \
            insert_lookup (root, \
                           get_insert_index_after_feature (root, \
                                                           existing_feature))
    elif position_reference == "before":
        print ("inserting {} before {}".format (feature, existing_feature))
        lookup_index = \
            insert_lookup (root, \
                           get_insert_index_after_feature (root, \
                                                           existing_feature))
    elif position_reference == "append":
        print ("appending {}".format (feature))
        lookup_index = append_lookup (root)
    else:
        print ("unknown position reference '{}'".format (position_reference))
        exit (1)

    if root.find ("./GSUB/FeatureList/FeatureRecord/FeatureTag[@value='" + \
                  feature + "']") is not None:
        print ("feature {} already exists".format (feature))
        exit (1)

    print ("adding FeatureIndex for DefaultLangSys")
    xpath = "./GSUB/ScriptList/ScriptRecord/Script/DefaultLangSys"
    for ls in root.findall (xpath):
        index = create_feature_record (root, feature, lookup_index)
        new_fi = ET.SubElement (ls, "FeatureIndex")
        new_fi.attrib["value"] = str (index)

    print ("adding FeatureIndex for LangSysRecord/LangSys")
    xpath = "./GSUB/ScriptList/ScriptRecord/Script/LangSysRecord/LangSys"
    for ls in root.findall (xpath):
        index = create_feature_record (root, feature, lookup_index)
        new_fi = ET.SubElement (ls, "FeatureIndex")
        new_fi.attrib["value"] = str (index)

    tree.write (output_filename)

if __name__ == "__main__":
    main ()
