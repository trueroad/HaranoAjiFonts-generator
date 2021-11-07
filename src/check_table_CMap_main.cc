//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// check_table_CMap_main.cc:
//   check pre defined CID coverage in conversion table by CMap file
//
// Copyright (C) 2019, 2021 Masamichi Hosoda.
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
#include <set>
#include <string>
#include <vector>

#include "cmdlineparse.hh"

#include "available_cids.hh"
#include "cmapfile.hh"
#include "version.hh"

namespace
{
  bool is_jisx0208 (int c)
  {
    if ((0x2121 <= c && c <= 0x217e) || // 1 ku

        // 2 ku
        (0x2221 <= c && c <= 0x222E) ||
        (0x223a <= c && c <= 0x2241) ||
        (0x224a <= c && c <= 0x2250) ||
        (0x225c <= c && c <= 0x226a) ||
        (0x2272 <= c && c <= 0x2279) ||
        (c == 0x227e) ||

        // 3 ku
        (0x2330 <= c && c <= 0x2339) || // Number
        (0x2341 <= c && c <= 0x235a) || // Latin alphabet upper case
        (0x2361 <= c && c <= 0x237a) || // Latin alphabet lower case

        // 4 ku
        (0x2421 <= c && c <= 0x2473) || // Hiragana

        // 5 ku
        (0x2521 <= c && c <= 0x2576) || // Katakana

        // 6 ku
        (0x2621 <= c && c <= 0x2638) || // Greek alphabet upper case
        (0x2641 <= c && c <= 0x2658) || // Greek alphabet lower case

        // 7 ku
        (0x2721 <= c && c <= 0x2741) || // Cyrillic alphabet upper case
        (0x2751 <= c && c <= 0x2771) || // Cyrillic alphabet lower case

        // 8 ku
        (0x2821 <= c && c <= 0x2840) || // Rule

        // 16 ku ~ 47 ku, Kanji 1 st
        (0x3021 <= c && c <= 0x307e) || // 16 ku
        (0x3121 <= c && c <= 0x317e) ||
        (0x3221 <= c && c <= 0x327e) ||
        (0x3321 <= c && c <= 0x337e) ||
        (0x3421 <= c && c <= 0x347e) ||
        (0x3521 <= c && c <= 0x357e) ||
        (0x3621 <= c && c <= 0x367e) ||
        (0x3721 <= c && c <= 0x377e) ||
        (0x3821 <= c && c <= 0x387e) ||
        (0x3921 <= c && c <= 0x397e) ||
        (0x3a21 <= c && c <= 0x3a7e) ||
        (0x3b21 <= c && c <= 0x3b7e) ||
        (0x3c21 <= c && c <= 0x3c7e) ||
        (0x3d21 <= c && c <= 0x3d7e) ||
        (0x3e21 <= c && c <= 0x3e7e) ||
        (0x3f21 <= c && c <= 0x3f7e) || // 31 ku

        (0x4021 <= c && c <= 0x407e) || // 32 ku
        (0x4121 <= c && c <= 0x417e) ||
        (0x4221 <= c && c <= 0x427e) ||
        (0x4321 <= c && c <= 0x437e) ||
        (0x4421 <= c && c <= 0x447e) ||
        (0x4521 <= c && c <= 0x457e) ||
        (0x4621 <= c && c <= 0x467e) ||
        (0x4721 <= c && c <= 0x477e) ||
        (0x4821 <= c && c <= 0x487e) ||
        (0x4921 <= c && c <= 0x497e) ||
        (0x4a21 <= c && c <= 0x4a7e) ||
        (0x4b21 <= c && c <= 0x4b7e) ||
        (0x4c21 <= c && c <= 0x4c7e) ||
        (0x4d21 <= c && c <= 0x4d7e) ||
        (0x4e21 <= c && c <= 0x4e7e) ||
        (0x4f21 <= c && c <= 0x4f53) || // 47 ku

        // 48 ku ~ 84 ku, Kanji 2 nd
        (0x5021 <= c && c <= 0x507e) || // 48 ku
        (0x5121 <= c && c <= 0x517e) ||
        (0x5221 <= c && c <= 0x527e) ||
        (0x5321 <= c && c <= 0x537e) ||
        (0x5421 <= c && c <= 0x547e) ||
        (0x5521 <= c && c <= 0x557e) ||
        (0x5621 <= c && c <= 0x567e) ||
        (0x5721 <= c && c <= 0x577e) ||
        (0x5821 <= c && c <= 0x587e) ||
        (0x5921 <= c && c <= 0x597e) ||
        (0x5a21 <= c && c <= 0x5a7e) ||
        (0x5b21 <= c && c <= 0x5b7e) ||
        (0x5c21 <= c && c <= 0x5c7e) ||
        (0x5d21 <= c && c <= 0x5d7e) ||
        (0x5e21 <= c && c <= 0x5e7e) ||
        (0x5f21 <= c && c <= 0x5f7e) || // 63 ku

        (0x6021 <= c && c <= 0x607e) || // 64 ku
        (0x6121 <= c && c <= 0x617e) ||
        (0x6221 <= c && c <= 0x627e) ||
        (0x6321 <= c && c <= 0x637e) ||
        (0x6421 <= c && c <= 0x647e) ||
        (0x6521 <= c && c <= 0x657e) ||
        (0x6621 <= c && c <= 0x667e) ||
        (0x6721 <= c && c <= 0x677e) ||
        (0x6821 <= c && c <= 0x687e) ||
        (0x6921 <= c && c <= 0x697e) ||
        (0x6a21 <= c && c <= 0x6a7e) ||
        (0x6b21 <= c && c <= 0x6b7e) ||
        (0x6c21 <= c && c <= 0x6c7e) ||
        (0x6d21 <= c && c <= 0x6d7e) ||
        (0x6e21 <= c && c <= 0x6e7e) ||
        (0x6f21 <= c && c <= 0x6f7e) || // 79 ku

        (0x7021 <= c && c <= 0x707e) || // 80 ku
        (0x7121 <= c && c <= 0x717e) ||
        (0x7221 <= c && c <= 0x727e) ||
        (0x7321 <= c && c <= 0x737e) ||
        (0x7421 <= c && c <= 0x7426)) // 84 ku
        return true;

    return false;
  }
};

int main (int argc, char *argv[])
{
  cmdlineparse::parser cmd;
  bool bjisx0208;

  cmd.set_version_string
    (std::string ("check_table_CMap: Harano Aji Fonts generator ") +
     version + "\n" +
     "(check pre defined CID coverage in conversion table by CMap file)\n"
     "Copyright (C) 2019, 2021 Masamichi Hosoda\n"
     "https://github.com/trueroad/HaranoAjiFonts-generator\n");
  cmd.add_default ();

  cmd.add_flag (0, "jisx0208", &bjisx0208,
                "    Check only JIS X 0208 coverage.\n"
                "    (for 2004-H and 2004-V)");

  cmd.set_usage_unamed_opts ("TABLE.TBL CR.TBL CMAP_FILE");

  cmd.add_description (0, "", cmdlineparse::arg_mode::no_argument,
                       "  (in) TABLE.TBL\n"
                       "    conversion table.\n"
                       "  (in) CR.TBL\n"
                       "    copy and rotate table.\n"
                       "  (in) CMAP_FILE\n"
                       "    The CMap file for CID coverage check.\n"
                       "    e.g. H, V, 2004-H, or 2004-V etc.");

  if (!cmd.parse (argc, argv))
    return 0;

  if (cmd.get_unamed_args ().size () != 3)
    {
      std::cout << cmd.build_help () << std::endl;
      return 1;
    }

  std::cout << cmd.get_version_string () << std::endl;

  const std::string table_filename = cmd.get_unamed_args ()[0];
  const std::string cr_filename = cmd.get_unamed_args ()[1];
  const std::string cmap_filename = cmd.get_unamed_args ()[2];

  std::cout
    << "inputs:" << std::endl
    << "    conversion table file: \"" << table_filename << "\""
    << std::endl
    << "    copy and rotate table: \"" << cr_filename << "\""
    << std::endl
    << "    CMap file            : \"" << cmap_filename << "\""
    << std::endl
    << "    JIS X 0208 flag      : ";
  if (bjisx0208)
    std::cout << "true" << std::endl << std::endl;
  else
    std::cout << "false" << std::endl << std::endl;

  const auto exists = get_available_cids (table_filename,
                                          cr_filename);

  cmapfile cmf;
  try
    {
      cmf.load (cmap_filename);
    }
  catch (std::exception &e)
    {
      std::cerr << "error: cmapfile: std::exception: " << e.what ()
                << std::endl;
      return 1;
    }

  std::set<int> non_jisx0208;

  std::map<int, int> miss;
  for (const auto &c: cmf.get_map ())
    {
      const auto letter = c.first;
      if (bjisx0208 && !is_jisx0208 (letter))
        {
          non_jisx0208.insert (letter);
          continue;
        }

      const auto cid = c.second;
      if (exists.find (cid) == exists.cend ())
        miss.emplace (c.first, c.second);
    }

  if (bjisx0208)
    {
      std::cout << "Number of non JIS X 0208 letters in CMap: "
                << non_jisx0208.size ()
                << std::endl;
    }

  if (miss.size ())
    for (const auto &m: miss)
      std::cout << "miss 0x" << std::hex << m.first << std::dec
                << " -> cid " << m.second << std::endl;
  else
    std::cout << "All CIDs exist." << std::endl;

  return 0;
}
