#!/usr/bin/env python3

#
# Harano Aji Fonts generator
# https://github.com/trueroad/HaranoAjiFonts-generator
#
# make_table_for_GPOS.py:
#   Make conversion table for GPOS.
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

def load_letterface_table (file):
    table = set ()
    with open (file, "r") as f:
        for line in f:
            if line.startswith ('#'):
                continue
            items = line.split ()
            name = items[0]
            cid = int (name[3:])
            table.add (cid)
    return table

def main ():
    if len (sys.argv) != 3:
        print ("Usage: add_gsub_v.py INPUT_TABLE.TBL LETTER_FACE.TBL > "
               "OUTPUT_TABLE.TBL")
        exit (1)

    conversion_table_filename = sys.argv[1]
    letterface_table_filename = sys.argv[2]

    letterface_table = load_letterface_table (letterface_table_filename)

    with open (conversion_table_filename, "r") as f:
        for line in f:
            if line.startswith ('#'):
                continue
            items = line.split ()
            if len (items) == 2:
                cid_in = int (items[0])
                cid_out = int (items[1])
                if cid_out in letterface_table:
                    print ("# {}\t{}".format (cid_in, cid_out))
                    print ("{}".format (cid_in))
                else:
                    print ("{}\t{}".format (cid_in, cid_out))
            elif len (items) == 1:
                print ("{}".format (int (items[0])))
            else:
                print ("# error")

if __name__ == "__main__":
    main ()
