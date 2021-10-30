//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// make_kanji_table_main.cc:
//   make kanji conversion table from SourceHan AI0 CID to AJ1 CID
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

#include <exception>
#include <iomanip>
#include <iostream>
#include <map>
#include <utility>

#include "AI0-SourceHan.hh"
#include "aj1x-kanji.hh"
#include "version.hh"

int main (int argc, char *argv[])
{
  std::cout
    << "# make_kanji_table: Harano Aji Fonts generator " << version
    << std::endl
    << "# (make kanji conversion table from SourceHan AI0 CID to AJ1 CID)"
    << std::endl
    << "# Copyright (C) 2019, 2021 Masamichi Hosoda" << std::endl
    << "# https://github.com/trueroad/HaranoAjiFonts-generator" << std::endl
    << "#" << std::endl;

  if (argc != 3)
    {
      std::cout
        << "# usage: make_kanji_table AI0-SOURCEHAN AJ16KANJI > TABLE.TBL"
        << std::endl
        << "#" << std::endl
        << "#     AIO-SOURCEHAN:" << std::endl
        << "#         AI0-SourceHan{Sans|Serif} file" << std::endl
        << "#         from the SourceHan repository." << std::endl
        << "#     AJ16KANJI:" << std::endl
        << "#         aj16-kanji.txt file" << std::endl
        << "#         from the SourceHan repository." << std::endl;
      return 1;
    }

  std::cout
    << "# inputs:" << std::endl
    << "#     AI0-SourceHan{Sans|Serif} file: \"" << argv[1] << "\""
    << std::endl
    << "#     aj16-kanji.txt file           : \"" << argv[2] << "\""
    << std::endl
    << "#" << std::endl;

  ai0_sourcehan ash;
  try
    {
      ash.load (argv[1]);
    }
  catch (std::exception &e)
    {
      std::cerr << "error: ash: std::exception: " << e.what ()
                << std::endl;
      return 1;
    }

  aj1x_kanji ak;
  try
    {
      ak.load (argv[2]);
    }
  catch (std::exception &e)
    {
      std::cerr << "error: ak: std::exception: " << e.what ()
                << std::endl;
      return 1;
    }

  std::map<int, int> map;
  std::map<int, int> dup;
  for (const auto &m: ash.get_map ())
    {
      auto cid_in = m.first;
      auto name = m.second;

      if (ak.get_map ().find (name) != ak.get_map ().end ())
        {
          auto cid_out = ak.get_map ().at (name);

          if (dup.find (cid_out) != dup.end ())
            {
              std::cout << "#duplicate: cid " << dup[cid_out]
                        << " ("
                        << ash.get_map ().at (dup[cid_out])
                        << "), cid " << cid_in
                        << " ("
                        << name
                        << ") -> cid "
                        << cid_out << std::endl;
              map[cid_in] = -1; // prefer lower cid_in
            }
          else
            {
              map[cid_in] = cid_out;
              dup[cid_out] = cid_in;
            }
        }
      else
        map[cid_in] = -1;
    }

  for (const auto &m: map)
    {
      if (m.second < 0)
        std::cout << m.first << std::endl;
      else
        std::cout << m.first << "\t" << m.second << std::endl;
    }

  std::map<int, std::string> miss;
  for (const auto &m: ak.get_map ())
    {
      const auto name = m.first;
      const auto cid = m.second;

      if (ash.get_rev ().find (name) == ash.get_rev ().end ())
        miss[cid] = name;
    }
  if (miss.size ())
    {
      std::cerr << "missing glyphs..." << std::endl;
      for (const auto &m: miss)
        {
          const auto cid = m.first;
          const auto name = m.second;

          std::cerr << cid << "\t" << name << std::endl;
        }
    }

  return 0;
}
