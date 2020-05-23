#!/bin/sh

BUILDDIR=$1

for x in ${BUILDDIR}/*; do
    echo "${x}"
    CONV=$(egrep "^[[:digit:]]+[[:space:]][[:digit:]]+" \
        ${x}/table.tbl | wc -l)
    COPY=$(egrep "^aji[[:digit:]]+[[:space:]]aji[[:digit:]]+" \
        ${x}/copy_and_rotate01.tbl | wc -l)
    TOTAL=$(expr ${CONV} + ${COPY} + 1)
    echo "conversion = ${CONV}, copy = ${COPY}, .notdef = 1: total ${TOTAL}"
done
