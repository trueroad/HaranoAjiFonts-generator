#!/usr/bin/env python3
#
# Harano Aji Fonts generator
# https://github.com/trueroad/HaranoAjiFonts-generator
#
# composite.py:
#   composite CFF glyph.
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

def scale_and_shift(cs, fd, sx, sy, dx, dy, last_x, last_y):
    # return (result_list, hstems, vstems, masks, x_last, y_last)

    stack = []
    result_list = []
    list_stack = []
    curr_list = cs.split()
    is_first = True
    is_first_move = True
    hstems = []
    vstems = []
    masks = []
    x_curr = last_x
    y_curr = last_y

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
                dx1 += dx - x_curr
                dy1 += dy - y_curr
                is_first_move = False
            x_curr += dx1
            y_curr += dy1
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
                dxa = stack.pop(0) * sx
                dya = stack.pop(0) * sy
                x_curr += dxa
                y_curr += dya
                result_list.append(str(dxa))
                result_list.append(str(dya))
            result_list.append(op)
            stack.clear()
        elif op == "hlineto":
            # |- dx1 {dya dxb}* hlineto (6) |-
            # |- {dxa dyb}+ hlineto (6) |-
            if len(stack) % 2 == 1:
                dx1 = stack.pop(0) * sx
                x_curr += dx1
                result_list.append(str(dx1))
                for _ in range(len(stack)//2):
                    dya = stack.pop(0) * sy
                    dxb = stack.pop(0) * sx
                    y_curr += dya
                    x_curr += dxb
                    result_list.append(str(dya))
                    result_list.append(str(dxb))
            else:
                for _ in range(len(stack)//2):
                    dxa = stack.pop(0) * sx
                    dyb = stack.pop(0) * sy
                    x_curr += dxa
                    y_curr += dyb
                    result_list.append(str(dxa))
                    result_list.append(str(dyb))
            result_list.append(op)
            stack.clear()
        elif op == "vlineto":
            # |- dy1 {dxa dyb}* vlineto (7) |-
            # |- {dya dxb}+ vlineto (7) |-
            if len(stack) % 2 == 1:
                dy1 = stack.pop(0) * sy
                y_curr += dy1
                result_list.append(str(dy1))
                for _ in range(len(stack)//2):
                    dxa = stack.pop(0) * sx
                    dyb = stack.pop(0) * sy
                    x_curr += dxa
                    y_curr += dyb
                    result_list.append(str(dxa))
                    result_list.append(str(dyb))
            else:
                for _ in range(len(stack)//2):
                    dya = stack.pop(0) * sy
                    dxb = stack.pop(0) * sx
                    y_curr += dya
                    x_curr += dxb
                    result_list.append(str(dya))
                    result_list.append(str(dxb))
            result_list.append(op)
            stack.clear()
        elif op == "rrcurveto":
            # |- {dxa dya dxb dyb dxc dyc}+ rrcurveto (8) |-
            for _ in range(len(stack)//6):
                dxa = stack.pop(0) * sx
                dya = stack.pop(0) * sy
                dxb = stack.pop(0) * sx
                dyb = stack.pop(0) * sy
                dxc = stack.pop(0) * sx
                dyc = stack.pop(0) * sy
                x_curr += dxa
                y_curr += dya
                x_curr += dxb
                y_curr += dyb
                x_curr += dxc
                y_curr += dyc
                result_list.append(str(dxa))
                result_list.append(str(dya))
                result_list.append(str(dxb))
                result_list.append(str(dyb))
                result_list.append(str(dxc))
                result_list.append(str(dyc))
            result_list.append(op)
            stack.clear()
        elif op == "hhcurveto":
            # |- dy1? {dxa dxb dyb dxc}+ hhcurveto (27) |-
            if len(stack) % 4 >= 1:
                dy1 = stack.pop(0) * sy
                y_curr += dy1
                result_list.append(str(dy1))
            for _ in range(len(stack)//4):
                dxa = stack.pop(0) * sx
                dxb = stack.pop(0) * sx
                dyb = stack.pop(0) * sy
                dxc = stack.pop(0) * sx
                x_curr += dxa                
                x_curr += dxb
                y_curr += dyb
                x_curr += dxc
                result_list.append(str(dxa))
                result_list.append(str(dxb))
                result_list.append(str(dyb))
                result_list.append(str(dxc))
            result_list.append(op)
            stack.clear()
        elif op == "hvcurveto":
            # |- dx1 dx2 dy2 dy3 {dya dxb dyb dxc dxd dxe dye dyf}* dxf? hvcurveto (31) |-
            # |- {dxa dxb dyb dyc dyd dxe dye dxf}+ dyf? hvcurveto (31) |-
            if len(stack) % 8 >= 4:
                dx1 = stack.pop(0) * sx
                dx2 = stack.pop(0) * sx
                dy2 = stack.pop(0) * sy
                dy3 = stack.pop(0) * sy
                x_curr += dx1
                x_curr += dx2
                y_curr += dy2
                y_curr += dy3
                result_list.append(str(dx1))
                result_list.append(str(dx2))
                result_list.append(str(dy2))
                result_list.append(str(dy3))
                for _ in range(len(stack)//8):
                    dya = stack.pop(0) * sy
                    dxb = stack.pop(0) * sx
                    dyb = stack.pop(0) * sy
                    dxc = stack.pop(0) * sx
                    dxd = stack.pop(0) * sx
                    dxe = stack.pop(0) * sx
                    dye = stack.pop(0) * sy
                    dyf = stack.pop(0) * sy
                    y_curr += dya
                    x_curr += dxb
                    y_curr += dyb
                    x_curr += dxc
                    x_curr += dxd
                    x_curr += dxe
                    y_curr += dye
                    y_curr += dyf
                    result_list.append(str(dya))
                    result_list.append(str(dxb))
                    result_list.append(str(dyb))
                    result_list.append(str(dxc))
                    result_list.append(str(dxd))
                    result_list.append(str(dxe))
                    result_list.append(str(dye))
                    result_list.append(str(dyf))
                if len(stack) > 0:
                    dxf = stack.pop(0) * sx
                    x_curr += dxf
                    result_list.append(str(dxf))
            else:
                for _ in range(len(stack)//8):
                    dxa = stack.pop(0) * sx
                    dxb = stack.pop(0) * sx
                    dyb = stack.pop(0) * sy
                    dyc = stack.pop(0) * sy
                    dyd = stack.pop(0) * sy
                    dxe = stack.pop(0) * sx
                    dye = stack.pop(0) * sy
                    dxf = stack.pop(0) * sx
                    x_curr += dxa
                    x_curr += dxb
                    y_curr += dyb
                    y_curr += dyc
                    y_curr += dyd
                    x_curr += dxe
                    y_curr += dye
                    x_curr += dxf
                    result_list.append(str(dxa))
                    result_list.append(str(dxb))
                    result_list.append(str(dyb))
                    result_list.append(str(dyc))
                    result_list.append(str(dyd))
                    result_list.append(str(dxe))
                    result_list.append(str(dye))
                    result_list.append(str(dxf))
                if len(stack) > 0:
                    dyf = stack.pop(0) * sy
                    y_curr += dyf
                    result_list.append(str(dyf))
            result_list.append(op)
            stack.clear()
        elif op == "rcurveline":
            # |- {dxa dya dxb dyb dxc dyc}+ dxd dyd rcurveline (24) |-
            for _ in range((len(stack)-2)//6):
                dxa = stack.pop(0) * sx
                dya = stack.pop(0) * sy
                dxb = stack.pop(0) * sx
                dyb = stack.pop(0) * sy
                dxc = stack.pop(0) * sx
                dyc = stack.pop(0) * sy
                x_curr += dxa
                y_curr += dya
                x_curr += dxb
                y_curr += dyb
                x_curr += dxc
                y_curr += dyc
                result_list.append(str(dxa))
                result_list.append(str(dya))
                result_list.append(str(dxb))
                result_list.append(str(dyb))
                result_list.append(str(dxc))
                result_list.append(str(dyc))
            dxd = stack.pop(0) * sx
            dyd = stack.pop(0) * sy
            x_curr += dxd
            y_curr += dyd
            result_list.append(str(dxd))
            result_list.append(str(dyd))
            result_list.append(op)
            stack.clear()
        elif op == "rlinecurve":
            # |- {dxa dya}+ dxb dyb dxc dyc dxd dyd rlinecurve (25) |-
            for _ in range((len(stack)-6)//2):
                dxa = stack.pop(0) * sx
                dya = stack.pop(0) * sy
                x_curr += dxa
                y_curr += dya
                result_list.append(str(dxa))
                result_list.append(str(dya))
            dxb = stack.pop(0) * sx
            dyb = stack.pop(0) * sy
            dxc = stack.pop(0) * sx
            dyc = stack.pop(0) * sy
            dxd = stack.pop(0) * sx
            dyd = stack.pop(0) * sy
            x_curr += dxb
            y_curr += dyb
            x_curr += dxc
            y_curr += dyc
            x_curr += dxd
            y_curr += dyd
            result_list.append(str(dxb))
            result_list.append(str(dyb))
            result_list.append(str(dxc))
            result_list.append(str(dyc))
            result_list.append(str(dxd))
            result_list.append(str(dyd))
            result_list.append(op)
            stack.clear()
        elif op == "vhcurveto":
            # |- dy1 dx2 dy2 dx3 {dxa dxb dyb dyc dyd dxe dye dxf}* dyf? vhcurveto (30) |-
            # |- {dya dxb dyb dxc dxd dxe dye dyf}* dxf? vhcurveto (30) |-
            if len(stack) % 8 >= 4:
                dy1 = stack.pop(0) * sy
                dx2 = stack.pop(0) * sx
                dy2 = stack.pop(0) * sy
                dx3 = stack.pop(0) * sx
                y_curr += dy1
                x_curr += dx2
                y_curr += dy2
                x_curr += dx3
                result_list.append(str(dy1))
                result_list.append(str(dx2))
                result_list.append(str(dy2))
                result_list.append(str(dx3))
                for _ in range(len(stack)//8):
                    dxa = stack.pop(0) * sx
                    dxb = stack.pop(0) * sx
                    dyb = stack.pop(0) * sy
                    dyc = stack.pop(0) * sy
                    dyd = stack.pop(0) * sy
                    dxe = stack.pop(0) * sx
                    dye = stack.pop(0) * sy
                    dxf = stack.pop(0) * sx
                    x_curr += dxa
                    x_curr += dxb
                    y_curr += dyb
                    y_curr += dyc
                    y_curr += dyd
                    x_curr += dxe
                    y_curr += dye
                    x_curr += dxf
                    result_list.append(str(dxa))
                    result_list.append(str(dxb))
                    result_list.append(str(dyb))
                    result_list.append(str(dyc))
                    result_list.append(str(dyd))
                    result_list.append(str(dxe))
                    result_list.append(str(dye))
                    result_list.append(str(dxf))
                if len(stack) > 0:
                    dyf = stack.pop(0) * sy
                    y_curr += dyf
                    result_list.append(str(dyf))
            else:
                for _ in range(len(stack)//8):
                    dya = stack.pop(0) * sy
                    dxb = stack.pop(0) * sx
                    dyb = stack.pop(0) * sy
                    dxc = stack.pop(0) * sx
                    dxd = stack.pop(0) * sx
                    dxe = stack.pop(0) * sx
                    dye = stack.pop(0) * sy
                    dyf = stack.pop(0) * sy
                    y_curr += dya
                    x_curr += dxb
                    y_curr += dyb
                    x_curr += dxc
                    x_curr += dxd
                    x_curr += dxe
                    y_curr += dye
                    y_curr += dyf
                    result_list.append(str(dya))
                    result_list.append(str(dxb))
                    result_list.append(str(dyb))
                    result_list.append(str(dxc))
                    result_list.append(str(dxd))
                    result_list.append(str(dxe))
                    result_list.append(str(dye))
                    result_list.append(str(dyf))
                if len(stack) > 0:
                    dxf = stack.pop(0) * sx
                    x_curr += dxf
                    result_list.append(str(dxf))
            result_list.append(op)
            stack.clear()
        elif op == "vvcurveto":
            # |- dx1? {dya dxb dyb dyc}+ vvcurveto (26) |-
            if len(stack) % 4 >= 1:
                dx1 = stack.pop(0) * sx
                x_curr += dx1
                result_list.append(str(dx1))
            for _ in range(len(stack)//4):
                dya = stack.pop(0) * sy
                dxb = stack.pop(0) * sx
                dyb = stack.pop(0) * sy
                dyc = stack.pop(0) * sy
                y_curr += dya
                x_curr += dxb
                y_curr += dyb
                y_curr += dyc
                result_list.append(str(dya))
                result_list.append(str(dxb))
                result_list.append(str(dyb))
                result_list.append(str(dyc))
            result_list.append(op)
            stack.clear()
        # elif op == "flex":
        #     # |- flex |- 
        elif op == "endchar": # endchar (14) |-
            if is_first and len(stack) > 0:
                _ = stack.pop(0) # w
                is_first = False
            stack.clear()
            break
        elif op == "hstem" or op == "hstemhm":
            # |- y dy {dya dyb}* hstem (1) |-
            # |- y dy {dya dyb}* hstemhm (18) |-
            if is_first and len(stack) % 2 == 1:
                _ = stack.pop(0) # w
                is_first = False
            y = stack.pop(0) * sy + dy
            dy1 = stack.pop(0)
            if dy1 >= 0: dy1 *= sy
            hstems.append((y, dy1))
            if dy1 >= 0: y += dy1
            for _ in range(len(stack)//2):
                dya = stack.pop(0) * sy
                dyb = stack.pop(0)
                y += dya
                if dyb >= 0: dyb *= sy
                hstems.append((y, dyb))
                if dyb >= 0: y += dyb
            stack.clear()
        elif op == "vstem" or op == "vstemhm":
            # |- x dx {dxa dxb}* vstem (3) |-
            # |- x dx {dxa dxb}* vstem (23) |-
            if is_first and len(stack) % 2 == 1:
                _ = stack.pop(0) # w
                is_first = False
            x = stack.pop(0) * sx + dx
            dx1 = stack.pop(0)
            if dx1 >= 0: dx1 *= sx
            vstems.append((x, dx1))
            if dx1 >= 0: x += dx1
            for _ in range(len(stack)//2):
                dxa = stack.pop(0) * sx
                dxb = stack.pop(0)
                x += dxa
                if dxb >= 0: dxb *= sx
                vstems.append((x, dxb))
                if dxb >= 0: x += dxb
            stack.clear()
        elif op == "hintmask" or op == "cntrmask":
            # |- hintmask (19 + mask) |-
            # |- cntrmask (20 + mask) |-
            if len(stack) > 0:
                # If hstem and vstem hints are both declared at the beginning of
                # a charstring, and this sequence is followed directly by the
                # hintmask or cntrmask operators, the vstem hint operator need
                # not be included. 
                if is_first and len(stack) % 2 == 1:
                    _ = stack.pop(0) # w
                    is_first = False
                x = stack.pop(0) * sx + dx
                dx1 = stack.pop(0)
                if dx1 >= 0: dx1 *= sx
                vstems.append((x, dx1))
                if dx1 >= 0: x += dx1
                for _ in range(len(stack)//2):
                    dxa = stack.pop(0) * sx
                    dxb = stack.pop(0)
                    x += dxa
                    if dxb >= 0: dxb *= sx
                    vstems.append((x, dxb))
                    if dxb >= 0: x += dxb
            masks.append(len(result_list))
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

    return (result_list, hstems, vstems, masks, x_curr, y_curr)

def composite(root, fd, wd, src_list):
    defaultWidthX = int(FDArray[fd]["defaultWidthX"])
    nominalWidthX = int(FDArray[fd]["nominalWidthX"])

    composite_list = []
    last_x = 0
    last_y = 0

    # scale and shift each glyph
    for name, sx, sy, dx, dy in src_list:
        print("  + glyph {} scale {} {} shift {} {}".format(name, sx, sy, dx, dy))
        cs = root.find("./CFF/CFFFont/CharStrings/CharString[@name='{}']".format(name))
        fd = int(cs.attrib["fdSelectIndex"])
        cs, hstem_list, vstem_list, mask_list, last_x, last_y = scale_and_shift(cs.text, fd, sx, sy, dx, dy, last_x, last_y)
        composite_list.append((cs, hstem_list, vstem_list, mask_list))

    result_list = []

    if wd != defaultWidthX:
        result_list.append(str(wd - nominalWidthX))

    # merge hstems

    total_hstems = []
    for _,hstem_list,_,_ in composite_list:
        for y, dy in hstem_list:
            total_hstems.append((y, dy, len(total_hstems)))
    # reorder
    total_hstems.sort()
    last_y = 0
    for y, dy, _ in total_hstems:
        result_list.append(str(y - last_y))
        result_list.append(str(dy))
        last_y = y
        if dy >= 0: last_y += dy
    if len(total_hstems) > 0:
        result_list.append("hstemhm")

    # merge vstems

    total_vstems = []
    for _,_,vstem_list,_ in composite_list:
        for x, dx in vstem_list:
            total_vstems.append((x, dx, len(total_vstems)))
    # reorder
    total_vstems.sort()
    last_x = 0
    for x, dx, _ in total_vstems:
        result_list.append(str(x - last_x))
        result_list.append(str(dx))
        last_x = x
        if dx >= 0: last_x += dx
    if len(total_vstems) > 0:
        result_list.append("vstemhm")

    total_stems = len(total_hstems) + len(total_vstems)
    stem_padding = (total_stems + 7) // 8 * 8 - total_stems

    # merge 

    last_hstems = 0
    last_vstems = 0
    for cs,hstem_list,vstem_list,mask_list in composite_list:
        hstems = len(hstem_list)
        vstems = len(vstem_list)

        # enable only next glyph stem hints.
        mask = ""
        for _,_,h in total_hstems:
            if h >= last_hstems and h < last_hstems + hstems:
                mask += "1"
            else:
                mask += "0"
        for _,_,h in total_vstems:
            if h >= last_vstems and h < last_vstems + vstems:
                mask += "1"
            else:
                mask += "0"
        mask += "0"*stem_padding
        result_list.append("hintmask")
        result_list.append(mask)

        # rewrite mask
        for m in mask_list:
            src_mask = cs[m+1]

            mask = ""
            for _,_,h in total_hstems:
                if h >= last_hstems and h < last_hstems + hstems:
                    mask += src_mask[h-last_hstems]
                else:
                    mask += "0"
            for _,_,h in total_vstems:
                if h >= last_vstems and h < last_vstems + vstems:
                    mask += src_mask[h-last_vstems+hstems]
                else:
                    mask += "0"
            mask += "0"*stem_padding
            if cs[m] == "cntrmask":
                # cntrmask not suported. delete it.
                cs[m] = ""
                cs[m+1] = ""
            else:
                cs[m+1] = mask

        result_list.extend(cs)

        last_hstems += hstems
        last_vstems += vstems

    result_list.append("endchar")

    return " ".join(result_list)

def load_composite_table(file):
    table = {}
    dst_name = None
    with open(file, "r") as f:
        for line in f:
            if line.startswith("#"):
                continue
            items = line.split()
            if items[0] == "+" and dst_name is not None:
                scr_name = items[1]
                sx = float(items[2])
                sy = float(items[3])
                dx = float(items[4])
                dy = float(items[5])
                table[dst_name][1].append((scr_name, sx, sy, dx, dy))
            else:
                dst_name = items[0]
                dst_wd = int(items[1])
                table[dst_name] = (dst_wd, [])
    return table

########################################################################

if len(sys.argv) <= 3:
    print("Usage: composite.py composite.tbl source.C_F_F_.ttx output.C_F_F_.ttx")
    exit(1)

composite_filename = sys.argv[1]
source_filename = sys.argv[2]
output_filename = sys.argv[3]

table = load_composite_table(composite_filename)

tree = ET.parse(source_filename)
root = tree.getroot()

load_FDArray(root)
load_GlobalSubrs(root)

for cs in root.findall("./CFF/CFFFont/CharStrings/CharString"):
    name = cs.attrib["name"]
    if name in table:
        print("composite {}".format(name))
        fd = int(cs.attrib["fdSelectIndex"])
        wd, src_list = table[name]
        cs.text = composite(root, fd, wd, src_list)

tree.write(output_filename)
