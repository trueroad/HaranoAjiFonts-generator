#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harano Aji Fonts generator.

https://github.com/trueroad/HaranoAjiFonts-generator

make_shift.py:
  create shift parameters from letter face

Copyright (C) 2020, 2022, 2023 Masamichi Hosoda.
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

import load_table


def calc_shift(name: str, width: int, ascender: int, descender: int,
               face_width: float, face_height: float, lsb: float, tsb: float
               ) -> tuple[float, float]:
    """Calc LSB and TSB."""
    new_lsb: float
    new_tsb: float
    if ((name == "aji08269" or
         name == "aji08273" or
         name == "aji08283")):
        # CID+707 -> CID+8269 (GSUB vert/vrt2, `°` U+00B0 'DEGREE SIGN')
        # CID+708 -> CID+8273 (GSUB vert/vrt2, `′` U+2032 'PRIME')
        # CID+709 -> CID+8283 (GSUB vert/vrt2, `″` U+2033 'DOUBLE PRIME')
        # Top left to bottom right
        new_lsb = width - (face_width + lsb)
        new_tsb = ascender - (descender + (face_height + tsb))
        return new_lsb, new_tsb
    elif (name == "aji16326" or
          name == "aji16327"):
        # CID+16326 U+3099 'COMBINING KATAKANA-HIRAGANA VOICED SOUND MARK'
        # CID+16327 U+309A 'COMBINING KATAKANA-HIRAGANA SEMI-VOICED SOUND MARK'
        # Left outside (right of previous letter face)
        # to left inside of letter face
        new_lsb = - lsb - face_width
        if new_lsb < 0:
            new_lsb = 0
        return new_lsb, tsb
    print("# no shift: {}".format(name))
    return lsb, tsb


def main() -> None:
    """Do main."""
    if len(sys.argv) == 1:
        print("Usage: make_shift.py letter_face01.tbl > shift.tbl")
        sys.exit(1)

    table_filename: str = sys.argv[1]

    table: list[tuple[str, float, float, float, float]] = \
        load_table.load_letter_face(table_filename)

    print("# name width x-trans y-trans x-scale y-scale")

    width: int = 1000
    ascender: int = 880
    descender: int = -120

    name: str
    x_min: float
    y_min: float
    x_max: float
    y_max: float
    for name, x_min, y_min, x_max, y_max in table:
        face_width: float = x_max - x_min
        face_height: float = y_max - y_min

        lsb: float = x_min
        tsb: float = ascender - y_max

        new_lsb: float
        new_tsb: float
        new_lsb, new_tsb = calc_shift(name, width, ascender, descender,
                                      face_width, face_height, lsb, tsb)

        print("{}\t{}\t{}\t{}\t{}\t{}".format(name, width,
                                              new_lsb - lsb,
                                              tsb - new_tsb,
                                              1, 1))


if __name__ == "__main__":
    main()
