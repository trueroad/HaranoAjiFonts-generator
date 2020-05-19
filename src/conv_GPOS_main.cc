//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// conv_GPOS_main.cc:
//   convert GPOS.ttx
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

#include <algorithm>
#include <iostream>
#include <string>
#include <utility>
#include <vector>

#include <pugixml.hpp>

#include "conv_table.hh"
#include "version.hh"

namespace
{
  // Convert SinglePos format 1
  void conv_single_pos_format1 (conv_table &ct, pugi::xml_node &doc)
  {
    auto single_pos_format1 = doc.select_nodes
      ("/ttFont/GPOS/LookupList/Lookup/SinglePos[@Format='1']");

    for (auto &sp: single_pos_format1)
      {
        auto single_pos_node = sp.node ();
        std::vector<pugi::xml_node> removes;

        auto glyphs = single_pos_node.select_nodes ("Coverage/Glyph");
        for (auto &glyph_select: glyphs)
          {
            auto glyph_node = glyph_select.node ();
            auto glyph_value_attr = glyph_node.attribute ("value");
            if (glyph_value_attr)
              {
                std::string cid_out = ct.convert (glyph_value_attr.value ());

                if (cid_out == "")
                  removes.push_back (glyph_node);
                else
                  glyph_value_attr = cid_out.c_str ();
              }
          }

        for (auto &n: removes)
          n.parent ().remove_child (n);
      }
  }

  // Convert SinglePos format 2
  void conv_single_pos_format2 (conv_table &ct, pugi::xml_node &doc)
  {
    auto single_pos_format2 = doc.select_nodes
      ("/ttFont/GPOS/LookupList/Lookup/SinglePos[@Format='2']");

    for (auto &sp: single_pos_format2)
      {
        auto single_pos_node = sp.node ();
        auto glyphs = single_pos_node.select_nodes ("Coverage/Glyph");
        auto values = single_pos_node.select_nodes ("Value");
        std::vector<pugi::xml_node> removes;

        auto it_g = glyphs.begin ();
        auto it_v = values.begin();
        for (; it_g != glyphs.end () && it_v != values.end (); ++it_g, ++it_v)
          {
            auto glyph_node = it_g->node ();
            auto glyph_value_attr = glyph_node.attribute ("value");
            if (glyph_value_attr)
              {
                std::string cid_out = ct.convert (glyph_value_attr.value ());

                if (cid_out == "")
                  {
                    removes.push_back (glyph_node);
                    removes.push_back (it_v->node ());
                  }
                else
                  glyph_value_attr = cid_out.c_str ();
              }
          }

        for (auto &n: removes)
          n.parent ().remove_child (n);
      }
  }

  // Remove empty SinglePos
  void remove_empty_single_pos (pugi::xml_node &doc)
  {
    auto single_pos_coverage = doc.select_nodes
      ("/ttFont/GPOS/LookupList/Lookup/SinglePos/Coverage");
    std::vector<pugi::xml_node> removes;

    for (auto &spc: single_pos_coverage)
      {
        auto glyph = spc.node ().child ("Glyph");
        if (!glyph)
          removes.push_back (spc.parent ());
      }
    for (auto &n: removes)
      n.parent ().remove_child (n);
  }

  // Sort SinglePos format 1 coverage
  void sort_single_pos_format1_coverage (pugi::xml_node &doc)
  {
    auto single_pos_format1_cov = doc.select_nodes
      ("/ttFont/GPOS/LookupList/Lookup/SinglePos[@Format='1']/Coverage");

    for (auto &cov: single_pos_format1_cov)
      {
        auto cov_node = cov.node ();
        std::vector<std::string> cids;
        std::vector<pugi::xml_node> removes;

        for (auto n: cov_node.children ("Glyph"))
          {
            auto glyph = n.attribute ("value");
            if (glyph)
              cids.push_back (glyph.value ());
            removes.push_back (n);
          }
        for (auto &n: removes)
          cov_node.remove_child (n);

        std::sort (cids.begin (), cids.end ());
        for (auto &c: cids)
          {
            auto node = cov_node.append_child ("Glyph");
            node.append_attribute ("value") = c.c_str ();
          }
      }
  }

  // Sort SinglePos format 2 coverage
  void sort_single_pos_format2_coverage (pugi::xml_node &doc)
  {
    auto single_pos_format2 = doc.select_nodes
      ("/ttFont/GPOS/LookupList/Lookup/SinglePos[@Format='2']");

    for (auto &sp: single_pos_format2)
      {
        auto single_pos_node = sp.node ();
        auto glyphs = single_pos_node.select_nodes ("Coverage/Glyph");
        auto values = single_pos_node.select_nodes ("Value");
        auto cov_node = single_pos_node.child ("Coverage");
        std::vector<std::pair<std::string, pugi::xml_node>> pairs;
        std::vector<pugi::xml_node> removes;

        auto it_g = glyphs.begin ();
        auto it_v = values.begin();
        for (; it_g != glyphs.end () && it_v != values.end (); ++it_g, ++it_v)
          {
            auto glyph_node = it_g->node ();
            auto value_node = it_v->node ();
            removes.push_back (glyph_node);
            removes.push_back (value_node);

            auto glyph_value_attr = glyph_node.attribute ("value");
            if (!glyph_value_attr)
              continue;

            pairs.push_back
              (std::make_pair (glyph_value_attr.value (), value_node));
          }

        std::sort (pairs.begin (), pairs.end ());

        for (auto &p: pairs)
          {
            auto glyph_node = cov_node.append_child ("Glyph");
            glyph_node.append_attribute ("value") = p.first.c_str ();

            single_pos_node.append_copy (p.second);
          }

        for (auto &n: removes)
          n.parent ().remove_child (n);
      }
  }

  // Convert PairPos format 1
  void conv_pair_pos_format1 (conv_table &ct, pugi::xml_node &doc)
  {
    auto pair_pos_format1 = doc.select_nodes
      ("/ttFont/GPOS/LookupList/Lookup/PairPos[@Format='1']");

    for (auto &pp: pair_pos_format1)
      {
        auto pair_pos_node = pp.node ();
        auto glyphs = pair_pos_node.select_nodes ("Coverage/Glyph");
        auto pairsets = pair_pos_node.select_nodes ("PairSet");
        std::vector<pugi::xml_node> removes;

        auto it_g = glyphs.begin ();
        auto it_p = pairsets.begin();
        for (; it_g != glyphs.end () && it_p != pairsets.end ();
             ++it_g, ++it_p)
          {
            auto glyph_node = it_g->node ();
            auto glyph_value_attr = glyph_node.attribute ("value");
            if (glyph_value_attr)
              {
                std::string cid_out = ct.convert (glyph_value_attr.value ());

                if (cid_out == "")
                  {
                    removes.push_back (glyph_node);
                    removes.push_back (it_p->node ());
                  }
                else
                  glyph_value_attr = cid_out.c_str ();
              }
          }

        for (auto &n: removes)
          n.parent ().remove_child (n);
        removes.clear ();

        auto second_glyphs =
          pair_pos_node.select_nodes ("PairSet/PairValueRecord/SecondGlyph");
        for (auto &second_glyph_select: second_glyphs)
          {
            auto second_glyph_node = second_glyph_select.node ();
            auto glyph_value_attr = second_glyph_node.attribute ("value");
            if (glyph_value_attr)
              {
                std::string cid_out = ct.convert (glyph_value_attr.value ());

                if (cid_out == "")
                  removes.push_back (second_glyph_node.parent ());
                else
                  glyph_value_attr = cid_out.c_str ();
              }
          }

        for (auto &n: removes)
          n.parent ().remove_child (n);
      }
  }
};

int main (int argc, char *argv[])
{
  std::cerr
    << "conv_GPOS: Harano Aji Fonts generator " << version
    << std::endl
    << "(convert GPOS.ttx)"
    << std::endl
    << "Copyright (C) 2019, 2020 Masamichi Hosoda" << std::endl
    << "https://github.com/trueroad/HaranoAjiFonts-generator" << std::endl
    << std::endl;

  if (argc != 3)
    {
      std::cerr
        << "usage: conv_GPOS TABLE.TBL FONT.G_P_O_S_.ttx > GPOS.ttx"
        << std::endl
        << std::endl
        << "     TABLE.TBL:" << std::endl
        << "         conversion table." << std::endl
        << "     FONT.G_P_O_S_.ttx:" << std::endl
        << "         The ttx file of the GPOS table extracted" << std::endl
        << "         from the original font file." << std::endl;
      return 1;
    }

  std::cerr
    << "inputs:" << std::endl
    << "    conversion table file     : \"" << argv[1] << "\""
    << std::endl
    << "    original font GPOS ttx file: \"" << argv[2] << "\""
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

  conv_single_pos_format1 (ct, doc);
  conv_single_pos_format2 (ct, doc);
  remove_empty_single_pos (doc);
  sort_single_pos_format1_coverage (doc);
  sort_single_pos_format2_coverage (doc);

  conv_pair_pos_format1 (ct, doc);

  auto glyphs
    = doc.select_nodes ("/ttFont/GPOS/LookupList/Lookup//Glyph");

  std::vector<pugi::xml_node> removes;
  for (auto it = glyphs.begin ();
       it != glyphs.end ();
       ++it)
    {
      auto glyph_node = it->node ();
      auto value_attr = glyph_node.attribute ("value");
      if (value_attr &&
          (value_attr.value ())[0] == 'c' &&
          (value_attr.value ())[1] == 'i' &&
          (value_attr.value ())[2] == 'd')
        {
          std::string cid_out = ct.convert (value_attr.value ());

          if (cid_out == "")
            removes.push_back (glyph_node);
          else
            value_attr = cid_out.c_str ();
        }
    }

  auto class_defs
    = doc.select_nodes ("/ttFont/GPOS/LookupList/Lookup//ClassDef");

  for (auto it = class_defs.begin ();
       it != class_defs.end ();
       ++it)
    {
      auto class_def_node = it->node ();
      auto glyph_attr = class_def_node.attribute ("glyph");
      if (glyph_attr)
        {
          std::string cid_out = ct.convert (glyph_attr.value ());

          if (cid_out == "")
            removes.push_back (class_def_node);
          else
            glyph_attr = cid_out.c_str ();
        }
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

  removes.clear ();
  auto mark_base_poses
    = doc.select_nodes ("/ttFont/GPOS/LookupList/Lookup/MarkBasePos");

  for (auto it = mark_base_poses.begin ();
       it != mark_base_poses.end ();
       ++it)
    {
      auto mark_base_pos_node = it->node ();
      auto mark_coverage_node = mark_base_pos_node.child ("MarkCoverage");
      auto base_coverage_node = mark_base_pos_node.child ("BaseCoverage");

      if (!mark_coverage_node || !base_coverage_node)
        {
          removes.push_back (mark_base_pos_node);
          continue;
        }

      auto mark_coverage_glyph = mark_coverage_node.child ("Glyph");
      auto base_coverage_glyph = base_coverage_node.child ("Glyph");

      if (!mark_coverage_glyph || !base_coverage_glyph)
        removes.push_back (mark_base_pos_node);
    }

  for (auto &n: removes)
    n.parent ().remove_child (n);

  doc.save (std::cout, "  ", pugi::format_default, pugi::encoding_utf8);

  return 0;
}
