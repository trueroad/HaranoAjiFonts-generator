//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// aj1x-kana.hh:
//   AJ1 Kana type identification
//
// Copyright (C) 2020 Masamichi Hosoda.
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

#ifndef INCLUDE_GUARD_AJ1X_KANA_HH
#define INCLUDE_GUARD_AJ1X_KANA_HH

inline bool
is_aj1x_kana_fullwidth_h (int cid)
{
  if ((  643 <= cid && cid <=   644) ||
      (  651 <= cid && cid <=   654) ||
      cid ==   660 ||
      (  842 <= cid && cid <=  1010) ||
      ( 7958 <= cid && cid <=  7960) ||
      ( 8313 <= cid && cid <=  8316) ||
      cid == 12181 ||
      cid == 12269 ||
      cid == 12271 ||
      cid == 16195 ||
      (16209 <= cid && cid <= 16221) ||
      (16236 <= cid && cid <= 16252) ||
      (16326 <= cid && cid <= 16327))
    return true;

  return false;
}

inline bool
is_aj1x_kana_fullwidth_v (int cid)
{
  if (cid ==  7891 ||
      ( 7918 <= cid && cid <=  7939) ||
      ( 8264 <= cid && cid <=  8265) ||
      ( 8271 <= cid && cid <=  8272) ||
      (12108 <= cid && cid <= 12110) ||
      cid == 12270 ||
      cid == 12272 ||
      (16333 <= cid && cid <= 16349))
    return true;

  return false;
}

inline bool
is_aj1x_kana_tuned_h (int cid)
{
  if ((12273 <= cid && cid <= 12455) ||
      (16352 <= cid && cid <= 16381))
    return true;

  return false;
}

inline bool
is_aj1x_kana_tuned_v (int cid)
{
  if ((12456 <= cid && cid <= 12638) ||
      (16382 <= cid && cid <= 16411))
    return true;

  return false;
}

inline bool
is_aj1x_kana_propotional_h (int cid)
{
  if (15449 <= cid && cid <= 15452)
    return true;
  else if (cid == 15455)
    return true;
  else if (15462 <= cid && cid <= 15463)
    return true;
  else if (15517 <= cid && cid <= 15724)
    return true;

  return false;
}

inline bool
is_aj1x_kana_propotional_v (int cid)
{
  if (15976 <= cid && cid <= 15979)
    return true;
  else if (15982 <= cid && cid <= 16192)
    return true;

  return false;
}

#endif // INCLUDE_GUARD_AJ1X_KANA_HH
