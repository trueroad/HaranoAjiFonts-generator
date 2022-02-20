//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// make_kana_pwid_table_main.cc:
//   Make AJ1 Kana pwid table
//
// Copyright (C) 2020, 2022 Masamichi Hosoda.
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
#include "aj1x-kana.hh"
#include "calc_width.hh"
#include "conv_table.hh"
#include "version.hh"

int main (int argc, char *argv[])
{
  std::cout
    << "# make_kana_pwid_table: Harano Aji Fonts generator " << version
    << std::endl
    << "# (Make AJ1 Kana pwid table)"
    << std::endl
    << "# Copyright (C) 2020 Masamichi Hosoda"
    << std::endl
    << "# https://github.com/trueroad/HaranoAjiFonts-generator"
    << std::endl
    << "#"
    << std::endl;

  if (argc != 3)
    {
      std::cerr
        << "usage: make_kana_pwid_table TABLE.TBL GSUB.FEA > KANA_PWID.TBL"
        << std::endl
        << std::endl
        << "   (in)  TABLE.TBL:" << std::endl
        << "         conversion table." << std::endl
        << "   (in)  GSUB.FEA:" << std::endl
        << "         GSUB feature file (e.g. aj17-gsub-jp04.fea)" << std::endl
        << std::endl;
      return 1;
    }

  std::string table_filename = argv[1];
  std::string aj1_gsub_feature_filename = argv[2];

  std::cout
    << "# inputs:" << std::endl
    << "#     conversion table   : \"" << table_filename << "\""
    << std::endl
    << "#     AJ1 GSUB feature   : \"" << aj1_gsub_feature_filename << "\""
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

  calc_width cw ("AJ1");

  for (const auto &p: ag.get_map ())
    {
      if (cw.get_width (p.first) == 1000 &&
          is_aj1x_kana_propotional_with_similar_h (p.second) &&
          std::find (ct.get_cid_outs ().begin (),
                     ct.get_cid_outs ().end (),
                     p.first) != ct.get_cid_outs ().end ())
        {
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
    }

  return 0;
}
