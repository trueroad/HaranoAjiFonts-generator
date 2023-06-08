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
from typing import Optional
import xml.etree.ElementTree as ET

import gsub


def main() -> None:
    if len(sys.argv) != 6:
        print('Usage: add_gsub_single_table.py {before|after|append}'
              ' EXISTING_FEATURE_TAG \\\n'
              '           NEW_FEATURE_TAG INPUT_GSUB.ttx OUTPUT_GSUB.ttx')
        sys.exit(1)

    position_reference: str = sys.argv[1]
    existing_feature_tag: str = sys.argv[2]
    feature_tag: str = sys.argv[3]
    input_filename: str = sys.argv[4]
    output_filename: str = sys.argv[5]

    tree: ET.ElementTree = ET.parse(input_filename)
    root: ET.Element = tree.getroot()

    lookups: list[set[str]] = gsub.list_features_by_lookup_index(root)
    index: int
    for index in range(len(lookups)):
        print("lookup index {}: {}".format(index, lookups[index]))
    print("")

    lookup_index: Optional[int]
    if position_reference == "after":
        print("inserting {} after {}".format(feature_tag,
                                             existing_feature_tag))
        lookup_index = \
            gsub.get_lookup_index_to_insert_after_feature(
                root, existing_feature_tag)
        if lookup_index is None:
            print(f"cannot find existing feature '{existing_feature_tag}'")
            sys.exit(1)
        lookup_index = gsub.insert_lookup(root, lookup_index)
    elif position_reference == "before":
        print("inserting {} before {}".format(feature_tag,
                                              existing_feature_tag))
        lookup_index = \
            gsub.get_lookup_index_to_insert_before_feature(
                root, existing_feature_tag)
        if lookup_index is None:
            print(f"cannot find existing feature '{existing_feature_tag}'")
            sys.exit(1)
        lookup_index = gsub.insert_lookup(root, lookup_index)
    elif position_reference == "append":
        print("appending {}".format(feature_tag))
        lookup_index = gsub.insert_lookup(root, -1)
    else:
        print("unknown position reference '{}'".format(position_reference))
        sys.exit(1)

    if root.find('./GSUB/FeatureList/FeatureRecord'
                 f"/FeatureTag[@value='{feature_tag}']") is not None:
        print("feature {} already exists".format(feature_tag))
        sys.exit(1)

    gsub.add_script_record(root, feature_tag, lookup_index)

    ET.indent(tree, '  ')
    tree.write(output_filename)


if __name__ == "__main__":
    main()
