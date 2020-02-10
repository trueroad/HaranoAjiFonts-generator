//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// aj1x-gsub.hh:
//   read aj1?-gsub-jp04 file and create map
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

#include "aj1x-gsub.hh"

#include <fstream>
#include <iostream>
#include <map>
#include <regex>
#include <string>

#include "regex_dispatcher_m.hh"

aj1x_gsub::aj1x_gsub ():
  regex_dispatcher::member_table<aj1x_gsub>
  ({
    { std::regex (R"(\s*feature\s+(\w+)\s*\{\s*\r?)"),
      &aj1x_gsub::feature_start},
    { std::regex (R"(\s*substitute\s+\\(\d+)\s+by\s+\\(\d+)\s*;\s*\r?)"),
      &aj1x_gsub::substitute_line},
    { std::regex (R"(\s*\}\s+(\w+)\s*;\s*\r?)"),
      &aj1x_gsub::feature_end},
  })
{
}

void aj1x_gsub::load (const std::string &filename,
                      const std::string &feature)
{
  map_.clear ();
  rev_.clear ();
  feature_ = feature;

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

bool aj1x_gsub::feature_start (const std::smatch &sm)
{
  auto feature {sm[1].str ()};

  if (feature == feature_)
    {
      if (bfeature_)
        {
          std::cout
            << "#warning: " << __func__ << ": no feature end" << std::endl;
        }
      bfeature_ = true;
    }

  return true;
}

bool aj1x_gsub::feature_end (const std::smatch &sm)
{
  auto feature {sm[1].str ()};

  if (feature == feature_)
    {
      if (!bfeature_)
        {
          std::cout
            << "#warning: " << __func__ << ": no feature start" << std::endl;
        }
      bfeature_ = false;
    }

  return true;
}

bool aj1x_gsub::substitute_line (const std::smatch &sm)
{
  auto cid_in {std::stoi (sm[1].str ())};
  auto cid_out {std::stoi (sm[2].str ())};

  if (!bfeature_)
    return true;

  if (map_.find (cid_in) != map_.end ())
    {
      if (map_[cid_in] != cid_out)
        {
          std::cout
            << "#warning: invalid aj1x-gsub-jp04.txt: duplicate: cid "
            << cid_in
            << " -> cid "
            << map_[cid_in]
            << ", cid "
            << cid_out
            << std::endl;
        }
    }
  else
    map_[cid_in] = cid_out;

  if (rev_.find (cid_out) != rev_.end ())
    {
      if (rev_[cid_out] != cid_in)
        {
          std::cout
            << "#duplicate in aj1x-gsub-jp04.txt: cid "
            << rev_[cid_out]
            << ", cid "
            << cid_in
            << " -> cid "
            << cid_out << std::endl;
        }
    }
  else
    rev_[cid_out] = cid_in;

  return true;
}
