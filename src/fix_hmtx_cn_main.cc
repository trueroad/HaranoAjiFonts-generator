//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// fix_hmtx_cn_main.cc:
//   fix AG1 hmtx width
//
// Copyright (C) 2019, 2020 Masamichi Hosoda.
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
#include <string>

#include <pugixml.hpp>

#include "conv_table.hh"
#include "version.hh"

namespace
{
  int ag1_width (int cid)
  {
    if ((    1 <= cid && cid <=    95) ||
        ( 7712 <= cid && cid <=  7715) ||
        (22353 <= cid && cid <= 22354))
      return -1; // pwid
    if ((  814 <= cid && cid <=   939) ||
        ( 7716 <= cid && cid <=  7716) ||
        (22355 <= cid && cid <= 22357))
      return 500; // hwid

    return 1000; // fwid
  }
};

int main (int argc, char *argv[])
{
  std::cerr
    << "# fix_hmtx_cn: Harano Aji Fonts generator " << version
    << "#" << std::endl
    << "# (fix AG1 hmtx width)"
    << "#" << std::endl
    << "# Copyright (C) 2019, 2020 Masamichi Hosoda" << std::endl
    << "# https://github.com/trueroad/HaranoAjiFonts-generator" << std::endl
    << "#" << std::endl;

  if (argc != 3)
    {
      std::cerr
        << "usage: fix_hmtx TABLE.TBL ag1_hmtx.ttx > fixed_ag1_hmtx.ttx"
        << std::endl
        << std::endl
        << "     TABLE.TBL:" << std::endl
        << "         conversion table." << std::endl
        << "     ag1_hmtx.ttx:" << std::endl
        << "         AG1 hmtx table which contains wrong width." << std::endl;
      return 1;
    }

  std::cerr
    << "# inputs:" << std::endl
    << "#     conversion table file: \"" << argv[1] << "\""
    << std::endl
    << "#     ag1_hmtx filename: \"" << argv[2] << "\""
    << std::endl
    << "#" << std::endl;

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

  pugi::xml_document doc;

  auto result = doc.load_file (argv[2]);
  if (!result)
    {
      std::cerr << "error: filename \"" << argv[2]
                << "\": " << result.description () << std::endl;
      return 1;
    }

  auto mtx_nodes
    = doc.select_nodes ("/ttFont/hmtx/mtx");

  for (auto it = mtx_nodes.begin ();
       it != mtx_nodes.end ();
       ++it)
    {
      auto mtx_node = it->node ();

      std::string cid_name = mtx_node.attribute ("name").as_string ();

      if (cid_name == ".notdef")
        cid_name = "0";

      auto cid_number_str
        = cid_name.substr (cid_name.find_first_of ("0123456789"));
      auto cid = std::stoi (cid_number_str);

      auto width = mtx_node.attribute ("width").as_int ();
      auto fixed_width = ag1_width (cid);

      if (fixed_width < 0)
        continue; // pwid
      if (width == fixed_width)
        continue;

      if (std::find (ct.get_cid_miss ().cbegin (),
                     ct.get_cid_miss ().cend (),
                     cid)
          == ct.get_cid_miss ().cend ())
        std::cerr << cid << "\t" << width << "\t" << fixed_width
                  << std::endl;
      else
        std::cerr << "miss\t"
                  << cid << "\t" << width << "\t" << fixed_width
                  << std::endl;

      mtx_node.attribute ("width") = fixed_width;
    }

  doc.save (std::cout, "  ", pugi::format_default, pugi::encoding_utf8);

  return 0;
}
