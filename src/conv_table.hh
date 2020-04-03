//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// conv_table.hh:
//   conversion table from CID to CID
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

#ifndef INCLUDE_GUARD_CONV_TABLE_HH
#define INCLUDE_GUARD_CONV_TABLE_HH

#include <map>
#include <string>
#include <vector>

#include "regex_dispatcher_m.hh"

const int aj17_max_cid = 23059;
const int aj1_max_cid = aj17_max_cid;

class conv_table: public regex_dispatcher::member_table<conv_table>
{
public:
  conv_table ();

  void load (const std::string &filename);
  std::string convert (const std::string cid_in_str);
  const std::map<int, int> &get_map (void) const noexcept
  {
    return map_;
  }
  const std::vector<int> &get_cid_outs (void) const noexcept
  {
    return cid_outs_;
  }
  const std::vector<int> &get_cid_miss (void) const noexcept
  {
    return cid_miss_;
  }

private:
  bool map_line (const std::smatch &);
  bool remove_line (const std::smatch &);

  bool set_map (int cid_in, int cid_out);

  std::map<int, int> map_;
  std::vector<int> cid_outs_;
  std::vector<int> cid_miss_;
};

#endif // INCLUDE_GUARD_CONV_TABLE_HH
