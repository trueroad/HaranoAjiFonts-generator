//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// make_jisx0208_table_main.cc:
//   make JIS X 0208 conversion table from JISX0208-SourceHan-Mapping.txt
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

#include <exception>
#include <iostream>

#include "jisx0208_mapping.hh"
#include "version.hh"

int main (int argc, char *argv[])
{
  std::cout
    << "# make_jisx0208_table: Harano Aji Fonts generator " << version
    << std::endl
    << "# (make JIS X 0208 conversion table from"
    " JISX0208-SourceHan-Mapping.txt)"
    << std::endl
    << "# Copyright (C) 2019 Masamichi Hosoda" << std::endl
    << "# https://github.com/trueroad/HaranoAjiFonts-generator" << std::endl
    << "#" << std::endl;

  if (argc != 3)
    {
      std::cout
        << "# usage: make_jisx0208_table MAPPING_FILE TYPE > TABLE.TBL"
        << std::endl
        << "#" << std::endl
        << "#     MAPPING_FILE:" << std::endl
        << "#         JISX0208-SourceHan-Mapping.txt file" << std::endl
        << "#         from Adobe blog." << std::endl
        << "#     TYPE:" << std::endl
        << "#         {Sans|Serif}." << std::endl;
      return 1;
    }

  std::cout
    << "# inputs:" << std::endl
    << "#     mapping file: \"" << argv[1] << "\""
    << std::endl
    << "#     type        : \"" << argv[2] << "\""
    << std::endl
    << "#" << std::endl;

  jisx0208 js;
  try
    {
      js.load (argv[1], argv[2]);
    }
  catch (std::exception &e)
    {
      std::cerr << "error: js: std::exception: " << e.what ()
                << std::endl;
      return 1;
    }

  for (const auto &m: js.get_map ())
    {
      if (m.second < 0)
        std::cout << m.first << std::endl;
      else
        std::cout << m.first << "\t" << m.second << std::endl;
    }

  return 0;
}
