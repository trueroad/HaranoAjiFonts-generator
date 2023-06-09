#!/usr/bin/env python3

#
# Harano Aji Fonts generator
# https://github.com/trueroad/HaranoAjiFonts-generator
#
# check_kana_coverage:
#   Check Kana coverage.
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

from typing import List, Set
import sys

import load_table


def make_hwid_h() -> Set[int]:
    retval: Set[int] = set()
    retval.add(326)
    for c in range(332, 389+1):
        retval.add(c)
    for c in range(391, 421+1):
        retval.add(c)
    for c in range(515, 598+1):
        retval.add(c)
    return retval


def make_hwid_v() -> Set[int]:
    retval: Set[int] = set()
    retval.add(9084)
    for c in range(9090, 9262+1):
        retval.add(c)
    return retval


def make_fwid_h() -> Set[int]:
    retval: Set[int] = set()
    for c in range(643, 644+1):
        retval.add(c)
    for c in range(651, 654+1):
        retval.add(c)
    retval.add(660)
    for c in range(842, 1010+1):
        retval.add(c)
    for c in range(7958, 7960+1):
        retval.add(c)
    for c in range(8313, 8316+1):
        retval.add(c)
    retval.add(12181)
    retval.add(12269)
    retval.add(12271)
    retval.add(16195)
    for c in range(16209, 16221+1):
        retval.add(c)
    for c in range(16236, 16252+1):
        retval.add(c)
    retval.add(16326)
    retval.add(16327)
    return retval


def make_fwid_v() -> Set[int]:
    retval: Set[int] = set()
    retval.add(7891)
    for c in range(7918, 7939+1):
        retval.add(c)
    for c in range(8264, 8265+1):
        retval.add(c)
    for c in range(8271, 8272+1):
        retval.add(c)
    for c in range(12108, 12110+1):
        retval.add(c)
    retval.add(12270)
    retval.add(12272)
    for c in range(16333, 16349+1):
        retval.add(c)
    return retval


def make_hkna() -> Set[int]:
    retval: Set[int] = set()
    for c in range(12273, 12455+1):
        retval.add(c)
    for c in range(16352, 16381+1):
        retval.add(c)
    return retval


def make_vkna() -> Set[int]:
    retval: Set[int] = set()
    for c in range(12456, 12638+1):
        retval.add(c)
    for c in range(16382, 16411+1):
        retval.add(c)
    return retval


def make_pwid_h() -> Set[int]:
    retval: Set[int] = set()
    for c in range(15449, 15452+1):
        retval.add(c)
    retval.add(15455)
    for c in range(15462, 15463+1):
        retval.add(c)
    for c in range(15517, 15724+1):
        retval.add(c)
    return retval


def make_pwid_v() -> Set[int]:
    retval: Set[int] = set()
    for c in range(15976, 15979+1):
        retval.add(c)
    for c in range(15982, 16192+1):
        retval.add(c)
    return retval


def main() -> None:
    if len(sys.argv) != 2:
        print('Usage: check_kana_coverage.py '
              'available.txt')
        sys.exit(1)

    print('Checking Kana coverage...')

    available_filename: str = sys.argv[1]

    available_list: List[int] = load_table.load_available(available_filename)

    # hwid
    hwid_h: Set[int] = make_hwid_h()
    missing_hwid_h: Set[int] = set()
    for cid in hwid_h:
        if not (cid in available_list):
            missing_hwid_h.add(cid)

    hwid_v: Set[int] = make_hwid_v()
    missing_hwid_v: Set[int] = set()
    for cid in hwid_v:
        if not (cid in available_list):
            missing_hwid_v.add(cid)

    print('Missing hwid Kana glyphs:'
          f' h={len(missing_hwid_h)}/{len(make_hwid_h ())},'
          f' v={len(missing_hwid_v)}/{len(make_hwid_v ())}')

    # fwid
    fwid_h: Set[int] = make_fwid_h()
    missing_fwid_h: Set[int] = set()
    for cid in fwid_h:
        if not (cid in available_list):
            missing_fwid_h.add(cid)

    fwid_v: Set[int] = make_fwid_v()
    missing_fwid_v: Set[int] = set()
    for cid in fwid_v:
        if not (cid in available_list):
            missing_fwid_v.add(cid)

    print('Missing fwid Kana glyphs:'
          f' h={len(missing_fwid_h)}/{len(make_fwid_h ())},'
          f' v={len(missing_fwid_v)}/{len(make_fwid_v ())}')

    print('  fwid h:')
    for cid in sorted(missing_fwid_h):
        print(f'    CID+{cid}: ', end='')
        if cid == 12269:
            print('Hiragana letter small ko')
        elif cid == 12271:
            print('Katakana letter small ko')
        else:
            print('unknown')

    print('  fwid v:')
    for cid in sorted(missing_fwid_v):
        print(f'    CID+{cid}: ', end='')
        if cid == 12270:
            print('Hiragana letter small ko')
        elif cid == 12272:
            print('Katakana letter small ko')
        else:
            print('unknown')

    # hkna/vkna
    hkna: Set[int] = make_hkna()
    missing_hkna: Set[int] = set()
    for cid in hkna:
        if not (cid in available_list):
            missing_hkna.add(cid)

    vkna: Set[int] = make_vkna()
    missing_vkna: Set[int] = set()
    for cid in vkna:
        if not (cid in available_list):
            missing_vkna.add(cid)

    print('Missing tuned Kana (hkna/vkna) glyphs:'
          f' h={len(missing_hkna)}/{len(make_hkna ())},'
          f' v={len(missing_vkna)}/{len(make_vkna ())}')

    print('  hkna:')
    for cid in sorted(missing_hkna):
        print(f'    CID+{cid}: ', end='')
        if cid == 12295:
            print('Hiragana letter small ko')
        elif cid == 12385:
            print('Katakana letter small ko')
        else:
            print('unknown')

    print('  vkna:')
    for cid in sorted(missing_vkna):
        print(f'    CID+{cid}: ', end='')
        if cid == 12478:
            print('Hiragana letter small ko')
        elif cid == 12568:
            print('Katakana letter small ko')
        else:
            print('unknown')

    # pwid
    pwid_h: Set[int] = make_pwid_h()
    missing_pwid_h: Set[int] = set()
    for cid in pwid_h:
        if not (cid in available_list):
            missing_pwid_h.add(cid)

    pwid_v: Set[int] = make_pwid_v()
    missing_pwid_v: Set[int] = set()
    for cid in pwid_v:
        if not (cid in available_list):
            missing_pwid_v.add(cid)

    print('Missing pwid Kana glyphs:'
          f' h={len(missing_pwid_h)}/{len(make_pwid_h ())},'
          f' v={len(missing_pwid_v)}/{len(make_pwid_v ())}')

    print('  pwid h:')
    for cid in sorted(missing_pwid_h):
        print(f'    CID+{cid}: ', end='')
        if cid == 15723:
            print('Hiragana letter small ko')
        elif cid == 15724:
            print('Katakana letter small ko')
        else:
            print('unknown')

    print('  pwid v:')
    for cid in sorted(missing_pwid_v):
        print(f'    CID+{cid}: ', end='')
        if cid == 16191:
            print('Hiragana letter small ko')
        elif cid == 16192:
            print('Katakana letter small ko')
        else:
            print('unknown')

    print('Complete.')


if __name__ == "__main__":
    main()
