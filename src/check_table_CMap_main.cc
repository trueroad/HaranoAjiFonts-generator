//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// check_table_CMap_main.cc:
//   check pre defined CID coverage in conversion table by CMap file
//
// Copyright (C) 2019 Masamichi Hosoda.
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
#include <iostream>
#include <vector>

#include "conv_table.hh"
#include "cmapfile.hh"
#include "version.hh"

int main (int argc, char *argv[])
{
  std::cerr
    << "check_table_CMap: Harano Aji Fonts generator " << version
    << std::endl
    << "(check pre defined CID coverage in conversion table by CMap file)"
    << std::endl
    << "Copyright (C) 2019 Masamichi Hosoda" << std::endl
    << "https://github.com/trueroad/HaranoAjiFonts-generator" << std::endl
    << std::endl;

  if (argc != 3)
    {
      std::cerr
        << "usage: check_table_CMap TABLE.TBL CMAP_FILE"
        << std::endl
        << std::endl
        << "     TABLE.TBL:" << std::endl
        << "         conversion table." << std::endl
        << "     CMAP_FILE:" << std::endl
        << "         The CMap file for CID coverage check." << std::endl
        << "         e.g. H, V, 2004-H, or 2004-V etc." << std::endl;
      return 1;
    }

  std::cerr
    << "inputs:" << std::endl
    << "    conversion table file: \"" << argv[1] << "\""
    << std::endl
    << "    CMap file            : \"" << argv[2] << "\""
    << std::endl << std::endl;

  conv_table ct;
  try
    {
      ct.load (argv[1]);
    }
  catch (std::exception &e)
    {
      std::cerr << "error: conv_table::load (): std::exception: "
                << e.what () << std::endl;
      return 1;
    }

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

  std::map<int, int> miss;
  for (const auto &c: cmf.get_map ())
    {
      if (std::find (ct.get_cid_outs ().begin (), ct.get_cid_outs ().end (),
                     c.second) == ct.get_cid_outs ().end())
        miss.emplace (c.first, c.second);
    }

  if (miss.size ())
    for (const auto &m: miss)
      std::cout << "miss 0x" << std::hex << m.first << std::dec
                << " -> cid " << m.second << std::endl;
  else
    std::cout << "All CIDs exist." << std::endl;

  return 0;
}
