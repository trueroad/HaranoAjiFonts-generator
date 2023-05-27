#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harano Aji Fonts generator.

https://github.com/trueroad/HaranoAjiFonts-generator

calc_letter_face.py:
  calc letter face of the CFF glyph.

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

import copy
import math
import re
import sys
from typing import cast, Final, TextIO, Union
import xml.etree.ElementTree as ET

debug_mode: bool = False

if debug_mode:
    import tkinter

FDArray: list[dict[str, Union[str, list[str]]]] = []
GlobalSubrs: list[str] = []


# load GlobalSubrs
def load_GlobalSubrs(root: ET.Element) -> None:
    cs: ET.Element
    for cs in root.findall("./CFF/GlobalSubrs/CharString"):
        if cs.text is not None:
            GlobalSubrs.append(cs.text)


# load FDArray
def load_FDArray(root: ET.Element) -> None:
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
    if len(GlobalSubrs) < 1240:
        return GlobalSubrs[index + 107]
    elif len(GlobalSubrs) < 33900:
        return GlobalSubrs[index + 1131]
    else:
        return GlobalSubrs[index + 32768]


def get_LocalSubr(fd: int, index: int) -> str:
    Subrs: list[str] = cast(list[str], FDArray[fd]["Subrs"])
    if len(Subrs) < 1240:
        return Subrs[index + 107]
    elif len(Subrs) < 33900:
        return Subrs[index + 1131]
    else:
        return Subrs[index + 32768]


# for debug
canvas: tkinter.Canvas
debug_before: bool = False
debug_before_x: float = 0.0
debug_before_y: float = 0.0
debug_first: bool = False
debug_first_x: float = 0.0
debug_first_y: float = 0.0
DEBUG_R: Final[float] = 3.0
DEBUG_XS: Final[float] = 0.5
DEBUG_YS: Final[float] = -0.5
DEBUG_XA: Final[float] = 100.0
DEBUG_YA: Final[float] = 540.0


def debug_print(msg: str) -> None:
    if debug_mode:
        print("# " + msg)


def draw_box() -> None:
    if not debug_mode:
        return

    canvas.create_rectangle(0 * DEBUG_XS + DEBUG_XA,
                            880 * DEBUG_YS + DEBUG_YA,
                            1000 * DEBUG_XS + DEBUG_XA,
                            -120 * DEBUG_YS + DEBUG_YA,
                            outline='white')
    canvas.create_line(0 * DEBUG_XS + DEBUG_XA, 0 * DEBUG_YS + DEBUG_YA,
                       1000 * DEBUG_XS + DEBUG_XA, 0 * DEBUG_YS + DEBUG_YA,
                       fill='white')


def draw_letter_face(x_min: float, y_min: float,
                     x_max: float, y_max: float) -> None:
    if not debug_mode:
        return

    canvas.create_rectangle(x_min * DEBUG_XS + DEBUG_XA,
                            y_min * DEBUG_YS + DEBUG_YA,
                            x_max * DEBUG_XS + DEBUG_XA,
                            y_max * DEBUG_YS + DEBUG_YA,
                            outline='green', dash=(2, 2))


def draw_bezier(x0: float, y0: float,
                x1: float, y1: float,
                x2: float, y2: float,
                x3: float, y3: float) -> None:
    if not debug_mode:
        return

    global debug_before
    global debug_before_x
    global debug_before_y

    canvas.create_line(x0 * DEBUG_XS + DEBUG_XA,
                       y0 * DEBUG_YS + DEBUG_YA,
                       x1 * DEBUG_XS + DEBUG_XA,
                       y1 * DEBUG_YS + DEBUG_YA,
                       dash=(2, 2))
    canvas.create_oval(x1 * DEBUG_XS + DEBUG_XA - DEBUG_R,
                       y1 * DEBUG_YS + DEBUG_YA - DEBUG_R,
                       x1 * DEBUG_XS + DEBUG_XA + DEBUG_R,
                       y1 * DEBUG_YS + DEBUG_YA + DEBUG_R)
    canvas.create_line(x2 * DEBUG_XS + DEBUG_XA,
                       y2 * DEBUG_YS + DEBUG_YA,
                       x3 * DEBUG_XS + DEBUG_XA,
                       y3 * DEBUG_YS + DEBUG_YA,
                       dash=(2, 2))
    canvas.create_oval(x2 * DEBUG_XS + DEBUG_XA - DEBUG_R,
                       y2 * DEBUG_YS + DEBUG_YA - DEBUG_R,
                       x2 * DEBUG_XS + DEBUG_XA + DEBUG_R,
                       y2 * DEBUG_YS + DEBUG_YA + DEBUG_R)

    debug_before_x = x0
    debug_before_y = y0

    i: int
    for i in range(1, 99):
        t: float = i / 100
        x: float
        y: float
        x, y = bezier(t, x0, y0, x1, y1, x2, y2, x3, y3)
        canvas.create_line(debug_before_x * DEBUG_XS + DEBUG_XA,
                           debug_before_y * DEBUG_YS + DEBUG_YA,
                           x * DEBUG_XS + DEBUG_XA,
                           y * DEBUG_YS + DEBUG_YA)
        debug_before_x = x
        debug_before_y = y

    point_path(x3, y3)


def point_end() -> None:
    if not debug_mode:
        return

    global debug_before
    global debug_before_x
    global debug_before_y
    global debug_first
    global debug_first_x
    global debug_first_y
    global debug_first

    if debug_first:
        canvas.create_line(debug_before_x * DEBUG_XS + DEBUG_XA,
                           debug_before_y * DEBUG_YS + DEBUG_YA,
                           debug_first_x * DEBUG_XS + DEBUG_XA,
                           debug_first_y * DEBUG_YS + DEBUG_YA)

    debug_before = False
    debug_before_x = 0.0
    debug_before_y = 0.0
    debug_first = False
    debug_first_x = 0.0
    debug_first_y = 0.0


def point_path(x: float, y: float) -> None:
    if not debug_mode:
        return

    global debug_before
    global debug_before_x
    global debug_before_y
    global debug_first
    global debug_first_x
    global debug_first_y

    canvas.create_oval(x * DEBUG_XS + DEBUG_XA - DEBUG_R,
                       y * DEBUG_YS + DEBUG_YA - DEBUG_R,
                       x * DEBUG_XS + DEBUG_XA + DEBUG_R,
                       y * DEBUG_YS + DEBUG_YA + DEBUG_R,
                       fill='red')
    if debug_before:
        canvas.create_line(debug_before_x * DEBUG_XS + DEBUG_XA,
                           debug_before_y * DEBUG_YS + DEBUG_YA,
                           x * DEBUG_XS + DEBUG_XA, y * DEBUG_YS + DEBUG_YA)

    if debug_first_x == x and debug_first_y == y:
        debug_before = False
        debug_first = False
    else:
        debug_before_x = x
        debug_before_y = y
        debug_before = True

    debug_print("path ({}, {})".format(x, y))


def point_move(x: float, y: float) -> None:
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


re_isInt: re.Pattern[str] = re.compile(r"^-?\d+$")
re_isFloat: re.Pattern[str] = re.compile(r"^-?\d+(?:\.\d+)?$")


def calc_CharString(cs: str, fd: int) -> tuple[float, float, float, float]:
    stack: list[float] = []
    list_stack: list[list[str]] = []
    curr_list: list[str] = cs.split()
    is_first: bool = True
    is_first_move: bool = True
    b_before: bool

    x_abs: float = 0.0
    y_abs: float = 0.0
    x_min: float = 0.0
    y_min: float = 0.0
    x_max: float = 0.0
    y_max: float = 0.0
    x_c_min: float
    y_c_min: float
    x_c_max: float
    y_c_max: float

    while len(curr_list) > 0:
        op: str = curr_list.pop(0)
        if re_isInt.match(op) is not None:
            stack.append(int(op))
        elif re_isFloat.match(op) is not None:
            stack.append(float(op))
        elif op == "rmoveto" or op == "hmoveto" or op == "vmoveto":
            # |- dx1 dy1 rmoveto (21) |-
            # |- dx1 hmoveto (22) |-
            # |- dy1 vmoveto (4) |-
            debug_print(op)
            dx1: float = 0.0
            dy1: float = 0.0
            if op == "rmoveto":
                if is_first and len(stack) > 2:
                    _ = stack.pop(0)  # w
                    is_first = False
                dx1 = stack[0]
                dy1 = stack[1]
            elif op == "hmoveto":
                if is_first and len(stack) > 1:
                    _ = stack.pop(0)  # w
                    is_first = False
                dx1 = stack[0]
            elif op == "vmoveto":
                if is_first and len(stack) > 1:
                    _ = stack.pop(0)  # w
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
                x_abs += stack.pop(0)  # dxa
                y_abs += stack.pop(0)  # dya
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
                x_abs += stack.pop(0)  # dx1
                point_path(x_abs, y_abs)
                x_min = min(x_abs, x_min)
                x_max = max(x_abs, x_max)
                for _ in range(len(stack)//2):
                    y_abs += stack.pop(0)  # dya
                    point_path(x_abs, y_abs)
                    y_min = min(y_abs, y_min)
                    y_max = max(y_abs, y_max)
                    x_abs += stack.pop(0)  # dxb
                    point_path(x_abs, y_abs)
                    x_min = min(x_abs, x_min)
                    x_max = max(x_abs, x_max)
            else:
                for _ in range(len(stack)//2):
                    x_abs += stack.pop(0)  # dxa
                    point_path(x_abs, y_abs)
                    x_min = min(x_abs, x_min)
                    x_max = max(x_abs, x_max)
                    y_abs += stack.pop(0)  # dyb
                    point_path(x_abs, y_abs)
                    y_min = min(y_abs, y_min)
                    y_max = max(y_abs, y_max)
            stack.clear()
        elif op == "vlineto":
            # |- dy1 {dxa dyb}* vlineto (7) |-
            # |- {dya dxb}+ vlineto (7) |-
            debug_print(op)
            if len(stack) % 2 == 1:
                y_abs += stack.pop(0)  # dy1
                point_path(x_abs, y_abs)
                y_min = min(y_abs, y_min)
                y_max = max(y_abs, y_max)
                for _ in range(len(stack)//2):
                    x_abs += stack.pop(0)  # dxa
                    point_path(x_abs, y_abs)
                    x_min = min(x_abs, x_min)
                    x_max = max(x_abs, x_max)
                    y_abs += stack.pop(0)  # dyb
                    point_path(x_abs, y_abs)
                    y_min = min(y_abs, y_min)
                    y_max = max(y_abs, y_max)
            else:
                for _ in range(len(stack)//2):
                    y_abs += stack.pop(0)  # dya
                    point_path(x_abs, y_abs)
                    y_min = min(y_abs, y_min)
                    y_max = max(y_abs, y_max)
                    x_abs += stack.pop(0)  # dxb
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
                x_abs += stack.pop(0)  # dxa
                y_abs += stack.pop(0)  # dya
                x1 = x_abs
                y1 = y_abs
                x_abs += stack.pop(0)  # dxb
                y_abs += stack.pop(0)  # dyb
                x2 = x_abs
                y2 = y_abs
                x_abs += stack.pop(0)  # dxc
                y_abs += stack.pop(0)  # dyc
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
                y_abs += stack.pop(0)  # dy1
            for _ in range(len(stack)//4):
                x_abs += stack.pop(0)  # dxa
                x1 = x_abs
                y1 = y_abs
                x_abs += stack.pop(0)  # dxb
                y_abs += stack.pop(0)  # dyb
                x2 = x_abs
                y2 = y_abs
                x_abs += stack.pop(0)  # dxc
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
            # |- dx1 dx2 dy2 dy3 {dya dxb dyb dxc dxd dxe dye dyf}* dxf?
            #     hvcurveto (31) |-
            # |- {dxa dxb dyb dyc dyd dxe dye dxf}+ dyf? hvcurveto (31) |-
            debug_print("op {}, stacks {}".format(op, len(stack)))
            if len(stack) % 8 >= 4:
                x0 = x_abs
                y0 = y_abs
                x_abs += stack.pop(0)  # dx1
                x1 = x_abs
                y1 = y_abs
                x_abs += stack.pop(0)  # dx2
                y_abs += stack.pop(0)  # dy2
                x2 = x_abs
                y2 = y_abs
                y_abs += stack.pop(0)  # dy3
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
                    y_abs += stack.pop(0)  # dya
                    x1 = x_abs
                    y1 = y_abs
                    x_abs += stack.pop(0)  # dxb
                    y_abs += stack.pop(0)  # dyb
                    x2 = x_abs
                    y2 = y_abs
                    x_abs += stack.pop(0)  # dxc
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
                    x_abs += stack.pop(0)  # dxd
                    x1 = x_abs
                    y1 = y_abs
                    x_abs += stack.pop(0)  # dxe
                    y_abs += stack.pop(0)  # dye
                    x2 = x_abs
                    y2 = y_abs
                    y_abs += stack.pop(0)  # dyf
                    x3 = x_abs
                    y3 = y_abs
                if len(stack) > 0:
                    x_abs += stack.pop(0)  # dxf
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
                    x_abs += stack.pop(0)  # dxa
                    x1 = x_abs
                    y1 = y_abs
                    x_abs += stack.pop(0)  # dxb
                    y_abs += stack.pop(0)  # dyb
                    x2 = x_abs
                    y2 = y_abs
                    y_abs += stack.pop(0)  # dyc
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
                    y_abs += stack.pop(0)  # dyd
                    x1 = x_abs
                    y1 = y_abs
                    x_abs += stack.pop(0)  # dxe
                    y_abs += stack.pop(0)  # dye
                    x2 = x_abs
                    y2 = y_abs
                    x_abs += stack.pop(0)  # dxf
                    x3 = x_abs
                    y3 = y_abs
                    b_before = True
                if len(stack) > 0:
                    y_abs += stack.pop(0)  # dyf
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
                x_abs += stack.pop(0)  # dxa
                y_abs += stack.pop(0)  # dya
                x1 = x_abs
                y1 = y_abs
                x_abs += stack.pop(0)  # dxb
                y_abs += stack.pop(0)  # dyb
                x2 = x_abs
                y2 = y_abs
                x_abs += stack.pop(0)  # dxc
                y_abs += stack.pop(0)  # dyc
                x3 = x_abs
                y3 = y_abs
                x_c_min, y_c_min, x_c_max, y_c_max = \
                    calc_curvebox(x0, y0, x1, y1, x2, y2, x3, y3)
                x_min = min(x_c_min, x_min)
                x_max = max(x_c_max, x_max)
                y_min = min(y_c_min, y_min)
                y_max = max(y_c_max, y_max)
            x_abs += stack.pop(0)  # dxd
            y_abs += stack.pop(0)  # dyd
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
                x_abs += stack.pop(0)  # dxa
                y_abs += stack.pop(0)  # dya
                point_path(x_abs, y_abs)
                x_min = min(x_abs, x_min)
                x_max = max(x_abs, x_max)
                y_min = min(y_abs, y_min)
                y_max = max(y_abs, y_max)
            x0 = x_abs
            y0 = y_abs
            x_abs += stack.pop(0)  # dxb
            y_abs += stack.pop(0)  # dyb
            x1 = x_abs
            y1 = y_abs
            x_abs += stack.pop(0)  # dxc
            y_abs += stack.pop(0)  # dyc
            x2 = x_abs
            y2 = y_abs
            x_abs += stack.pop(0)  # dxd
            y_abs += stack.pop(0)  # dyd
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
            # |- dy1 dx2 dy2 dx3 {dxa dxb dyb dyc dyd dxe dye dxf}* dyf?
            #     vhcurveto (30) |-
            # |- {dya dxb dyb dxc dxd dxe dye dyf}* dxf? vhcurveto (30) |-
            debug_print(op)
            if len(stack) % 8 >= 4:
                x0 = x_abs
                y0 = y_abs
                y_abs += stack.pop(0)  # dy1
                x1 = x_abs
                y1 = y_abs
                x_abs += stack.pop(0)  # dx2
                y_abs += stack.pop(0)  # dy2
                x2 = x_abs
                y2 = y_abs
                x_abs += stack.pop(0)  # dx3
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
                    x_abs += stack.pop(0)  # dxa
                    x1 = x_abs
                    y1 = y_abs
                    x_abs += stack.pop(0)  # dxb
                    y_abs += stack.pop(0)  # dyb
                    x2 = x_abs
                    y2 = y_abs
                    y_abs += stack.pop(0)  # dyc
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
                    y_abs += stack.pop(0)  # dyd
                    x1 = x_abs
                    y1 = y_abs
                    x_abs += stack.pop(0)  # dxe
                    y_abs += stack.pop(0)  # dye
                    x2 = x_abs
                    y2 = y_abs
                    x_abs += stack.pop(0)  # dxf
                    x3 = x_abs
                    y3 = y_abs
                if len(stack) > 0:
                    y_abs += stack.pop(0)  # dyf
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
                    y_abs += stack.pop(0)  # dya
                    x1 = x_abs
                    y1 = y_abs
                    x_abs += stack.pop(0)  # dxb
                    y_abs += stack.pop(0)  # dyb
                    x2 = x_abs
                    y2 = y_abs
                    x_abs += stack.pop(0)  # dxc
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
                    x_abs += stack.pop(0)  # dxd
                    x1 = x_abs
                    y1 = y_abs
                    x_abs += stack.pop(0)  # dxe
                    y_abs += stack.pop(0)  # dye
                    x2 = x_abs
                    y2 = y_abs
                    y_abs += stack.pop(0)  # dyf
                    x3 = x_abs
                    y3 = y_abs
                    b_before = True
                if len(stack) > 0:
                    x_abs += stack.pop(0)  # dxf
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
                x_abs += stack.pop(0)  # dx1
            for _ in range(len(stack)//4):
                y_abs += stack.pop(0)  # dya
                x1 = x_abs
                y1 = y_abs
                x_abs += stack.pop(0)  # dxb
                y_abs += stack.pop(0)  # dyb
                x2 = x_abs
                y2 = y_abs
                y_abs += stack.pop(0)  # dyc
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
        elif op == "endchar":  # endchar (14) |-
            debug_print(op)
            if is_first and len(stack) > 0:
                _ = stack.pop(0)  # w
                is_first = False
            point_end()
            stack.clear()
            break
        elif op == "hstem" or op == "hstemhm":
            # |- y dy {dya dyb}* hstem (1) |-
            # |- y dy {dya dyb}* hstemhm (18) |-
            debug_print(op)
            if is_first and len(stack) % 2 == 1:
                _ = stack.pop(0)  # w
                is_first = False
            _ = stack.pop(0)  # y
            _ = stack.pop(0)  # dy
            for _ in range(len(stack)//2):
                _ = stack.pop(0)  # dya
                _ = stack.pop(0)  # dyb
            stack.clear()
        elif op == "vstem" or op == "vstemhm":
            # |- x dx {dxa dxb}* vstem (3) |-
            # |- x dx {dxa dxb}* vstem (23) |-
            debug_print(op)
            if is_first and len(stack) % 2 == 1:
                _ = stack.pop(0)  # w
                is_first = False
            _ = stack.pop(0)  # x
            _ = stack.pop(0)  # dx
            for _ in range(len(stack)//2):
                _ = stack.pop(0)  # dxa
                _ = stack.pop(0)  # dxb
            stack.clear()
        elif op == "hintmask" or op == "cntrmask":
            # |- hintmask (19 + mask) |-
            # |- cntrmask (20 + mask) |-
            debug_print(op)
            if len(stack) > 0:
                if is_first and len(stack) % 2 == 1:
                    _ = stack.pop(0)  # w
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
            curr_list = get_LocalSubr(fd, int(stack.pop())).split()
        elif op == "callgsubr":
            list_stack.append(curr_list)
            curr_list = get_GlobalSubr(int(stack.pop())).split()
        elif op == "return":
            curr_list = list_stack.pop()
        else:
            raise Exception("unknown operator {}".format(op))
    return x_min, y_min, x_max, y_max


def calc_curvebox(x0: float, y0: float,
                  x1: float, y1: float,
                  x2: float, y2: float,
                  x3: float, y3: float
                  ) -> tuple[float, float, float, float]:
    x_candidate: list[float] = [float(x0), float(x3)]
    y_candidate: list[float] = [float(y0), float(y3)]

    a: float = - 3.0 * x0 + 9.0 * x1 - 9.0 * x2 + 3.0 * x3
    b: float = 6.0 * x0 - 12.0 * x1 + 6.0 * x2
    c: float = - 3.0 * x0 + 3.0 * x1
    t_candidate: list[float] = solve_equation_real(a, b, c)

    a = - 3.0 * y0 + 9.0 * y1 - 9.0 * y2 + 3.0 * y3
    b = 6.0 * y0 - 12.0 * y1 + 6.0 * y2
    c = - 3.0 * y0 + 3.0 * y1
    t_candidate += solve_equation_real(a, b, c)

    debug_print("cacl_curvebox")
    debug_print("  0-candidate ({}, {})".format(x0, y0))
    debug_print("  3-candidate ({}, {})".format(x3, y3))

    t: float
    for t in t_candidate:
        if 0.0 <= t and t <= 1.0:
            x, y = bezier(t, x0, y0, x1, y1, x2, y2, x3, y3)
            debug_print("  t-candidate ({}, {})".format(x, y))
            x_candidate.append(x)
            y_candidate.append(y)

    x_min = min(x_candidate)
    y_min = min(y_candidate)
    x_max = max(x_candidate)
    y_max = max(y_candidate)

    debug_print("  result min  ({}, {})".format(x_min, y_min))
    debug_print("  result max  ({}, {})".format(x_max, y_max))

    draw_bezier(x0, y0, x1, y1, x2, y2, x3, y3)
    return x_min, y_min, x_max, y_max


def solve_equation_real(a: float, b: float, c: float) -> list[float]:
    r: list[float] = []
    debug_print("solve with a={}, b={}, c={}".format(a, b, c))
    if a != 0.0:
        d = b * b - 4.0 * a * c
        debug_print("  quadratic equation. D={}".format(d))
        if d < 0.0:
            debug_print("  complex roots. no candidate.")
            return []
        elif d > 0.0:
            debug_print("  real roots.")
            r += [(-b + math.sqrt(d)) / (2.0*a)]
            r += [(-b - math.sqrt(d)) / (2.0*a)]
        else:
            debug_print("  multiple root.")
            r += [-b / (2.0*a)]
    else:
        debug_print("  linear equation")
        if b != 0.0:
            r += [-c / b]
        else:
            debug_print("  zero divide. no candidate.")
        debug_print("  root = {}".format(r))
    return r


def bezier(t: float,
           x0: float, y0: float,
           x1: float, y1: float,
           x2: float, y2: float,
           x3: float, y3: float) -> tuple[float, float]:
    x: float = \
        (-1.0 * x0 + 3.0 * x1 - 3.0 * x2 + 1.0 * x3) * t * t * t \
        + (3.0 * x0 - 6.0 * x1 + 3.0 * x2) * t * t \
        + (-3.0 * x0 + 3.0 * x1) * t \
        + 1.0 * x0
    y: float = \
        (-1.0 * y0 + 3.0 * y1 - 3.0 * y2 + 1.0 * y3) * t * t * t \
        + (3.0 * y0 - 6.0 * y1 + 3.0 * y2) * t * t \
        + (-3.0 * y0 + 3.0 * y1) * t \
        + 1.0 * y0
    return x, y


def load_calcTable(file: str) -> list[str]:
    table: list[str] = []
    f: TextIO
    with open(file, "r") as f:
        line: str
        for line in f:
            if line.startswith("#"):
                continue
            items: list[str] = line.split()
            name0: str = items[0]
            name: str = items[1]
            if re_isInt.match(name) is not None:
                name = name0
            table.append(name)
    return table

########################################################################


def main() -> None:
    """Do main."""
    if len(sys.argv) <= 2:
        print("Usage: calc_letter_face.py calc.tbl CFF.ttx > letter_face.tbl")
        exit(1)

    calc_filename: str = sys.argv[1]
    source_filename: str = sys.argv[2]

    table: list[str] = load_calcTable(calc_filename)

    tree: ET.ElementTree = ET.parse(source_filename)
    root: ET.Element = tree.getroot()

    load_FDArray(root)
    load_GlobalSubrs(root)

    print("# name x_min y_min x_max y_max")

    cs: ET.Element
    for cs in root.findall("./CFF/CFFFont/CharStrings/CharString"):
        name: str = cs.attrib["name"]
        if name in table and cs.text is not None:
            fd: int = int(cs.attrib["fdSelectIndex"])
            if debug_mode:
                window: tkinter.Tk = tkinter.Tk()
                global canvas
                canvas = tkinter.Canvas(window, width=700, height=700)
                canvas.pack()
                draw_box()
            x_min: float
            y_min: float
            x_max: float
            y_max: float
            x_min, y_min, x_max, y_max = calc_CharString(cs.text, fd)
            print("{}\t{}\t{}\t{}\t{}".
                  format(name, x_min, y_min, x_max, y_max))
            if debug_mode:
                draw_letter_face(x_min, y_min, x_max, y_max)
                window.mainloop()


if __name__ == '__main__':
    main()
