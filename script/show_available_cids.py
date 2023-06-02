#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harano Aji Fonts generator.

https://github.com/trueroad/HaranoAjiFonts-generator

show_available_cids.py:
  Show available CIDs.

Copyright (C) 2021 Masamichi Hosoda.
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

from typing import Set, List, TextIO
import sys

import load_table


def load_table_set(file: str) -> Set[int]:
    """Load table for existing AJ1 CID."""
    s: Set[int] = set()
    table: list[tuple[int, int]] = load_table.load_as_list(file)

    cid: int
    for _, cid in table:
        if cid in s:
            print(f'Duplicate: table: {cid}', file=sys.stderr)
        s.add(cid)

    return s


def load_copy_and_rotate_table(file: str) -> Set[int]:
    """Load copy_and_rotate_table for existing AJ1 CID."""
    s: Set[int] = set()
    f: TextIO
    with open(file, "r") as f:
        line: str
        for line in f:
            if line.startswith("#"):
                continue
            items: List[str] = line.split()
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
        print('Usage: show_available_cids.py'
              + ' TABLE.TBL COPY_AND_ROTATE_DO.TBL PRE_ROTATED.TBL')
        sys.exit(1)

    table: str = sys.argv[1]
    copy_and_rotate: str = sys.argv[2]
    pre_rotated: str = sys.argv[3]

    s_notdef: Set[int] = {0}
    s_table: Set[int] = load_table_set(table)
    s_copy_and_rotate: Set[int] = \
        load_copy_and_rotate_table(copy_and_rotate)
    s_pre_rotated: Set[int] = \
        load_copy_and_rotate_table(pre_rotated)

    s_total: Set[int] = s_notdef | s_table | s_copy_and_rotate | s_pre_rotated
    cid: int
    for cid in sorted(s_total):
        print(cid)

    i: int
    for i in (s_notdef & s_table):
        print(f'Duplicate: notdef & table: {i}',
              file=sys.stderr)
    for i in (s_notdef & s_copy_and_rotate):
        print(f'Duplicate: notdef & copy_and_rotate: {i}',
              file=sys.stderr)
    for i in (s_notdef & s_pre_rotated):
        print(f'Duplicate: notdef & pre_rotated: {i}',
              file=sys.stderr)
    for i in (s_table & s_copy_and_rotate):
        print(f'Duplicate: table & copy_and_rotate: {i}',
              file=sys.stderr)
    for i in (s_table & s_pre_rotated):
        print(f'Duplicate: table & pre_rotated: {i}',
              file=sys.stderr)
    for i in (s_copy_and_rotate & s_pre_rotated):
        print(f'Duplicate: copy_and_rotate & pre_rotated: {i}',
              file=sys.stderr)

    print(f'conversion = {len(s_table)}, '
          f'copy + pre-rotated = {len(s_copy_and_rotate | s_pre_rotated)}, '
          f'.notdef = {len(s_notdef)}: total {len(s_total)}\n'
          f'  (copy = {len(s_copy_and_rotate)}, '
          f'pre-rotated = {len(s_pre_rotated)})',
          file=sys.stderr)


if __name__ == "__main__":
    main()
