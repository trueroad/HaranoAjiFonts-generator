//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// prefer_unicode.cc:
//   determine Unicode to prefer
//
// Copyright (C) 2019, 2022 Masamichi Hosoda.
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions
// are met:
//
// * Redistributions of source code must retain the above copyright notice,
//   this list of conditions and the following disclaimer.
//
// * Redistributions in binary form must reproduce the above copyright notice,
//   this list of conditions and the following disclaimer in the documentation
//   and/or other materials provided with the distribution.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
// ARE DISCLAIMED.
// IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
// FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
// DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
// OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
// HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
// LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
// OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
// SUCH DAMAGE.
//

#include "cmapfile.hh"
#include "prefer_unicode.hh"

namespace
{
  bool is_prefer (int u)
  {
    // Lower priority area from TeXLive dvipdfmx r50124 (2019-02-25):
    // tt_cmap.c: is_PUA_or_presentation ()
    return
      !((u >= 0x2E80 && u <= 0x2EF3) || (u >= 0x2F00 && u <= 0x2FD5) ||
        (u >= 0xE000 && u <= 0xF8FF) || (u >= 0xFB00 && u <= 0xFB4F) ||
        (u >= 0xF0000 && u <= 0xFFFFD) || (u >= 0x100000 && u <= 0x10FFFD));
  }
}

int prefer_unicode (int u1, int u2, const cmapfile &cmf)
{
  if (u1 == u2)
    return u1;

  bool bc1 = cmf.get_map ().find (u1) != cmf.get_map ().end ();
  bool bc2 = cmf.get_map ().find (u2) != cmf.get_map ().end ();

  if (bc1 && !bc2)
    return u1;
  if (bc2 && !bc1)
    return u2;

  bool b1 = is_prefer (u1);
  bool b2 = is_prefer (u2);

  if (b1 && !b2)
    return u1;
  if (b2 && !b1)
    return u2;

  return u1 < u2 ? u1 : u2;
}
