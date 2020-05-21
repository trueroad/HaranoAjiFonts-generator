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

#include "conv_table.hh"
#include "version.hh"

class calc_width
{
public:
  calc_width (const std::string &ros, pugi::xml_document &doc):
    ros_ (ros),
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

  int get_width (int cid)
  {
    if (ros_ == "AJ1")
      return aj1_width (cid);
    else if (ros_ == "AG1")
      return ag1_width (cid);
    else if (ros_ == "AC1")
      return ac1_width (cid);
    else if (ros_ == "AKR")
      return akr_width (cid);
    else if (ros_ == "AK1")
      return ak1_width (cid);

    return -1; // no change
  }

private:
  // Adobe-Japan1 (AJ1)
  int aj1_width (int cid)
  {
    if ((    1 <= cid && cid <=   230) ||
        ( 9354 <= cid && cid <=  9737) ||
        (15449 <= cid && cid <= 15975) ||
        (20317 <= cid && cid <= 20426))
      return -1; // pwid
    if ((  231 <= cid && cid <=   632) ||
        ( 8718 <= cid && cid <=  8719) ||
        (12063 <= cid && cid <= 12087))
      return 500; // hwid
    if (9758 <= cid && cid <= 9778)
      return 333; // twid
    if (9738 <= cid && cid <= 9757)
      return 250; // qwid

    return 1000; // fwid
  }

  // Adobe-GB1 (AG1)
  int ag1_width (int cid)
  {
    if ((    1 <= cid && cid <=    95) ||
        ( 7712 <= cid && cid <=  7715) ||
        (22353 <= cid && cid <= 22354))
      return -1; // pwid
    if ((  814 <= cid && cid <=   939) ||
        ( 7716 <= cid && cid <=  7716) ||
        (22355 <= cid && cid <= 22357))
      return 500; // hwid

    return 1000; // fwid
  }

  // Adobe-CNS1 (AC1)
  int ac1_width (int cid)
  {
    if ((    1 <= cid && cid <=    98) ||
        (17601 <= cid && cid <= 17601))
      return -1; // pwid
    if ((13648 <= cid && cid <= 13742) ||
        (17603 <= cid && cid <= 17603))
      return 500; // hwid

    return 1000; // fwid
  }

  // Adobe-KR (AKR)
  int akr_width (int cid)
  {
    // pwid CIDs but require to set width related to hangul width
    if (cid == 108)
      return hangul_width_ / 2;
    else if (cid == 110)
      return hangul_width_ / 3;
    else if (cid == 111)
      return hangul_width_ / 4;
    else if (cid == 112)
      return hangul_width_ / 6;
    else if (cid == 114)
      return hangul_width_ / 8;
    else if (cid == 115)
      return hangul_width_ / 16;

    // pwid CID but set to figure space width calculated from digit width
    if (cid == 113)
      return figure_space_width_;

    if ((    0 <= cid && cid <=     0) ||
        (  119 <= cid && cid <=   119) ||
        (  128 <= cid && cid <=   128) ||
        (  132 <= cid && cid <=   132) ||
        (  135 <= cid && cid <=   135) ||
        (  136 <= cid && cid <=   136) ||
        (  138 <= cid && cid <=   147) ||
        (  152 <= cid && cid <=   155) ||
        (  158 <= cid && cid <=   169) ||
        (11451 <= cid && cid <= 11877) ||
        (11895 <= cid && cid <= 11895) ||
        (11923 <= cid && cid <= 11925) ||
        (11932 <= cid && cid <= 11976) ||
        (11978 <= cid && cid <= 12107) ||
        (12151 <= cid && cid <= 12234) ||
        (14238 <= cid && cid <= 22479) ||
        (22690 <= cid && cid <= 22896))
      return 1000; // fwid
    if ((    1 <= cid && cid <=   108) ||
        (  110 <= cid && cid <=   118) ||
        (  120 <= cid && cid <=   127) ||
        (  129 <= cid && cid <=   131) ||
        (  133 <= cid && cid <=   133) ||
        (  134 <= cid && cid <=   134) ||
        (  137 <= cid && cid <=   137) ||
        (  148 <= cid && cid <=   151) ||
        (  156 <= cid && cid <=   156) ||
        (  157 <= cid && cid <=   157) ||
        ( 3001 <= cid && cid <=  3052) ||
        (11878 <= cid && cid <= 11894) ||
        (11896 <= cid && cid <= 11922) ||
        (11926 <= cid && cid <= 11931) ||
        (11977 <= cid && cid <= 11977) ||
        (22480 <= cid && cid <= 22689))
      return -1; // pwid
    if ((  109 <= cid && cid <=   109) ||
        (  170 <= cid && cid <=  3000) ||
        ( 3053 <= cid && cid <=  3056) ||
        ( 3059 <= cid && cid <= 11450) ||
        (12108 <= cid && cid <= 12150) ||
        (12237 <= cid && cid <= 13500))
      return hangul_width_; // Monospaced -> hangul width
    if (cid == 3057)
      return -1; // Two-em -> pwid
    if (cid == 3058)
      return -1; // Three-em -> pwid
    if (cid == 12235 || cid == 12236)
      return 250; // qwid
    if (13501 <= cid && cid <= 14237)
      return 0; // Zero-width

    std::cerr << "# Width error: AKR CID+" << cid << std::endl;

    return -1; // no change
  }

  // Adobe-Korea1 (AK1)
  int ak1_width (int cid)
  {
    if (   1 <= cid && cid <=  100)
      return -1; // pwid
    if (8094 <= cid && cid <= 8190)
      return 500; // hwid

    return 1000; // fwid
  }

  std::string ros_;
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

  calc_width cw (ros, doc);

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
