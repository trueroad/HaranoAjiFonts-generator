//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// gpos_single.cc:
//   read `GPOS` table single adjustment position and create map
//
// Copyright (C) 2020 Masamichi Hosoda.
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

#include "gpos_single.hh"

#include <iostream>
#include <set>
#include <sstream>
#include <string>

#include <pugixml.hpp>

#include "gpos_value.hh"

namespace
{
  int name2cid (const std::string &name)
  {
    return std::stoi (name.substr (name.find_first_of ("0123456789")));
  }

  gpos_value get_gpos_value (pugi::xml_node node)
  {
    gpos_value retval;

    auto xp_attr = node.attribute ("XPlacement");
    if (xp_attr)
      retval.xPlacement = xp_attr.as_int ();

    auto yp_attr = node.attribute ("YPlacement");
    if (yp_attr)
      retval.yPlacement = yp_attr.as_int ();

    auto xa_attr = node.attribute ("XAdvance");
    if (xa_attr)
      retval.xAdvance = xa_attr.as_int ();

    auto ya_attr = node.attribute ("YAdvance");
    if (ya_attr)
      retval.yAdvance = ya_attr.as_int ();

    return retval;
  }
};

void gpos_single::load (pugi::xml_document &doc, const std::string &feature)
{
  std::stringstream ss;
  ss << "ttFont/GPOS/FeatureList/FeatureRecord/FeatureTag[@value='"
     << feature
     << "']";

  auto feature_tags = doc.select_nodes (ss.str ().c_str ());

  std::set<int> lookuplist;
  for (auto &ft: feature_tags)
    {
      auto feature_tag_node = ft.node ();
      auto feature_record_node = feature_tag_node.parent ();
      auto feature_node = feature_record_node.child ("Feature");
      for (auto &n: feature_node.children ("LookupListIndex"))
        {
          auto value = n.attribute ("value");
          if (value)
            lookuplist.emplace (value.as_int ());
        }
    }

  for (auto index: lookuplist)
    {
      std::stringstream sp_name;
      sp_name << "ttFont/GPOS/LookupList/Lookup[@index='"
              << index
              << "']/SinglePos";

      auto single_pos_nodes = doc.select_nodes (sp_name.str ().c_str ());
      for (auto &sp: single_pos_nodes)
        {
          auto single_pos_node = sp.node ();
          auto format_attr = single_pos_node.attribute ("Format");

          if (!format_attr)
            continue;
          int format = format_attr.as_int ();

          auto glyphs = single_pos_node.select_nodes ("Coverage/Glyph");

          switch (format)
            {
            case 1:
              {
                auto gv = get_gpos_value (single_pos_node.child ("Value"));

                for (auto &g: glyphs)
                  {
                    auto glyph_node = g.node ();
                    auto glyph_value_attr = glyph_node.attribute ("value");

                    if (glyph_value_attr)
                      {
                        int cid = name2cid (glyph_value_attr.value ());
                        map_[cid] = gv;
                      }
                  }
              }
              break;
            case 2:
              {
                auto values =
                  single_pos_node.select_nodes ("Value");

                auto it_g = glyphs.begin ();
                auto it_v = values.begin ();
                for (; it_g != glyphs.end () && it_v != values.end ();
                     ++it_g, ++it_v)
                  {
                    auto glyph_node = it_g->node ();
                    auto glyph_value_attr = glyph_node.attribute ("value");

                    if (glyph_value_attr)
                      {
                        int cid = name2cid (glyph_value_attr.value ());
                        map_[cid] = get_gpos_value (it_v->node ());
                      }
                  }
              }
              break;
            default:
              std::cerr << "error: unknown SinglePos format "
                        << format << std::endl;
              break;
            }
        }
    }
}
