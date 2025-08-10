#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harano Aji Fonts generator.

https://github.com/trueroad/HaranoAjiFonts-generator

make_copy_duplicated_table.py:
  make copy duplicated table.

Copyright (C) 2025 Masamichi Hosoda.
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
from typing import Any, TextIO, Union

import load_table


def main() -> None:
    """Do main."""
    if len(sys.argv) != 3:
        print('Usage: make_copy_duplicated_table.py table-cmap.tbl table.tbl'
              '> copy_duplicated.tbl',
              file=sys.stderr)
        sys.exit(1)

    table_cmap_filename: str = sys.argv[1]
    table_filename: str = sys.argv[2]

    s_table: set[int] = load_table.load_pre_defined_cid_set(table_filename)
    s_cid_dst: set[int] = set()

    f: TextIO
    with open(table_cmap_filename, 'r') as f:
        row: int = 0
        line: str
        for line in f:
            row += 1
            if not line.startswith('#COPY_AND_ROTATE\t'):
                continue
            items: list[str] = line.split()
            if len(items) != 4 or \
               not items[1].startswith('aji') or \
               not items[2].startswith('aji'):
                print(f'Error: invalid format. row {row}, '
                      f"filename '{table_filename}'",
                      file=sys.stderr)
                sys.exit(1)
            try:
                cid_src: int = int(items[1][3:])
                cid_dst: int = int(items[2][3:])
                angle: int = int(items[3])
            except ValueError:
                print(f'Error: invalid number. row {row}, '
                      f"filename '{table_filename}'",
                      file=sys.stderr)
                sys.exit(1)

            if cid_dst in s_table:
                print(f'#already exists pre-defined CID+{cid_dst} in table: '
                      f'CID+{cid_src} -> CID+{cid_dst}')
            else:
                if cid_dst in s_cid_dst:
                    print(f'#duplicate destination pre-defined CID+{cid_dst}: '
                          f'CID+{cid_src} -> CID+{cid_dst}')
                else:
                    print(f'aji{cid_src:05}\taji{cid_dst:05}\t{angle}')
                    s_cid_dst.add(cid_dst)


if __name__ == '__main__':
    main()
