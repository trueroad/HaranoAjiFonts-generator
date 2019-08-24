#!/bin/sh

for x in build/*/table.tbl; do
    echo "${x} without .notdef"
    egrep "^[[:digit:]]+[[:space:]][[:digit:]]+" ${x} | wc -l
done
