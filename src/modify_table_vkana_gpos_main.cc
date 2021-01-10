//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// modify_table_vkana_gpos_main.cc:
//   Modify conversion table for VKana GPOS
//
// Copyright (C) 2021 Masamichi Hosoda.
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
#include <iostream>
#include <string>

#include "aj1x-gsub.hh"
#include "aj1x-kana.hh"
#include "conv_table.hh"
#include "version.hh"

namespace
{
  void output_line (int in, int out)
  {
    std::cout << in;
    if (out >= 0)
      std::cout << "\t"
                << out;
    std::cout << std::endl;
  }
};

int main (int argc, char *argv[])
{
  std::cout
    << "# modify_table_vkana_gpos: Harano Aji Fonts generator "
    << version
    << std::endl
    << "# (Modify conversion table for VKana GPOS)"
    << std::endl
    << "# Copyright (C) 2021 Masamichi Hosoda" << std::endl
    << "# https://github.com/trueroad/HaranoAjiFonts-generator" << std::endl
    << "#" << std::endl;

  if (argc != 3)
    {
      std::cout
        << "# usage: modify_table_vkana_gpos TABLE_IN.TBL GSUB.FEA \\"
        "#        > TABLE_OUT.TBL"
        << "#" << std::endl
        << "#" << std::endl
        << "#    (in)  TABLE_IN.TBL:" << std::endl
        << "#          conversion table." << std::endl
        << "#    (in)  GSUB.FEA:" << std::endl
        << "#          GSUB feature file (e.g. aj17-gsub-jp04.fea)"
        << std::endl
        << "#    (out) TABLE_OUT.TBL:" << std::endl
        << "#          conversion table." << std::endl;
      return 1;
    }

  const std::string table_filename = argv[1];
  const std::string aj1_gsub_feature_filename = argv[2];

  std::cout
    << "# input:" << std::endl
    << "#     conversion table file: \"" << table_filename << "\""
    << std::endl
    << "#     AJ1 GSUB feature     : \"" << aj1_gsub_feature_filename << "\""
    << std::endl
    << "#"
    << std::endl;

  conv_table ct;
  try
    {
      ct.load (table_filename);
    }
  catch (std::exception &e)
    {
      std::cerr << "error: conv_table::load (): std::exception: " << e.what ()
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

  for (const auto &m: ct.get_map ())
    {
      const auto cid_in = m.first;
      const auto cid_out = m.second;

      if (is_aj1x_kana_fullwidth_v (cid_out))
        {
          if (ag_vkna.get_map ().find (cid_out) != ag_vkna.get_map ().end ())
            {
              const auto cid_vkna = ag_vkna.get_map ().at (cid_out);
              std::cout << "# ";
              output_line (cid_in, cid_out);
              output_line (cid_in, cid_vkna);
            }
          else
            {
              if (ag_vert.get_rev ().find (cid_out) !=
                  ag_vert.get_rev ().end ())
                {
                  const auto cid_h = ag_vert.get_rev ().at (cid_out);

                  if (ag_vkna.get_map ().find (cid_h) !=
                      ag_vkna.get_map ().end ())
                    {
                      const auto cid_h_vkna = ag_vkna.get_map ().at (cid_h);
                      std::cout << "# ";
                      output_line (cid_in, cid_out);
                      output_line (cid_in, cid_h_vkna);
                      std::cerr << "warning: direct vkna miss: AI0 CID+"
                                << cid_in
                                << " -> AJ1 CID+"
                                << cid_out
                                << " -(rev vert)-> CID+"
                                << cid_h
                                << " -(vkna)-> CID+"
                                << cid_h_vkna
                                << std::endl;
                    }
                  else
                    {
                      output_line (cid_in, cid_out);
                      std::cerr << "warning: both vkna miss: AI0 CID+"
                                << cid_in
                                << " -> AJ1 CID+"
                                << cid_out
                                << " -(rev vert)-> CID+"
                                << cid_h
                                << " -(vkna)-> miss"
                                << std::endl;
                    }
                }
              else
                {
                  output_line (cid_in, cid_out);
                  std::cerr << "warning: vkna and rev vert miss: AI0 CID+"
                            << cid_in
                            << " -> AJ1 CID+"
                            << cid_out
                            << " -(vkna/rev vert)-> miss"
                            << std::endl;
                }
            }
        }
      else
        output_line (cid_in, cid_out);
    }

  return 0;
}
