#!/bin/sh

cat build/HaranoAjiGothic-*/palt_to_pwid_copy01.tbl | sort | uniq \
    | sed -e "s/palt_to_pwid/palt_to_pwid fixed/" \
    > common-data/palt_to_pwid_fixed_sans.tbl
cat build/HaranoAjiMincho-*/palt_to_pwid_copy01.tbl | sort | uniq \
    | sed -e "s/palt_to_pwid/palt_to_pwid fixed/" \
    > common-data/palt_to_pwid_fixed_serif.tbl

cat build/HaranoAjiGothic-*/vpal_to_pwidvert_copy01.tbl | sort | uniq \
    | sed -e "s/vpal_to_pwidvert/vpal_to_pwidvert fixed/" \
    > common-data/vpal_to_pwidvert_fixed_sans.tbl
cat build/HaranoAjiMincho-*/vpal_to_pwidvert_copy01.tbl | sort | uniq \
    | sed -e "s/vpal_to_pwidvert/vpal_to_pwidvert fixed/" \
    > common-data/vpal_to_pwidvert_fixed_serif.tbl
