#!/usr/bin/env python3

#
# Harano Aji Fonts generator
# https://github.com/trueroad/HaranoAjiFonts-generator
#
# missing_kanji_to_tex.py:
#   Missing Kanji CIDs log file to tex file.
#
# Copyright (C) 2021, 2022 Masamichi Hosoda.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#

from typing import List
import sys


def print_list_line(cidlist: List[int]) -> None:
    print('\\fontsize{10pt}{15pt}\\selectfont%')
    print('CID+', end='')
    for cid in cidlist:
        print(f'{cid}, ')
    print('\n\\fontsize{42pt}{42pt}\\selectfont%')
    for cid in cidlist:
        print('\\CID{' + f'{cid}' + '}%')
    print('')


def print_list(cidlist: List[int]) -> None:
    i: int = 0
    line: List[int] = []
    for cid in cidlist:
        line.append(cid)
        i += 1
        if (i % 10) == 0:
            print_list_line(line)
            line = []
    if len(line) > 0:
        print_list_line(line)


def load_table(file: str) -> List[int]:
    retval: List[int] = []
    with open(file, "r") as f:
        for line in f:
            if line.startswith('missing'):
                continue
            items: List[str] = line.split()
            if len(items) > 1:
                cid: int = int(items[0])
                retval.append(cid)
    return retval


def main() -> None:
    if len(sys.argv) != 2:
        print('Usage: missing_kanji_to_tex.py table-kanji.log')
        sys.exit(1)

    table: str = sys.argv[1]
    cidlist: List[int] = load_table(table)

    if len(cidlist) == 0:
        print('None')
        return

    cidlist.sort()

    print_list(cidlist)


if __name__ == "__main__":
    main()
