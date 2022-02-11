//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// fontcmap_reverse.hh:
//   read cmap table of the original font file and create an reverse map
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

#ifndef INCLUDE_GUARD_FONTCMAP_REVERSE_HH
#define INCLUDE_GUARD_FONTCMAP_REVERSE_HH

#include <map>
#include <set>
#include <string>

class cmapfile;

class fontcmap_reverse
{
public:
  void load_ttx (const std::string &filename, const cmapfile &cmf,
                 int format = 12, int platform_id = 0,
                 int plat_enc_id = 4, int lang = 0);
  const std::map<int, int> &get_map (void) const noexcept
  {
    return map_;
  }

private:
  std::map<int, int> map_;
  std::set<int> dup_;
};

#endif // INCLUDE_GUARD_FONTCMAP_REVERSE_HH
