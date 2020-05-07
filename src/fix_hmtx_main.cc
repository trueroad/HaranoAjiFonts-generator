//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// fix_hmtx_main.cc:
//   fix {AJ1|AG1} hmtx width
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
  // Adobe-Japan1 (AJ1)
  int aj1_width (int cid)
  {
    if ((    1 <= cid && cid <=   230) ||
        ( 9354 <= cid && cid <=  9737) ||
        (15449 <= cid && cid <= 15975) ||
        (20317 <= cid && cid <= 20426))
      return -1; // pwid
    if ((  231 <= cid && cid <=   632) ||
        ( 8718 <= cid && cid <=  8719) ||
        (12063 <= cid && cid <= 12087))
      return 500; // hwid
    if (9758 <= cid && cid <= 9778)
      return 333; // twid
    if (9738 <= cid && cid <= 9757)
      return 250; // qwid

    return 1000; // fwid
  }

  // Adobe-GB1 (AG1)
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

  int get_width (const std::string &ros, int cid)
  {
    if (ros == "AJ1")
      return aj1_width (cid);
    else if (ros == "AG1")
      return ag1_width (cid);

    return -1; // no change
  }
};

int main (int argc, char *argv[])
{
  std::cerr
    << "# fix_hmtx: Harano Aji Fonts generator " << version
    << "#" << std::endl
    << "# (fix {AJ1|AG1} hmtx width)"
    << "#" << std::endl
    << "# Copyright (C) 2019, 2020 Masamichi Hosoda" << std::endl
    << "# https://github.com/trueroad/HaranoAjiFonts-generator" << std::endl
    << "#" << std::endl;

  if (argc != 4)
    {
      std::cerr
        << "usage: fix_hmtx ROS TABLE.TBL aj1_hmtx.ttx > fixed_aj1_hmtx.ttx"
        << std::endl
        << std::endl
        << "     ROS:" << std::endl
        << "         {AJ1|AG1}" << std::endl
        << "     TABLE.TBL:" << std::endl
        << "         conversion table." << std::endl
        << "     aj1_hmtx.ttx:" << std::endl
        << "         {AJ1|AG1} hmtx table which contains wrong width."
        << std::endl;
      return 1;
    }

  std::string ros = argv[1];
  std::string table_filename = argv[2];
  std::string aj1_hmtx_filename = argv[3];

  std::cerr
    << "# inputs:" << std::endl
    << "#     ROS : \"" << ros << "\""
    << std::endl
    << "#     conversion table file: \"" << table_filename << "\""
    << std::endl
    << "#     aj1_hmtx filename: \"" << aj1_hmtx_filename << "\""
    << std::endl
    << "#" << std::endl;

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

  pugi::xml_document doc;

  auto result = doc.load_file (aj1_hmtx_filename.c_str ());
  if (!result)
    {
      std::cerr << "error: filename \"" << aj1_hmtx_filename
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
      auto fixed_width = get_width (ros, cid);

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
