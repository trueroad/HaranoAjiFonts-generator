//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// conv_table.cc:
//   conversion table from CID to CID
//
// Copyright (C) 2019, 2020 Masamichi Hosoda.
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

#include "conv_table.hh"

#include <algorithm>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <map>
#include <regex>
#include <sstream>
#include <string>

#include "regex_dispatcher_m.hh"

conv_table::conv_table ():
  regex_dispatcher::member_table<conv_table>
  ({
    { std::regex (R"((\d+)\s+(\d+)\r?)"),
      &conv_table::map_line},
    { std::regex (R"((\d+)\r?)"),
      &conv_table::remove_line},
  })
{
}

void conv_table::load (const std::string &filename)
{
  map_.clear ();

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
  int before = 0;
  for (auto i: cid_outs_)
    {
      if (i == before)
        {
          std::cerr << "warning: invalid table: duplicate in cid_out: cid "
                    << i << std::endl;
          continue;
        }
      if (i > (before + 1))
        {
          if ( i == (before + 2) )
            {
              std::cerr << "miss pre-defined cid: cid " << (before + 1)
                        << std::endl;
              cid_miss_.push_back (before + 1);
            }
          else
            {
              std::cerr << "miss pre-defined cid: cid " << (before + 1)
                        << " - cid " << (i - 1) << std::endl;
              for (int j = before + 1; j < i; ++j)
                cid_miss_.push_back (j);
            }
        }
      before = i;
    }
}

std::string conv_table::convert (const std::string cid_in_str)
{
  if (cid_in_str[0] == 'c' && cid_in_str[1] == 'i' && cid_in_str[2] == 'd')
    {
      auto cid_in = std::stoi (cid_in_str.c_str () + 3, nullptr, 10);
      if (map_.find (cid_in) != map_.end ())
        {
          if (map_.at (cid_in) >= 0)
            {
              std::stringstream ss;
              ss << "aji" << std::setw (5) << std::setfill ('0')
                 << map_.at (cid_in);
              return ss.str (); // convert
            }

          return ""; // remove cid
        }

      std::cerr << "original font cid is not found in table: "
                << cid_in_str << std::endl;
      return ""; // remove cid
    }

  if (cid_in_str != ".notdef")
    std::cerr << "warning: invalid cid name: " << cid_in_str
              << std::endl;
  return cid_in_str; // no change
}

namespace
{
  output_cid_or_remove (int cid)
  {
    if (cid < 0)
      std::cerr << "remove";
    else
      std::cerr << cid;
  }
};

bool conv_table::set_map (int cid_in, int cid_out)
{
  if (map_.find (cid_in) != map_.end ())
    {
      std::cerr
        << "warning: invalid table: duplicate in table: cid " << cid_in
        << " -> cid ";
      output_cid_or_remove (map_[cid_in]);
      std::cerr
        << ", cid ";
      output_cid_or_remove (cid_out);
      std::cerr
        << std::endl;
    }
  else
    map_[cid_in] = cid_out;

  if (cid_out >= 0)
    cid_outs_.push_back (cid_out);

  return true;
}

bool conv_table::map_line (const std::smatch &sm)
{
  auto cid_in {std::stoi (sm[1].str ())};
  auto cid_out {std::stoi (sm[2].str ())};

  return set_map (cid_in, cid_out);
}

bool conv_table::remove_line (const std::smatch &sm)
{
  auto cid {std::stoi (sm[1].str ())};

  return set_map (cid, -1);
}
