#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harano Aji Fonts generator.

https://github.com/trueroad/HaranoAjiFonts-generator

gsub.py:
  GSUB module.

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

import sys
from typing import Optional
import xml.etree.ElementTree as ET


def get_gsub_lookup_indexes(root: ET.Element, feature_tag: str) -> set[int]:
    """Get GSUB Lookup indexes from feature tag."""
    indexes: set[int] = set()

    lli: ET.Element
    for lli in root.findall('./GSUB/FeatureList/FeatureRecord'
                            f"/FeatureTag[@value='{feature_tag}']"
                            '/../Feature/LookupListIndex'):
        index_str: Optional[str] = lli.get('value')
        if index_str is not None:
            indexes.add(int(index_str))

    return indexes


def get_gsub_lookup_index_max(root: ET.Element) -> int:
    """Get GSUB Lookup index maximum."""
    max_index: int = -1
    lookup: ET.Element
    for lookup in root.findall('./GSUB/LookupList/Lookup'):
        index: int = int(lookup.get('index', '-1'))
        if max_index < index:
            max_index = index
    return max_index


def get_gsub_single_substs(root: ET.Element, lookup_index: int
                           ) -> list[tuple[str, str]]:
    """Get GSUB single substs from lookup index."""
    substs: list[tuple[str, str]] = []

    elem: ET.Element
    for elem in root.findall('./GSUB/LookupList'
                             f"/Lookup[@index='{lookup_index}']"
                             '/SingleSubst/Substitution'):
        name_in: Optional[str] = elem.get('in')
        name_out: Optional[str] = elem.get('out')
        if name_in is not None and name_out is not None:
            substs.append((name_in, name_out))
    return substs


def add_gsub_single_substs(root: ET.Element, lookup_index: int,
                           substs: list[tuple[str, str]]) -> None:
    """Add GSUB single substs in lookup index."""
    ss: Optional[ET.Element] = root.find('./GSUB/LookupList'
                                         f"/Lookup[@index='{lookup_index}']"
                                         '/SingleSubst')
    if ss is None:
        print('Error: not found SingleSubst.', file=sys.stderr)
        sys.exit(1)
    name_in: str
    name_out: str
    for name_in, name_out in substs:
        elem: Optional[ET.Element] = ss.find(f"Substitution[@in='{name_in}']")
        if elem is None:
            print(f'Adding: {name_in} -> {name_out}', file=sys.stderr)
            new_elem: ET.Element = ET.SubElement(ss, 'Substitution')
            new_elem.set('in', name_in)
            new_elem.set('out', name_out)
        else:
            old_name_out: Optional[str] = elem.get('out')
            if old_name_out == name_out:
                print(f'Already exists: {name_in} -> {name_out}',
                      file=sys.stderr)
            else:
                print(f'Warning: overwriting {name_in} -> {name_out} '
                      f'(exists {old_name_out})', file=sys.stderr)
                elem.set('out', name_out)


def remove_gsub_single_substs(root: ET.Element, lookup_index: int,
                              substs: list[tuple[str, str]]) -> None:
    """Remove GSUB single substs in lookup index."""
    ss: Optional[ET.Element] = root.find('./GSUB/LookupList'
                                         f"/Lookup[@index='{lookup_index}']"
                                         '/SingleSubst')
    if ss is None:
        print('Error: not found SingleSubst.', file=sys.stderr)
        sys.exit(1)
    name_in: str
    name_out: str
    for name_in, name_out in substs:
        elem: ET.Element
        for elem in ss.findall(f"./Substitution[@in='{name_in}']"
                               f"[@out='{name_out}']"):
            ss.remove(elem)


def copy_gsub_single_substs(root: ET.Element,
                            lookup_index_src: int, lookup_index_dst: int
                            ) -> None:
    """Copy GSUB single substs in lookup index."""
    substs: list[tuple[str, str]] = \
        get_gsub_single_substs(root, lookup_index_src)
    add_gsub_single_substs(root, lookup_index_dst, substs)


def main() -> None:
    """Test main."""
    if len(sys.argv) != 2:
        print('Usage: gsub.py GSUB.ttx')
        sys.exit(1)

    filename: str = sys.argv[1]

    tree: ET.ElementTree = ET.parse(filename)
    root: ET.Element = tree.getroot()

    import pprint

    i: int
    for i in range(get_gsub_lookup_index_max(root) + 1):
        print('\nGSUB lookup index: {i}')
        print('single substs:')
        pprint.pprint(get_gsub_single_substs(root, i))


if __name__ == '__main__':
    main()
