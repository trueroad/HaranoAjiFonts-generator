//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// make_glyphorder_main.cc:
//   make glyphorder.ttx
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

#include <exception>
#include <iomanip>
#include <iostream>
#include <map>

#include <pugixml.hpp>

#include "conv_table.hh"
#include "version.hh"

int main (int argc, char *argv[])
{
  std::cerr
    << "make_glyphorder: Harano Aji Fonts generator " << version
    << std::endl
    << "(make glyphorder.ttx)"
    << std::endl
    << "Copyright (C) 2019 Masamichi Hosoda" << std::endl
    << "https://github.com/trueroad/HaranoAjiFonts-generator" << std::endl
    << std::endl;

  if (argc != 2)
    {
      std::cerr
        << "usage: make_glyphorder TABLE.TBL > glyphorder.ttx"
        << std::endl
        << std::endl
        << "     TABLE.TBL:" << std::endl
        << "         conversion table." << std::endl;
      return 1;
    }

  std::cerr
    << "input:" << std::endl
    << "    conversion table file: \"" << argv[1] << "\""
    << std::endl << std::endl;

  conv_table ct;
  try
    {
      ct.load (argv[1]);
    }
  catch (std::exception &e)
    {
      std::cerr << "error: conv_table: std::exception: " << e.what ()
                << std::endl;
      return 1;
    }

  pugi::xml_document doc;

  auto decl = doc.prepend_child (pugi::node_declaration);
  decl.append_attribute ("version") = "1.0";
  decl.append_attribute ("encoding") = "UTF-8";

  auto ttFont = doc.append_child ("ttFont");
  ttFont.append_attribute ("ttLibVersion") = "3.38";

  auto GlyphOrder = ttFont.append_child ("GlyphOrder");

  GlyphOrder.append_child ("GlyphID").append_attribute ("name")
    = ".notdef";

  for (int i = 1; i <= aj1_max_cid; ++i)
    {
      std::stringstream ss;
      ss << "aji" << std::setw (5) << std::setfill ('0') << i;

      GlyphOrder.append_child ("GlyphID").append_attribute ("name")
        = ss.str ().c_str ();
    }

  doc.save (std::cout, "  ", pugi::format_default, pugi::encoding_utf8);

  return 0;
}
