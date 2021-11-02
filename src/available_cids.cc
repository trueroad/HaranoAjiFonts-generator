//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// available_cids.cc:
//   Get available CIDs
//
// Copyright (C) 2021 Masamichi Hosoda.
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

#include "available_cids.hh"

#include <exception>
#include <iostream>
#include <set>
#include <string>

#include "conv_table.hh"
#include "copy_and_rotate_table.hh"

namespace
{
  std::set<int> load_cr_cids (const std::string &filename)
  {
    copy_and_rotate_table crt;
    crt.load (filename);

    auto cid_outs = crt.get_cid_outs ();
    std::set<int> retval (cid_outs.begin (), cid_outs.end ());

    return retval;
  }
};

std::set<int> get_available_cids (const std::string &table_filename,
                                  const std::string &copy_and_rotate_filename)
{
  std::set<int> retval;

  conv_table ct;
  try
    {
      ct.load (table_filename);
    }
  catch (std::exception &e)
    {
      std::cerr << "error: conv_table::load (): std::exception: "
                << e.what () << std::endl;
      return retval;
    }

  try
    {
      retval = load_cr_cids (copy_and_rotate_filename);
    }
  catch (std::exception &e)
    {
      std::cerr << "error: load_cr_cids (): std::exception: "
                << e.what () << std::endl;
      return retval;
    }

  std::copy (ct.get_cid_outs ().begin (), ct.get_cid_outs ().end (),
             std::inserter (retval, retval.end ()));

  return retval;
}
