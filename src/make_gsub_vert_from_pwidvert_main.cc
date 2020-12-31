//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// make_gsub_vert_from_pwidvert_main.cc:
//   Make GSUB vert table from pwidvert copying table
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

#include <exception>
#include <iomanip>
#include <iostream>
#include <map>

#include "aj1x-gsub.hh"
#include "copy_and_rotate_table.hh"
#include "version.hh"

int main (int argc, char *argv[])
{
  std::cout
    << "# make_gsub_vert_from_pwidvert: Harano Aji Fonts generator " << version
    << std::endl
    << "# (Make GSUB vert table from pwidvert copying table)"
    << std::endl
    << "# Copyright (C) 2020 Masamichi Hosoda" << std::endl
    << "# https://github.com/trueroad/HaranoAjiFonts-generator" << std::endl
    << "#" << std::endl;

  if (argc != 3)
    {
      std::cerr
        << "usage: make_gsub_vert_from_pwidvert"
        " VPAL_TO_PWIDVERT_COPY.TBL GSUB.FEA \\" << std::endl
        << "           > FEATURE_VERT_FROM_PWIDVERT.TBL" << std::endl
        << std::endl
        << "  (in)  VPAL_TO_PWIDVERT_COPY.TBL:" << std::endl
        << "        pwidvert copying table." << std::endl
        << "  (in)  GSUB.FEA:" << std::endl
        << "        AJ1 GSUB feature file (e.g. aj17-gsub-jp04.fea)"
        << std::endl;
      return 1;
    }

  std::string copy_and_rotate_filename = argv[1];
  std::string aj1_gsub_feature_filename = argv[2];
  
  std::cout
    << "# inputs:" << std::endl
    << "#     pwidvert copying table: \"" << copy_and_rotate_filename << "\""
    << std::endl
    << "#     AJ1 GSUB feature  file: \"" << aj1_gsub_feature_filename << "\""
    << std::endl
    << "#" << std::endl;

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
      ag.load (aj1_gsub_feature_filename, "vert");
    }
  catch (std::exception &e)
    {
      std::cerr << "error: aj1x_gsub::load: std::exception: " << e.what ()
                << std::endl;
      return 1;
    }

  for (const auto &cr_entry: cr.get_map ())
    {
      auto cid_out = (cr_entry.second).first;
      if (ag.get_rev ().find (cid_out) !=
          ag.get_rev ().end ())
        {
          auto cid_in = ag.get_rev ().at (cid_out);
          std::cout
            << "aji"
            << std::setw (5) << std::setfill ('0')
            << cid_in
            << "\taji"
            << std::setw (5) << std::setfill ('0')
            << cid_out
            << "\t0"
            << std::endl;
        }
    }

  return 0;
}
