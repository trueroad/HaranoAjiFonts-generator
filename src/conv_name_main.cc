//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// conv_name_main.cc:
//   convert name.ttx
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

#include <iostream>
#include <string>

#include <pugixml.hpp>

#include "name.hh"
#include "version.hh"

namespace
{
  std::string trim (const std::string &s)
  {
    std::string retval;

    auto left = s.find_first_not_of (" \t\r\n");
    if (left != std::string::npos)
      retval = s.substr (left);
    else
      retval = s;

    auto right = retval.find_first_of ("\r\n");
    if (left != std::string::npos)
      retval = retval.substr (0, right);

    return retval;
  }
};

int main (int argc, char *argv[])
{
  std::cerr
    << "conv_name: Harano Aji Fonts generator " << version
    << std::endl
    << "(convert name.ttx)"
    << std::endl
    << "Copyright (C) 2019 Masamichi Hosoda" << std::endl
    << "https://github.com/trueroad/HaranoAjiFonts-generator" << std::endl
    << std::endl;

  if (argc != 4)
    {
      std::cerr
        << "usage: conv_name FONTNAME TOOL_VER FONT._n_a_m_e.ttx > name.ttx"
        << std::endl
        << std::endl
        << "     FONTNAME:" << std::endl
        << "         New font name." << std::endl
        << "     TOOL_VER:" << std::endl
        << "         The version of ttx etc." << std::endl
        << "     FONT._n_a_m_e.ttx:" << std::endl
        << "         The ttx file of the name table extracted" << std::endl
        << "         from the original font file." << std::endl;
      return 1;
    }

  std::cerr
    << "inputs:" << std::endl
    << "    new font name              : \"" << argv[1] << "\""
    << std::endl
    << "    the version of ttx etc.    : \"" << argv[2] << "\""
    << std::endl
    << "    original font name ttx file: \"" << argv[3] << "\""
    << std::endl << std::endl;

  std::string fontname = argv[1];
  std::string tool_ver = argv[2];

  pugi::xml_document doc;

  auto result = doc.load_file (argv[3]);
  if (!result)
    {
      std::cerr << "error: filename \"" << argv[3]
                << "\": " << result.description () << std::endl;
      return 1;
    }

  auto name = doc.child ("ttFont").child ("name");

  auto uniq_id_node
    = doc.select_node ("/ttFont/name/namerecord[@nameID='3']").node ();
  auto org_uniq_id = trim (uniq_id_node.text ().get ());

  auto uniq_id = fontname + " version " + version;
  uniq_id_node.text ().set (uniq_id.c_str ());

  auto copyright_notice_node
    = doc.select_node ("/ttFont/name/namerecord[@nameID='0']").node ();
  auto copyright_notice = trim (copyright_notice_node.text ().get ());
  copyright_notice = prepend_copyright + copyright_notice;
  copyright_notice_node.text ().set (copyright_notice.c_str ());

  auto version_string_node
    = doc.select_node ("/ttFont/name/namerecord[@nameID='5']").node ();
  version_string_node.text ().set ((uniq_id + ";" + tool_ver).c_str ());

  auto manufacture_name_node
    = doc.select_node ("/ttFont/name/namerecord[@nameID='8']").node ();
  manufacture_name_node.text ().set (manufacture_name);

  auto designer_node
    = doc.select_node ("/ttFont/name/namerecord[@nameID='9']").node ();
  designer_node.parent ().remove_child (designer_node);

  std::string description
    = "This font is base on the font \"" + org_uniq_id + "\"";
  auto description_node
    = doc.select_node ("/ttFont/name/namerecord[@nameID='10']").node ();
  description_node.text ().set (description.c_str ());

  auto url_vendor_node
    = doc.select_node ("/ttFont/name/namerecord[@nameID='11']").node ();
  url_vendor_node.text ().set (url_vendor);

  auto url_designer_node
    = doc.select_node ("/ttFont/name/namerecord[@nameID='12']").node ();
  url_designer_node.parent ().remove_child (url_designer_node);

  doc.save (std::cout, "  ", pugi::format_default, pugi::encoding_utf8);

  return 0;
}
