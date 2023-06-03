#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harano Aji Fonts generator.

https://github.com/trueroad/HaranoAjiFonts-generator

divide_gsub_vrt2.py:
  Divide GSUB vrt2 table.

Copyright (C) 2023 Masamichi Hosoda.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED.
IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
SUCH DAMAGE.
"""

from typing import Optional
import sys
import xml.etree.ElementTree as ET


def get_max_index(root: ET.Element) -> int:
    """Get max index."""
    i: int = 0
    lookup: ET.Element
    for lookup in root.findall("./GSUB/LookupList/Lookup"):
        index_str: Optional[str] = lookup.get('index')
        if index_str is not None and i != int(index_str):
            print(f'Lookup index error: index {index_str}, expected {i}')
            sys.exit(1)
        i += 1

    return i - 1


def get_indexes(root: ET.Element, feature: str) -> set[int]:
    """Get indexes."""
    indexes: set[int] = set()

    lli: ET.Element
    for lli in root.findall('./GSUB/FeatureList/FeatureRecord'
                            f"/FeatureTag[@value='{feature}']"
                            '/../Feature/LookupListIndex'):
        index_str: Optional[str] = lli.get('value')
        if index_str is not None:
            indexes.add(int(index_str))

    return indexes


def insert_lookup(root: ET.Element, insert_index: int) -> int:
    """Insert lookup."""
    max_index: int = get_max_index(root)

    if insert_index < 0:
        insert_index = max_index + 1

    print(f'preparing to insert lookup index {insert_index}')
    if insert_index < max_index + 1:
        renum_index: int
        for renum_index in reversed(range(insert_index, max_index + 1)):
            print('renumbering lookup index '
                  f'{renum_index} to {renum_index + 1}')
            l: Optional[ET.Element] = \
                root.find(f"./GSUB/LookupList/Lookup[@index='{renum_index}']")
            if l is None:
                print('cannot find Lookup index {renum_index}')
                sys.exit(1)
            l.set('index', str(renum_index + 1))

            lli: ET.Element
            # In KR/K1, `LookupIndex`s requiring renumbering exist outside of
            # `./GSUB/FeatureList/FeatureRecord/Feature`, such as
            # `./GSUB/LookupList/Lookup/ChainContextSubst/SubstLookupRecord`.
            for lli in root.findall('./GSUB//LookupListIndex'
                                    f"[@value='{renum_index}']"):
                lli.set('value', str(renum_index + 1))

    print(f'inserting lookup index {insert_index}')
    ll: Optional[ET.Element] = root.find('./GSUB/LookupList')
    if ll is None:
        print('cannot find LookupList')
        sys.exit(1)
    new_l: ET.Element = ET.Element('Lookup')
    ll.insert(insert_index, new_l)
    new_l.set('index', str(insert_index))
    new_lt: ET.Element = ET.SubElement(new_l, 'LookupType')
    new_lt.set('value', '1')
    new_lf: ET.Element = ET.SubElement(new_l, 'LookupFlag')
    new_lf.set('value', '0')
    new_ss: ET.Element = ET.SubElement(new_l, 'SingleSubst')
    new_ss.set('index', '0')

    return insert_index


def copy_singlesubst(root: ET.Element, src_index: int, dst_index: int) -> None:
    """Copy SingleSubst."""
    dst_ss: Optional[ET.Element] = \
        root.find(f"./GSUB/LookupList/Lookup[@index='{dst_index}']"
                  '/SingleSubst')
    if dst_ss is None:
        print('cannot find dst_index: {dst_index}')
        sys.exit(1)

    s: ET.Element
    for s in root.findall("./GSUB/LookupList/Lookup[@index='"
                          f'{src_index}'
                          "']/SingleSubst/Substitution"):
        new_s: ET.Element = ET.SubElement(dst_ss, 'Substitution')
        s_in: Optional[str] = s.get('in')
        s_out: Optional[str] = s.get('out')
        if s_in is not None and s_out is not None:
            new_s.set('in', s_in)
            new_s.set('out', s_out)


def replace_index_feature(root: ET.Element, feature: str,
                          old_index: int, new_index: int) -> None:
    """Replace index of feature."""
    lli: ET.Element
    for lli in root.findall('./GSUB/FeatureList/FeatureRecord'
                            f"/FeatureTag[@value='{feature}']"
                            '/../Feature'
                            f"/LookupListIndex[@value='{old_index}']"):
        lli.set('value', str(new_index))


def main() -> None:
    """Do main."""
    if len(sys.argv) != 3:
        print('Usage: divide_gsub_vrt2.py INPUT_GSUB.ttx OUTPUT_GSUB.ttx')
        sys.exit(1)

    input_filename: str = sys.argv[1]
    output_filename: str = sys.argv[2]

    tree: ET.ElementTree = ET.parse(input_filename)
    root: ET.Element = tree.getroot()

    max_index: int = get_max_index(root)
    vert_indexes: set[int] = get_indexes(root, 'vert')
    vrt2_indexes: set[int] = get_indexes(root, 'vrt2')

    print(f'max index   : {max_index}\n'
          f'vert indexes: {vert_indexes}\n'
          f'vrt2 indexes: {vrt2_indexes}')

    if len(vert_indexes) != 1:
        print('len(vert_indexes) != 1')
        sys.exit(1)
    if len(vrt2_indexes) != 1:
        print('len(vrt2_indexes) != 1')
        sys.exit(1)
    if vert_indexes != vrt2_indexes:
        print('vert_indexes != vrt2_indexes')
        sys.exit(1)

    vert_index: int = list(vert_indexes)[0]

    insert_index: int = insert_lookup(root, vert_index + 1)
    copy_singlesubst(root, vert_index, insert_index)
    replace_index_feature(root, 'vrt2', vert_index, insert_index)

    ET.indent(tree, '  ')
    tree.write(output_filename)


if __name__ == "__main__":
    main()
