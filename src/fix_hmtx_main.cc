//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// fix_hmtx_main.cc:
//   fix {AJ1|AG1|AC1|AKR|AK1} hmtx width
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
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>

#include <pugixml.hpp>

#include "calc_width.hh"
#include "conv_table.hh"
#include "version.hh"

class calc_width_ext: public calc_width
{
public:
  calc_width_ext (const std::string &ros, pugi::xml_document &doc):
    calc_width (ros),
    doc_ (doc)
  {
    if (ros_ == "AKR")
      {
        // Get hangul width from CID+221
        // It is first row of akr9-hangul.txt in
        // https://github.com/adobe-type-tools/Adobe-KR
        auto hangul_width_attr =
          doc.select_node ("/ttFont/hmtx/mtx[@name='aji00221']")
          .node ().attribute ("width");
        if (hangul_width_attr)
          {
            hangul_width_ = hangul_width_attr.as_int ();
            std::cerr << "hangul width: " << hangul_width_ << std::endl;
          }
        else
          std::cerr << "error: cannot get hangul width" << std::endl;

        // Calc figure space width from digit width (CID+17 -- CID+26)
        int digit_width_sum = 0;
        int number_of_cids = 0;
        std::cerr << "digit width:";
        for (int cid = 17; cid < (26 + 1); ++cid)
          {
            std::stringstream ss;
            ss << "/ttFont/hmtx/mtx[@name='aji"
               << std::setw (5) << std::setfill ('0') << cid
               << "']";

            auto digit_width_attr = doc.select_node (ss.str ().c_str())
              .node ().attribute ("width");
            if (digit_width_attr)
              {
                int width = digit_width_attr.as_int ();
                digit_width_sum += width;
                ++number_of_cids;
                std::cerr << " " << width;
              }
          }
        figure_space_width_ = digit_width_sum / number_of_cids;
        std::cerr << " -> " << figure_space_width_ << std::endl;
      }
  }

private:
  int get_hangul_width (void)
  {
    return hangul_width_;
  }
  int get_figure_space_width (void)
  {
    return figure_space_width_;
  }

  pugi::xml_document &doc_;
  int hangul_width_ = -1; // default no change
  int figure_space_width_ = -1; // default no change
};

int main (int argc, char *argv[])
{
  std::cerr
    << "# fix_hmtx: Harano Aji Fonts generator " << version << std::endl
    << "# (fix {AJ1|AG1|AC1|AKR|AK1} hmtx width)" << std::endl
    << "# Copyright (C) 2019, 2020 Masamichi Hosoda" << std::endl
    << "# https://github.com/trueroad/HaranoAjiFonts-generator" << std::endl
    << "#" << std::endl;

  if (argc != 4)
    {
      std::cerr
        << "usage: fix_hmtx ROS TABLE.TBL aj1_hmtx.ttx > fixed_aj1_hmtx.ttx"
        << std::endl
        << std::endl
        << "     ROS:" << std::endl
        << "         {AJ1|AG1|AC1|AKR|AK1}" << std::endl
        << "     TABLE.TBL:" << std::endl
        << "         conversion table." << std::endl
        << "     aj1_hmtx.ttx:" << std::endl
        << "         {AJ1|AG1|AC1|AKR|AK1} "
        "hmtx table which contains wrong width."
        << std::endl;
      return 1;
    }

  std::string ros = argv[1];
  std::string table_filename = argv[2];
  std::string aj1_hmtx_filename = argv[3];

  std::cerr
    << "# inputs:" << std::endl
    << "#     ROS : \"" << ros << "\""
    << std::endl
    << "#     conversion table file: \"" << table_filename << "\""
    << std::endl
    << "#     aj1_hmtx filename: \"" << aj1_hmtx_filename << "\""
    << std::endl
    << "#" << std::endl;

  conv_table ct;
  try
    {
      ct.load (table_filename);
    }
  catch (std::exception &e)
    {
      std::cerr << "error: conv_table::load (): std::exception: "
                << e.what () << std::endl;
      return 1;
    }

  pugi::xml_document doc;

  auto result = doc.load_file (aj1_hmtx_filename.c_str ());
  if (!result)
    {
      std::cerr << "error: filename \"" << aj1_hmtx_filename
                << "\": " << result.description () << std::endl;
      return 1;
    }

  calc_width_ext cw (ros, doc);

  auto mtx_nodes
    = doc.select_nodes ("/ttFont/hmtx/mtx");

  for (auto it = mtx_nodes.begin ();
       it != mtx_nodes.end ();
       ++it)
    {
      auto mtx_node = it->node ();

      std::string cid_name = mtx_node.attribute ("name").as_string ();

      if (cid_name == ".notdef")
        cid_name = "0";

      auto cid_number_str
        = cid_name.substr (cid_name.find_first_of ("0123456789"));
      auto cid = std::stoi (cid_number_str);

      auto width = mtx_node.attribute ("width").as_int ();
      auto fixed_width = cw.get_width (cid);

      if (fixed_width < 0)
        continue; // pwid
      if (width == fixed_width)
        continue;

      if (std::find (ct.get_cid_miss ().cbegin (),
                     ct.get_cid_miss ().cend (),
                     cid)
          == ct.get_cid_miss ().cend ())
        std::cerr << cid << "\t" << width << "\t" << fixed_width
                  << std::endl;
      else
        std::cerr << "miss\t"
                  << cid << "\t" << width << "\t" << fixed_width
                  << std::endl;

      mtx_node.attribute ("width") = fixed_width;
    }

  doc.save (std::cout, "  ", pugi::format_default, pugi::encoding_utf8);

  return 0;
}
