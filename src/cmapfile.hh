//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// cmapfile.hh:
//   read CMap file (UTF-32 to pre-defined CID) and create map
//
// Copyright (C) 2019 Masamichi Hosoda.
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

#ifndef INCLUDE_GUARD_CMAPFILE_HH
#define INCLUDE_GUARD_CMAPFILE_HH

#include <map>
#include <regex>
#include <string>

#include "regex_dispatcher_m.hh"

class cmapfile: public regex_dispatcher::member_table<cmapfile>
{
public:
  cmapfile ();

  void load (const std::string &filename);
  const std::map<int, int> &get_map (void) const noexcept
  {
    return map_;
  }

private:
  bool cidchar_dec (const std::smatch &);
  bool cidchar_hex (const std::smatch &);
  bool cidrange_dec (const std::smatch &);
  bool cidrange_hex (const std::smatch &);
  bool begincidchar (const std::smatch &);
  bool begincidrange (const std::smatch &);
  bool endcidchar (const std::smatch &);
  bool endcidrange (const std::smatch &);

  bool cidchar (int uni, int cid);
  bool cidrange (int u1, int u2, int cid);

  void set_map (int uni, int cid);

  std::map<int, int> map_;
  std::map<int, int> dup_;
  bool is_char_ = false;
  bool is_range_ = false;
  int chars_ = 0;
  int ranges_ = 0;
};

#endif // INCLUDE_GUARD_CMAPFILE_HH
