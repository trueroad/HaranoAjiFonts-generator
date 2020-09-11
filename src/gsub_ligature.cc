//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// gsub_ligature.cc:
//   read `GSUB` table ligature substitution and create map
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

#include "gsub_ligature.hh"

#include <iostream>
#include <set>
#include <sstream>
#include <string>
#include <vector>

#include <pugixml.hpp>

void gsub_ligature::load (pugi::xml_document &doc, const std::string &feature)
{
  std::stringstream ss;
  ss << "ttFont/GSUB/FeatureList/FeatureRecord/FeatureTag[@value='"
     << feature
     << "']";

  auto feature_tags = doc.select_nodes (ss.str ().c_str ());

  std::set<int> lookuplist;
  for (auto it = feature_tags.begin ();
       it != feature_tags.end ();
       ++it)
    {
      auto feature_tag_node = it->node ();
      auto feature_record_node = feature_tag_node.parent ();
      auto feature_node = feature_record_node.child ("Feature");
      for (auto n: feature_node.children ("LookupListIndex"))
        {
          auto value = n.attribute ("value");
          if (value)
            lookuplist.emplace (value.as_int ());
        }
    }

  for (auto index: lookuplist)
    {
      std::stringstream ss;
      ss << "ttFont/GSUB/LookupList/Lookup[@index='"
         << index
         << "']/LigatureSubst/LigatureSet";

      auto ligatureset = doc.select_nodes (ss.str ().c_str ());

      for (auto &ls: ligatureset)
        {
          const char* first = ls.node ().attribute ("glyph").value ();

          if (first[0] == 'c' && first[1] == 'i' && first[2] == 'd')
            {
              auto nfirst = std::stoi (first + 3);

              auto ligature = ls.node ().select_nodes ("Ligature");
              for (auto &l: ligature)
                {
                  std::vector<int> cid_in;
                  cid_in.push_back (nfirst);

                  std::string components =
                    l.node ().attribute ("components").value ();

                  while (components.size ())
                    {
                      auto head = components.substr (0, 3);
                      if (head == "cid")
                        {
                          auto number = components.substr (3, 5);
                          cid_in.push_back (std::stoi (number));
                        }
                      else
                        break;

                      if (components.size () > 8 &&
                          components.substr (8, 1) == ",")
                        components = components.substr (9);
                      else
                        break;
                    }

                  const char* glyph = l.node ().attribute ("glyph").value ();
                  if (glyph[0] == 'c' && glyph[1] == 'i' && glyph[2] == 'd')
                    {
                      auto nglyph = std::stoi (glyph + 3);
                      map_[cid_in] = nglyph;
                      rev_[nglyph] = cid_in;
                    }
                }
            }
        }
    }
}
