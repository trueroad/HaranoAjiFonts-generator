#!/usr/bin/env python3
#
# Harano Aji Fonts generator
# https://github.com/trueroad/HaranoAjiFonts-generator
#
# make_shift.py:
#   create shift parameters from letter face
#
# Copyright (C) 2020 Masamichi Hosoda.
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

import sys

def load_table (file):
    table = {}
    with open (file, "r") as f:
        for line in f:
            if line.startswith ('#'):
                continue
            items = line.split ()
            name = items[0]
            x_min = float (items[1])
            y_min = float (items[2])
            x_max = float (items[3])
            y_max = float (items[4])
            table[name] = (x_min, y_min, x_max, y_max)
    return table

def main ():
    if len (sys.argv) == 1:
        print ("Usage: make_shift.py letter_face01.tbl > shift.tbl")
        exit (1)

    table_filename = sys.argv[1]

    table = load_table (table_filename)

    print ("# name width x-trans y-trans x-scale y-scale")

    width = 1000
    ascender = 880
    descender = -120

    for name in table:
        x_min, y_min, x_max, y_max = table[name]

        face_width = x_max - x_min
        face_height = y_max - y_min

        lsb = x_min
        tsb = ascender - y_max

        new_lsb = width - (face_width + lsb)
        new_tsb = ascender - (descender + (face_height + tsb))

        print ("{}\t{}\t{}\t{}\t{}\t{}".format (name, width,
                                                new_lsb - lsb,
                                                tsb - new_tsb,
                                                1, 1))

if __name__ == "__main__":
    main ()
