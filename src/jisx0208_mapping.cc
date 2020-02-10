//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// jisx0208_mapping.cc:
//   read JIS X 0208 mapping file and create map
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

#include "jisx0208_mapping.hh"

#include <fstream>
#include <iostream>
#include <map>
#include <regex>
#include <string>

jisx0208::jisx0208 ():
  regex_dispatcher::member_table<jisx0208>
  ({
    { std::regex (R"(\d+-\d+\tU\+[\dA-F]+\t(\d+)\t(\d+)\t(\d+)\r?)"),
      &jisx0208::line},
    { std::regex (R"(\d+-\d+\tU\+[\dA-F]+\t(\d+) \((\d+)\)\t(\d+) \((\d+)\)\t(\d+) \((\d+)\)\r?)"),
      &jisx0208::line_dual},
    { std::regex (R"(\d+-\d+\tU\+[\dA-F]+\t(\d+) \[(\d+)\]\t(\d+) \[(\d+)\]\t(\d+) \[(\d+)\]\r?)"),
      &jisx0208::line_dual},
  })
{
}

void jisx0208::load (const std::string &filename, const std::string &type)
{
  map_.clear ();
  dup_.clear ();

  if (type == "Sans")
    bsans = true;
  else if (type == "Serif")
    bsans = false;
  else
    {
      std::cerr << "error: " << __func__ << ":unknown type: \""
                << type << "\"" << std::endl;
      return;
    }

  std::ifstream ifs;
  ifs.open (filename);
  if (!ifs)
    {
      std::cerr << "error: " << __func__ << ": open failed."
                << std::endl;
      return;
    }

  process_stream (ifs);
}

bool jisx0208::line (const std::smatch &sm)
{
  auto cid_out {std::stoi (sm[1].str ())};
  auto cid_in {std::stoi (sm[bsans ? 2 : 3].str ())};

  return set_map (cid_in, cid_out);
}

bool jisx0208::line_dual (const std::smatch &sm)
{
  auto cid_out {std::stoi (sm[1].str ())};
  auto cid_out_fw {std::stoi (sm[2].str ())};
  auto cid_in {std::stoi (sm[bsans ? 3 : 5].str ())};
  auto cid_in_fw {std::stoi (sm[bsans ? 4 : 6].str ())};

  return (set_map (cid_in, cid_out) && set_map (cid_in_fw, cid_out_fw));
}

bool jisx0208::set_map (int cid_in, int cid_out)
{
  if (map_.find (cid_in) != map_.end ())
    {
      std::cout
        << "#duplicate: cid "
        << cid_in
        << " -> cid "
        << map_[cid_in]
        << ", cid "
        << cid_out << std::endl;
    }
  else
    map_[cid_in] = cid_out;

  if (dup_.find (cid_out) != dup_.end ())
    {
      std::cout
        << "#duplicate: cid "
        << dup_[cid_out]
        << ", cid "
        << cid_in
        << " -> cid "
        << cid_out << std::endl;
    }
  else
    dup_[cid_out] = cid_in;

  return true;
}
