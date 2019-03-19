//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// make_feature_table_main.cc:
//   make featured glyph conversion table from GSUB substitution
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

#include <exception>
#include <iomanip>
#include <iostream>
#include <map>

#include <pugixml.hpp>

#include "aj1x-gsub.hh"
#include "conv_table.hh"
#include "gsub_single.hh"
#include "version.hh"

int main (int argc, char *argv[])
{
  std::cout
    << "# make_feature_table: Harano Aji Fonts generator " << version
    << std::endl
    << "# (make featured glyph conversion table from GSUB substitution)"
    << std::endl
    << "# Copyright (C) 2019 Masamichi Hosoda" << std::endl
    << "# https://github.com/trueroad/HaranoAjiFonts-generator" << std::endl
    << "#" << std::endl;

  if (argc != 5)
    {
      std::cout
        << "# usage: make_feature_table TABLE.TBL FEATURE \\"
        << std::endl
        << "#        FONT.G_S_U_B_.ttx AJ16GSUB.txt > TABLE_FEATURE.TBL"
        << std::endl
        << "#" << std::endl
        << "#     TABLE.TBL:" << std::endl
        << "#         conversion table." << std::endl
        << "#     FEATURE:" << std::endl
        << "#         OpenType feature name." << std::endl
        << "#     FONT.G_S_U_B_.ttx:" << std::endl
        << "#         The ttx file of the GSUB table extracted" << std::endl
        << "#         from the original font file." << std::endl
        << "#     AJ16GSUB.txt:" << std::endl
        << "#         aj16-gsub-jp04.txt file" << std::endl
        << "#         from Adobe blog." << std::endl;
      return 1;
    }

  std::cout
    << "# inputs:" << std::endl
    << "#     TABLE.TBL        : \"" << argv[1] << "\""
    << std::endl
    << "#     FEATURE          : \"" << argv[2] << "\""
    << std::endl
    << "#     FONT.G_S_U_B_.ttx: \"" << argv[3] << "\""
    << std::endl
    << "#     AJ16GSUB.txt     : \"" << argv[4] << "\""
    << std::endl
    << "#" << std::endl;

  conv_table ct;
  try
    {
      ct.load (argv[1]);
    }
  catch (std::exception &e)
    {
      std::cerr << "error: conv_table::load: std::exception: " << e.what ()
                << std::endl;
      return 1;
    }

  pugi::xml_document doc;
  auto result = doc.load_file (argv[3]);
  if (!result)
    {
      std::cerr << "error: filename \"" << argv[3]
                << "\": " << result.description () << std::endl;
      return 1;
    }

  gsub_single gs;
  try
    {
      gs.load (doc, argv[2]);
    }
  catch (std::exception &e)
    {
      std::cerr << "error: gsub_single::load: std::exception: " << e.what ()
                << std::endl;
      return 1;
    }

  aj1x_gsub ag;
  try
    {
      ag.load (argv[4], argv[2]);
    }
  catch (std::exception &e)
    {
      std::cerr << "error: aj1x_gsub::load: std::exception: " << e.what ()
                << std::endl;
      return 1;
    }

  std::map<int, int> map;
  std::map<int, int> dup;
  for (const auto &m: gs.get_rev ())
    {
      auto cid_in_v = m.first;
      auto cid_in_h = m.second;
      if (ct.get_map ().find (cid_in_h) == ct.get_map ().end () ||
          ct.get_map ().at (cid_in_h) < 0)
        {
          std::cout
            << "#Cannot convert: "
            << "AI0 featured cid "
            << cid_in_v
            << " -> AI0 cid "
            << cid_in_h
            << " -> ???" << std::endl;
          continue;
        }

      auto cid_out_h = ct.get_map ().at (cid_in_h);
      if (ag.get_map ().find (cid_out_h) == ag.get_map ().end () ||
          ag.get_map ().at (cid_out_h) < 0)
        {
          std::cout
            << "#Cannot convert: "
            << "AI0 featured cid "
            << cid_in_v
            << " -> AI0 cid "
            << cid_in_h
            << " -> pre-defined cid "
            << cid_out_h
            << " -> ???" << std::endl;
          continue;
        }

      auto cid_out_v = ag.get_map ().at (cid_out_h);
      if (map.find (cid_in_v) != map.end ())
        {
          if (map[cid_in_v] != cid_out_v)
            {
              std::cout
                << "#warning: invalid: duplicate in cid_in_v: cid "
                << cid_in_v
                << " -> cid "
                << map[cid_in_v]
                << ", cid "
                << cid_out_v << std::endl;
            }
        }
      else
        map[cid_in_v] = cid_out_v;

      if (dup.find (cid_out_v) != dup.end ())
        {
          if (dup[cid_out_v] != cid_in_v)
            {
              std::cout
                << "#duplicate in cid_out_v: cid "
                << dup[cid_out_v]
                << ", cid "
                << cid_in_v
                << " -> cid "
                << cid_out_v << std::endl;
            }
        }
      else
        dup[cid_out_v] = cid_in_v;
    }

  for (const auto &m: map)
    {
      if (m.second < 0)
        std::cout << m.first << std::endl;
      else
        std::cout << m.first << "\t" << m.second << std::endl;
    }

  return 0;
}
