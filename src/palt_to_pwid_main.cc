//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// palt_to_pwid_main.cc:
//   Create tables for `GPOS` palt to `GSUB' pwid conversion
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

#include <fstream>
#include <iomanip>
#include <iostream>
#include <map>
#include <utility>
#include <sstream>
#include <string>

#include <pugixml.hpp>

#include "aj1x-gsub.hh"
#include "conv_table.hh"
#include "gpos_single.hh"
#include "gpos_value.hh"
#include "version.hh"

int main (int argc, char *argv[])
{
  std::cout
    << "palt_to_pwid: Harano Aji Fonts generator " << version
    << std::endl
    << "(Create tables for `GPOS` palt to `GSUB' pwid conversion)"
    << std::endl
    << "Copyright (C) 2020 Masamichi Hosoda"
    << std::endl
    << "https://github.com/trueroad/HaranoAjiFonts-generator"
    << std::endl
    << std::endl;

  if (argc != 7)
    {
      std::cerr
        << "usage: palt_to_pwid TABLE.TBL FONT.G_P_O_S_.ttx GSUB.FEA FONT._h_m_t_x.ttx OUTPUT_COPY.TBL OUTPUT_ADJUST.TBL"
        << std::endl
        << std::endl
        << "   (in)  TABLE.TBL:" << std::endl
        << "         conversion table." << std::endl
        << "   (in)  FONT.G_P_O_S_.ttx:" << std::endl
        << "         The ttx file of the GPOS table extracted" << std::endl
        << "         from the original font file." << std::endl
        << "   (in)  GSUB.FEA:" << std::endl
        << "         GSUB feature file (e.g. aj17-gsub-jp04.fea)" << std::endl
        << "   (in)  FONT._h_m_t_x.ttx:" << std::endl
        << "         The ttx file of the hmtx table extracted" << std::endl
        << "         from the original font file." << std::endl
        << "   (out) OUT_COPY.TBL:" << std::endl
        << "         Output copy & rotate table" << std::endl
        << "   (out) OUT_ADJUST.TBL:" << std::endl
        << "         Output adjust table" << std::endl
        << std::endl;
      return 1;
    }

  std::string table_filename = argv[1];
  std::string ai0_gpos_filename = argv[2];
  std::string aj1_gsub_feature_filename = argv[3];
  std::string ai0_hmtx_filename = argv[4];
  std::string copy_tbl_filename = argv[5];
  std::string adjust_tbl_filename = argv [6];

  std::cout
    << "inputs:" << std::endl
    << "    conversion table   : \"" << table_filename << "\""
    << std::endl
    << "    AI0 GPOS table     : \"" << ai0_gpos_filename << "\""
    << std::endl
    << "    AJ1 GSUB feature   : \"" << aj1_gsub_feature_filename << "\""
    << std::endl
    << "    AI0 hmtx table     : \"" << ai0_hmtx_filename << "\""
    << std::endl
    << "outputs:" << std::endl
    << "    copy & rotate table: \"" << copy_tbl_filename << "\""
    << std::endl
    << "    adjust table       : \"" << adjust_tbl_filename << "\""
    << std::endl;

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

  pugi::xml_document doc_GPOS;
  auto result = doc_GPOS.load_file (ai0_gpos_filename.c_str ());
  if (!result)
    {
      std::cerr << "error: filename \"" << ai0_gpos_filename
                << "\": " << result.description () << std::endl;
      return 1;
    }

  gpos_single gs;
  try
    {
      gs.load (doc_GPOS, "palt");
    }
  catch (std::exception &e)
    {
      std::cerr << "error: gpos_single::load: std::exception: " << e.what ()
                << std::endl;
      return 1;
    }

  aj1x_gsub ag;
  try
    {
      ag.load (aj1_gsub_feature_filename, "pwid");
    }
  catch (std::exception &e)
    {
      std::cerr << "error: aj1x_gsub::load: std::exception: " << e.what ()
                << std::endl;
      return 1;
    }

  pugi::xml_document doc_hmtx;
  result = doc_hmtx.load_file (ai0_hmtx_filename.c_str ());
  if (!result)
    {
      std::cerr << "error: filename \"" << ai0_hmtx_filename
                << "\": " << result.description () << std::endl;
      return 1;
    }

  std::ofstream ofs_copy_tbl (copy_tbl_filename);
  ofs_copy_tbl << "# palt_to_pwid" << std::endl;

  std::ofstream ofs_adjust_tbl (adjust_tbl_filename);
  ofs_adjust_tbl << "# palt_to_pwid" << std::endl;

  for (auto &m: gs.get_map ())
    {
      auto ai0_cid = m.first;

      if (ct.get_map ().find (ai0_cid) == ct.get_map ().end ())
        {
          std::cout << "no conversion table: " << ai0_cid << std::endl;
          continue;
        }
      auto aj1_cid = ct.get_map ().at (ai0_cid);
      if (aj1_cid < 0)
        {
          std::cout << "conversion result negative: " << ai0_cid << std::endl;
          continue;
        }

      if (ag.get_map ().find (aj1_cid) == ag.get_map ().end ())
        {
          std::cout << "no gsub: "
                    << ai0_cid << " -> "
                    << aj1_cid << std::endl;
          continue;
        }
      auto aj1_pwid_cid = ag.get_map ().at (aj1_cid);

      if (std::find (ct.get_cid_outs ().begin (),
                     ct.get_cid_outs ().end (),
                     aj1_pwid_cid) != ct.get_cid_outs ().end ())
        {
          std::cout << "pwid exists: "
                    << ai0_cid << " -> "
                    << aj1_cid << " -> "
                    << aj1_pwid_cid << std::endl;
          continue;
        }

      std::cout << ai0_cid << " -> "
                << aj1_cid << " -> "
                << aj1_pwid_cid << std::endl;

      std::stringstream ss;
      ss << "/ttFont/hmtx/mtx[@name='cid"
         << std::setw (5) << std::setfill ('0') << ai0_cid
         << "']";
      auto hmtx_attr = doc_hmtx.select_node (ss.str ().c_str ())
        .node ().attribute ("width");
      if (!hmtx_attr)
        {
          std::cout << "error: failed to get hmtx width" << std::endl;
          continue;
        }
      auto width = hmtx_attr.as_int ();

      auto gv = m.second;
      if (gv.yPlacement || gv.yAdvance)
        {
          std::cout
            << "error: yPlacement or yAdvance not equal zero"
            << std::endl;
        }
      if (!gv.xPlacement && !gv.xAdvance)
        {
          std::cout
            << "error: xPlacement and xAdvance equal zero"
            << std::endl;
          continue;
        }

      ofs_copy_tbl
        << "aji"
        << std::setw (5) << std::setfill ('0')
        << aj1_cid << "\taji"
        << std::setw (5) << std::setfill ('0')
        << aj1_pwid_cid << "\t0"
        << std::endl;
      ofs_adjust_tbl
        << "aji"
        << std::setw (5) << std::setfill ('0')
        << aj1_pwid_cid << "\t"
        << width + gv.xAdvance << "\t"
        << gv.xPlacement << "\t0\t1\t1"
        << std::endl;
    }

  return 0;
}
