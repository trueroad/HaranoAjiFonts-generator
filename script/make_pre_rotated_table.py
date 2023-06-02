#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harano Aji Fonts generator.

https://github.com/trueroad/HaranoAjiFonts-generator

make_pre_rotated_table.py:
  make pre-rotated table.

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
from typing import Final, TextIO

import load_table


# From Pre-Rotated Glyphs in https://github.com/adobe-type-tools/Adobe-Japan1
PRE_ROTATED_GLYPHS_AJ1: Final[list[tuple[list[tuple[int, int]], int]]] = \
    [([(1, 325), (390, 390), (501, 503), (599, 628), (630, 632),
       (8718, 8719), (326, 389), (391, 421), (515, 598), (423, 424),
       (504, 514), (422, 422), (425, 500), (629, 629)], 8720),
     ([(9354, 9778), (12063, 12087)], 12870),
     ([(15456, 15461), (15464, 15516), (15725, 15975)], 16469),
     ([(20317, 20426)], 20961)]

# From Pre-Rotated Glyphs in https://github.com/adobe-type-tools/Adobe-GB1
PRE_ROTATED_GLYPHS_AG1: Final[list[tuple[list[tuple[int, int]], int]]] = \
    [([(1, 95), (7712, 7715), (814, 939), (7716, 7716)], 22127),
     ([(22353, 22357)], 29059)]

# From Pre-Rotated Glyphs in https://github.com/adobe-type-tools/Adobe-CNS1
PRE_ROTATED_GLYPHS_AC1: Final[list[tuple[list[tuple[int, int]], int]]] = \
    [([(1, 98), (13648, 13742)], 17408),
     ([(17601, 17601), (17603, 17603)], 17604)]

# From Pre-Rotated Glyphs in
# https://github.com/adobe-type-tools/Adobe-KR/blob/master/5093.Adobe-Korea1-2.pdf
PRE_ROTATED_GLYPHS_AK1: Final[list[tuple[list[tuple[int, int]], int]]] = \
    [([(1, 100), (8094, 8190)], 18155)]

# No Pre-Rotated Glyphs in https://github.com/adobe-type-tools/Adobe-KR
PRE_ROTATED_GLYPHS_AKR: Final[list[tuple[list[tuple[int, int]], int]]] = \
    []


def load_copy_and_rotate_table(file: str) -> set[int]:
    """Load copy_and_rotate_table for existing AJ1 CID."""
    s: set[int] = set()
    f: TextIO
    with open(file, "r") as f:
        line: str
        for line in f:
            if line.startswith("#"):
                continue
            items: list[str] = line.split()
            name_dst: str = items[1]
            cid_dst: int = int(name_dst[3:])
            if cid_dst in s:
                print(f'Duplicate: copy_and_rotate: {cid_dst}',
                      file=sys.stderr)
            s.add(cid_dst)
    return s


def main() -> None:
    """Do main."""
    if len(sys.argv) != 4:
        print("Usage: make_pre_rotated_table.py ROS table.tbl "
              "copy_and_rotate_do.tbl > pre_rotated.tbl",
              file=sys.stderr)
        sys.exit(1)

    ros: str = sys.argv[1]
    table: str = sys.argv[2]
    copy_and_rotate: str = sys.argv[3]

    s_notdef: set[int] = {0}
    s_table: set[int] = load_table.load_pre_defined_cid_set(table)
    s_copy_and_rotate: set[int] = \
        load_copy_and_rotate_table(copy_and_rotate)

    s_total: set[int] = s_notdef | s_table | s_copy_and_rotate

    pre_rotated_glyphs: list[tuple[list[tuple[int, int]], int]]
    if ros == 'AJ1':
        pre_rotated_glyphs = PRE_ROTATED_GLYPHS_AJ1
    elif ros == 'AG1':
        pre_rotated_glyphs = PRE_ROTATED_GLYPHS_AG1
    elif ros == 'AC1':
        pre_rotated_glyphs = PRE_ROTATED_GLYPHS_AC1
    elif ros == 'AKR':
        pre_rotated_glyphs = PRE_ROTATED_GLYPHS_AKR
    elif ros == 'AK1':
        pre_rotated_glyphs = PRE_ROTATED_GLYPHS_AK1
    else:
        print('ROS is not AJ1, AG1, AC1, AKR, or AK1.',
              file=sys.stderr)
        sys.exit(1)

    print("# name_src name_dst angle")

    pre_rotated_max: int = -1
    h_ranges: list[tuple[int, int]]
    pre_rotated_range_first: int
    for h_ranges, pre_rotated_range_first in pre_rotated_glyphs:
        pre_rotated: int = pre_rotated_range_first
        h_range_first: int
        h_range_last: int
        for h_range_first, h_range_last in h_ranges:
            horizontal: int
            for horizontal in range(h_range_first, h_range_last + 1):
                if horizontal in s_total and pre_rotated not in s_total:
                    print(f'aji{horizontal:05}\taji{pre_rotated:05}\t90')
                    if pre_rotated_max < pre_rotated:
                        pre_rotated_max = pre_rotated
                pre_rotated += 1

    cid_max: int = load_table.load_pre_defined_cid_max(table)
    s_total_max: int = max(s_total)
    if s_total_max != cid_max and pre_rotated_max != cid_max:
        print(f'Error: cid_max ({cid_max}) != s_total_max ({s_total_max}) '
              f'and cid_max != pre_rotated_max {pre_rotated_max}')
        sys.exit(1)


if __name__ == '__main__':
    main()
