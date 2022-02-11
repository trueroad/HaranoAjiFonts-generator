//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// make_conv_table_main.cc:
//   make conversion table from original font CID to pre-defined CID
//
// Copyright (C) 2019, 2022 Masamichi Hosoda.
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
#include <utility>

#include "cmapfile.hh"
#include "fontcmap_reverse.hh"
#include "prefer_unicode.hh"
#include "version.hh"

int main (int argc, char *argv[])
{
  std::cout
    << "# make_conv_table: Harano Aji Fonts generator " << version
    << std::endl
    << "# (make conversion table from original font CID to pre-defined CID)"
    << std::endl
    << "# Copyright (C) 2019, 2022 Masamichi Hosoda" << std::endl
    << "# https://github.com/trueroad/HaranoAjiFonts-generator" << std::endl
    << "#" << std::endl;

  if (argc != 3)
    {
      std::cout
        << "# usage: make_conv_table FONT._c_m_a_p.ttx CMAP_FILE > TABLE.TBL"
        << std::endl
        << "#" << std::endl
        << "#     FONT._c_m_a_p.ttx:" << std::endl
        << "#         The ttx file of the cmap table extracted" << std::endl
        << "#         from the original font file." << std::endl
        << "#     CMAP_FILE:" << std::endl
        << "#         The CMap file of the pre-defined CID." << std::endl
        << "#         e.g. UniJIS2004-UTF32-H etc." << std::endl;
      return 1;
    }

  std::cout
    << "# inputs:" << std::endl
    << "#     original font cmap ttx file: \"" << argv[1] << "\""
    << std::endl
    << "#     pre-defined CID's CMap file: \"" << argv[2] << "\""
    << std::endl
    << "#" << std::endl;

  cmapfile cmf;
  try
    {
      cmf.load (argv[2]);
    }
  catch (std::exception &e)
    {
      std::cerr << "error: cmapfile: std::exception: " << e.what ()
                << std::endl;
      return 1;
    }

  fontcmap_reverse fcr;
  try
    {
      fcr.load_ttx (argv[1], cmf);
    }
  catch (std::exception &e)
    {
      std::cerr << "error: fontcmap_reverse: std::exception: " << e.what ()
                << std::endl;
      return 1;
    }

  std::map<int, int> map;
  std::map<int, int> dup;
  for (const auto &m: fcr.get_map ())
    {
      auto cid_in = m.first;
      auto uni = m.second;

      if (cmf.get_map ().find (uni) != cmf.get_map ().end ())
        {
          auto cid_out = cmf.get_map ().at (uni);

          if (dup.find (cid_out) != dup.end ())
            {
              auto bf_uni = fcr.get_map ().at (dup[cid_out]);
              auto prefer = prefer_unicode (bf_uni, uni, cmf);
              std::cout << "#duplicate: cid " << dup[cid_out]
                        << " (U+"
                        << std::setw (4) << std::setfill ('0')
                        << std::hex << std::uppercase
                        << bf_uni
                        << std::dec;
              if (prefer == bf_uni)
                std::cout << " preferred";
              std::cout << "), cid "
                        << cid_in
                        << " (U+"
                        << std::setw (4) << std::hex
                        << uni
                        << std::nouppercase << std::dec
                        << std::setfill (' ');
              if (prefer == uni)
                std::cout << " preferred";
              std::cout <<  ") -> cid "
                        << cid_out << std::endl;
              if (prefer == bf_uni)
                map[cid_in] = -1;
              else if (prefer == uni)
                {
                  map[dup[cid_out]] = -1;
                  map[cid_in] = cid_out;
                  dup[cid_out] = cid_in;
                }
            }
          else
            {
              map[cid_in] = cid_out;
              dup[cid_out] = cid_in;
            }
        }
      else
        map[cid_in] = -1;
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
