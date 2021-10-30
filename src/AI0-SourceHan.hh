//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// AI0-SourceHan.hh:
//   read AI0-SourceHan{Sans|Serif} file and create map
//
// Copyright (C) 2019, 2021 Masamichi Hosoda.
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

#ifndef INCLUDE_GUARD_AI0_SOURCEHAN_HH
#define INCLUDE_GUARD_AI0_SOURCEHAN_HH

#include <map>
#include <regex>
#include <string>

#include "regex_dispatcher_m.hh"

class ai0_sourcehan: public regex_dispatcher::member_table<ai0_sourcehan>
{
public:
  ai0_sourcehan ();

  void load (const std::string &filename);
  const std::map<int, std::string> &get_map (void) const noexcept
  {
    return map_;
  }
  const std::map<std::string, int> &get_rev (void) const noexcept
  {
    return dup_;
  }

private:
  bool data_line (const std::smatch &);

  std::map<int, std::string> map_;
  std::map<std::string, int> dup_;
};

#endif // INCLUDE_GUARD_AI0_SOURCEHAN_HH
