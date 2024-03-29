//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// add_cmap_main.cc:
//   Add CIDs to cmap
//
// Copyright (C) 2020, 2021 Masamichi Hosoda.
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
#include <set>
#include <sstream>
#include <string>

#include <pugixml.hpp>

#include "available_cids.hh"
#include "cmapfile.hh"
#include "version.hh"

namespace
{
  void check_and_add (pugi::xml_node table_node,
                      const std::map<int, int> &map_cmap,
                      const std::set<int> &exists,
                      int uni_CMap, int cid_CMap)
  {
    bool bexist = (exists.find (cid_CMap) != exists.end());

    if (map_cmap.find (uni_CMap) == map_cmap.end ())
      {
        if (bexist)
          {
            auto map_node = table_node.append_child ("map");
            {
              std::stringstream ss;
              ss << "0x" << std::hex << uni_CMap;
              map_node.append_attribute ("code").
                set_value (ss.str ().c_str ());
            }
            {
              std::stringstream ss;
              ss << "aji"
                 << std::setw (5) << std::setfill ('0')
                 << cid_CMap;
              map_node.append_attribute ("name").
                set_value (ss.str ().c_str ());
            }

            std::cout << "added: ";
          }
        else
          {
            std::cout << "miss cid: ";
          }
        std::cout
          << "U+"
          << std::setw (4) << std::setfill ('0')
          << std::hex << std::uppercase
          << uni_CMap
          << " -> CID+"
          << std::setfill (' ')
          << std::dec << std::nouppercase
          << cid_CMap
          << std::endl;
      }
    else
      {
        if (map_cmap.at (uni_CMap) == cid_CMap)
          return;

        if (bexist)
          {
            std::stringstream ss_select;
            ss_select << "map[@code='0x" << std::hex << uni_CMap << "']";

            auto map_node =
              table_node.select_node (ss_select.str ().c_str ()).node ();
            if (map_node)
              {
                std::stringstream ss;
                ss << "aji"
                   << std::setw (5) << std::setfill ('0')
                   << cid_CMap;
                map_node.attribute ("name").set_value (ss.str ().c_str ());
                std::cout << "changed: ";
              }
          }
        std::cout
          << "warning: no match: U+"
          << std::setw (4) << std::setfill ('0')
          << std::hex << std::uppercase
          << uni_CMap
          << " -> CMap CID+"
          << std::setfill (' ')
          << std::dec << std::nouppercase
          << cid_CMap;
        if (!bexist)
          std::cout << " (miss)";
        std::cout
          << ", cmap CID+"
          << map_cmap.at (uni_CMap)
          << std::endl;
      }
  }

  std::map<int, int> load_cmap_table (pugi::xml_node table_node)
  {
    std::map<int, int> map;

    for (auto &m: table_node.children ("map"))
      {
        auto uni = m.attribute ("code").as_int ();
        std::string name = m.attribute ("name").value ();
        auto cid = std::stoi (name.substr (3));

        if (map.find (uni) != map.end ())
          {
            std::cerr
              << "error: duplicate code in cmap table: U+"
              << std::setw (4) << std::setfill ('0')
              << std::hex << std::uppercase
              << uni
              << " -> CID+"
              << std::setfill (' ')
              << std::dec << std::nouppercase
              << cid
              << std::endl;

            continue;
          }

        map[uni] = cid;
      }

    return map;
  }
};

int main (int argc, char *argv[])
{
  std::cout
    << "add_cmap: Harano Aji Fonts generator " << version
    << std::endl
    << "(Add CIDs to cmap)"
    << std::endl
    << "Copyright (C) 2020, 2021 Masamichi Hosoda"
    << std::endl
    << "https://github.com/trueroad/HaranoAjiFonts-generator"
    << std::endl
    << std::endl;

  if (argc != 6)
    {
      std::cerr
        << "usage: add_cmap TABLE.TBL CR.TBL CMAP_FILE cmap_IN.ttx"
        " cmap_OUT.ttx"
        << std::endl
        << std::endl
        << "   (in)  TABLE.TBL:" << std::endl
        << "         conversion table." << std::endl
        << "   (in)  CR.TBL:" << std::endl
        << "         copy and rotate table." << std::endl
        << "   (in)  CMAP_FILE:" << std::endl
        << "         The CMap file of the pre-defined CID." << std::endl
        << "         e.g. UniJIS2004-UTF32-H etc." << std::endl
        << "   (in)  cmap_IN.ttx:" << std::endl
        << "         Input AJ1 cmap table." << std::endl
        << "   (out) cmap_OUT.ttx:" << std::endl
        << "         Output (CIDs added) AJ1 cmap table." << std::endl
        << std::endl;
      return 1;
    }

  std::string table_filename = argv[1];
  std::string cr_filename = argv[2];
  std::string CMap_filename = argv[3];
  std::string cmap_in_filename = argv[4];
  std::string cmap_out_filename = argv[5];

  std::cout
    << "inputs:" << std::endl
    << "    conversion table             : \"" << table_filename << "\""
    << std::endl
    << "    copy and rotate table        : \"" << cr_filename << "\""
    << std::endl
    << "    CMap file                    : \"" << CMap_filename << "\""
    << std::endl
    << "    input AJ1 cmap table         : \"" << cmap_in_filename << "\""
    << std::endl
    << "    output (CID added) cmap table: \"" << cmap_out_filename << "\""
    << std::endl
    << std::endl;

  std::set<int> exists = get_available_cids (table_filename,
                                             cr_filename);

  cmapfile cmf;
  try
    {
      cmf.load (CMap_filename);
    }
  catch (std::exception &e)
    {
      std::cerr << "error: cmapfile: std::exception: " << e.what ()
                << std::endl;
      return 1;
    }

  pugi::xml_document doc;
  auto result = doc.load_file (cmap_in_filename.c_str ());
  if (!result)
    {
      std::cerr << "error: filename \"" << cmap_in_filename
                << "\": " << result.description () << std::endl;
      return 1;
    }

  auto cmap_format4 = doc.select_nodes ("ttFont/cmap/cmap_format_4");
  for (auto &t: cmap_format4)
    {
      auto table_node = t.node ();
      auto map_cmap = load_cmap_table (table_node);

      for (auto &c: cmf.get_map ())
        {
          if (c.first >= 0x10000)
            break;
          check_and_add (table_node, map_cmap, exists, c.first, c.second);
        }
    }

  auto cmap_format12 = doc.select_nodes ("ttFont/cmap/cmap_format_12");
  for (auto &t: cmap_format12)
    {
      auto table_node = t.node ();
      auto map_cmap = load_cmap_table (table_node);

      for (auto &c: cmf.get_map ())
        check_and_add (table_node, map_cmap, exists, c.first, c.second);
    }

  doc.save_file (cmap_out_filename.c_str (), "  ",
                 pugi::format_default, pugi::encoding_utf8);

  return 0;
}
