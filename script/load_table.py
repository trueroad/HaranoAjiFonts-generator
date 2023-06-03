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


#
# For table.tbl
#


def load_base(filename: Union[str, bytes, os.PathLike[Any]]
              ) -> tuple[list[tuple[int, int]], int]:
    """Load table.tbl base."""
    table: list[tuple[int, int]] = []
    cid_max: int = -1
    f: TextIO
    with open(filename, 'r') as f:
        row: int = 0
        line: str
        for line in f:
            row += 1
            if line.startswith('#'):
                continue
            items: list[str] = line.split()
            if len(items) == 2 and items[1].isdecimal():
                cid_out: int = int(items[1])
                if items[0].isdecimal():
                    table.append((int(items[0]), cid_out))
                elif items[0] != 'max':
                    print('Error: 1st column is not integer (cid_in) or '
                          "'max'.\n"
                          f"  row {row}, filename '{str(filename)}',\n"
                          f"  1st column: '{items[0]}'",
                          file=sys.stderr)
                    sys.exit(1)
                if cid_max < cid_out:
                    cid_max = cid_out
            elif len(items) == 1 and items[0].isdecimal():
                table.append((int(items[0]), -1))
            else:
                print(f'Error: Invalid table format.\n'
                      f"  row {row}, filename '{str(filename)}',\n"
                      f"  line: '{line}'",
                      file=sys.stderr)
                sys.exit(1)
    return table, cid_max


def load_as_list(filename: Union[str, bytes, os.PathLike[Any]]
                 ) -> list[tuple[int, int]]:
    """Load table.tbl as list without no-conversion AI0 CID."""
    table: list[tuple[int, int]] = []
    cid_in: int
    cid_out: int
    for cid_in, cid_out in load_base(filename)[0]:
        if cid_out >= 0:
            table.append((cid_in, cid_out))
    return table


def load_as_list_with_noconv(filename: Union[str, bytes, os.PathLike[Any]]
                             ) -> list[tuple[int, int]]:
    """Load table.tbl as list with no-conversion AI0 CID."""
    return load_base(filename)[0]


def load_as_dict(filename: Union[str, bytes, os.PathLike[Any]]
                 ) -> dict[int, int]:
    """Load table.tbl as dict."""
    table: dict[int, int] = {}
    cid_in: int
    cid_out: int
    for cid_in, cid_out in load_base(filename)[0]:
        if cid_out >= 0:
            table[cid_in] = cid_out
    return table


def load_pre_defined_cid_set(filename: Union[str, bytes, os.PathLike[Any]]
                             ) -> set[int]:
    """Load table.tbl for pre-defined CID (not including reserved)."""
    s: set[int] = set()
    cid: int
    for _, cid in load_base(filename)[0]:
        if cid in s:
            print(f'Duplicate: table: {cid}', file=sys.stderr)
        if cid >= 0:
            s.add(cid)
    return s


def load_pre_defined_cid_max(filename: Union[str, bytes, os.PathLike[Any]]
                             ) -> int:
    """Load table.tbl for pre-defined CID max (including reserved)."""
    return load_base(filename)[1]


#
# Main
#


def main() -> None:
    """Test main."""
    if len(sys.argv) != 2:
        print('Usage: load_table.py table.tbl')
        sys.exit(1)

    import pprint

    table_filename: str = sys.argv[1]

    table_list: list[tuple[int, int]] = load_as_list(table_filename)
    print('table.tbl list')
    pprint.pprint(table_list)

    table_dict: dict[int, int] = load_as_dict(table_filename)
    print('\ntable.tbl dict')
    pprint.pprint(table_dict)

    table_set: set[int] = load_pre_defined_cid_set(table_filename)
    print('\ntable.tbl pre-defined CID set (not including reserved)')
    pprint.pprint(table_set)

    cid_max: int = load_pre_defined_cid_max(table_filename)
    print('\ntable.tbl pre-defined CID max (including reserved)')
    print(cid_max)


if __name__ == '__main__':
    main()
