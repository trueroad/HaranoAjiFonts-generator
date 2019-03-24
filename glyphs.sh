#!/bin/sh

for x in "$@"; do

  if [ ! -f ${x%.*}.ttx ]; then
    ttx -t GlyphOrder $x > /dev/null 2> /dev/null
  fi

  echo ${x%.*}
  grep "<GlyphID id=" ${x%.*}.ttx | wc -l

done
