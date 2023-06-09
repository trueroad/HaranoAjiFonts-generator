#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harano Aji Fonts generator.

https://github.com/trueroad/HaranoAjiFonts-generator

check_aj16-kanji_coverage:
  Check aj16-kanji.txt coverage.

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


def load_aj16(file: str) -> List[int]:
    """Load aj16-kanji.txt."""
    retval: List[int] = []
    with open(file, "r") as f:
        for line in f:
            if line.startswith('#'):
                continue
            items: List[str] = line.split()
            if len(items) > 1:
                cid: int = int(items[0])
                retval.append(cid)
    return retval


def main() -> None:
    """Do main."""
    if len(sys.argv) != 3:
        print('Usage: check_aj16-kanji_coverage.py aj16-kanji.txt '
              'available.txt')
        sys.exit(1)

    print('Checking aj16-kanji.txt coverage...')

    aj16_filename: str = sys.argv[1]
    available_filename: str = sys.argv[2]

    aj16_list: List[int] = load_aj16(aj16_filename)
    available_list: List[int] = load_table.load_available(available_filename)

    missing_list: List[int] = []
    for cid in aj16_list:
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
