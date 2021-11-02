//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// copy_and_rotate_table.hh:
//   Copy and rotate table
//
// Copyright (C) 2020, 2021 Masamichi Hosoda.
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

#ifndef INCLUDE_GUARD_COPY_AND_ROTATE_TABLE_HH
#define INCLUDE_GUARD_COPY_AND_ROTATE_TABLE_HH

#include <map>
#include <string>
#include <vector>

#include "regex_dispatcher_m.hh"

class copy_and_rotate_table:
  public regex_dispatcher::member_table<copy_and_rotate_table>
{
public:
  copy_and_rotate_table ();

  void load (const std::string &filename);

  /*
  const std::map<int, std::pair<int, int>> &get_map (void) const noexcept
  {
    return map_;
  }
  */
  const std::vector<int> &get_cid_outs (void) const noexcept
  {
    return cid_outs_;
  }

private:
  bool map_line (const std::smatch &);

  bool set_map (int cid_in, int cid_out, int rotate);

  //std::map<int, std::pair<int, int>> map_;
  std::vector<int> cid_outs_;
};

#endif // INCLUDE_GUARD_COPY_AND_ROTATE_TABLE_HH
