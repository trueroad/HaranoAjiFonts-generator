//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// conv_CFF_main.cc:
//   convert CFF.ttx
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

#include <exception>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>

#include <pugixml.hpp>

#include "walker_CFF.hh"
#include "version.hh"

int main (int argc, char *argv[])
{
  std::cerr
    << "conv_CFF: Harano Aji Fonts generator " << version
    << std::endl
    << "(convert CFF.ttx)"
    << std::endl
    << "Copyright (C) 2019, 2020 Masamichi Hosoda" << std::endl
    << "https://github.com/trueroad/HaranoAjiFonts-generator" << std::endl
    << std::endl;

  if (argc != 3)
    {
      std::cerr
        << "usage: conv_CFF TABLE.TBL FONT.C_F_F_.ttx > CFF.ttx"
        << std::endl
        << std::endl
        << "     TABLE.TBL:" << std::endl
        << "         conversion table." << std::endl
        << "     FONT.C_F_F_.ttx:" << std::endl
        << "         The ttx file of the CFF table extracted" << std::endl
        << "         from the original font file." << std::endl;
      return 1;
    }

  std::cerr
    << "inputs:" << std::endl
    << "    conversion table file     : \"" << argv[1] << "\""
    << std::endl
    << "    original font CFF ttx file: \"" << argv[2] << "\""
    << std::endl << std::endl;

  walker_CFF wcff;
  try
    {
      wcff.load (argv[1]);
    }
  catch (std::exception &e)
    {
      std::cerr << "error: walker_CFF::load (): std::exception: "
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

  try
    {
      auto CFF = doc.child ("ttFont").child ("CFF");
      wcff.walk (CFF, "CharString");
    }
  catch (std::exception &e)
    {
      std::cerr << "error: walk: std::exception: " << e.what ()
                << std::endl;
      return 1;
    }

  auto CharStrings =
    doc.child ("ttFont").child ("CFF").child ("CFFFont").child ("CharStrings");
  auto notdef =
    CharStrings.select_node ("CharString[@name='.notdef']").node ();

  auto GlobalSubrs = doc.select_node ("ttFont/CFF/GlobalSubrs").node ();
  auto gs_size = GlobalSubrs.select_nodes ("CharString").size ();
  std::string dummy_cs;
  std::cerr << "global subrs len: " << gs_size << std::endl;
  if (gs_size == 1239 || gs_size == 33899)
    {
      std::cerr << "cannot add global subr" << std::endl;
      dummy_cs = notdef.text ().get ();
    }
  else
    {
      int index;
      if (gs_size < 1239)
        {
          index = gs_size - 107;
        }
      else if (gs_size < 33899)
        {
          index = gs_size - 1131;
        }
      else
        {
          index = gs_size - 32768;
        }
      auto node = GlobalSubrs.append_child ("CharString");
      node.append_attribute ("index") = std::to_string (gs_size).c_str ();
      node.text ().set (notdef.text ().get ());

      std::stringstream ss;
      ss << index << " callgsubr";
      dummy_cs = ss.str ().c_str ();

      notdef.text () = dummy_cs.c_str ();
    }

  for (auto i: wcff.get_conv_table ().get_cid_miss ())
    {
      std::stringstream ss;
      ss << "aji" << std::setw (5) << std::setfill ('0') << i;

      auto node = CharStrings.append_child ("CharString");
      node.append_attribute ("name") = ss.str ().c_str ();
      for (auto a: notdef.attributes ())
        {
          if (std::string (a.name ()) != std::string ("name"))
            node.append_attribute (a.name ()) = a.value ();
        }
      node.text ().set (dummy_cs.c_str ());
    }

  doc.save (std::cout, "  ", pugi::format_default, pugi::encoding_utf8);

  return 0;
}
