//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// AI0-SourceHan.cc:
//   read AI0-SourceHan{Sans|Serif} file and create map
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

#include "AI0-SourceHan.hh"

#include <fstream>
#include <iostream>
#include <map>
#include <regex>
#include <string>

#include "regex_dispatcher_m.hh"

ai0_sourcehan::ai0_sourcehan ():
  regex_dispatcher::member_table<ai0_sourcehan>
  ({
    { std::regex (R"((\d+)\t[^\t]+\t[^\t]+\t([^\t]+)\r?)"),
      &ai0_sourcehan::data_line},
  })
{
}

void ai0_sourcehan::load (const std::string &filename)
{
  map_.clear ();
  dup_.clear ();

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

bool ai0_sourcehan::data_line (const std::smatch &sm)
{
  auto cid {std::stoi (sm[1].str ())};
  auto name {sm[2].str ()};

  if (dup_.find (name) != dup_.end ())
    std::cout
      << "#duplicate name in AI0-SourceHan file: cid "
      << dup_[name]
      << " , cid "
      << cid
      << " -> "
      << name << std::endl;
  else
    dup_[name] = cid;

  if (map_.find (cid) != map_.end ())
    std::cout
      << "#warning: invalid AI0-SourceHan file: duplicate cid "
      << cid << std::endl;
  else
    map_[cid] = name;

  return true;
}
