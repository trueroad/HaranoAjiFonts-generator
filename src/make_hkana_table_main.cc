//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// make_hkana_table_main.cc:
//   Make horizontal Kana table
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

#include "aj1x-gsub.hh"
#include "aj1x-kana.hh"
#include "conv_table.hh"
#include "version.hh"

int main (int argc, char *argv[])
{
  std::cout
    << "make_hkana_table: Harano Aji Fonts generator " << version
    << std::endl
    << "(Make horizontal Kana table)"
    << std::endl
    << "Copyright (C) 2020, 2023 Masamichi Hosoda"
    << std::endl
    << "https://github.com/trueroad/HaranoAjiFonts-generator"
    << std::endl << std::endl;

  if (argc != 5)
    {
      std::cerr
        << "usage: make_hkana_table TABLE.TBL GSUB.FEA \\"
        << std::endl
        << "       COPY_HKANA.TBL FEATURE_HKNA.TBL"
        << std::endl
        << std::endl
        << "   (in)  TABLE.TBL:" << std::endl
        << "         conversion table." << std::endl
        << "   (in)  GSUB.FEA:" << std::endl
        << "         GSUB feature file (e.g. aj17-gsub-jp04.fea)" << std::endl
        << "   (out) COPY_HKANA.TBL:" << std::endl
        << "         Horizontal Kana copy and rotate table." << std::endl
        << "   (out) FEATURE_HKNA.TBL:" << std::endl
        << "         GSUB hkna table." << std::endl
        << std::endl;
      return 1;
    }

  std::string table_filename = argv[1];
  std::string aj1_gsub_feature_filename = argv[2];
  std::string copy_hkana_filename = argv[3];
  std::string feature_hkna_filename = argv[4];

  std::cout
    << "inputs:" << std::endl
    << "    conversion table          : \"" << table_filename << "\""
    << std::endl
    << "    AJ1 GSUB feature          : \"" << aj1_gsub_feature_filename << "\""
    << std::endl
    << "outputs:" << std::endl
    << "    Horizontal Kana copy table: \"" << copy_hkana_filename << "\""
    << std::endl
    << "    GSUB hkna table           : \"" << feature_hkna_filename << "\""
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

  aj1x_gsub ag;
  try
    {
      ag.load (aj1_gsub_feature_filename, "hkna");
    }
  catch (std::exception &e)
    {
      std::cerr << "error: aj1x_gsub::load: std::exception: " << e.what ()
                << std::endl;
      return 1;
    }

  std::ofstream ofs_copy (copy_hkana_filename);
  std::ofstream ofs_feature (feature_hkna_filename);

  for (const auto &p: ag.get_map ())
    {
      const int cid_aj1_hkna_in = p.first;
      const int cid_aj1_hkna_out = p.second;

      if (std::find (ct.get_cid_outs ().begin (),
                     ct.get_cid_outs ().end (),
                     cid_aj1_hkna_out) != ct.get_cid_outs ().end ())
        {
          std::cout << "already exists hkna out: AJ1 CID+"
                    << cid_aj1_hkna_in
                    << " -(hkna)-> AJ1 CID+"
                    << cid_aj1_hkna_out
                    << std::endl;
          continue;
        }

      if (std::find (ct.get_cid_outs ().begin (),
                     ct.get_cid_outs ().end (),
                     p.first) == ct.get_cid_outs ().end ())
        {
          std::cout << "missing hkna in: AJ1 CID+"
                    << cid_aj1_hkna_in
                    << " -(hkna)-> AJ1 CID+"
                    << cid_aj1_hkna_out
                    << std::endl;
          continue;
        }

      ofs_copy << "aji"
               << std::setw (5) << std::setfill ('0')
               << cid_aj1_hkna_in
               << "\taji"
               << std::setw (5) << std::setfill ('0')
               << cid_aj1_hkna_out
               << "\t0"
               << std::endl;

      ofs_feature << "aji"
                  << std::setw (5) << std::setfill ('0')
                  << cid_aj1_hkna_in
                  << "\taji"
                  << std::setw (5) << std::setfill ('0')
                  << cid_aj1_hkna_out
                  << "\t0"
                  << std::endl;
    }

  return 0;
}
