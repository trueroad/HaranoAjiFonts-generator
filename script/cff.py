#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harano Aji Fonts generator.

https://github.com/trueroad/HaranoAjiFonts-generator

cff.py:
  CFF module.

Copyright (C) 2020 Yukimasa Morimi.
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

#
# Refarence
#   * Adobe Technical Note #5176: "The Compact Font Format Specification"
#     https://wwwimages2.adobe.com/content/dam/acom/en/devnet/font/pdfs/5176.CFF.pdf
#   * Adobe Technical Note #5177: "The Type 2 Charstring Format"
#     https://wwwimages2.adobe.com/content/dam/acom/en/devnet/font/pdfs/5177.Type2.pdf
#

import re
import sys
from typing import cast, Final, Union
import xml.etree.ElementTree as ET

FDArray: list[dict[str, Union[str, list[str]]]] = []
GlobalSubrs: list[str] = []


def load_GlobalSubrs(root: ET.Element) -> None:
    """Load GlobalSubrs."""
    cs: ET.Element
    for cs in root.findall("./CFF/GlobalSubrs/CharString"):
        if cs.text is not None:
            GlobalSubrs.append(cs.text)


def load_FDArray(root: ET.Element) -> None:
    """Load FDArray."""
    fd: ET.Element
    for fd in root.findall("./CFF/CFFFont/FDArray/FontDict"):
        FontDict: dict[str, Union[str, list[str]]] = {}
        cs: ET.Element
        for cs in fd.findall("./Private/*"):
            if "value" in cs.attrib:
                FontDict[cs.tag] = cs.attrib["value"]
        Subrs: list[str] = []
        for cs in fd.findall("./Private/Subrs/CharString"):
            if cs.text is not None:
                Subrs.append(cs.text)
        FontDict["Subrs"] = Subrs
        FDArray.append(FontDict)


def get_GlobalSubr(index: int) -> str:
    """Get GlobalSubr."""
    if len(GlobalSubrs) < 1240:
        return GlobalSubrs[index + 107]
    elif len(GlobalSubrs) < 33900:
        return GlobalSubrs[index + 1131]
    else:
        return GlobalSubrs[index + 32768]


def get_LocalSubr(fd: int, index: int) -> str:
    """Get LocalSubr."""
    Subrs: list[str] = cast(list[str], FDArray[fd]["Subrs"])
    if len(Subrs) < 1240:
        return Subrs[index + 107]
    elif len(Subrs) < 33900:
        return Subrs[index + 1131]
    else:
        return Subrs[index + 32768]


re_isInt: Final[re.Pattern[str]] = re.compile(r"^-?\d+$")
re_isFloat: Final[re.Pattern[str]] = re.compile(r"^-?\d+(?:\.\d+)?$")


def main() -> None:
    """Test main."""
    if len(sys.argv) != 2:
        print("Usage: cff.py CFF.ttx")
        sys.exit(1)

    tree: ET.ElementTree = ET.parse(sys.argv[1])
    root: ET.Element = tree.getroot()

    load_FDArray(root)
    load_GlobalSubrs(root)

    import pprint
    print('FDArray')
    pprint.pprint(FDArray)
    print('\nGlobalSubrs')
    pprint.pprint(GlobalSubrs)


if __name__ == '__main__':
    main()
