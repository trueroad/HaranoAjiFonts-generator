#!/usr/bin/env python3
#
# Harano Aji Fonts generator
# https://github.com/trueroad/HaranoAjiFonts-generator
#
# calc_letter_face.py:
#   calc letter face of the CFF glyph.
#
# Copyright (C) 2020 Yukimasa Morimi.
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

debug_mode = False

if debug_mode:
    import tkinter

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

# for debug
window = 0
canvas = 0
debug_before = False
debug_before_x = 0
debug_before_y = 0
debug_first = False
debug_first_x = 0
debug_first_y = 0

def debug_print(msg):
    if debug_mode:
        print("# " + msg)

def draw_box():
    if not debug_mode:
        return

    r = 3
    xs = 0.5
    ys = -0.5
    xa = 60
    ya = 500

    canvas.create_rectangle(0 * xs + xa, 880 * ys + ya,
                            1000 * xs + xa, -120 * ys + ya,
                            outline='white')
    canvas.create_line(0 * xs + xa, 0 * ys + ya,
                       1000 * xs + xa, 0 * ys + ya,
                       fill='white')

def draw_letter_face(x_min, y_min, x_max, y_max):
    if not debug_mode:
        return

    r = 3
    xs = 0.5
    ys = -0.5
    xa = 60
    ya = 500

    canvas.create_rectangle(x_min * xs + xa, y_min * ys + ya,
                            x_max * xs + xa, y_max * ys + ya,
                            outline='green', dash=(2, 2))

def point_end():
    if not debug_mode:
        return

    global debug_before
    global debug_before_x
    global debug_before_y
    global debug_first
    global debug_first_x
    global debug_first_y
    global debug_first

    r = 3
    xs = 0.5
    ys = -0.5
    xa = 60
    ya = 500

    if debug_first:
        canvas.create_line(debug_before_x * xs + xa,
                           debug_before_y * ys + ya,
                           debug_first_x * xs + xa,
                           debug_first_y * ys + ya)

    debug_before = False
    debug_before_x = 0
    debug_before_y = 0
    debug_first = False
    debug_first_x = 0
    debug_first_y = 0

def point_path(x, y):
    if not debug_mode:
        return

    global debug_before
    global debug_before_x
    global debug_before_y
    global debug_first
    global debug_first_x
    global debug_first_y

    r = 3
    xs = 0.5
    ys = -0.5
    xa = 60
    ya = 500

    canvas.create_oval(x * xs + xa - r, y * ys + ya - r,
                       x * xs + xa + r, y * ys + ya + r,
                       fill='red')
    if debug_before:
        canvas.create_line(debug_before_x * xs + xa,
                           debug_before_y * ys + ya,
                           x * xs + xa, y * ys + ya)

    if debug_first_x == x and debug_first_y == y:
        debug_before = False
        debug_first = False
    else:
        debug_before_x = x
        debug_before_y = y
        debug_before = True

    debug_print("path ({}, {})".format(x, y))

def point_move(x, y):
    if not debug_mode:
        return

    global debug_first
    global debug_first_x
    global debug_first_y

    point_end()
    point_path(x, y)

    debug_first = True
    debug_first_x = x
    debug_first_y = y

def point_ctrl(x, y):
    if not debug_mode:
        return

    global debug_before_x
    global debug_before_y

    r = 3
    xs = 0.5
    ys = -0.5
    xa = 60
    ya = 500

    canvas.create_oval(x * xs + xa - r, y * ys + ya - r,
                       x * xs + xa + r, y * ys + ya + r)
    if debug_before:
        canvas.create_line(debug_before_x * xs + xa,
                           debug_before_y * ys + ya,
                           x * xs + xa, y * ys + ya)
    debug_before_x = x
    debug_before_y = y
    debug_print("ctrl ({}, {})".format(x, y))

re_isInt = re.compile(r"^-?\d+$")
re_isFloat = re.compile(r"^-?\d+(?:\.\d+)?$")

def calc_CharString(cs, fd):
    stack = []
    list_stack = []
    curr_list = cs.split()
    is_first = True
    is_first_move = True

    x_abs = 0
    y_abs = 0
    x_min = 0
    y_min = 0
    x_max = 0
    y_max = 0

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
            debug_print(op)
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
            x_abs += dx1
            y_abs += dy1
            point_move(x_abs, y_abs)
            if is_first_move:
                x_min = x_abs
                x_max = x_abs
                y_min = y_abs
                y_max = y_abs
                is_first_move = False
            else:
                x_min = min(x_abs, x_min)
                x_max = max(x_abs, x_max)
                y_min = min(y_abs, y_min)
                y_max = max(y_abs, y_max)
            stack.clear()
        elif op == "rlineto":
            # |- {dxa dya}+ rlineto (5) |-
            for _ in range(len(stack)//2):
                x_abs += stack.pop(0) # dxa
                y_abs += stack.pop(0) # dya
                point_path(x_abs, y_abs)
                x_min = min(x_abs, x_min)
                x_max = max(x_abs, x_max)
                y_min = min(y_abs, y_min)
                y_max = max(y_abs, y_max)
            stack.clear()
        elif op == "hlineto":
            # |- dx1 {dya dxb}* hlineto (6) |-
            # |- {dxa dyb}+ hlineto (6) |-
            debug_print(op)
            if len(stack) % 2 == 1:
                x_abs += stack.pop(0) # dx1
                point_path(x_abs, y_abs)
                x_min = min(x_abs, x_min)
                x_max = max(x_abs, x_max)
                for _ in range(len(stack)//2):
                    y_abs += stack.pop(0) # dya
                    point_path(x_abs, y_abs)
                    y_min = min(y_abs, y_min)
                    y_max = max(y_abs, y_max)
                    x_abs += stack.pop(0) # dxb
                    point_path(x_abs, y_abs)
                    x_min = min(x_abs, x_min)
                    x_max = max(x_abs, x_max)
            else:
                for _ in range(len(stack)//2):
                    x_abs += stack.pop(0) # dxa
                    point_path(x_abs, y_abs)
                    x_min = min(x_abs, x_min)
                    x_max = max(x_abs, x_max)
                    y_abs += stack.pop(0) # dyb
                    point_path(x_abs, y_abs)
                    y_min = min(y_abs, y_min)
                    y_max = max(y_abs, y_max)
            stack.clear()
        elif op == "vlineto":
            # |- dy1 {dxa dyb}* vlineto (7) |-
            # |- {dya dxb}+ vlineto (7) |-
            debug_print(op)
            if len(stack) % 2 == 1:
                y_abs += stack.pop(0) # dy1
                point_path(x_abs, y_abs)
                y_min = min(y_abs, y_min)
                y_max = max(y_abs, y_max)
                for _ in range(len(stack)//2):
                    x_abs += stack.pop(0) # dxa
                    point_path(x_abs, y_abs)
                    x_min = min(x_abs, x_min)
                    x_max = max(x_abs, x_max)
                    y_abs += stack.pop(0) # dyb
                    point_path(x_abs, y_abs)
                    y_min = min(y_abs, y_min)
                    y_max = max(y_abs, y_max)
            else:
                for _ in range(len(stack)//2):
                    y_abs += stack.pop(0) # dya
                    point_path(x_abs, y_abs)
                    y_min = min(y_abs, y_min)
                    y_max = max(y_abs, y_max)
                    x_abs += stack.pop(0) # dxb
                    point_path(x_abs, y_abs)
                    x_min = min(x_abs, x_min)
                    x_max = max(x_abs, x_max)
            stack.clear()
        elif op == "rrcurveto":
            # |- {dxa dya dxb dyb dxc dyc}+ rrcurveto (8) |-
            debug_print(op)
            for _ in range(len(stack)//6):
                x0 = x_abs
                y0 = y_abs
                x_abs += stack.pop(0) # dxa
                y_abs += stack.pop(0) # dya
                x1 = x_abs
                y1 = y_abs
                x_abs += stack.pop(0) # dxb
                y_abs += stack.pop(0) # dyb
                x2 = x_abs
                y2 = y_abs
                x_abs += stack.pop(0) # dxc
                y_abs += stack.pop(0) # dyc
                x3 = x_abs
                y3 = y_abs
                x_c_min, y_c_min, x_c_max, y_c_max = \
                    calc_curvebox(x0, y0, x1, y1, x2, y2, x3, y3)
                x_min = min(x_c_min, x_min)
                x_max = max(x_c_max, x_max)
                y_min = min(y_c_min, y_min)
                y_max = max(y_c_max, y_max)
            stack.clear()
        elif op == "hhcurveto":
            # |- dy1? {dxa dxb dyb dxc}+ hhcurveto (27) |-
            debug_print(op)
            x0 = x_abs
            y0 = y_abs
            if len(stack) % 4 >= 1:
                y_abs += stack.pop(0) # dy1
            for _ in range(len(stack)//4):
                x_abs += stack.pop(0) # dxa
                x1 = x_abs
                y1 = y_abs
                x_abs += stack.pop(0) # dxb
                y_abs += stack.pop(0) # dyb
                x2 = x_abs
                y2 = y_abs
                x_abs += stack.pop(0) # dxc
                x3 = x_abs
                y3 = y_abs
                x_c_min, y_c_min, x_c_max, y_c_max = \
                    calc_curvebox(x0, y0, x1, y1, x2, y2, x3, y3)
                x_min = min(x_c_min, x_min)
                x_max = max(x_c_max, x_max)
                y_min = min(y_c_min, y_min)
                y_max = max(y_c_max, y_max)
                x0 = x_abs
                y0 = y_abs
            stack.clear()
        elif op == "hvcurveto":
            # |- dx1 dx2 dy2 dy3 {dya dxb dyb dxc dxd dxe dye dyf}* dxf? hvcurveto (31) |-
            # |- {dxa dxb dyb dyc dyd dxe dye dxf}+ dyf? hvcurveto (31) |-
            debug_print("op {}, stacks {}".format(op, len(stack)))
            if len(stack) % 8 >= 4:
                x0 = x_abs
                y0 = y_abs
                x_abs += stack.pop(0) # dx1
                x1 = x_abs
                y1 = y_abs
                x_abs += stack.pop(0) # dx2
                y_abs += stack.pop(0) # dy2
                x2 = x_abs
                y2 = y_abs
                y_abs += stack.pop(0) # dy3
                x3 = x_abs
                y3 = y_abs
                for _ in range(len(stack)//8):
                    x_c_min, y_c_min, x_c_max, y_c_max = \
                        calc_curvebox(x0, y0, x1, y1, x2, y2, x3, y3)
                    x_min = min(x_c_min, x_min)
                    x_max = max(x_c_max, x_max)
                    y_min = min(y_c_min, y_min)
                    y_max = max(y_c_max, y_max)
                    x0 = x_abs
                    y0 = y_abs
                    y_abs += stack.pop(0) # dya
                    x1 = x_abs
                    y1 = y_abs
                    x_abs += stack.pop(0) # dxb
                    y_abs += stack.pop(0) # dyb
                    x2 = x_abs
                    y2 = y_abs
                    x_abs += stack.pop(0) # dxc
                    x3 = x_abs
                    y3 = y_abs
                    x_c_min, y_c_min, x_c_max, y_c_max = \
                        calc_curvebox(x0, y0, x1, y1, x2, y2, x3, y3)
                    x_min = min(x_c_min, x_min)
                    x_max = max(x_c_max, x_max)
                    y_min = min(y_c_min, y_min)
                    y_max = max(y_c_max, y_max)
                    x0 = x_abs
                    y0 = y_abs
                    x_abs += stack.pop(0) # dxd
                    x1 = x_abs
                    y1 = y_abs
                    x_abs += stack.pop(0) # dxe
                    y_abs += stack.pop(0) # dye
                    x2 = x_abs
                    y2 = y_abs
                    y_abs += stack.pop(0) # dyf
                    x3 = x_abs
                    y3 = y_abs
                if len(stack) > 0:
                    x_abs += stack.pop(0) # dxf
                    x3 = x_abs
                x_c_min, y_c_min, x_c_max, y_c_max = \
                    calc_curvebox(x0, y0, x1, y1, x2, y2, x3, y3)
                x_min = min(x_c_min, x_min)
                x_max = max(x_c_max, x_max)
                y_min = min(y_c_min, y_min)
                y_max = max(y_c_max, y_max)
            else:
                b_before = False
                for _ in range(len(stack)//8):
                    if b_before:
                        x_c_min, y_c_min, x_c_max, y_c_max = \
                            calc_curvebox(x0, y0, x1, y1, x2, y2, x3, y3)
                        x_min = min(x_c_min, x_min)
                        x_max = max(x_c_max, x_max)
                        y_min = min(y_c_min, y_min)
                        y_max = max(y_c_max, y_max)
                    x0 = x_abs
                    y0 = y_abs
                    x_abs += stack.pop(0) # dxa
                    x1 = x_abs
                    y1 = y_abs
                    x_abs += stack.pop(0) # dxb
                    y_abs += stack.pop(0) # dyb
                    x2 = x_abs
                    y2 = y_abs
                    y_abs += stack.pop(0) # dyc
                    x3 = x_abs
                    y3 = y_abs
                    x_c_min, y_c_min, x_c_max, y_c_max = \
                        calc_curvebox(x0, y0, x1, y1, x2, y2, x3, y3)
                    x_min = min(x_c_min, x_min)
                    x_max = max(x_c_max, x_max)
                    y_min = min(y_c_min, y_min)
                    y_max = max(y_c_max, y_max)
                    x0 = x_abs
                    y0 = y_abs
                    y_abs += stack.pop(0) # dyd
                    x1 = x_abs
                    y1 = y_abs
                    x_abs += stack.pop(0) # dxe
                    y_abs += stack.pop(0) # dye
                    x2 = x_abs
                    y2 = y_abs
                    x_abs += stack.pop(0) # dxf
                    x3 = x_abs
                    y3 = y_abs
                    b_before = True
                if len(stack) > 0:
                    y_abs += stack.pop(0) # dyf
                    y3 = y_abs
                x_c_min, y_c_min, x_c_max, y_c_max = \
                    calc_curvebox(x0, y0, x1, y1, x2, y2, x3, y3)
                x_min = min(x_c_min, x_min)
                x_max = max(x_c_max, x_max)
                y_min = min(y_c_min, y_min)
                y_max = max(y_c_max, y_max)
            stack.clear()
        elif op == "rcurveline":
            # |- {dxa dya dxb dyb dxc dyc}+ dxd dyd rcurveline (24) |-
            debug_print(op)
            for _ in range((len(stack)-2)//6):
                x0 = x_abs
                y0 = y_abs
                x_abs += stack.pop(0) # dxa
                y_abs += stack.pop(0) # dya
                x1 = x_abs
                y1 = y_abs
                x_abs += stack.pop(0) # dxb
                y_abs += stack.pop(0) # dyb
                x2 = x_abs
                y2 = y_abs
                x_abs += stack.pop(0) # dxc
                y_abs += stack.pop(0) # dyc
                x3 = x_abs
                y3 = y_abs
                x_c_min, y_c_min, x_c_max, y_c_max = \
                    calc_curvebox(x0, y0, x1, y1, x2, y2, x3, y3)
                x_min = min(x_c_min, x_min)
                x_max = max(x_c_max, x_max)
                y_min = min(y_c_min, y_min)
                y_max = max(y_c_max, y_max)
            x_abs += stack.pop(0) # dxd
            y_abs += stack.pop(0) # dyd
            point_path(x_abs, y_abs)
            x_min = min(x_abs, x_min)
            x_max = max(x_abs, x_max)
            y_min = min(y_abs, y_min)
            y_max = max(y_abs, y_max)
            stack.clear()
        elif op == "rlinecurve":
            # |- {dxa dya}+ dxb dyb dxc dyc dxd dyd rlinecurve (25) |-
            debug_print(op)
            for _ in range((len(stack)-6)//2):
                x_abs += stack.pop(0) # dxa
                y_abs += stack.pop(0) # dya
                point_path(x_abs, y_abs)
                x_min = min(x_abs, x_min)
                x_max = max(x_abs, x_max)
                y_min = min(y_abs, y_min)
                y_max = max(y_abs, y_max)
            x0 = x_abs
            y0 = y_abs
            x_abs += stack.pop(0) # dxb
            y_abs += stack.pop(0) # dyb
            x1 = x_abs
            y1 = y_abs
            x_abs += stack.pop(0) # dxc
            y_abs += stack.pop(0) # dyc
            x2 = x_abs
            y2 = y_abs
            x_abs += stack.pop(0) # dxd
            y_abs += stack.pop(0) # dyd
            x3 = x_abs
            y3 = y_abs
            x_c_min, y_c_min, x_c_max, y_c_max = \
                calc_curvebox(x0, y0, x1, y1, x2, y2, x3, y3)
            x_min = min(x_c_min, x_min)
            x_max = max(x_c_max, x_max)
            y_min = min(y_c_min, y_min)
            y_max = max(y_c_max, y_max)
            stack.clear()
        elif op == "vhcurveto":
            # |- dy1 dx2 dy2 dx3 {dxa dxb dyb dyc dyd dxe dye dxf}* dyf? vhcurveto (30) |-
            # |- {dya dxb dyb dxc dxd dxe dye dyf}* dxf? vhcurveto (30) |-
            debug_print(op)
            if len(stack) % 8 >= 4:
                x0 = x_abs
                y0 = y_abs
                y_abs += stack.pop(0) # dy1
                x1 = x_abs
                y1 = y_abs
                x_abs += stack.pop(0) # dx2
                y_abs += stack.pop(0) # dy2
                x2 = x_abs
                y2 = y_abs
                x_abs += stack.pop(0) # dx3
                x3 = x_abs
                y3 = y_abs
                for _ in range(len(stack)//8):
                    x_c_min, y_c_min, x_c_max, y_c_max = \
                        calc_curvebox(x0, y0, x1, y1, x2, y2, x3, y3)
                    x_min = min(x_c_min, x_min)
                    x_max = max(x_c_max, x_max)
                    y_min = min(y_c_min, y_min)
                    y_max = max(y_c_max, y_max)
                    x0 = x_abs
                    y0 = y_abs
                    x_abs += stack.pop(0) # dxa
                    x1 = x_abs
                    y1 = y_abs
                    x_abs += stack.pop(0) # dxb
                    y_abs += stack.pop(0) # dyb
                    x2 = x_abs
                    y2 = y_abs
                    y_abs += stack.pop(0) # dyc
                    x3 = x_abs
                    y3 = y_abs
                    x_c_min, y_c_min, x_c_max, y_c_max = \
                        calc_curvebox(x0, y0, x1, y1, x2, y2, x3, y3)
                    x_min = min(x_c_min, x_min)
                    x_max = max(x_c_max, x_max)
                    y_min = min(y_c_min, y_min)
                    y_max = max(y_c_max, y_max)
                    x0 = x_abs
                    y0 = y_abs
                    y_abs += stack.pop(0) # dyd
                    x1 = x_abs
                    y1 = y_abs
                    x_abs += stack.pop(0) # dxe
                    y_abs += stack.pop(0) # dye
                    x2 = x_abs
                    y2 = y_abs
                    x_abs += stack.pop(0) # dxf
                    x3 = x_abs
                    y3 = y_abs
                if len(stack) > 0:
                    y_abs += stack.pop(0) # dyf
                    y3 = y_abs
                x_c_min, y_c_min, x_c_max, y_c_max = \
                    calc_curvebox(x0, y0, x1, y1, x2, y2, x3, y3)
                x_min = min(x_c_min, x_min)
                x_max = max(x_c_max, x_max)
                y_min = min(y_c_min, y_min)
                y_max = max(y_c_max, y_max)
            else:
                b_before = False
                for _ in range(len(stack)//8):
                    if b_before:
                        x_c_min, y_c_min, x_c_max, y_c_max = \
                            calc_curvebox(x0, y0, x1, y1, x2, y2, x3, y3)
                        x_min = min(x_c_min, x_min)
                        x_max = max(x_c_max, x_max)
                        y_min = min(y_c_min, y_min)
                        y_max = max(y_c_max, y_max)
                    x0 = x_abs
                    y0 = y_abs
                    y_abs += stack.pop(0) # dya
                    x1 = x_abs
                    y1 = y_abs
                    x_abs += stack.pop(0) # dxb
                    y_abs += stack.pop(0) # dyb
                    x2 = x_abs
                    y2 = y_abs
                    x_abs += stack.pop(0) # dxc
                    x3 = x_abs
                    y3 = y_abs
                    x_c_min, y_c_min, x_c_max, y_c_max = \
                        calc_curvebox(x0, y0, x1, y1, x2, y2, x3, y3)
                    x_min = min(x_c_min, x_min)
                    x_max = max(x_c_max, x_max)
                    y_min = min(y_c_min, y_min)
                    y_max = max(y_c_max, y_max)
                    x0 = x_abs
                    y0 = y_abs
                    x_abs += stack.pop(0) # dxd
                    x1 = x_abs
                    y1 = y_abs
                    x_abs += stack.pop(0) # dxe
                    y_abs += stack.pop(0) # dye
                    x2 = x_abs
                    y2 = y_abs
                    y_abs += stack.pop(0) # dyf
                    x3 = x_abs
                    y3 = y_abs
                    b_before = True
                if len(stack) > 0:
                    x_abs += stack.pop(0) # dxf
                    x3 = x_abs
                x_c_min, y_c_min, x_c_max, y_c_max = \
                    calc_curvebox(x0, y0, x1, y1, x2, y2, x3, y3)
                x_min = min(x_c_min, x_min)
                x_max = max(x_c_max, x_max)
                y_min = min(y_c_min, y_min)
                y_max = max(y_c_max, y_max)
            stack.clear()
        elif op == "vvcurveto":
            # |- dx1? {dya dxb dyb dyc}+ vvcurveto (26) |-
            debug_print(op)
            x0 = x_abs
            y0 = y_abs
            if len(stack) % 4 >= 1:
                x_abs += stack.pop(0) # dx1
            for _ in range(len(stack)//4):
                y_abs += stack.pop(0) # dya
                x1 = x_abs
                y1 = y_abs
                x_abs += stack.pop(0) # dxb
                y_abs += stack.pop(0) # dyb
                x2 = x_abs
                y2 = y_abs
                y_abs += stack.pop(0) # dyc
                x3 = x_abs
                y3 = y_abs
                x_c_min, y_c_min, x_c_max, y_c_max = \
                    calc_curvebox(x0, y0, x1, y1, x2, y2, x3, y3)
                x_min = min(x_c_min, x_min)
                x_max = max(x_c_max, x_max)
                y_min = min(y_c_min, y_min)
                y_max = max(y_c_max, y_max)
                x0 = x_abs
                y0 = y_abs
            stack.clear()
        # elif op == "flex":
        #     # |- flex |- 
        elif op == "endchar": # endchar (14) |-
            debug_print(op)
            if is_first and len(stack) > 0:
                _ = stack.pop(0) # w
                is_first = False
            point_end()
            stack.clear()
            break
        elif op == "hstem" or op == "hstemhm":
            # |- y dy {dya dyb}* hstem (1) |-
            # |- y dy {dya dyb}* hstemhm (18) |-
            debug_print(op)
            if is_first and len(stack) % 2 == 1:
                _ = stack.pop(0) # w
                is_first = False
            _ = stack.pop(0) # y
            _ = stack.pop(0) # dy
            for _ in range(len(stack)//2):
                _ = stack.pop(0) # dya
                _ = stack.pop(0) # dyb
            stack.clear()
        elif op == "vstem" or op == "vstemhm":
            # |- x dx {dxa dxb}* vstem (3) |-
            # |- x dx {dxa dxb}* vstem (23) |-
            debug_print(op)
            if is_first and len(stack) % 2 == 1:
                _ = stack.pop(0) # w
                is_first = False
            _ = stack.pop(0) # x
            _ = stack.pop(0) # dx
            for _ in range(len(stack)//2):
                _ = stack.pop(0) # dxa
                _ = stack.pop(0) # dxb
            stack.clear()
        elif op == "hintmask" or op == "cntrmask":
            # |- hintmask (19 + mask) |-
            # |- cntrmask (20 + mask) |-
            debug_print(op)
            if len(stack) > 0:
                if is_first and len(stack) % 2 == 1:
                    _ = stack.pop(0) # w
                    is_first = False
                _ = stack.pop(0)
                _ = stack.pop(0)
                for _ in range(len(stack)//2):
                    _ = stack.pop(0)
                    _ = stack.pop(0)
            _ = curr_list.pop(0)
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
    return x_min, y_min, x_max, y_max

def calc_curvebox(x0, y0, x1, y1, x2, y2, x3, y3):
    # !!!FIXME!!!: This is just an estimate without calculating the curve.
    x_min = min(x0, x1, x2, x3)
    y_min = min(y0, y1, y2, y3)
    x_max = max(x0, x1, x2, x3)
    y_max = max(y0, y1, y2, y3)
    point_ctrl(x1, y1)
    point_ctrl(x2, y2)
    point_path(x3, y3)
    return x_min, y_min, x_max, y_max

def load_calcTable(file):
    table = []
    with open(file, "r") as f:
        for line in f:
            if line.startswith("#"):
                continue
            items = line.split()
            name0 = items[0]
            name = items[1]
            if re_isInt.match(name) is not None:
                name = name0
            table.append(name)
    return table

########################################################################

if len(sys.argv) <= 2:
    print("Usage: calc_letter_face.py calc.tbl CFF.ttx > letter_face.tbl")
    exit(1)

calc_filename = sys.argv[1]
source_filename = sys.argv[2]

table = load_calcTable(calc_filename)

tree = ET.parse(source_filename)
root = tree.getroot()

load_FDArray(root)
load_GlobalSubrs(root)

print("# name x_min y_min x_max y_max")

for cs in root.findall("./CFF/CFFFont/CharStrings/CharString"):
    name = cs.attrib["name"]
    if name in table:
        fd = int(cs.attrib["fdSelectIndex"])
        if debug_mode:
            window = tkinter.Tk()
            canvas = tkinter.Canvas(window, width=620, height=620)
            canvas.pack()
            draw_box()
        x_min, y_min, x_max, y_max = calc_CharString(cs.text, fd)
        print("{}\t{}\t{}\t{}\t{}". \
              format(name, x_min, y_min, x_max, y_max))
        if debug_mode:
            draw_letter_face(x_min, y_min, x_max, y_max)
            window.mainloop()
