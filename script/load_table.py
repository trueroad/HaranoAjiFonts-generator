#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harano Aji Fonts generator.

https://github.com/trueroad/HaranoAjiFonts-generator

load_table.py:
  Load table.tbl module.

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

import os
import sys
from typing import Any, TextIO, Union


def load_as_dict(filename: Union[str, bytes, os.PathLike[Any]]
                 ) -> dict[int, int]:
    """Load table.tbl as dict."""
    table: dict[int, int] = {}
    f: TextIO
    with open(filename, 'r') as f:
        line: str
        for line in f:
            if line.startswith('#'):
                continue
            if line.startswith('max'):
                continue
            items: list[str] = line.split()
            if len(items) == 2 and \
               items[0].isdecimal() and items[1].isdecimal():
                table[int(items[0])] = int(items[1])
    return table


def load_as_list(filename: Union[str, bytes, os.PathLike[Any]]
                 ) -> list[tuple[int, int]]:
    """Load table.tbl as list."""
    table: list[tuple[int, int]] = []
    f: TextIO
    with open(filename, 'r') as f:
        line: str
        for line in f:
            if line.startswith('#'):
                continue
            if line.startswith('max'):
                continue
            items: list[str] = line.split()
            if len(items) == 2 and \
               items[0].isdecimal() and items[1].isdecimal():
                table.append((int(items[0]), int(items[1])))
    return table


def load_as_list_with_noconv(filename: Union[str, bytes, os.PathLike[Any]]
                             ) -> list[tuple[int, int]]:
    """Load table.tbl as list with no-conversion AI0 CID."""
    table: list[tuple[int, int]] = []
    f: TextIO
    with open(filename, 'r') as f:
        line: str
        for line in f:
            if line.startswith('#'):
                continue
            if line.startswith('max'):
                continue
            items: list[str] = line.split()
            if len(items) == 2 and \
               items[0].isdecimal() and items[1].isdecimal():
                table.append((int(items[0]), int(items[1])))
            if len(items) == 1 and items[0].isdecimal():
                table.append((int(items[0]), -1))
    return table


def load_pre_defined_cid_set(filename: Union[str, bytes, os.PathLike[Any]]
                             ) -> set[int]:
    """Load table.tbl for pre-defined CID."""
    s: set[int] = set()
    table: list[tuple[int, int]] = load_as_list(filename)

    cid: int
    for _, cid in table:
        if cid in s:
            print(f'Duplicate: table: {cid}', file=sys.stderr)
        s.add(cid)

    return s


def load_pre_defined_cid_max(filename: Union[str, bytes, os.PathLike[Any]]
                             ) -> int:
    """Load table.tbl for pre-defined CID max."""
    cid_max: int = -1
    f: TextIO
    with open(filename, 'r') as f:
        line: str
        for line in f:
            if line.startswith('#'):
                continue
            items: list[str] = line.split()
            if len(items) == 2 and items[1].isdecimal():
                cid: int = int(items[1])
                if cid > cid_max:
                    cid_max = cid

    return cid_max


def main() -> None:
    """Test main."""
    if len(sys.argv) != 2:
        print('Usage: load_table.py table.tbl')
        sys.exit(1)

    table_filename: str = sys.argv[1]
    d: dict[int, int] = load_as_dict(table_filename)
    lc: list[tuple[int, int]] = load_as_list(table_filename)
    lnc: list[tuple[int, int]] = load_as_list_with_noconv(table_filename)
    spd: set[int] = load_pre_defined_cid_set(table_filename)

    import pprint
    print('dict')
    pprint.pprint(d)
    print('\nlist')
    pprint.pprint(lc)
    print('\nlist with noconv')
    pprint.pprint(lnc)
    print('\npre-defined CID set')
    pprint.pprint(spd)


if __name__ == '__main__':
    main()
