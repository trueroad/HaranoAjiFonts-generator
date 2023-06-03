#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harano Aji Fonts generator.

https://github.com/trueroad/HaranoAjiFonts-generator

make_table_for_GPOS.py:
  Make conversion table for GPOS.

Copyright (C) 2020, 2023 Masamichi Hosoda.
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

import load_table


def main() -> None:
    """Do main."""
    if len(sys.argv) != 3:
        print("Usage: make_table_for_GPOS.py (in)table.tbl "
              "(in)leter_face.tbl > (out)table_for_GPOS.tbl")
        sys.exit(1)

    conversion_table_filename: str = sys.argv[1]
    letterface_table_filename: str = sys.argv[2]

    conversion_table: list[tuple[int, int]] = \
        load_table.load_as_list_with_noconv(conversion_table_filename)
    letterface_table: set[int] = \
        load_table.load_letter_face_cid_set(letterface_table_filename)

    cid_in: int
    cid_out: int
    for cid_in, cid_out in conversion_table:
        if cid_out >= 0:
            if cid_out in letterface_table:
                print("# {}\t{}".format(cid_in, cid_out))
                print("{}".format(cid_in))
            else:
                print("{}\t{}".format(cid_in, cid_out))
        else:
            print("{}".format(cid_in))


if __name__ == "__main__":
    main()
