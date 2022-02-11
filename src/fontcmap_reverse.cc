//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// fontcmap_reverse.cc:
//   read cmap table of the original font file and create an reverse map
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

#include "fontcmap_reverse.hh"

#include <iomanip>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <string>

#include <pugixml.hpp>

#include "prefer_unicode.hh"

void fontcmap_reverse::load_ttx (const std::string &filename,
                                 const cmapfile &cmf,
                                 int format, int platform_id,
                                 int plat_enc_id, int lang)
{
  map_.clear ();
  dup_.clear ();

  pugi::xml_document doc;

  auto result = doc.load_file (filename.c_str ());
  if (!result)
    {
      std::cerr
        << "error: " << __func__ << ": filename \"" << filename << "\": "
        << result.description () << std::endl;
      return;
    }

  const auto &ttfont = doc.child ("ttFont");
  const auto &cmap = ttfont.child ("cmap");

  std::stringstream ss;
  ss << "cmap_format_" << format;

  for (const auto &m: cmap.children (ss.str ().c_str()))
    {
      auto platformID = m.attribute ("platformID").as_int ();
      auto platEncID = m.attribute ("platEncID").as_int ();
      auto language = m.attribute ("language").as_int ();

      if (platformID == platform_id && platEncID == plat_enc_id
          && language == lang)
        {
          for (const auto &n: m.children ("map"))
            {
              auto code = n.attribute ("code").as_int ();

              if (dup_.find (code) != dup_.end ())
                std::cout
                  << "#warning: invalid font cmap: duplicate U+"
                  << std::setw (4) << std::setfill ('0')
                  << std::hex << std::uppercase
                  << code
                  << std::nouppercase << std::dec
                  << std::setfill (' ') << std::endl;
              else
                dup_.emplace (code);

              const char *name = n.attribute ("name").as_string ();
              if (name[0] == 'c' && name[1] == 'i' && name[2] == 'd')
                {
                  auto cid = std::stoi (name+3, nullptr, 10);
                  if (map_.find (cid) != map_.end ())
                    {
                      auto prefer_code = prefer_unicode (map_[cid], code, cmf);
                      std::cout
                        << "#duplicate in font cmap: cid "
                        << cid
                        << " -> U+"
                        << std::setw (4) << std::setfill ('0')
                        << std::hex << std::uppercase
                        << map_[cid]
                        << ", U+"
                        << std::setw (4)
                        << code
                        << ": prefer U+"
                        << std::setw (4)
                        << prefer_code
                        << std::nouppercase << std::dec
                        << std::setfill (' ') << std::endl;
                      if (map_[cid] != prefer_code)
                        map_[cid] = prefer_code;
                    }
                  else
                    map_.emplace (cid, code);
                }
            }

          break;
        }
    }
}
