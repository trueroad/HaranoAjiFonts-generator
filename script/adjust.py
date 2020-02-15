#!/usr/bin/env python3
#
# Harano Aji Fonts generator
# https://github.com/trueroad/HaranoAjiFonts-generator
#
# adjust.py:
#   adjust the position of the CFF glyph.
#
# Copyright (C) 2020 Yukimasa Morimi.
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
#
#
# Refarence
#   * Adobe Technical Note #5176: "The Compact Font Format Specification"
#     https://wwwimages2.adobe.com/content/dam/acom/en/devnet/font/pdfs/5176.CFF.pdf
#   * Adobe Technical Note #5177: "The Type 2 Charstring Format"
#     https://wwwimages2.adobe.com/content/dam/acom/en/devnet/font/pdfs/5177.Type2.pdf
#

import copy
import re
import sys
import xml.etree.ElementTree as ET

FDArray = []
GlobalSubrs = []

# load GlobalSubrs
def load_GlobalSubrs(root):
    for cs in root.findall("./CFF/GlobalSubrs/CharString"):
        GlobalSubrs.append(cs.text)

# load FDArray
def load_FDArray(root):
    for fd in root.findall("./CFF/CFFFont/FDArray/FontDict"):
        FontDict = {}
        for cs in fd.findall("./Private/*"):
            if "value" in cs.attrib:
                FontDict[cs.tag] = cs.attrib["value"]
        Subrs = []
        for cs in fd.findall("./Private/Subrs/CharString"):
            Subrs.append(cs.text)
        FontDict["Subrs"] = Subrs
        FDArray.append(FontDict)

def get_GlobalSubr(index):
    if len(GlobalSubrs) < 1240:
        return GlobalSubrs[index + 107]
    elif len(GlobalSubrs) < 33900:
        return GlobalSubrs[index + 1131]
    else:
        return GlobalSubrs[index + 32768]

def get_LocalSubr(fd, index):
    Subrs = FDArray[fd]["Subrs"]
    if len(Subrs) < 1240:
        return Subrs[index + 107]
    elif len(Subrs) < 33900:
        return Subrs[index + 1131]
    else:
        return Subrs[index + 32768]

re_isInt = re.compile(r"^-?\d+$")
re_isFloat = re.compile(r"^-?\d+(?:\.\d+)?$")

def adjust_CharString(cs, fd, wd, dx, dy, sx, sy):
    defaultWidthX = int(FDArray[fd]["defaultWidthX"])
    nominalWidthX = int(FDArray[fd]["nominalWidthX"])

    stack = []
    result_list = []
    list_stack = []
    curr_list = cs.split()
    is_first = True
    is_first_move = True

    if wd != defaultWidthX:
        result_list.append(str(wd - nominalWidthX))

    while len(curr_list) > 0:
        op = curr_list.pop(0)
        if re_isInt.match(op) is not None:
            stack.append(int(op))
        elif re_isFloat.match(op) is not None:
            stack.append(float(op))
        elif op == "rmoveto" or op == "hmoveto" or op == "vmoveto":
            # |- dx1 dy1 rmoveto (21) |-
            # |- dx1 hmoveto (22) |-
            # |- dy1 vmoveto (4) |-
            dx1 = 0
            dy1 = 0
            if op == "rmoveto":
                if is_first and len(stack) > 2:
                    _ = stack.pop(0) # w
                    is_first = False
                dx1 = stack[0]
                dy1 = stack[1]
            elif op == "hmoveto":
                if is_first and len(stack) > 1:
                    _ = stack.pop(0) # w
                    is_first = False
                dx1 = stack[0]
            elif op == "vmoveto":
                if is_first and len(stack) > 1:
                    _ = stack.pop(0) # w
                    is_first = False
                dy1 = stack[0]
            dx1 *= sx
            dy1 *= sy
            if is_first_move:
                dx1 += dx
                dy1 += dy
                is_first_move = False
            if dx1 != 0 and dy1 != 0:
                result_list.append(str(dx1))
                result_list.append(str(dy1))
                result_list.append("rmoveto")
            elif dy1 == 0:
                result_list.append(str(dx1))
                result_list.append("hmoveto")
            elif dx1 == 0:
                result_list.append(str(dy1))
                result_list.append("vmoveto")
            stack.clear()
        elif op == "rlineto":
            # |- {dxa dya}+ rlineto (5) |-
            for _ in range(len(stack)//2):
                result_list.append(str(stack.pop(0) * sx)) # dxa
                result_list.append(str(stack.pop(0) * sy)) # dya
            result_list.append(op)
            stack.clear()
        elif op == "hlineto":
            # |- dx1 {dya dxb}* hlineto (6) |-
            # |- {dxa dyb}+ hlineto (6) |-
            if len(stack) % 2 == 1:
                result_list.append(str(stack.pop(0) * sx)) # dx1
                for _ in range(len(stack)//2):
                    result_list.append(str(stack.pop(0) * sy)) # dya
                    result_list.append(str(stack.pop(0) * sx)) # dxb
            else:
                for _ in range(len(stack)//2):
                    result_list.append(str(stack.pop(0) * sx)) # dxa
                    result_list.append(str(stack.pop(0) * sy)) # dyb
            result_list.append(op)
            stack.clear()
        elif op == "vlineto":
            # |- dy1 {dxa dyb}* vlineto (7) |-
            # |- {dya dxb}+ vlineto (7) |-
            if len(stack) % 2 == 1:
                result_list.append(str(stack.pop(0) * sy)) # dy1
                for _ in range(len(stack)//2):
                    result_list.append(str(stack.pop(0) * sx)) # dxa
                    result_list.append(str(stack.pop(0) * sy)) # dyb
            else:
                for _ in range(len(stack)//2):
                    result_list.append(str(stack.pop(0) * sy)) # dya
                    result_list.append(str(stack.pop(0) * sx)) # dxb
            result_list.append(op)
            stack.clear()
        elif op == "rrcurveto":
            # |- {dxa dya dxb dyb dxc dyc}+ rrcurveto (8) |-
            for _ in range(len(stack)//6):
                result_list.append(str(stack.pop(0) * sx)) # dxa
                result_list.append(str(stack.pop(0) * sy)) # dya
                result_list.append(str(stack.pop(0) * sx)) # dxb
                result_list.append(str(stack.pop(0) * sy)) # dyb
                result_list.append(str(stack.pop(0) * sx)) # dxc
                result_list.append(str(stack.pop(0) * sy)) # dyc
            result_list.append(op)
            stack.clear()
        elif op == "hhcurveto":
            # |- dy1? {dxa dxb dyb dxc}+ hhcurveto (27) |-
            if len(stack) % 4 >= 1:
                result_list.append(str(stack.pop(0) * sy)) # dy1
            for _ in range(len(stack)//4):
                result_list.append(str(stack.pop(0) * sx)) # dxa
                result_list.append(str(stack.pop(0) * sx)) # dxb
                result_list.append(str(stack.pop(0) * sy)) # dyb
                result_list.append(str(stack.pop(0) * sx)) # dxc
            result_list.append(op)
            stack.clear()
        elif op == "hvcurveto":
            # |- dx1 dx2 dy2 dy3 {dya dxb dyb dxc dxd dxe dye dyf}* dxf? hvcurveto (31) |-
            # |- {dxa dxb dyb dyc dyd dxe dye dxf}+ dyf? hvcurveto (31) |-
            if len(stack) % 8 >= 4:
                result_list.append(str(stack.pop(0) * sx)) # dx1
                result_list.append(str(stack.pop(0) * sx)) # dx2
                result_list.append(str(stack.pop(0) * sy)) # dy2
                result_list.append(str(stack.pop(0) * sy)) # dy3
                for _ in range(len(stack)//8):
                    result_list.append(str(stack.pop(0) * sy)) # dya
                    result_list.append(str(stack.pop(0) * sx)) # dxb
                    result_list.append(str(stack.pop(0) * sy)) # dyb
                    result_list.append(str(stack.pop(0) * sx)) # dxc
                    result_list.append(str(stack.pop(0) * sx)) # dxd
                    result_list.append(str(stack.pop(0) * sx)) # dxe
                    result_list.append(str(stack.pop(0) * sy)) # dye
                    result_list.append(str(stack.pop(0) * sy)) # dyf
                if len(stack) > 0:
                    result_list.append(str(stack.pop(0) * sx)) # dxf
            else:
                for _ in range(len(stack)//8):
                    result_list.append(str(stack.pop(0) * sx)) # dxa
                    result_list.append(str(stack.pop(0) * sx)) # dxb
                    result_list.append(str(stack.pop(0) * sy)) # dyb
                    result_list.append(str(stack.pop(0) * sy)) # dyc
                    result_list.append(str(stack.pop(0) * sy)) # dyd
                    result_list.append(str(stack.pop(0) * sx)) # dxe
                    result_list.append(str(stack.pop(0) * sy)) # dye
                    result_list.append(str(stack.pop(0) * sx)) # dxf
                if len(stack) > 0:
                    result_list.append(str(stack.pop(0) * sy)) # dyf
            result_list.append(op)
            stack.clear()
        elif op == "rcurveline":
            # |- {dxa dya dxb dyb dxc dyc}+ dxd dyd rcurveline (24) |-
            for _ in range((len(stack)-2)//6):
                result_list.append(str(stack.pop(0) * sx)) # dxa
                result_list.append(str(stack.pop(0) * sy)) # dya
                result_list.append(str(stack.pop(0) * sx)) # dxb
                result_list.append(str(stack.pop(0) * sy)) # dyb
                result_list.append(str(stack.pop(0) * sx)) # dxc
                result_list.append(str(stack.pop(0) * sy)) # dyc
            result_list.append(str(stack.pop(0) * sx)) # dxd
            result_list.append(str(stack.pop(0) * sy)) # dyd
            result_list.append(op)
            stack.clear()
        elif op == "rlinecurve":
            # |- {dxa dya}+ dxb dyb dxc dyc dxd dyd rlinecurve (25) |-
            for _ in range((len(stack)-6)//2):
                result_list.append(str(stack.pop(0) * sx)) # dxa
                result_list.append(str(stack.pop(0) * sy)) # dya
            result_list.append(str(stack.pop(0) * sx)) # dxb
            result_list.append(str(stack.pop(0) * sy)) # dyb
            result_list.append(str(stack.pop(0) * sx)) # dxc
            result_list.append(str(stack.pop(0) * sy)) # dyc
            result_list.append(str(stack.pop(0) * sx)) # dxd
            result_list.append(str(stack.pop(0) * sy)) # dyd
            result_list.append(op)
            stack.clear()
        elif op == "vhcurveto":
            # |- dy1 dx2 dy2 dx3 {dxa dxb dyb dyc dyd dxe dye dxf}* dyf? vhcurveto (30) |-
            # |- {dya dxb dyb dxc dxd dxe dye dyf}* dxf? vhcurveto (30) |-
            if len(stack) % 8 >= 4:
                result_list.append(str(stack.pop(0) * sy)) # dy1
                result_list.append(str(stack.pop(0) * sx)) # dx2
                result_list.append(str(stack.pop(0) * sy)) # dy2
                result_list.append(str(stack.pop(0) * sx)) # dx3
                for _ in range(len(stack)//8):
                    result_list.append(str(stack.pop(0) * sx)) # dxa
                    result_list.append(str(stack.pop(0) * sx)) # dxb
                    result_list.append(str(stack.pop(0) * sy)) # dyb
                    result_list.append(str(stack.pop(0) * sy)) # dyc
                    result_list.append(str(stack.pop(0) * sy)) # dyd
                    result_list.append(str(stack.pop(0) * sx)) # dxe
                    result_list.append(str(stack.pop(0) * sy)) # dye
                    result_list.append(str(stack.pop(0) * sx)) # dxf
                if len(stack) > 0:
                    result_list.append(str(stack.pop(0) * sy)) # dyf
            else:
                for _ in range(len(stack)//8):
                    result_list.append(str(stack.pop(0) * sy)) # dya
                    result_list.append(str(stack.pop(0) * sx)) # dxb
                    result_list.append(str(stack.pop(0) * sy)) # dyb
                    result_list.append(str(stack.pop(0) * sx)) # dxc
                    result_list.append(str(stack.pop(0) * sx)) # dxd
                    result_list.append(str(stack.pop(0) * sx)) # dxe
                    result_list.append(str(stack.pop(0) * sy)) # dye
                    result_list.append(str(stack.pop(0) * sy)) # dyf
                if len(stack) > 0:
                    result_list.append(str(stack.pop(0) * sx)) # dxf
            result_list.append(op)
            stack.clear()
        elif op == "vvcurveto":
            # |- dx1? {dya dxb dyb dyc}+ vvcurveto (26) |-
            if len(stack) % 4 >= 1:
                result_list.append(str(stack.pop(0) * sx)) # dx1
            for _ in range(len(stack)//4):
                result_list.append(str(stack.pop(0) * sy)) # dya
                result_list.append(str(stack.pop(0) * sx)) # dxb
                result_list.append(str(stack.pop(0) * sy)) # dyb
                result_list.append(str(stack.pop(0) * sy)) # dyc
            result_list.append(op)
            stack.clear()
        # elif op == "flex":
        #     # |- flex |- 
        elif op == "endchar": # endchar (14) |-
            if is_first and len(stack) > 0:
                _ = stack.pop(0) # w
                is_first = False
            result_list.append(op)
            stack.clear()
            break
        elif op == "hstem" or op == "hstemhm":
            # |- y dy {dya dyb}* hstem (1) |-
            # |- y dy {dya dyb}* hstemhm (18) |-
            if is_first and len(stack) % 2 == 1:
                _ = stack.pop(0) # w
                is_first = False
            result_list.append(str(stack.pop(0) * sy + dy)) # y
            result_list.append(str(stack.pop(0) * sy)) # dy
            for _ in range(len(stack)//2):
                result_list.append(str(stack.pop(0) * sy)) # dya
                result_list.append(str(stack.pop(0) * sy)) # dyb
            result_list.append(op)
            stack.clear()
        elif op == "vstem" or op == "vstemhm":
            # |- x dx {dxa dxb}* vstem (3) |-
            # |- x dx {dxa dxb}* vstem (23) |-
            if is_first and len(stack) % 2 == 1:
                _ = stack.pop(0) # w
                is_first = False
            result_list.append(str(stack.pop(0) * sx + dx)) # x
            result_list.append(str(stack.pop(0) * sx)) # dx
            for _ in range(len(stack)//2):
                result_list.append(str(stack.pop(0) * sx)) # dxa
                result_list.append(str(stack.pop(0) * sx)) # dxb
            result_list.append(op)
            stack.clear()
        elif op == "hintmask" or op == "cntrmask":
            # |- hintmask (19 + mask) |-
            # |- cntrmask (20 + mask) |-
            if len(stack) > 0:
                if is_first and len(stack) % 2 == 1:
                    _ = stack.pop(0) # w
                    is_first = False
                result_list.append(str(stack.pop(0) * sx + dx))
                result_list.append(str(stack.pop(0) * sx))
                for _ in range(len(stack)//2):
                    result_list.append(str(stack.pop(0) * sx))
                    result_list.append(str(stack.pop(0) * sx))
            result_list.append(op)
            result_list.append(curr_list.pop(0))
            stack.clear()
        elif op == "callsubr":
            list_stack.append(curr_list)
            curr_list = get_LocalSubr(fd, stack.pop()).split()
        elif op == "callgsubr":
            list_stack.append(curr_list)
            curr_list = get_GlobalSubr(stack.pop()).split()
        elif op == "return":
            curr_list = list_stack.pop()
        else:
            raise Exception("unknown operator {}".format(op))
    return " ".join(result_list)


def load_adjustTable(file):
    table = {}
    with open(file, "r") as f:
        for line in f:
            if line.startswith("#"):
                continue
            items = line.split()
            name = items[0]
            wd = int(items[1])
            dx = float(items[2]) if len(items) >= 2 else 0
            dy = float(items[3]) if len(items) >= 3 else 0
            sx = float(items[4]) if len(items) >= 4 else 0
            sy = float(items[5]) if len(items) >= 5 else 0
            table[name] = (wd, dx, dy, sx, sy)
    return table

########################################################################

if len(sys.argv) <= 3:
    print("Usage: adjust.py adjust.tbl source.C_F_F_.ttx output.C_F_F_.ttx")
    exit(1)

adjust_filename = sys.argv[1]
source_filename = sys.argv[2]
output_filename = sys.argv[3]

table = load_adjustTable(adjust_filename)

tree = ET.parse(source_filename)
root = tree.getroot()

load_FDArray(root)
load_GlobalSubrs(root)

for cs in root.findall("./CFF/CFFFont/CharStrings/CharString"):
    name = cs.attrib["name"]
    if name in table:
        print("adjust {}".format(name))
        fd = int(cs.attrib["fdSelectIndex"])
        wd, dx, dy, sx, sy = table[name]
        cs.text = adjust_CharString(cs.text, fd, wd, dx, dy, sx, sy)

tree.write(output_filename)
