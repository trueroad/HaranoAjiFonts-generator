//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// make_vkana_table_main.cc:
//   Make VKana table
//
// Copyright (C) 2020, 2023 Masamichi Hosoda.
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
#include <fstream>
#include <iomanip>
#include <iostream>
#include <map>
#include <utility>
#include <vector>

#include <pugixml.hpp>

#include "aj1x-gsub.hh"
#include "aj1x-kana.hh"
#include "calc_width.hh"
#include "conv_table.hh"
#include "gsub_single.hh"
#include "version.hh"

int main (int argc, char *argv[])
{
  std::cout
    << "make_vkana_table: Harano Aji Fonts generator " << version
    << std::endl
    << "(Make VKana table)"
    << std::endl
    << "Copyright (C) 2020, 2023 Masamichi Hosoda"
    << std::endl
    << "https://github.com/trueroad/HaranoAjiFonts-generator"
    << std::endl << std::endl;

  if (argc != 7)
    {
      std::cerr
        << "usage: make_vkana_table TABLE.TBL FONT.G_S_U_B_.ttx GSUB.FEA \\"
        << std::endl
        << "       TABLE_VKANA.TBL COPY_VKANA.TBL FEATURE_VKNA.TBL"
        << std::endl
        << std::endl
        << "   (in)  TABLE.TBL:" << std::endl
        << "         conversion table." << std::endl
        << "   (in)  FONT.G_S_U_B_.ttx:" << std::endl
        << "         The ttx file of the GSUB table extracted" << std::endl
        << "         from the original font file." << std::endl
        << "   (in)  GSUB.FEA:" << std::endl
        << "         GSUB feature file (e.g. aj17-gsub-jp04.fea)" << std::endl
        << "   (out) TABLE_VKANA.TBL:" << std::endl
        << "         VKana conversion table." << std::endl
        << "   (out) COPY_VKANA.TBL:" << std::endl
        << "         VKana copy and rotate table." << std::endl
        << "   (out) FEATURE_VKNA.TBL:" << std::endl
        << "         GSUB vkna table." << std::endl
        << std::endl;
      return 1;
    }

  std::string table_filename = argv[1];
  std::string font_gsub_filename = argv[2];
  std::string aj1_gsub_feature_filename = argv[3];
  std::string table_vkana_filename = argv[4];
  std::string copy_vkana_filename = argv[5];
  std::string feature_vkna_filename = argv[6];

  std::cout
    << "inputs:" << std::endl
    << "    conversion table      : \"" << table_filename << "\""
    << std::endl
    << "    original GSUB ttx     : \"" << font_gsub_filename << "\""
    << std::endl
    << "    AJ1 GSUB feature      : \"" << aj1_gsub_feature_filename << "\""
    << std::endl
    << "outputs:" << std::endl
    << "    VKana conversion table: \"" << table_vkana_filename << "\""
    << std::endl
    << "    VKana copy table      : \"" << copy_vkana_filename << "\""
    << std::endl
    << "    GSUB vkna table       : \"" << feature_vkna_filename << "\""
    << std::endl << std::endl;

  conv_table ct;
  try
    {
      ct.load (table_filename);
    }
  catch (std::exception &e)
    {
      std::cerr << "error: conv_table::load (): std::exception: "
                << e.what () << std::endl;
      return 1;
    }

  pugi::xml_document doc;
  auto result = doc.load_file (font_gsub_filename.c_str ());
  if (!result)
    {
      std::cerr << "error: filename \"" << argv[3]
                << "\": " << result.description () << std::endl;
      return 1;
    }

  gsub_single gs;
  try
    {
      gs.load (doc, "vert");
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
      ag.load (aj1_gsub_feature_filename, "vkna");
    }
  catch (std::exception &e)
    {
      std::cerr << "error: aj1x_gsub::load: std::exception: " << e.what ()
                << std::endl;
      return 1;
    }

  calc_width cw ("AJ1");

  std::ofstream ofs_table (table_vkana_filename);
  std::ofstream ofs_copy (copy_vkana_filename);
  std::ofstream ofs_feature (feature_vkna_filename);

  for (const auto &p: ag.get_map ())
    {
      const int cid_aj1_vkna_in = p.first;
      const int cid_aj1_vkna_out = p.second;

      if (std::find (ct.get_cid_outs ().begin (),
                     ct.get_cid_outs ().end (),
                     cid_aj1_vkna_out) != ct.get_cid_outs ().end ())
        {
          std::cout << "already exists vkna out: AJ1 CID+"
                    << cid_aj1_vkna_in
                    << " -(vkna)-> AJ1 CID+"
                    << cid_aj1_vkna_out
                    << std::endl;
          continue;
        }

      if (std::find (ct.get_cid_outs ().begin (),
                     ct.get_cid_outs ().end (),
                     p.first) == ct.get_cid_outs ().end ())
        {
          std::cout << "missing vkna in: AJ1 CID+"
                    << cid_aj1_vkna_in
                    << " -(vkna)-> AJ1 CID+"
                    << cid_aj1_vkna_out
                    << std::endl;
          continue;
        }

      int cid_ai0 = -1;
      for (const auto &m: ct.get_map ())
        {
          if (m.second == cid_aj1_vkna_in)
            {
              cid_ai0 = m.first;
              break;
            }
        }
      if (cid_ai0 < 0)
        {
          std::cerr << "error: can't find AI0 CID from AJ1 CID+"
                    << cid_aj1_vkna_in
                    << std::endl;
          return 1;
        }

      int cid_ai0_from;
      if (is_aj1x_kana_fullwidth_h (cid_aj1_vkna_in) &&
          gs.get_map ().find (cid_ai0) != gs.get_map ().end ())
        {
          cid_ai0_from = gs.get_map ().at (cid_ai0);
          std::cout
            << "AI0 CID+"
            << cid_ai0_from
            << " -(vert rev)-> AI0 CID+"
            << cid_ai0
            << " -(conv table)->"
            << std::endl
            << "    AJ1 CID+"
            << cid_aj1_vkna_in
            << " -(vkna)-> AJ1 CID+"
            << cid_aj1_vkna_out
            << std::endl;
        }
      else if (is_aj1x_kana_fullwidth_v (cid_aj1_vkna_in))
        {
          cid_ai0_from = cid_ai0;
          std::cout
            << "(vert) AI0 CID+"
            << cid_ai0_from
            << " -(conv table)->"
            << std::endl
            << "    AJ1 CID+"
            << cid_aj1_vkna_in
            << " -(vkna)-> AJ1 CID+"
            << cid_aj1_vkna_out
            << std::endl;
        }
      else
        {
          std::cout
            << "unknown Kana type: AJ1 CID+"
            << cid_aj1_vkna_in
            << std::endl;
          continue;
        }

      if (ct.get_map ().at (cid_ai0_from) < 0)
        {
          std::cout << "    convert" << std::endl;
          ofs_table << cid_ai0_from
                    << "\t"
                    << cid_aj1_vkna_out
                    << std::endl;
        }
      else
        {
          int copy_from = ct.get_map ().at (cid_ai0_from);
          std::cout << "    copy from AJ1 CID+"
                    << copy_from
                    << std::endl;
          ofs_copy << "aji"
                   << std::setw (5) << std::setfill ('0')
                   << copy_from
                   << "\taji"
                   << std::setw (5) << std::setfill ('0')
                   << cid_aj1_vkna_out
                   << "\t0"
                   << std::endl;
        }

      ofs_feature << "aji"
                  << std::setw (5) << std::setfill ('0')
                  << cid_aj1_vkna_in
                  << "\taji"
                  << std::setw (5) << std::setfill ('0')
                  << cid_aj1_vkna_out
                  << "\t0"
                  << std::endl;
    }

  return 0;
}
