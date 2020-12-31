//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// vpal_to_pwidvert_main.cc:
//   Create tables for `GPOS` vpal to `GSUB' pwid vert conversion
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

#include "aj1x-kana.hh"
#include "aj1x-gsub.hh"
#include "conv_table.hh"
#include "gpos_single.hh"
#include "gpos_value.hh"
#include "version.hh"

int main (int argc, char *argv[])
{
  std::cout
    << "vpal_to_pwidvert: Harano Aji Fonts generator " << version
    << std::endl
    << "(Create tables for `GPOS` vpal to `GSUB' pwid vert conversion)"
    << std::endl
    << "Copyright (C) 2020 Masamichi Hosoda"
    << std::endl
    << "https://github.com/trueroad/HaranoAjiFonts-generator"
    << std::endl
    << std::endl;

  if (argc != 9)
    {
      std::cerr
        << "usage: vpalt_to_pwidvert TABLE.TBL FONT.G_P_O_S_.ttx GSUB.FEA FONT._h_m_t_x.ttx FONT._v_m_t_x.ttx OUTPUT_COPY.TBL OUTPUT_ADJUST.TBL OUTPUT_HEIGHT.TBL"
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
        << "   (in)  FONT._v_m_t_x.ttx:" << std::endl
        << "         The ttx file of the vmtx table extracted" << std::endl
        << "         from the original font file." << std::endl
        << "   (out) OUT_COPY.TBL:" << std::endl
        << "         Output copy & rotate table" << std::endl
        << "   (out) OUT_ADJUST.TBL:" << std::endl
        << "         Output adjust table" << std::endl
        << "   (out) OUT_HEIGHT.TBL:" << std::endl
        << "         Output height table" << std::endl
        << std::endl;
      return 1;
    }

  std::string table_filename = argv[1];
  std::string ai0_gpos_filename = argv[2];
  std::string aj1_gsub_feature_filename = argv[3];
  std::string ai0_hmtx_filename = argv[4];
  std::string ai0_vmtx_filename = argv[5];
  std::string copy_tbl_filename = argv[6];
  std::string adjust_tbl_filename = argv [7];
  std::string height_tbl_filename = argv [8];

  std::cout
    << "inputs:" << std::endl
    << "    TABLE.TBL          : \"" << table_filename << "\""
    << std::endl
    << "    AI0 GPOS table     : \"" << ai0_gpos_filename << "\""
    << std::endl
    << "    AJ1 GSUB feature   : \"" << aj1_gsub_feature_filename << "\""
    << std::endl
    << "    AI0 hmtx table     : \"" << ai0_hmtx_filename << "\""
    << std::endl
    << "    AI0 vmtx table     : \"" << ai0_vmtx_filename << "\""
    << std::endl
    << "outputs:" << std::endl
    << "    copy & rotate table: \"" << copy_tbl_filename << "\""
    << std::endl
    << "    adjust table       : \"" << adjust_tbl_filename << "\""
    << std::endl
    << "    height table       : \"" << height_tbl_filename << "\""
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
      gs.load (doc_GPOS, "vpal");
    }
  catch (std::exception &e)
    {
      std::cerr << "error: gpos_single::load: std::exception: " << e.what ()
                << std::endl;
      return 1;
    }

  aj1x_gsub ag_vert;
  try
    {
      ag_vert.load (aj1_gsub_feature_filename, "vert");
    }
  catch (std::exception &e)
    {
      std::cerr << "error: aj1x_gsub::load: std::exception: " << e.what ()
                << std::endl;
      return 1;
    }

  aj1x_gsub ag_vkna;
  try
    {
      ag_vkna.load (aj1_gsub_feature_filename, "vkna");
    }
  catch (std::exception &e)
    {
      std::cerr << "error: aj1x_gsub::load: std::exception: " << e.what ()
                << std::endl;
      return 1;
    }

  aj1x_gsub ag_pwid;
  try
    {
      ag_pwid.load (aj1_gsub_feature_filename, "pwid");
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

  pugi::xml_document doc_vmtx;
  result = doc_vmtx.load_file (ai0_vmtx_filename.c_str ());
  if (!result)
    {
      std::cerr << "error: filename \"" << ai0_vmtx_filename
                << "\": " << result.description () << std::endl;
      return 1;
    }

  std::ofstream ofs_copy_tbl (copy_tbl_filename);
  ofs_copy_tbl << "# vpal_to_pwidvert" << std::endl;

  std::ofstream ofs_adjust_tbl (adjust_tbl_filename);
  ofs_adjust_tbl << "# vpal_to_pwidvert" << std::endl;

  std::ofstream ofs_height_tbl (height_tbl_filename);
  ofs_height_tbl << "# vpal_to_pwidvert" << std::endl;

  for (auto &m: gs.get_map ())
    {
      auto ai0_cid_vpal = m.first;

      // For source AJ1 CID
      if (ct.get_map ().find (ai0_cid_vpal) == ct.get_map ().end ())
        {
          std::cout
            << "no conversion table: vpal AI0 CID+"
            << " -> miss"
            << std::endl;
          continue;
        }
      auto aj1_cid_src = ct.get_map ().at (ai0_cid_vpal);
      if (aj1_cid_src < 0)
        {
          std::cout
            << "missing conversion table: vpal AI0 CID+"
            << ai0_cid_vpal
            << " -> miss"
            << std::endl;
          continue;
        }

      std::cout
        << "SRC: vpal AI0 CID+"
        << ai0_cid_vpal
        << " -> AJ1 CID+"
        << aj1_cid_src
        << std::endl;

      // For destination AJ1 CID
      int aj1_cid_base;
      std::string vknavert;
      if (is_aj1x_kana_tuned_v (aj1_cid_src) &&
          ag_vkna.get_rev ().find (aj1_cid_src) !=
          ag_vkna.get_rev ().end ())
        {
          aj1_cid_base = ag_vkna.get_rev ().at (aj1_cid_src);
          vknavert = "vkna";
        }
      else if (ag_vert.get_rev ().find (aj1_cid_src) !=
               ag_vert.get_rev ().end ())
        {
          aj1_cid_base = ag_vert.get_rev ().at (aj1_cid_src);
          vknavert = "vert";
        }
      else
        {
          std::cout
            << "can't find AJ1 base: SRC AJ1 CID+"
            << aj1_cid_src
            << " -(rev vkna/vert)-> miss"
            << std::endl;
          continue;
        }

      if (ag_pwid.get_map ().find (aj1_cid_base) == ag_pwid.get_map ().end ())
        {
          std::cout
            << "no gsub pwid: SRC AJ1 CID+"
            << aj1_cid_src
            << " -(rev "
            << vknavert
            << ")-> AJ1 CID+"
            << aj1_cid_base
            << " -(pwid)-> miss"
            << std::endl;
          continue;
        }
      auto aj1_cid_pwid = ag_pwid.get_map ().at (aj1_cid_base);

      if (ag_vert.get_map ().find (aj1_cid_pwid) == ag_vert.get_map ().end ())
        {
          std::cout
            << "no gsub vert: SRC AJ1 CID+"
            << aj1_cid_src
            << " -(rev "
            << vknavert
            << ")-> AJ1 CID+"
            << aj1_cid_base
            << " -(pwid)-> AJ1 CID+"
            << aj1_cid_pwid
            << " -(vert)-> miss"
            << std::endl;
          continue;
        }
      auto aj1_cid_dst = ag_vert.get_map ().at (aj1_cid_pwid);

      std::cout
        << "DST: SRC AJ1 CID+"
        << aj1_cid_src
        << " -(rev "
        << vknavert
        << ")-> AJ1 CID+"
        << aj1_cid_base
        << " -(pwid)-> AJ1 CID+"
        << aj1_cid_pwid
        << " -(vert)-> AJ1 CID+"
        << aj1_cid_dst
        << std::endl;

      std::stringstream ss_h;
      ss_h << "/ttFont/hmtx/mtx[@name='cid"
           << std::setw (5) << std::setfill ('0') << ai0_cid_vpal
           << "']";
      auto hmtx_attr = doc_hmtx.select_node (ss_h.str ().c_str ())
        .node ().attribute ("width");
      if (!hmtx_attr)
        {
          std::cout << "error: failed to get hmtx width" << std::endl;
          continue;
        }
      auto width = hmtx_attr.as_int ();

      std::stringstream ss_v;
      ss_v << "/ttFont/vmtx/mtx[@name='cid"
           << std::setw (5) << std::setfill ('0') << ai0_cid_vpal
           << "']";
      auto vmtx_attr = doc_vmtx.select_node (ss_v.str ().c_str ())
        .node ().attribute ("height");
      if (!vmtx_attr)
        {
          std::cout << "error: failed to get vmtx height" << std::endl;
          continue;
        }
      auto height = vmtx_attr.as_int ();

      auto gv = m.second;
      if (gv.xPlacement || gv.xAdvance)
        {
          std::cout
            << "error: xPlacement or xAdvance not equal zero"
            << std::endl;
        }
      if (!gv.yPlacement && !gv.yAdvance)
        {
          std::cout
            << "error: yPlacement and yAdvance equal zero"
            << std::endl;
          continue;
        }

      ofs_copy_tbl
        << "aji"
        << std::setw (5) << std::setfill ('0')
        << aj1_cid_src << "\taji"
        << std::setw (5) << std::setfill ('0')
        << aj1_cid_dst << "\t0"
        << std::endl;
      ofs_adjust_tbl
        << "aji"
        << std::setw (5) << std::setfill ('0')
        << aj1_cid_dst << "\t"
        << width << "\t0\t"
        << -gv.yPlacement << "\t1\t1"
        << std::endl;
      ofs_height_tbl
        << "aji"
        << std::setw (5) << std::setfill ('0')
        << aj1_cid_dst << "\t"
        << height + gv.yAdvance
        << std::endl;
    }

  return 0;
}
