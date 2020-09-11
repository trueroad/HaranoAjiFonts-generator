//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// aj1x-gsub-ligature.hh:
//   read aj1?-gsub-jp04.txt file ligature and create map
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

#ifndef INCLUDE_GUARD_AJ1X_GSUB_LIGATURE_HH
#define INCLUDE_GUARD_AJ1X_GSUB_LIGATURE_HH

#include <map>
#include <regex>
#include <string>
#include <vector>

#include "regex_dispatcher_m.hh"

class aj1x_gsub_ligature:
  public regex_dispatcher::member_table<aj1x_gsub_ligature>
{
public:
  aj1x_gsub_ligature ();

  void load (const std::string &filename, const std::string &feature);
  const std::map<std::vector<int>, int> &get_map (void) const noexcept
  {
    return map_;
  }
  const std::map<int, std::vector<int>> &get_rev (void) const noexcept
  {
    return rev_;
  }

private:
  bool feature_start (const std::smatch &);
  bool feature_end (const std::smatch &);
  bool substitute_line (const std::smatch &);

  std::string feature_;
  bool bfeature_ = false;
  std::map<std::vector<int>, int> map_;
  std::map<int, std::vector<int>> rev_;
};

#endif // INCLUDE_GUARD_AJ1X_GSUB_LIGATURE_HH
