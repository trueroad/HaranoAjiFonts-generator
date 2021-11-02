//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// copy_and_rotate_table.cc:
//   Copy and rotate table
//
// Copyright (C) 2019-2021 Masamichi Hosoda.
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

#include "copy_and_rotate_table.hh"

#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>
#include <regex>
#include <string>
#include <utility>

#include "regex_dispatcher_m.hh"

copy_and_rotate_table::copy_and_rotate_table ():
  regex_dispatcher::member_table<copy_and_rotate_table>
  ({
    { std::regex (R"(aji(\d+)\s+aji(\d+)\s+(\d+)\r?)"),
      &copy_and_rotate_table::map_line},
  })
{
}

void copy_and_rotate_table::load (const std::string &filename)
{
  //map_.clear ();

  std::ifstream ifs;
  ifs.open (filename);
  if (!ifs)
    {
      std::cerr << "error: " << __func__ << ": open failed."
                << std::endl;
      return;
    }

  process_stream (ifs);

  std::sort (cid_outs_.begin (), cid_outs_.end ());
}

namespace
{
  void output_cid_or_remove (int cid)
  {
    if (cid < 0)
      std::cerr << "remove";
    else
      std::cerr << cid;
  }
};

bool copy_and_rotate_table::set_map (int cid_in, int cid_out, int rotate)
{
  /*
  if (map_.find (cid_in) != map_.end ())
    {
      std::cerr
        << "warning: invalid table: duplicate in table: cid " << cid_in
        << " -> cid ";
      output_cid_or_remove (map_[cid_in].first);
      std::cerr
        << ", cid ";
      output_cid_or_remove (cid_out);
      std::cerr
        << std::endl;
    }
  else
    map_[cid_in] = std::make_pair (cid_out, rotate);
  */

  if (cid_out >= 0)
    cid_outs_.push_back (cid_out);

  return true;
}

bool copy_and_rotate_table::map_line (const std::smatch &sm)
{
  auto cid_in {std::stoi (sm[1].str ())};
  auto cid_out {std::stoi (sm[2].str ())};
  auto rotate {std::stoi (sm[3].str ())};

  return set_map (cid_in, cid_out, rotate);
}
