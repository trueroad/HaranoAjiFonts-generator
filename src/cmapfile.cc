//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// cmapfile.cc:
//   read CMap file (UTF-32 to pre-defined CID) and create map
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

#include "cmapfile.hh"

#include <fstream>
#include <iomanip>
#include <iostream>
#include <map>
#include <regex>
#include <string>

#include "regex_dispatcher_m.hh"

cmapfile::cmapfile ():
  regex_dispatcher::member_table<cmapfile>
  ({
    { std::regex (R"(<([\da-fA-F]+)>\s*(\d+)\r?)"),
      &cmapfile::cidchar_dec},
    { std::regex (R"(<([\da-fA-F]+)>\s*([\da-fA-F]+)\r?)"),
      &cmapfile::cidchar_hex},
    { std::regex (R"(<([\da-fA-F]+)>\s*<([\da-fA-F]+)>\s*(\d+)\r?)"),
      &cmapfile::cidrange_dec},
    { std::regex (R"(<([\da-fA-F]+)>\s*<([\da-fA-F]+)>\s*([\da-fA-F]+)\r?)"),
      &cmapfile::cidrange_hex},
    { std::regex (R"((\d+)\s*begincidchar\r?)"),
      &cmapfile::begincidchar},
    { std::regex (R"((\d+)\s*begincidrange\r?)"),
      &cmapfile::begincidrange},
    { std::regex (R"(endcidchar\r?)"),
      &cmapfile::endcidchar},
    { std::regex (R"(endcidrange\r?)"),
      &cmapfile::endcidrange},
  })
{
}

void cmapfile::load (const std::string &filename)
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

void cmapfile::set_map (int uni, int cid)
{
  if (dup_.find (cid) != dup_.end ())
    std::cout
      << "#duplicate in CMap file: U+"
      << std::setw (4) << std::setfill ('0')
      << std::hex << std::uppercase
      << dup_[cid]
      << ", U+"
      << std::setw (4)
      << uni
      << std::nouppercase << std::dec
      << std::setfill (' ')
      << " -> cid " << cid << std::endl;
  else
    dup_[cid] = uni;

  if (map_.find (uni) != map_.end ())
    std::cout
      << "#warning: invalid CMap file: duplicate U+"
      << std::setw (4) << std::setfill ('0')
      << std::hex << std::uppercase
      << uni
      << std::nouppercase << std::dec
      << std::setfill (' ') << std::endl;
  else
    map_[uni] = cid;
}

bool cmapfile::cidchar (int uni, int cid)
{
  if (is_char_)
    {
      set_map (uni, cid);

      if (chars_ > 0)
        --chars_;
      else
        std::cout << "#warning: invalid CMap file: " << __func__
                  << ": extra char" << std::endl;
    }

  return true;
}

bool cmapfile::cidchar_dec (const std::smatch &sm)
{
  auto uni {std::stoi (sm[1].str (), nullptr, 16)};
  auto cid {std::stoi (sm[2].str ())};

  return cidchar (uni, cid);
}

bool cmapfile::cidchar_hex (const std::smatch &sm)
{
  auto uni {std::stoi (sm[1].str (), nullptr, 16)};
  auto cid {std::stoi (sm[2].str (), nullptr, 16)};

  return cidchar (uni, cid);
}

bool cmapfile::cidrange (int u1, int u2, int cid)
{
  if (is_range_)
    {
      if (u1 > u2)
        {
          std::cout << "#warning: invalid CMap file: " << __func__
                    << ": start > end" << std::endl;
        }
      int i = u1, c = cid;
      while ( i <= u2)
        set_map (i++, c++);

      if (ranges_ > 0)
        --ranges_;
      else
        std::cout << "#warning: invalid CMap file: " << __func__
                  << ": extra range" << std::endl;
    }

  return true;
}

bool cmapfile::cidrange_dec (const std::smatch &sm)
{
  auto u1 {std::stoi (sm[1].str (), nullptr, 16)};
  auto u2 {std::stoi (sm[2].str (), nullptr, 16)};
  auto cid {std::stoi (sm[3].str ())};

  return cidrange (u1, u2, cid);
}

bool cmapfile::cidrange_hex (const std::smatch &sm)
{
  auto u1 {std::stoi (sm[1].str (), nullptr, 16)};
  auto u2 {std::stoi (sm[2].str (), nullptr, 16)};
  auto cid {std::stoi (sm[3].str (), nullptr, 16)};

  return cidrange (u1, u2, cid);
}

bool cmapfile::begincidchar (const std::smatch &sm)
{
  auto chars {std::stoi (sm[1].str ())};

  if (is_char_)
    {
      std::cout << "#warning: invalid CMap file: " << __func__
                << ": no endcidchar" << std::endl;
    }
  if (is_range_)
    {
      std::cout << "#warning: invalid CMap file: " << __func__
                << ": no endcidrange" << std::endl;
      is_range_ = false;
    }
  is_char_ = true;
  chars_ = chars;

  return true;
}

bool cmapfile::begincidrange (const std::smatch &sm)
{
  auto ranges {std::stoi (sm[1].str ())};

  if (is_char_)
    {
      std::cout << "#warning: invalid CMap file: " << __func__
                << ": no endcidchar" << std::endl;
      is_char_ = false;
    }
  if (is_range_)
    {
      std::cout << "#warning: invalid CMap file:" << __func__
                << ": no endcidrange" << std::endl;
    }
  is_range_ = true;
  ranges_ = ranges;

  return true;
}

bool cmapfile::endcidchar (const std::smatch &sm)
{
  if (is_char_)
    {
      if (chars_)
        std::cout << "#warning: invalid CMap file: " << __func__
                  << ": wrong begincidchar" << std::endl;
      is_char_ = false;
    }
  else
    std::cout << "#warning: invalid CMap file: " << __func__
              << ": no begincidchar" << std::endl;

  if (is_range_)
    {
      std::cout << "#warning: invalid CMap file: " << __func__
                << ": no endcidrange" << std::endl;
      is_range_ = false;
    }

  return true;
}

bool cmapfile::endcidrange (const std::smatch &sm)
{
  if (is_char_)
    {
      std::cout << "#warning: invalid CMap file: " << __func__
                << ": no endcidchar" << std::endl;
      is_char_ = false;
    }

  if (is_range_)
    {
      if (ranges_)
        std::cout << "#warning: invalid CMap file: " << __func__
                  << ": wrong begincidrange" << std::endl;
      is_range_ = false;
    }
  else
    std::cout << "#warning: invalid CMap file: " << __func__
              << ": no begincidrange" << std::endl;

  return true;
}
