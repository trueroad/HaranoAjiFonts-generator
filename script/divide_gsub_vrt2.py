#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harano Aji Fonts generator.

https://github.com/trueroad/HaranoAjiFonts-generator

divide_gsub_vrt2.py:
  Divide GSUB vrt2 table.

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

from typing import Optional
import sys
import xml.etree.ElementTree as ET

import gsub


def main() -> None:
    """Do main."""
    if len(sys.argv) != 3:
        print('Usage: divide_gsub_vrt2.py INPUT_GSUB.ttx OUTPUT_GSUB.ttx')
        sys.exit(1)

    input_filename: str = sys.argv[1]
    output_filename: str = sys.argv[2]

    tree: ET.ElementTree = ET.parse(input_filename)
    root: ET.Element = tree.getroot()

    max_index: int = gsub.get_gsub_lookup_index_max(root)
    vert_indexes: set[int] = gsub.get_gsub_lookup_indexes(root, 'vert')
    vrt2_indexes: set[int] = gsub.get_gsub_lookup_indexes(root, 'vrt2')

    print(f'max index   : {max_index}\n'
          f'vert indexes: {vert_indexes}\n'
          f'vrt2 indexes: {vrt2_indexes}')

    if len(vert_indexes) != 1:
        print('len(vert_indexes) != 1')
        sys.exit(1)
    if len(vrt2_indexes) != 1:
        print('len(vrt2_indexes) != 1')
        sys.exit(1)
    if vert_indexes != vrt2_indexes:
        print('vert_indexes != vrt2_indexes')
        sys.exit(1)

    vert_index: int = list(vert_indexes)[0]

    insert_index: int = gsub.insert_lookup(root, vert_index + 1)
    gsub.copy_gsub_single_substs(root, vert_index, insert_index)
    gsub.replace_lookup_index_of_feature(root, 'vrt2',
                                         vert_index, insert_index)

    ET.indent(tree, '  ')
    tree.write(output_filename)


if __name__ == "__main__":
    main()
