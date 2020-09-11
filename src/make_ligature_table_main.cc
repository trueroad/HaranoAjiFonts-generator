//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// make_ligature_table_main.cc:
//   make featured glyph conversion table from GSUB ligature substitution
//
// Copyright (C) 2020 Masamichi Hosoda.
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

#include <algorithm>
#include <exception>
#include <iomanip>
#include <iostream>
#include <map>

#include <pugixml.hpp>

#include "aj1x-gsub-ligature.hh"
#include "conv_table.hh"
#include "gsub_ligature.hh"
#include "version.hh"

int main (int argc, char *argv[])
{
  std::cout
    << "# make_ligature_table: Harano Aji Fonts generator " << version
    << std::endl
    << "# (make featured glyph conversion table from"
    " GSUB ligature substitution)"
    << std::endl
    << "# Copyright (C) 2020 Masamichi Hosoda" << std::endl
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

  gsub_ligature gl;
  try
    {
      gl.load (doc, argv[2]);
    }
  catch (std::exception &e)
    {
      std::cerr << "error: gsub_ligature::load: std::exception: " << e.what ()
                << std::endl;
      return 1;
    }

  aj1x_gsub_ligature al;
  try
    {
      al.load (argv[4], argv[2]);
    }
  catch (std::exception &e)
    {
      std::cerr << "error: aj1x_gsub_ligature::load: std::exception: "
                << e.what ()
                << std::endl;
      return 1;
    }

  std::cout << "#" <<std::endl
            << "# GSUB" << std::endl
            << "#" << std::endl;
  for (auto &m: gl.get_map ())
    {
      std::cout << "# ";
      for (auto cid: m.first)
        {
          std::cout << "CID+" << cid << " ";
        }
      std::cout << "-> CID+" << m.second << std::endl;
    }

  std::cout << "#" <<std::endl
            << "# AJ1x" << std::endl
            << "#" << std::endl;
  for (auto &l: al.get_map ())
    {
      std::cout << "# ";
      for (auto cid: l.first)
        {
          std::cout << "CID+" << cid << " ";
        }
      std::cout << "-> CID+" << l.second << std::endl;
    }

  auto outs = ct.get_cid_outs ();
  for (auto &m: gl.get_map ())
    {
      if (ct.get_map ().find (m.second) != ct.get_map ().end () &&
          std::find (outs.begin (), outs.end (),
                     ct.get_map (). at (m.second)) == outs.end ())
        {
          std::vector<int> aj1_cids;
          for (auto cid: m.first)
            {
              if (ct.get_map ().find (cid) == ct.get_map ().end ())
                {
                  aj1_cids.clear ();
                  break;
                }

              aj1_cids.push_back (ct.get_map ().at (cid));
            }

          if (aj1_cids.size () &&
              al.get_map ().find (aj1_cids) != al.get_map ().end ())
            {
              std::cout << m.second << "\t" << al.get_map ().at (aj1_cids)
                        << std::endl;
            }
        }
    }

  return 0;
}
