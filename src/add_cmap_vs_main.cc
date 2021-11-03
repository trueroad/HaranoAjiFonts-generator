//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// add_cmap_vs_main.cc:
//   Add CIDs to cmap variation selector
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

#include <fstream>
#include <iomanip>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <vector>

#include <pugixml.hpp>

#include "available_cids.hh"
#include "version.hh"

class aj1_sequence
{
public:
  int base;
  int vs;
  int cid;
};

namespace
{
  int aji_string_to_int (const std::string &name)
  {
    if (name.length () < 4 || name.substr (0, 3) != "aji")
      return -1;

    return std::stoi (name.substr (3));
  }

  int find_default_cid (int uni, pugi::xml_document &doc)
  {
    std::stringstream ss;
    ss << "ttFont/cmap/cmap_format_12/map[@code='0x"
       << std::hex
       << uni
       << "']";

    auto map_tags = doc.select_nodes (ss.str ().c_str ());

    for (auto &map: map_tags)
      return aji_string_to_int (map.node ().attribute ("name").value ());

    return -1;
  }

  void check_and_add (const aj1_sequence &as,
                      const std::set<int> &exists,
                      pugi::xml_document &doc)
  {
    if (exists.find (as.cid) == exists.end ())
      {
        std::cerr << "missing CID: U+"
                  << std::hex << std::setw (4) << std::setfill ('0')
                  << as.base
                  << " U+"
                  << std::hex << std::setw (4) << std::setfill ('0')
                  << as.vs
                  << ", CID+"
                  << std::dec
                  << as.cid
                  << std::endl;
        return;
      }

    const auto default_cid = find_default_cid (as.base, doc);
    if (default_cid < 0)
      {
        std::cerr << "warning: cannot find default CID: U+"
                  << std::hex << std::setw (4) << std::setfill ('0')
                  << as.base
                  << " U+"
                  << std::hex << std::setw (4) << std::setfill ('0')
                  << as.vs
                  << ", CID+"
                  << std::dec
                  << as.cid
                  << std::endl;
      }

    const bool bdefault = (as.cid == default_cid);

    std::stringstream ss;
    ss << "ttFont/cmap/cmap_format_14/map[@uv='0x"
       << std::hex
       << as.base
       << "'][@uvs='0x"
       << std::hex
       << as.vs
       << "']";

    auto map_tags = doc.select_nodes (ss.str ().c_str ());

    if (map_tags.empty ())
      {
        auto parent = doc.select_node ("ttFont/cmap/cmap_format_14").node ();
        auto node = parent.append_child ("map");
        {
          std::stringstream ss;
          ss << "0x" << std::hex << as.base;
          node.append_attribute ("uv") = ss.str ().c_str ();
        }
        {
          std::stringstream ss;
          ss << "0x" << std::hex << as.vs;
          node.append_attribute ("uvs") = ss.str ().c_str ();
        }
        std::cerr << "Add: U+"
                  << std::hex << std::setw (4) << std::setfill ('0')
                  << as.base
                  << " U+"
                  << std::hex << std::setw (4) << std::setfill ('0')
                  << as.vs
                  << std::dec;
        if (bdefault)
          {
            std::cerr << ", default (CID+"
                      << as.cid
                      << ")"
                      << std::endl;
          }
        else
          {
            std::stringstream ss;
            ss << "aji" << as.cid;
            node.append_attribute ("name") = ss.str ().c_str ();

            std::cerr << ", CID+"
                      << as.cid
                      << std::endl;
          }
        return;
      }

    for (auto &map: map_tags)
      {
        auto node = map.node ();
        auto name_attr = node.attribute ("name");
        if (name_attr)
          {
            const auto cmap_cid = aji_string_to_int (name_attr.value ());

            if (bdefault)
              {
                node.remove_attribute (name_attr);

                std::cerr << "Changed: U+"
                          << std::hex << std::setw (4) << std::setfill ('0')
                          << as.base
                          << " U+"
                          << std::hex << std::setw (4) << std::setfill ('0')
                          << as.vs
                          << std::dec
                          << ", CID+"
                          << cmap_cid
                          << " -> default (CID+"
                          << default_cid
                          << ")"
                          << std::endl;
              }
            else if (cmap_cid != as.cid)
              {
                std::stringstream ss_name;
                ss_name << "aji" << as.cid;
                node.append_attribute ("name") = ss_name.str ().c_str ();

                std::cerr << "Changed: U+"
                          << std::hex << std::setw (4) << std::setfill ('0')
                          << as.base
                          << " U+"
                          << std::hex << std::setw (4) << std::setfill ('0')
                          << as.vs
                          << std::dec
                          << ", CID+"
                          << cmap_cid
                          << " -> CID+"
                          << as.cid
                          << std::endl;
              }
          }
        else
          {
            if (!bdefault)
              {
                std::stringstream ss_name;
                ss_name << "aji" << as.cid;
                node.append_attribute ("name") = ss_name.str ().c_str ();

                std::cerr << "Changed: U+"
                          << std::hex << std::setw (4) << std::setfill ('0')
                          << as.base
                          << " U+"
                          << std::hex << std::setw (4) << std::setfill ('0')
                          << as.vs
                          << std::dec
                          << ", default (CID+"
                          << default_cid
                          << ") -> CID+"
                          << as.cid
                          << std::endl;
              }
          }
      }
  }

  std::vector<aj1_sequence> load_sequence (const std::string &filename)
  {
    std::vector<aj1_sequence> retval;

    std::ifstream ifs;
    ifs.open (filename);
    if (!ifs)
      {
        std::cerr << "error: " << __func__ << ": open failed."
                  << std::endl;
        return retval;
      }

    std::string line;
    while (std::getline (ifs, line))
      {
        std::stringstream ss (line);
        std::string base_str;
        ss >> base_str;
        if (base_str.at (0) == '#')
          continue;

        std::string vs_str;
        std::string category;
        std::string cid_str;
        ss >> vs_str >> category >> cid_str;

        aj1_sequence as;
        as.base = std::stoi (base_str, nullptr, 16);
        as.vs = std::stoi (vs_str, nullptr, 16);
        if (cid_str.size () <= 4 || cid_str.substr (0, 4) != "CID+")
          {
            std::cerr << "error: parse: " << line << std::endl;
            continue;
          }
        as.cid = std::stoi (cid_str.substr (4));

        retval.push_back (as);
      }

    return retval;
  }

};

int main (int argc, char *argv[])
{
  std::cout
    << "add_cmap_vs: Harano Aji Fonts generator " << version
    << std::endl
    << "(Add CIDs to cmap variation selector)"
    << std::endl
    << "Copyright (C) 2021 Masamichi Hosoda"
    << std::endl
    << "https://github.com/trueroad/HaranoAjiFonts-generator"
    << std::endl
    << std::endl;

  if (argc != 6)
    {
      std::cerr
        << "usage: add_cmap_vs TABLE.TBL CR.TBL AJ1_SEQ.txt cmap_IN.ttx"
        " cmap_OUT.ttx"
        << std::endl
        << std::endl
        << "   (in)  TABLE.TBL:" << std::endl
        << "         conversion table." << std::endl
        << "   (in)  CR.TBL:" << std::endl
        << "         copy and rotate table." << std::endl
        << "   (in)  AJ1_SEQ.txt:" << std::endl
        << "         The sequences file of the AdobeJapan1." << std::endl
        << "         i.e. Adobe-Japan1_sequences.txt." << std::endl
        << "   (in)  cmap_IN.ttx:" << std::endl
        << "         Input AJ1 cmap table." << std::endl
        << "   (out) cmap_OUT.ttx:" << std::endl
        << "         Output (CIDs added) AJ1 cmap table." << std::endl
        << std::endl;
      return 1;
    }

  std::string table_filename = argv[1];
  std::string cr_filename = argv[2];
  std::string seq_filename = argv[3];
  std::string cmap_in_filename = argv[4];
  std::string cmap_out_filename = argv[5];

  std::cout
    << "inputs:" << std::endl
    << "    conversion table             : \"" << table_filename << "\""
    << std::endl
    << "    copy and rotate table        : \"" << cr_filename << "\""
    << std::endl
    << "    Sequences file               : \"" << seq_filename << "\""
    << std::endl
    << "    input AJ1 cmap table         : \"" << cmap_in_filename << "\""
    << std::endl
    << "    output (CID added) cmap table: \"" << cmap_out_filename << "\""
    << std::endl
    << std::endl;

  auto exists = get_available_cids (table_filename,
                                             cr_filename);

  auto seqs = load_sequence (seq_filename);

  pugi::xml_document doc;
  auto result = doc.load_file (cmap_in_filename.c_str ());
  if (!result)
    {
      std::cerr << "error: filename \"" << cmap_in_filename
                << "\": " << result.description () << std::endl;
      return 1;
    }

  for (const auto &as: seqs)
    {
      /*
      std::cout << std::hex << std::setw (4) << std::setfill ('0')
                << as.base
                << " "
                << std::hex << std::setw (4) << std::setfill ('0')
                << as.vs
                << " CID+"
                << std::dec
                << as.cid
                << std::endl;
      */

      check_and_add (as, exists, doc);
    }

  doc.save_file (cmap_out_filename.c_str (), "  ",
                 pugi::format_default, pugi::encoding_utf8);
  return 0;
}
