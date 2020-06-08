#!/bin/sh

cat build/HaranoAjiGothic-*/palt_to_pwid_copy01.tbl | sort | uniq \
    | sed -e "s/palt_to_pwid/palt_to_pwid fixed/" \
    > common-data/palt_to_pwid_fixed_sans.tbl
cat build/HaranoAjiMincho-*/palt_to_pwid_copy01.tbl | sort | uniq \
    | sed -e "s/palt_to_pwid/palt_to_pwid fixed/" \
    > common-data/palt_to_pwid_fixed_serif.tbl
