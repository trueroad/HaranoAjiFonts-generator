//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// conv_GSUB_main.cc:
//   convert GSUB.ttx
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

#include <iostream>
#include <string>
#include <sstream>
#include <vector>

#include <pugixml.hpp>

#include "conv_table.hh"
#include "version.hh"

int main (int argc, char *argv[])
{
  std::cerr
    << "conv_GSUB: Harano Aji Fonts generator " << version
    << std::endl
    << "(convert GSUB.ttx)"
    << std::endl
    << "Copyright (C) 2019, 2020 Masamichi Hosoda" << std::endl
    << "https://github.com/trueroad/HaranoAjiFonts-generator" << std::endl
    << std::endl;

  if (argc != 3)
    {
      std::cerr
        << "usage: conv_GSUB TABLE.TBL FONT.G_S_U_B_.ttx > GSUB.ttx"
        << std::endl
        << std::endl
        << "     TABLE.TBL:" << std::endl
        << "         conversion table." << std::endl
        << "     FONT.G_S_U_B_.ttx:" << std::endl
        << "         The ttx file of the GSUB table extracted" << std::endl
        << "         from the original font file." << std::endl;
      return 1;
    }

  std::cerr
    << "inputs:" << std::endl
    << "    conversion table file     : \"" << argv[1] << "\""
    << std::endl
    << "    original font GSUB ttx file: \"" << argv[2] << "\""
    << std::endl << std::endl;

  conv_table ct;
  try
    {
      ct.load (argv[1]);
    }
  catch (std::exception &e)
    {
      std::cerr << "error: conv_table::load (): std::exception: "
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

  auto substs
    = doc.select_nodes ("/ttFont/GSUB/LookupList/Lookup/SingleSubst"
                        "/Substitution");

  std::vector<pugi::xml_node> removes;
  for (auto it = substs.begin ();
       it != substs.end ();
       ++it)
    {
      auto subst_node = it->node ();
      auto in_attr = subst_node.attribute ("in");
      auto out_attr = subst_node.attribute ("out");

      if (in_attr)
        {
          std::string cid_in = ct.convert (in_attr.value ());

          if (cid_in == "")
            {
              removes.push_back (subst_node);
              continue;
            }
          else
            in_attr = cid_in.c_str ();
        }
      if (out_attr)
        {
          std::string cid_out = ct.convert (out_attr.value ());

          if (cid_out == "")
            removes.push_back (subst_node);
          else
            out_attr = cid_out.c_str ();
        }
    }

  auto alternate_sets
    = doc.select_nodes ("/ttFont/GSUB/LookupList/Lookup/AlternateSubst"
                        "/AlternateSet");

  for (auto it = alternate_sets.begin ();
       it != alternate_sets.end ();
       ++it)
    {
      auto altset_node = it->node ();
      auto glyph_attr = altset_node.attribute ("glyph");
      if (glyph_attr)
        {
          std::string cid = ct.convert (glyph_attr.value ());

          if (cid == "")
            removes.push_back (altset_node);
          else
            {
              glyph_attr = cid.c_str ();
              for (auto n: altset_node.children ("Alternate"))
                {
                  auto glyph_attr = n.attribute ("glyph");
                  if (glyph_attr)
                    {
                      std::string cid = ct.convert (glyph_attr.value ());
                      if (cid == "")
                        removes.push_back (n);
                      else
                        glyph_attr = cid.c_str ();
                    }
                }
            }
        }
    }

  auto ligature_sets
    = doc.select_nodes ("/ttFont/GSUB/LookupList/Lookup/LigatureSubst"
                        "/LigatureSet");

  for (auto it = ligature_sets.begin ();
       it != ligature_sets.end ();
       ++it)
    {
      auto ligset_node = it->node ();
      auto glyph_attr = ligset_node.attribute ("glyph");

      if (!glyph_attr)
        {
          removes.push_back (ligset_node);
          continue;
        }

      std::string cid = ct.convert (glyph_attr.value ());
      if (cid == "")
        {
          removes.push_back (ligset_node);
          continue;
        }
      glyph_attr = cid.c_str ();

      bool bremain = false;
      for (auto n: ligset_node.children ("Ligature"))
        {
          auto components_attr = n.attribute ("components");
          auto glyph_attr = n.attribute ("glyph");

          if (!components_attr || !glyph_attr)
            {
              removes.push_back (n);
              continue;
            }

          std::string cid = ct.convert (glyph_attr.value ());
          if (cid == "")
            {
              removes.push_back (n);
              continue;
            }
          glyph_attr = cid.c_str ();

          std::stringstream ss {components_attr.value ()};
          std::string buff;
          std::string cid_outs;
          while (std::getline (ss, buff, ','))
            {
              std::string cid = ct.convert (buff);
              if (cid == "")
                {
                  cid_outs = "";
                  break;
                }
              cid_outs = cid_outs + cid + ",";
            }
          if (cid_outs == "")
            {
              removes.push_back (n);
              continue;
            }
          if (cid_outs.back () == ',')
            cid_outs.pop_back ();
          components_attr = cid_outs.c_str ();
          bremain = true;
        }
      if (!bremain)
        removes.push_back (ligset_node);
    }

  auto chain_subst
    = doc.select_nodes ("/ttFont/GSUB/LookupList/Lookup/ChainContextSubst");

  for (auto it = chain_subst.begin ();
       it != chain_subst.end ();
       ++it)
    {
      auto chain_subst_node = it->node ();

      removes.push_back (chain_subst_node);
      /* // ***FIX ME** Coverage must be sorted by glyph ids.
      bool bexist = false;
      bool bremain = false;
      for (auto coverage: chain_subst_node.children ("BacktrackCoverage"))
        {
          bexist = true;
          bremain = false;
          for (auto glyph: coverage.children ("Glyph"))
            {
              auto glyph_attr = glyph.attribute ("value");

              if (!glyph_attr)
                {
                  removes.push_back (glyph);
                  continue;
                }

              std::string cid = ct.convert (glyph_attr.value ());
              if (cid == "")
                {
                  removes.push_back (glyph);
                  continue;
                }
              glyph_attr = cid.c_str ();
              bremain = true;
            }

          if (!bremain)
            {
              removes.push_back (chain_subst_node);
              break;
            }
        }
      if (bexist && !bremain)
        continue;

      bexist = false;
      bremain = false;
      for (auto coverage: chain_subst_node.children ("InputCoverage"))
        {
          bexist = true;
          bremain = false;
          for (auto glyph: coverage.children ("Glyph"))
            {
              auto glyph_attr = glyph.attribute ("value");

              if (!glyph_attr)
                {
                  removes.push_back (glyph);
                  continue;
                }

              std::string cid = ct.convert (glyph_attr.value ());
              if (cid == "")
                {
                  removes.push_back (glyph);
                  continue;
                }
              glyph_attr = cid.c_str ();
              bremain = true;
            }

          if (!bremain)
            {
              removes.push_back (chain_subst_node);
              break;
            }
        }
      if (bexist && !bremain)
        continue;

      for (auto coverage: chain_subst_node.children ("LookAheadCoverage"))
        {
          bremain = false;
          for (auto glyph: coverage.children ("Glyph"))
            {
              auto glyph_attr = glyph.attribute ("value");

              if (!glyph_attr)
                {
                  removes.push_back (glyph);
                  continue;
                }

              std::string cid = ct.convert (glyph_attr.value ());
              if (cid == "")
                {
                  removes.push_back (glyph);
                  continue;
                }
              glyph_attr = cid.c_str ();
              bremain = true;
            }

          if (!bremain)
            {
              removes.push_back (chain_subst_node);
              break;
            }
        }
      */
    }


  for (auto &n: removes)
    n.parent ().remove_child (n);

  auto coverages
    = doc.select_nodes ("/ttFont/GPOS/LookupList/Lookup//Coverage");

  for (auto it = coverages.begin ();
       it != coverages.end ();
       ++it)
    {
      auto coverage_node = it->node ();
      std::vector<std::string> cids;
      std::vector<pugi::xml_node> nodes;
      for (auto n: coverage_node.children ("Glyph"))
        {
          auto glyph = n.attribute ("value");
          if (glyph)
            cids.push_back (glyph.value ());
          nodes.push_back (n);
        }
      for (auto n: nodes)
        coverage_node.remove_child (n);

      std::sort (cids.begin (), cids.end ());
      for (auto c: cids)
        {
          auto n = coverage_node.append_child ("Glyph");
          n.append_attribute ("value") = c.c_str ();
        }
    }

  doc.save (std::cout, "  ", pugi::format_default, pugi::encoding_utf8);

  return 0;
}
