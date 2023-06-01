//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// merge_table_main.cc:
//   merge conversion tables
//
// Copyright (C) 2019, 2023 Masamichi Hosoda.
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
#include <exception>
#include <iostream>
#include <map>

#include "conv_table.hh"
#include "version.hh"

int main (int argc, char *argv[])
{
  std::cout
    << "# merge_table: Harano Aji Fonts generator " << version
    << std::endl
    << "# (merge conversion tables)"
    << std::endl
    << "# Copyright (C) 2019, 2023 Masamichi Hosoda" << std::endl
    << "# https://github.com/trueroad/HaranoAjiFonts-generator" << std::endl
    << "#" << std::endl;

  if (argc != 3)
    {
      std::cout
        << "# usage: merge_table TABLE1.TBL TABLE2.TBL > TABLE.TBL"
        << "#" << std::endl
        << "#" << std::endl
        << "#     TABLE1.TBL:" << std::endl
        << "#         conversion table." << std::endl
        << "#     TABLE2.TBL:" << std::endl
        << "#         conversion table (preferred)." << std::endl;
      return 1;
    }

  std::cout
    << "# input:" << std::endl
    << "#     conversion table file            : \"" << argv[1] << "\""
    << std::endl
    << "#     conversion table file (preferred): \"" << argv[2] << "\""
    << std::endl
    << "#"
    << std::endl;

  conv_table ct1;
  try
    {
      ct1.load (argv[1]);
    }
  catch (std::exception &e)
    {
      std::cerr << "error: conv_table 1: std::exception: " << e.what ()
                << std::endl;
      return 1;
    }

  conv_table ct2;
  try
    {
      ct2.load (argv[2]);
    }
  catch (std::exception &e)
    {
      std::cerr << "error: conv_table 2: std::exception: " << e.what ()
                << std::endl;
      return 1;
    }

  auto b = std::min (ct1.get_map ().begin ()->first,
                     ct2.get_map ().begin ()->first);
  auto e = std::max
    (ct1.get_map ().size () != 0 ? ct1.get_map ().rbegin ()->first : 0,
     ct2.get_map ().size () != 0 ? ct2.get_map ().rbegin ()->first : 0);

  std::map<int, int> map;
  std::map<int, int> dup;
  for (int cid_in = b; cid_in <= e; ++cid_in)
    {
      if (ct2.get_map ().find (cid_in) != ct2.get_map ().end ())
        {
          auto cid_out = ct2.get_map ().at (cid_in);

          if (cid_out >= 0)
            {
              if (dup.find (cid_out) != dup.end () &&
                  dup[cid_out] != cid_in)
                {
                  std::cout << "#duplicate cid "
                            << dup[cid_out]
                            << " (removed), cid "
                            << cid_in
                            << " (preferred) -> cid "
                            << cid_out << std::endl;
                  map[dup[cid_out]] = -1;
                }
              map[cid_in] = cid_out;
              dup[cid_out] = cid_in;

              continue;
            }
        }

      if (ct1.get_map ().find (cid_in) != ct1.get_map ().end ())
        {
          auto cid_out = ct1.get_map ().at (cid_in);

          if (cid_out >= 0)
            {
              if (dup.find (cid_out) != dup.end () &&
                  dup[cid_out] != cid_in)
                {
                  std::cout
                    << "#duplicate: cid "
                    << dup[cid_out]
                    << " (preferred), cid "
                    << cid_in
                    << " (ignored) -> cid "
                    << cid_out << std::endl;
                }
              else
                {
                  map[cid_in] = cid_out;
                  dup[cid_out] = cid_in;
                }
            }
          else
            map[cid_in] = -1;
        }
      else
        map[cid_in] = -1;
    }

  int cid_max = -1;
  for (const auto &m: map)
    {
      if (m.second < 0)
        std::cout << m.first << std::endl;
      else
        {
          std::cout << m.first << "\t" << m.second << std::endl;
          if (cid_max < m.second)
            {
              cid_max = m.second;
            }
        }
    }

  auto ct1_cid_max = ct1.get_cid_max ();
  auto ct2_cid_max = ct2.get_cid_max ();
  if (ct2_cid_max < ct1_cid_max)
    {
      if (cid_max < ct1_cid_max)
        {
          std::cout << "max\t" << ct1.get_cid_max () << std::endl;
        }
    }
  else
    {
      if (cid_max < ct2_cid_max)
        {
          std::cout << "max\t" << ct2.get_cid_max () << std::endl;
        }
    }

  return 0;
}
