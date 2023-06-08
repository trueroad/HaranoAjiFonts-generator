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


def list_features_by_lookup_index(root: ET.Element) -> list[set[str]]:
    """List feature tags by lookup index."""
    result: list[set[str]] = []
    fr: ET.Element
    for fr in root.findall('./GSUB/FeatureList/FeatureRecord'):
        ft: Optional[ET.Element] = fr.find('./FeatureTag')
        if ft is None:
            continue
        feature_tag: Optional[str] = ft.get('value')
        if feature_tag is None:
            continue
        lli: ET.Element
        for lli in fr.findall('./Feature/LookupListIndex'):
            value: Optional[str] = lli.get('value')
            if value is not None and value.isdecimal():
                lookup_index: int = int(value)
                while len(result) <= lookup_index:
                    result.append(set())
                result[lookup_index] |= {feature_tag}
    return result


def get_lookup_index_to_insert_before_feature(root: ET.Element,
                                              feature_tag: str
                                              ) -> Optional[int]:
    """Get lookup index to insert before the specified feature tag."""
    lookups: list[set[str]] = list_features_by_lookup_index(root)
    i: int
    for i in range(len(lookups)):
        if feature_tag in lookups[i]:
            return i
    return None


def get_lookup_index_to_insert_after_feature(root: ET.Element,
                                             feature_tag: str
                                             ) -> Optional[int]:
    """Get lookup index to insert after the specified feature tag."""
    lookups: list[set[str]] = list_features_by_lookup_index(root)
    result: Optional[int] = None
    i: int
    for i in range(len(lookups)):
        if feature_tag in lookups[i]:
            result = i
    if result is not None:
        result += 1
    return result


def insert_lookup(root: ET.Element, lookup_index_to_insert: int) -> int:
    """Insert lookup."""
    max_index: int = get_gsub_lookup_index_max(root)

    insert_index: int
    if lookup_index_to_insert < 0:
        insert_index = max_index + 1
    else:
        insert_index = lookup_index_to_insert

    print(f'preparing to insert lookup index {insert_index}',
          file=sys.stderr)
    if insert_index < max_index + 1:
        renum_index: int
        for renum_index in reversed(range(insert_index, max_index + 1)):
            print('renumbering lookup index '
                  f'{renum_index} to {renum_index + 1}', file=sys.stderr)
            l: Optional[ET.Element] = \
                root.find(f"./GSUB/LookupList/Lookup[@index='{renum_index}']")
            if l is None:
                print('cannot find Lookup index {renum_index}',
                      file=sys.stderr)
                sys.exit(1)
            l.set('index', str(renum_index + 1))

            lli: ET.Element
            # In KR/K1, `LookupIndex`s requiring renumbering exist outside of
            # `./GSUB/FeatureList/FeatureRecord/Feature`, such as
            # `./GSUB/LookupList/Lookup/ChainContextSubst/SubstLookupRecord`.
            for lli in root.findall('./GSUB//LookupListIndex'
                                    f"[@value='{renum_index}']"):
                lli.set('value', str(renum_index + 1))

    print(f'inserting lookup index {insert_index}', file=sys.stderr)
    ll: Optional[ET.Element] = root.find('./GSUB/LookupList')
    if ll is None:
        print('cannot find LookupList', file=sys.stderr)
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


def get_gsub_feature_record_index_max(root: ET.Element) -> int:
    """Get GSUB feature record index maximum."""
    max_index: int = -1
    fr: ET.Element
    for fr in root.findall('./GSUB/FeatureList/FeatureRecord'):
        index: int = int(fr.get('index', '-1'))
        if max_index < index:
            max_index = index
    return max_index


def create_feature_record(root: ET.Element,
                          feature_tag:  str, lookup_index: int) -> int:
    """Create feature record that has specified lookup index."""
    max_index: int = get_gsub_feature_record_index_max(root)

    print(f'creating feature record index {max_index + 1}'
          f" that has '{feature_tag}' lookup index {lookup_index}",
          file=sys.stderr)
    fl: Optional[ET.Element] = root.find('./GSUB/FeatureList')
    if fl is None:
        print('cannot find FeatureList', file=sys.stderr)
        sys.exit(1)
    new_fr = ET.SubElement(fl, 'FeatureRecord')
    new_fr.set('index', str(max_index + 1))
    new_ft = ET.SubElement(new_fr, 'FeatureTag')
    new_ft.set('value', feature_tag)
    new_f = ET.SubElement(new_fr, 'Feature')
    new_lli = ET.SubElement(new_f, 'LookupListIndex')
    new_lli.set('index', '0')
    new_lli.set('value', str(lookup_index))

    return max_index + 1


def add_script_record(root: ET.Element,
                      feature_tag: str, lookup_index: int) -> None:
    """Add script record that has specified feature tag and lookup index."""
    ls: ET.Element
    index: int
    new_fi: ET.Element

    print('adding FeatureIndex for DefaultLangSys', file=sys.stderr)
    for ls in root.findall('./GSUB/ScriptList/ScriptRecord/Script'
                           '/DefaultLangSys'):
        index = create_feature_record(root, feature_tag, lookup_index)
        new_fi = ET.SubElement(ls, 'FeatureIndex')
        new_fi.set('value', str(index))

    print('adding FeatureIndex for LangSysRecord/LangSys', file=sys.stderr)
    xpath = "./GSUB/ScriptList/ScriptRecord/Script/LangSysRecord/LangSys"
    for ls in root.findall('./GSUB/ScriptList/ScriptRecord/Script/'
                           'LangSysRecord/LangSys'):
        index = create_feature_record(root, feature_tag, lookup_index)
        new_fi = ET.SubElement(ls, 'FeatureIndex')
        new_fi.set('value', str(index))


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
