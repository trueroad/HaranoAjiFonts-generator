#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harano Aji Fonts generator.

https://github.com/trueroad/HaranoAjiFonts-generator

make_adjust.py:
  read hmtx.ttx and create adjustment parameters.

Copyright (C) 2020 Yukimasa Morimi.
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

import load_table


def adjust_type_aj1(cid: int) -> str:
    """Get adjust type from AJ1 CID."""
    if 1011 <= cid and cid <= 1058:  # Greek
        return 'c'
    if cid == 16222:  # ς AJ1 CID+16222 U+03C2 GREEK SMALL LETTER FINAL SIGMA
        return 'c'
    if 1059 <= cid and cid <= 1124:  # Cyrillic
        return 'c'
    if cid == 647:  # ¨ AJ1 CID+647 U+00A8 'DIAERESIS'
        return 'c'
    if cid == 707:  # ° AJ1 CID+707 U+00B0 'DEGREE SIGN'
        return 'l'
    if cid == 645:  # ´ AJ1 CID+645 U+00B4 'ACUTE ACCENT'
        return 'c'
    if cid == 708:  # ′ AJ1 CID+708 U+2032 'PRIME'
        return 'l'
    if cid == 709:  # ″ AJ1 CID+709 U+2033 'DOUBLE PRIME'
        return 'l'
    if cid == 12111:  # ‼ AJ1 CID+12111 U+203C 'DOUBLE EXCLAMATION MARK'
        return 'c'
    if cid == 16278:  # ⁇ AJ1 CID+16278 U+2047 'DOUBLE QUESTION MARK'
        return 'c'
    if cid == 16279:  # ⁈ AJ1 CID+16279 U+2048 'QUESTION EXCLAMATION MARK'
        return 'c'
    if cid == 12112:  # ⁉ AJ1 CID+12112 U+2049 'EXCLAMATION QUESTION MARK'
        return 'c'
    if cid == 8025:  # ℓ AJ1 CID+8025 U+2113 'SCRIPT SMALL L'
        return 'c'
    if cid == 7610:  # № AJ1 CID+7610 U+2116 'NUMERO SIGN'
        return 'c'
    if cid == 693:  # − AJ1 CID+693 U+2212 'MINUS SIGN'
        return 'c'
    if cid == 16270:  # ✓ AJ1 CID+16270 U+2713 'CHECK MARK'
        return 'c'
    if cid == 16328:  # AJ1 CID+16328 U+20DD 'COMBINING ENCLOSING CIRCLE'
        return 'r'
    if cid == 11035:  # AJ1 CID+11035 U+20DE 'COMBINING ENCLOSING SQUARE'
        return 'r'
    if cid == 16326:
        # AJ1 CID+16326 U+3099 'COMBINING KATAKANA-HIRAGANA VOICED SOUND MARK'
        return ''  # calc by make_shift.py
    if cid == 16327:
        # AJ1 CID+16327 U+309A
        # 'COMBINING KATAKANA-HIRAGANA SEMI-VOICED SOUND MARK'
        return ''  # calc by make_shift.py
    return ''


def adjust(ros: str, cid: int, name: str,
           source_width: int, output_width: int) -> None:
    """Output adjust parameter."""
    t: str
    if ros == 'AJ1':
        t = adjust_type_aj1(cid)
    else:
        t = 'c'

    dx: int
    if t == "l":
        print("{}\t{}\t{}\t{}\t{}\t{}".format(name, output_width, 0, 0, 1, 1))
    elif t == "c":
        dx = (output_width - source_width) // 2
        print("{}\t{}\t{}\t{}\t{}\t{}".format(name, output_width, dx, 0, 1, 1))
    elif t == "r":
        dx = (output_width - source_width)
        print("{}\t{}\t{}\t{}\t{}\t{}".format(name, output_width, dx, 0, 1, 1))
    else:
        print("# {}".format(name))


def load_hmtx(root: ET.Element) -> dict[str, int]:
    """Load hmtx."""
    hmtx: dict[str, int] = {}
    mtx: ET.Element
    for mtx in root.findall("./hmtx/mtx"):
        name: Optional[str] = mtx.attrib["name"]
        width_str: Optional[str] = mtx.attrib["width"]
        if name is not None and width_str is not None and \
           width_str.isdecimal():
            hmtx[name] = int(width_str)
    return hmtx

########################################################################


def main() -> None:
    """Do main."""
    if len(sys.argv) <= 4:
        print("Usage: make_adjust.py ROS table.tbl "
              "Source._h_m_t_x.ttx hmtx.ttx > adjust.tbl")
        sys.exit(1)

    ros: str = sys.argv[1]
    table_filename: str = sys.argv[2]
    source_filename: str = sys.argv[3]
    output_filename: str = sys.argv[4]

    table: dict[int, int] = load_table.load_as_dict(table_filename)

    source_tree: ET.ElementTree = ET.parse(source_filename)
    source_root: ET.Element = source_tree.getroot()
    source_hmtx = load_hmtx(source_root)

    output_tree: ET.ElementTree = ET.parse(output_filename)
    output_root: ET.Element = output_tree.getroot()
    output_hmtx = load_hmtx(output_root)

    print("# name width x-trans y-trans x-scale y-scale")

    source_name: str
    source_width: int
    for source_name, source_width in source_hmtx.items():
        if source_name.startswith("cid"):
            source_cid: int = int(source_name[3:])
            if source_cid in table:
                output_cid: int = table[source_cid]
                output_name: str = "aji{:05}".format(output_cid)
                if output_name in output_hmtx:
                    output_width: int = output_hmtx[output_name]
                    if source_width != output_width:
                        adjust(ros, output_cid, output_name,
                               source_width, output_width)


if __name__ == '__main__':
    main()
