#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harano Aji Fonts generator.

https://github.com/trueroad/HaranoAjiFonts-generator

make_pre_rotated_height.py:
  make pre-rotated height.

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
from typing import Final, Optional, TextIO
import xml.etree.ElementTree as ET


def load_pre_rotated_table(file: str) -> list[tuple[int, int]]:
    """Load pre-rotated table."""
    table: list[tuple[int, int]] = []
    f: TextIO
    with open(file, "r") as f:
        line: str
        for line in f:
            if line.startswith("#"):
                continue
            items: list[str] = line.split()
            name_src: str = items[0]
            cid_src: int = int(name_src[3:])
            name_dst: str = items[1]
            cid_dst: int = int(name_dst[3:])
            table.append((cid_src, cid_dst))
    return table


def main() -> None:
    """Do main."""
    if len(sys.argv) != 3:
        print("Usage: make_pre_rotated_height.py pre_rotated.tbl hmtx.ttx "
              "> height_pre_rotated.tbl",
              file=sys.stderr)
        sys.exit(1)

    pre_rotated_filename: str = sys.argv[1]
    hmtx_filename: str = sys.argv[2]

    pre_rotated: list[tuple[int, int]] = \
        load_pre_rotated_table(pre_rotated_filename)

    tree: ET.ElementTree = ET.parse(hmtx_filename)
    root: ET.Element = tree.getroot()

    cid_src: int
    cid_dst: int
    for cid_src, cid_dst in pre_rotated:
        hmtx: Optional[ET.Element] = \
            root.find(f"./hmtx/mtx[@name='aji{cid_src:05}']")
        if hmtx is not None:
            width: int = int(hmtx.get('width', default=1000))
            print(f'aji{cid_dst:05}\t{width}')


if __name__ == '__main__':
    main()
