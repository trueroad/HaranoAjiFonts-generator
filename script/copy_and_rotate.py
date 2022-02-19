#!/usr/bin/env python3
#
# Harano Aji Fonts generator
# https://github.com/trueroad/HaranoAjiFonts-generator
#
# copy_and_rotate.py:
#   copy and rotate the CFF glyph.
#
# Copyright (C) 2020 Yukimasa Morimi.
# Copyright (C) 2020, 2022 Masamichi Hosoda.
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

def copy_and_rotate_CharString(cs, fd, angle):
    if angle == 0:
        return cs
    elif angle == 90:
        return copy_and_rotate_CharString90(cs, fd)
    elif angle == 180 or angle == -180:
        return copy_and_rotate_CharString90(
            copy_and_rotate_CharString90(cs, fd), fd)
    elif angle == 270 or angle == -90:
        return copy_and_rotate_CharString90(
            copy_and_rotate_CharString90(
                copy_and_rotate_CharString90(cs, fd), fd), fd)

    print ("angle {} is not supported.".format(angle));
    return cs

def copy_and_rotate_CharString90(cs, fd):
    # x_{rotated} =  y_{original} - decender
    # y_{rotated} = -x_{original} + acender
    wd = 1000 # acender - decender
    dx = 120  # -decender
    dy = 880  # acender
    sx = 1    # x_{rotated} = y_{original} * sx + dx
    sy = -1   # y_{rotated} = x_{original} * sy + dy

    defaultWidthX = int(FDArray[fd]["defaultWidthX"])
    nominalWidthX = int(FDArray[fd]["nominalWidthX"])

    stack = []
    result_list = []
    list_stack = []
    curr_list = cs.split()
    is_first = True
    is_first_move = True

    hstems = 0
    vstems = 0
    vstem_list = []

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
            dx1, dy1 = dy1, dx1
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
                x = stack.pop(0) # dxa
                y = stack.pop(0) # dya
                x, y = y, x
                result_list.append(str(x * sx)) # dxa
                result_list.append(str(y * sy)) # dya
            result_list.append(op)
            stack.clear()
        elif op == "hlineto":
            # |- dx1 {dya dxb}* hlineto (6) |-
            # |- {dxa dyb}+ hlineto (6) |-
            if len(stack) % 2 == 1:
                result_list.append(str(stack.pop(0) * sy)) # dy1 <- dx1
                for _ in range(len(stack)//2):
                    y = stack.pop(0) # dya
                    x = stack.pop(0) # dxb
                    x, y = y, x
                    result_list.append(str(x * sx)) # dxa
                    result_list.append(str(y * sy)) # dyb
            else:
                for _ in range(len(stack)//2):
                    x = stack.pop(0) # dxa
                    y = stack.pop(0) # dyb
                    x, y = y, x
                    result_list.append(str(y * sy)) # dya
                    result_list.append(str(x * sx)) # dxb
            result_list.append("vlineto")
            stack.clear()
        elif op == "vlineto":
            # |- dy1 {dxa dyb}* vlineto (7) |-
            # |- {dya dxb}+ vlineto (7) |-
            if len(stack) % 2 == 1:
                result_list.append(str(stack.pop(0) * sx)) # dx1 <- dy1
                for _ in range(len(stack)//2):
                    x = stack.pop(0) # dxa
                    y = stack.pop(0) # dyb
                    x, y = y, x
                    result_list.append(str(y * sy)) # dya
                    result_list.append(str(x * sx)) # dxb
            else:
                for _ in range(len(stack)//2):
                    y = stack.pop(0) # dya
                    x = stack.pop(0) # dxb
                    x, y = y, x
                    result_list.append(str(x * sx)) # dxa
                    result_list.append(str(y * sy)) # dyb
            result_list.append("hlineto")
            stack.clear()
        elif op == "rrcurveto":
            # |- {dxa dya dxb dyb dxc dyc}+ rrcurveto (8) |-
            for _ in range(len(stack)//6):
                x = stack.pop(0) # dxa
                y = stack.pop(0) # dya
                x, y = y, x
                result_list.append(str(x * sx)) # dxa
                result_list.append(str(y * sy)) # dya
                x = stack.pop(0) # dxb
                y = stack.pop(0) # dyb
                x, y = y, x
                result_list.append(str(x * sx)) # dxb
                result_list.append(str(y * sy)) # dyb
                x = stack.pop(0) # dxc
                y = stack.pop(0) # dyc
                x, y = y, x
                result_list.append(str(x * sx)) # dxc
                result_list.append(str(y * sy)) # dyc
            result_list.append(op)
            stack.clear()
        elif op == "hhcurveto":
            # |- dy1? {dxa dxb dyb dxc}+ hhcurveto (27) |-
            if len(stack) % 4 >= 1:
                result_list.append(str(stack.pop(0) * sx)) # dx1 <- dy1
            for _ in range(len(stack)//4):
                result_list.append(str(stack.pop(0) * sy)) # dya <- dxa
                x = stack.pop(0) # dxb
                y = stack.pop(0) # dyb
                x, y = y, x
                result_list.append(str(x * sx)) # dxb
                result_list.append(str(y * sy)) # dyb
                result_list.append(str(stack.pop(0) * sy)) # dyc <- dxc
            result_list.append("vvcurveto")
            stack.clear()
        elif op == "hvcurveto":
            # |- dx1 dx2 dy2 dy3 {dya dxb dyb dxc dxd dxe dye dyf}* dxf? hvcurveto (31) |-
            # |- {dxa dxb dyb dyc dyd dxe dye dxf}+ dyf? hvcurveto (31) |-
            if len(stack) % 8 >= 4:
                result_list.append(str(stack.pop(0) * sy)) # dy1 <- dx1
                x = stack.pop(0) # dx2
                y = stack.pop(0) # dy2
                x, y = y, x
                result_list.append(str(x * sx)) # dx2
                result_list.append(str(y * sy)) # dy2
                result_list.append(str(stack.pop(0) * sx)) # dx3 <- dy3
                for _ in range(len(stack)//8):
                    result_list.append(str(stack.pop(0) * sx)) # dxa <- dya
                    x = stack.pop(0) # dxb
                    y = stack.pop(0) # dyb
                    x, y = y, x
                    result_list.append(str(x * sx)) # dxb
                    result_list.append(str(y * sy)) # dyb
                    result_list.append(str(stack.pop(0) * sy)) # dyc <- dxc
                    result_list.append(str(stack.pop(0) * sy)) # dyd <- dxd
                    x = stack.pop(0) # dxe
                    y = stack.pop(0) # dye
                    x, y = y, x
                    result_list.append(str(x * sx)) # dxe
                    result_list.append(str(y * sy)) # dye
                    result_list.append(str(stack.pop(0) * sx)) # dxf <- dyf
                if len(stack) > 0:
                    result_list.append(str(stack.pop(0) * sy)) # dyf <- dxf
            else:
                for _ in range(len(stack)//8):
                    result_list.append(str(stack.pop(0) * sy)) # dya <- dxa
                    x = stack.pop(0) # dxb
                    y = stack.pop(0) # dyb
                    x, y = y, x
                    result_list.append(str(x * sx)) # dxb
                    result_list.append(str(y * sy)) # dyb
                    result_list.append(str(stack.pop(0) * sx)) # dxc <- dyc
                    result_list.append(str(stack.pop(0) * sx)) # dxd <- dyd
                    x = stack.pop(0) # dxe
                    y = stack.pop(0) # dye
                    x, y = y, x
                    result_list.append(str(x * sx)) # dxe
                    result_list.append(str(y * sy)) # dye
                    result_list.append(str(stack.pop(0) * sy)) # dyf <- dxf
                if len(stack) > 0:
                    result_list.append(str(stack.pop(0) * sx)) # dxf <- dyf
            result_list.append("vhcurveto")
            stack.clear()
        elif op == "rcurveline":
            # |- {dxa dya dxb dyb dxc dyc}+ dxd dyd rcurveline (24) |-
            for _ in range((len(stack)-2)//6):
                x = stack.pop(0) # dxa
                y = stack.pop(0) # dya
                x, y = y, x
                result_list.append(str(x * sx)) # dxa
                result_list.append(str(y * sy)) # dya
                x = stack.pop(0) # dxb
                y = stack.pop(0) # dyb
                x, y = y, x
                result_list.append(str(x * sx)) # dxb
                result_list.append(str(y * sy)) # dyb
                x = stack.pop(0) # dxc
                y = stack.pop(0) # dyc
                x, y = y, x
                result_list.append(str(x * sx)) # dxc
                result_list.append(str(y * sy)) # dyc
            x = stack.pop(0) # dxd
            y = stack.pop(0) # dyd
            x, y = y, x
            result_list.append(str(x * sx)) # dxd
            result_list.append(str(y * sy)) # dyd
            result_list.append(op)
            stack.clear()
        elif op == "rlinecurve":
            # |- {dxa dya}+ dxb dyb dxc dyc dxd dyd rlinecurve (25) |-
            for _ in range((len(stack)-6)//2):
                x = stack.pop(0) # dxa
                y = stack.pop(0) # dya
                x, y = y, x
                result_list.append(str(x * sx)) # dxa
                result_list.append(str(y * sy)) # dya
            x = stack.pop(0) # dxb
            y = stack.pop(0) # dyb
            x, y = y, x
            result_list.append(str(x * sx)) # dxb
            result_list.append(str(y * sy)) # dyb
            x = stack.pop(0) # dxc
            y = stack.pop(0) # dyc
            x, y = y, x
            result_list.append(str(x * sx)) # dxc
            result_list.append(str(y * sy)) # dyc
            x = stack.pop(0) # dxd
            y = stack.pop(0) # dyd
            x, y = y, x
            result_list.append(str(x * sx)) # dxd
            result_list.append(str(y * sy)) # dyd
            result_list.append(op)
            stack.clear()
        elif op == "vhcurveto":
            # |- dy1 dx2 dy2 dx3 {dxa dxb dyb dyc dyd dxe dye dxf}* dyf? vhcurveto (30) |-
            # |- {dya dxb dyb dxc dxd dxe dye dyf}* dxf? vhcurveto (30) |-
            if len(stack) % 8 >= 4:
                result_list.append(str(stack.pop(0) * sx)) # dx1 <- dy1
                x = stack.pop(0) # dx2
                y = stack.pop(0) # dy2
                x, y = y, x
                result_list.append(str(x * sx)) # dx2
                result_list.append(str(y * sy)) # dy2
                result_list.append(str(stack.pop(0) * sy)) # dy3 <- dx3
                for _ in range(len(stack)//8):
                    result_list.append(str(stack.pop(0) * sy)) # dya <- dxa
                    x = stack.pop(0) # dxb
                    y = stack.pop(0) # dyb
                    x, y = y, x
                    result_list.append(str(x * sx)) # dxb
                    result_list.append(str(y * sy)) # dyb
                    result_list.append(str(stack.pop(0) * sx)) # dxc <- dyc
                    result_list.append(str(stack.pop(0) * sx)) # dxd <- dyd
                    x = stack.pop(0) # dxe
                    y = stack.pop(0) # dye
                    x, y = y, x
                    result_list.append(str(x * sx)) # dxe
                    result_list.append(str(y * sy)) # dye
                    result_list.append(str(stack.pop(0) * sy)) # dyf <- dxf
                if len(stack) > 0:
                    result_list.append(str(stack.pop(0) * sx)) # dxf <- dyf
            else:
                for _ in range(len(stack)//8):
                    result_list.append(str(stack.pop(0) * sx)) # dxa <- dya
                    x = stack.pop(0) # dxb
                    y = stack.pop(0) # dyb
                    x, y = y, x
                    result_list.append(str(x * sx)) # dxb
                    result_list.append(str(y * sy)) # dyb
                    result_list.append(str(stack.pop(0) * sy)) # dyc <- dxc
                    result_list.append(str(stack.pop(0) * sy)) # dyd <- dxd
                    x = stack.pop(0) # dxe
                    y = stack.pop(0) # dye
                    x, y = y, x
                    result_list.append(str(x * sx)) # dxe
                    result_list.append(str(y * sy)) # dye
                    result_list.append(str(stack.pop(0) * sx)) # dxf <- dyf
                if len(stack) > 0:
                    result_list.append(str(stack.pop(0) * sy)) # dyf <- dxf
            result_list.append("hvcurveto")
            stack.clear()
        elif op == "vvcurveto":
            # |- dx1? {dya dxb dyb dyc}+ vvcurveto (26) |-
            if len(stack) % 4 >= 1:
                result_list.append(str(stack.pop(0) * sy)) # dy1 <- dx1
            for _ in range(len(stack)//4):
                result_list.append(str(stack.pop(0) * sx)) # dxa <- dya
                x = stack.pop(0) # dxb
                y = stack.pop(0) # dyb
                x, y = y, x
                result_list.append(str(x * sx)) # dxb
                result_list.append(str(y * sy)) # dyb
                result_list.append(str(stack.pop(0) * sx)) # dxc <- dyc
            result_list.append("hhcurveto")
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
            vstems = len(stack)//2
            vstem_list.append(str(stack.pop(0) * sx + dx)) # x <- y
            vstem_list.append(str(stack.pop(0) * sx)) # dx <- dy
            for _ in range(len(stack)//2):
                vstem_list.append(str(stack.pop(0) * sx)) # dxa <- dya
                vstem_list.append(str(stack.pop(0) * sx)) # dya <- dyb
            if op == "hstem":
                vstem_list.append("vstem")
            elif op == "hstemhm":
                vstem_list.append("vstemhm")
            stack.clear()
        elif op == "vstem" or op == "vstemhm":
            # |- x dx {dxa dxb}* vstem (3) |-
            # |- x dx {dxa dxb}* vstem (23) |-
            if is_first and len(stack) % 2 == 1:
                _ = stack.pop(0) # w
                is_first = False
            hstems = len(stack)//2
            rev_y = []
            y_before = stack.pop(0) * sy + dy # y <- x
            rev_y.append(y_before)
            y = stack.pop(0) # dx
            y *= sy # dy <- dx
            rev_y.append(y_before + y)
            y_before += y
            for _ in range(len(stack)//2):
                y = stack.pop(0) * sy # dya, <- dxa
                rev_y.append(y_before + y)
                y_before += y
                y = stack.pop(0) # dxb
                if y < 0:
                    print("warning: cannot handle negative stem")
                y *= sy # dyb <- dxb
                rev_y.append(y_before + y)
                y_before += y
            y_before = 0
            for _ in range(len(rev_y)//2):
                y1 = rev_y.pop()
                y2 = rev_y.pop()
                y_diff = y2 - y1
                if y_diff < 0:
                    y1, y2 = y2, y1
                    y2 -= y_diff * 2
                    print ("debug: negative stem");
                result_list.append(str(y1 - y_before))
                result_list.append(str(y2 - y1))
                y_before = y2
            if op == "vstem":
                result_list.append("hstem")
            elif op == "vstemhm":
                result_list.append("hstemhm")
            if len(vstem_list) > 0:
                result_list.extend (vstem_list)
                vstem_list.clear()
            stack.clear()
        elif op == "hintmask" or op == "cntrmask":
            # |- hintmask (19 + mask) |-
            # |- cntrmask (20 + mask) |-
            if len(stack) > 0:
                if is_first and len(stack) % 2 == 1:
                    _ = stack.pop(0) # w
                    is_first = False
                hstems = len(stack)//2
                rev_y = []
                y_before = stack.pop(0) * sy + dy # y <- x
                rev_y.append(y_before)
                y = stack.pop(0) # dx
                y *= sy # dy <- dx
                rev_y.append(y_before + y)
                y_before += y
                for _ in range(len(stack)//2):
                    y = stack.pop(0) * sy # dya <- dxa
                    rev_y.append(y_before + y)
                    y_before += y
                    y = stack.pop(0) # dxb
                    if y < 0:
                        print("warning: cannot handle negative stem")
                    y *= sy # dyb <- dxb
                    rev_y.append(y_before + y)
                    y_before += y
                y_before = 0
                for _ in range(len(rev_y)//2):
                    y1 = rev_y.pop()
                    y2 = rev_y.pop()
                    y_diff = y2 - y1
                    if y_diff < 0:
                        y1, y2 = y2, y1
                        y2 -= y_diff * 2
                        print ("debug: negative stem");
                    result_list.append(str(y1 - y_before))
                    result_list.append(str(y2 - y1))
                    y_before = y2
                result_list.append("hstemhm")
            if len(vstem_list) > 0:
                result_list.extend (vstem_list)
                vstem_list.clear()
            result_list.append(op)
            mask = curr_list.pop(0)
            print("debug: vstems {}, hstems {}".format(vstems, hstems))
            vmask = mask[0:vstems]
            hmask = mask[vstems:vstems+hstems]
            remain = mask[vstems+hstems:]
            print("debug: mask {},{},{} -> {},{},{}".\
                  format(vmask, hmask, remain, hmask, vmask, remain))
            result_list.append(hmask + vmask + remain)
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


def load_copy_and_rotateTable(file):
    table = {}
    with open(file, "r") as f:
        for line in f:
            if line.startswith("#"):
                continue
            items = line.split()
            name_src = items[0]
            name_dst = items[1]
            angle = int(items[2])
            table[name_dst] = (name_src, angle)
    return table

########################################################################

if len(sys.argv) <= 3:
    print("Usage: copy_and_rotate.py copy_and_rotate.tbl "\
          "source.C_F_F_.ttx output.C_F_F_.ttx")
    exit(1)

copy_and_rotate_filename = sys.argv[1]
source_filename = sys.argv[2]
output_filename = sys.argv[3]

table = load_copy_and_rotateTable(copy_and_rotate_filename)

tree = ET.parse(source_filename)
root = tree.getroot()

load_FDArray(root)
load_GlobalSubrs(root)

for cs_dst in root.findall("./CFF/CFFFont/CharStrings/CharString"):
    name_dst = cs_dst.attrib["name"]
    if name_dst in table:
        name_src, angle = table[name_dst]
        print("copy and rotate {} to {} angle {}".\
              format(name_src, name_dst, angle))
        cs_src = root.find("./CFF/CFFFont/CharStrings/CharString"\
                           "[@name='{}']".format(name_src))
        cs_dst.attrib["fdSelectIndex"] = cs_src.attrib["fdSelectIndex"]
        fd = int(cs_dst.attrib["fdSelectIndex"])
        cs_dst.text = copy_and_rotate_CharString(cs_src.text, fd, angle)

tree.write(output_filename)
