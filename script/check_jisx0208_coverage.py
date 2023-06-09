#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harano Aji Fonts generator.

https://github.com/trueroad/HaranoAjiFonts-generator

check_jisx0208_coverage:
  Check JISX0208-SourceHan-Mapping.txt coverage.

Copyright (C) 2021, 2023 Masamichi Hosoda.
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

from typing import List
import sys

import load_table


# JISX0208-SourceHan-Mapping.txt: Source Han's JIS X 0208 mapping file from
# Adobe-Japan1-6 vs Source Han
# https://ccjktype.fonts.adobe.com/2019/03/aj16-vs-source-han.html
def load_jisx0208(file: str) -> List[int]:
    """Load JISX0208-SourceHan-Mapping.txt."""
    retval: List[int] = []
    with open(file, "r") as f:
        for line in f:
            if line.startswith('#'):
                continue
            items: List[str] = line.split()
            if len(items) > 2:
                cid: int = int(items[2])
                retval.append(cid)
                if len(items) > 3:
                    if items[3].startswith('('):
                        cid_fwid: int = int(items[3][1:-1])
                        retval.append(cid_fwid)
                    elif items[3].startswith('['):
                        cid_jp90: int = int(items[3][1:-1])
                        retval.append(cid_jp90)
    return retval


def main() -> None:
    """Do main."""
    if len(sys.argv) != 3:
        print('Usage: check_jisx0208_coverage.py '
              'JISX0208-SourceHan-Mapping.txt '
              'available.txt')
        sys.exit(1)

    print('Checking jisx0208 coverage...')

    jisx0208_filename: str = sys.argv[1]
    available_filename: str = sys.argv[2]

    jisx0208_list: List[int] = load_jisx0208(jisx0208_filename)
    available_list: List[int] = load_table.load_available(available_filename)

    # print(sorted(jisx0208_list))

    missing_list: List[int] = []
    for cid in jisx0208_list:
        if not (cid in available_list):
            missing_list.append(cid)

    if len(missing_list) > 0:
        for cid in missing_list:
            print(f'Missing: CID+{cid}')
    else:
        print(f'No missing CIDs')

    print('Complete.')


if __name__ == "__main__":
    main()
