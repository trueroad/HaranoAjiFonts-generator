//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// gsub_single.cc:
//   read `GSUB` table single substitution and create map
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

#include "gsub_single.hh"

#include <iostream>
#include <set>
#include <sstream>
#include <string>

#include <pugixml.hpp>

void gsub_single::load (pugi::xml_document &doc, const std::string &feature)
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
         << "']/SingleSubst/Substitution";

      auto substitutions = doc.select_nodes (ss.str ().c_str ());

      for (auto it = substitutions.begin ();
           it != substitutions.end ();
           ++it)
        {
          const char* in = it->node ().attribute ("in"). value ();
          const char* out = it->node ().attribute ("out"). value ();

          if (in[0] == 'c' && in[1] == 'i' && in[2] == 'd' &&
              out[0] == 'c' && out[1] == 'i' && out[2] == 'd')
            {
              auto cid_in = std::stoi (in + 3);
              auto cid_out = std::stoi (out + 3);

              if (map_.find (cid_in) != map_.end ())
                {
                  if (map_[cid_in] != cid_out)
                    {
                      std::cout
                        << "#warning: invalid GSUB table: duplicate: cid "
                        << cid_in
                        << " -> cid "
                        << map_[cid_in]
                        << ", cid "
                        << cid_out
                        << std::endl;
                    }
                }
              else
                map_[cid_in] = cid_out;

              if (rev_.find (cid_out) != rev_.end ())
                {
                  if (rev_[cid_out] != cid_in)
                    {
                      std::cout
                        << "#duplicate in GSUB table: cid "
                        << rev_[cid_out]
                        << ", cid "
                        << cid_in
                        << " -> cid "
                        << cid_out << std::endl;
                    }
                }
              else
                rev_[cid_out] = cid_in;
            }
        }
    }
}
