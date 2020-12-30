//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// make_gsub_single_table_main.cc:
//   Make GSUB single table
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
#include <utility>
#include <vector>

#include "aj1x-gsub.hh"
#include "copy_and_rotate_table.hh"
#include "conv_table.hh"
#include "version.hh"

int main (int argc, char *argv[])
{
  std::cout
    << "# make_gsub_single_table: Harano Aji Fonts generator " << version
    << std::endl
    << "# (Make GSUB single table)"
    << std::endl
    << "# Copyright (C) 2020 Masamichi Hosoda"
    << std::endl
    << "# https://github.com/trueroad/HaranoAjiFonts-generator"
    << std::endl
    << "#"
    << std::endl;

  if (argc != 5)
    {
      std::cerr
        << "usage: make_gsub_single_table FEATURE TABLE.TBL "
        "COPY_AND_ROTATE.TBL \\"
        << std::endl
        << "           GSUB.FEA > FEATURE.TBL"
        << std::endl
        << std::endl
        << "   (in)  FEATURE  :" << std::endl
        << "         GSUB feature name." << std::endl
        << "   (in)  TABLE.TBL:" << std::endl
        << "         conversion table." << std::endl
        << "   (in)  COPY_AND_ROTATE.TBL:" << std::endl
        << "         copy and rotate table." << std::endl
        << "   (in)  GSUB.FEA:" << std::endl
        << "         GSUB feature file (e.g. aj17-gsub-jp04.fea)" << std::endl
        << std::endl;
      return 1;
    }

  std::string feature_name = argv[1];
  std::string table_filename = argv[2];
  std::string copy_and_rotate_filename = argv[3];
  std::string aj1_gsub_feature_filename = argv[4];

  std::cout
    << "# inputs:" << std::endl
    << "#     GSUB feature name    : \"" << feature_name << "\""
    << std::endl
    << "#     conversion table     : \"" << table_filename << "\""
    << std::endl
    << "#     copy and rotate table: \"" << copy_and_rotate_filename << "\""
    << std::endl
    << "#     AJ1 GSUB feature     : \"" << aj1_gsub_feature_filename << "\""
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

  copy_and_rotate_table cr;
  try
    {
      cr.load (copy_and_rotate_filename);
    }
  catch (std::exception &e)
    {
      std::cerr << "error: copy_and_rotate_table::load (): std::exception: "
                << e.what () << std::endl;
      return 1;
    }

  aj1x_gsub ag;
  try
    {
      ag.load (aj1_gsub_feature_filename, feature_name);
    }
  catch (std::exception &e)
    {
      std::cerr << "error: aj1x_gsub::load: std::exception: " << e.what ()
                << std::endl;
      return 1;
    }

  for (const auto &p: ag.get_map ())
    {
      bool b_miss_in = std::find (ct.get_cid_outs ().begin (),
                                  ct.get_cid_outs ().end (),
                                  p.first) == ct.get_cid_outs ().end () &&
        std::find (cr.get_cid_outs ().begin (),
                   cr.get_cid_outs ().end (),
                   p.first) == cr.get_cid_outs ().end ();
      bool b_miss_out = std::find (ct.get_cid_outs ().begin (),
                                   ct.get_cid_outs ().end (),
                                   p.second) == ct.get_cid_outs ().end () &&
        std::find (cr.get_cid_outs ().begin (),
                   cr.get_cid_outs ().end (),
                   p.second) == cr.get_cid_outs ().end ();

      if (b_miss_in && b_miss_out)
        {
          std::cout
            << "# missing both CIDs: CID+"
            << p.first
            << " -> CID+"
            << p.second
            << std::endl;
          continue;
        }
      if (b_miss_in)
        {
          std::cout
            << "# missing CID in: CID+"
            << p.first
            << " but adding entry"
            << std::endl;
        }
      if (b_miss_out)
        {
          std::cout
            << "# missing CID out: CID+"
            << p.first
            << " -> CID+"
            << p.second
            << std::endl;
          continue;
        }

      std::cout
        << "aji"
        << std::setw (5) << std::setfill ('0')
        << p.first
        << "\taji"
        << std::setw (5) << std::setfill ('0')
        << p.second
        << "\t0"
        << std::endl;
    }

  return 0;
}
