//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// conv_mtx_main.cc:
//   convert hmtx.ttx and vmtx.ttx
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
#include <sstream>
#include <string>

#include <pugixml.hpp>

#include "walker_conv.hh"
#include "version.hh"

int main (int argc, char *argv[])
{
  std::cerr
    << "conv_mtx: Harano Aji Fonts generator " << version
    << std::endl
    << "(convert hmtx.ttx and vmtx.ttx)"
    << std::endl
    << "Copyright (C) 2019 Masamichi Hosoda" << std::endl
    << "https://github.com/trueroad/HaranoAjiFonts-generator" << std::endl
    << std::endl;

  if (argc != 3)
    {
      std::cerr
        << "usage: conv_cmap TABLE.TBL FONT._h_m_t_x.ttx > hmtx.ttx"
        << std::endl
        << "       conv_cmap TABLE.TBL FONT._v_m_t_x.ttx > vmtx.ttx"
        << std::endl
        << std::endl
        << "     TABLE.TBL:" << std::endl
        << "         conversion table." << std::endl
        << "     FONT._h_m_t_x.ttx:" << std::endl
        << "         The ttx file of the hmtx table extracted" << std::endl
        << "         from the original font file." << std::endl
        << "     FONT._v_m_t_x.ttx:" << std::endl
        << "         The ttx file of the vmtx table extracted" << std::endl
        << "         from the original font file." << std::endl;
      return 1;
    }

  std::cerr
    << "inputs:" << std::endl
    << "    conversion table file          : \"" << argv[1] << "\""
    << std::endl
    << "    original font {h|v}mtx ttx file: \"" << argv[2] << "\""
    << std::endl << std::endl;

  walker_conv wconv;
  try
    {
      wconv.load (argv[1]);
    }
  catch (std::exception &e)
    {
      std::cerr << "error: walker_conv::load (): std::exception: "
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

  auto mtx = doc.child ("ttFont").child ("hmtx");
  if (!mtx)
    mtx = doc.child ("ttFont").child ("vmtx");
  if (!mtx)
    {
      std::cerr << "error: hmtx and vmtx not found" << std::endl;

      return 1;
    }

  try
    {
      wconv.walk (mtx, "mtx");
    }
  catch (std::exception &e)
    {
      std::cerr << "error: walk: std::exception: " << e.what ()
                << std::endl;
      return 1;
    }

  auto notdef = mtx.select_node ("mtx[@name='.notdef']").node ();

  for (auto i: wconv.get_conv_table ().get_cid_miss ())
    {
      std::stringstream ss;
      ss << "aji" << std::setw (5) << std::setfill ('0') << i;

      auto node = mtx.append_child ("mtx");
      node.append_attribute ("name") = ss.str ().c_str ();
      for (auto a: notdef.attributes ())
        {
          if (std::string (a.name ()) != std::string ("name"))
            node.append_attribute (a.name ()) = a.value ();
        }
    }

  doc.save (std::cout, "  ", pugi::format_default, pugi::encoding_utf8);

  return 0;
}
