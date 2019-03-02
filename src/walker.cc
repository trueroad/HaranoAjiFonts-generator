//
// Harano Aji Fonts generator
// https://github.com/trueroad/HaranoAjiFonts-generator
//
// walker.hh:
//   xml walker
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

#include "walker.hh"

#include <vector>

#include <pugixml.hpp>

walker::next_action walker::walk_recursion (pugi::xml_node &node)
{
  switch (before (node))
    {
    case walker::next_action::cont:
      break;
    case walker::next_action::no_children:
      return walker::next_action::cont;
    case walker::next_action::remove:
      return walker::next_action::remove;
    case walker::next_action::abort:
      return walker::next_action::abort;
    default:
      return walker::next_action::abort;
    }

  std::vector<pugi::xml_node> remove;
  for (auto n: node.children ())
    {
      switch (walk_recursion (n))
        {
        case walker::next_action::cont:
          break;
        case walker::next_action::abort:
          return walker::next_action::abort;
        case walker::next_action::remove:
          remove.push_back (n);
          break;
        default:
          return walker::next_action::abort;
        }
    }

  for (auto n: remove)
    node.remove_child (n);

  if (!after (node))
    return walker::next_action::abort;

  return walker::next_action::cont;
}
