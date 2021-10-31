#!/usr/bin/env python3

#
# Harano Aji Fonts generator
# https://github.com/trueroad/HaranoAjiFonts-generator
#
# show_available_cids.py:
#   Show available CIDs.
#
# Copyright (C) 2021 Masamichi Hosoda.
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

from typing import Set, List
import sys


def load_table(file: str) -> Set[int]:
    s: Set[int] = set()
    with open(file, "r") as f:
        for line in f:
            if line.startswith('#'):
                continue
            items: List[str] = line.split()
            if len(items) > 1:
                cid: int = int(items[1])
                if cid in s:
                    print(f'Duplicate: table: {cid}',
                          file=sys.stderr)
                s.add(cid)
    return s


def load_copy_and_rotate_table(file: str) -> Set[int]:
    s: Set[int] = set()
    with open(file, "r") as f:
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
    if len(sys.argv) != 3:
        print('Usage: show_available_cids.py'
              + ' TABLE.TBL COPY_AND_ROTATE_DO.TBL')
        sys.exit(1)

    table: str = sys.argv[1]
    copy_and_rotate: str = sys.argv[2]

    s_notdef: Set[int] = {0}
    s_table: Set[int] = load_table(table)
    s_copy_and_rotate: Set[int] = \
        load_copy_and_rotate_table(copy_and_rotate)

    s_total: Set[int] = s_notdef | s_table | s_copy_and_rotate
    for cid in sorted(s_total):
        print(cid)

    for i in (s_notdef & s_table):
        print(f'Duplicate: notdef & table: {i}',
              file=sys.stderr)
    for i in (s_notdef & s_copy_and_rotate):
        print(f'Duplicate: notdef & copy_and_rotate: {i}',
              file=sys.stderr)
    for i in (s_table & s_copy_and_rotate):
        print(f'Duplicate: table & copy_and_rotate: {i}',
              file=sys.stderr)

    print(f'conversion = {len(s_table)}, copy = {len(s_copy_and_rotate)}, '
          f'.notdef = {len(s_notdef)}: total {len(s_total)}',
          file=sys.stderr)


if __name__ == "__main__":
    main()
