#!/bin/sh

BUILDDIR=$1

if [ ! -d "${BUILDDIR}" ]; then
    echo "not found"
    exit
fi

DIR=$(cd $(dirname $0); pwd)
SCRIPTDIR=${DIR}/script

for x in ${BUILDDIR}/HaranoAji*; do
    echo "${x}"
    AVAILABLE_TXT=${x}/available.txt
    AVAILABLE_LOG=${x}/available.log
    if [ -e ${AVAILABLE_TXT} ]; then
        AVAILABLE_TXT=/dev/null
    fi
    if [ -e ${AVAILABLE_LOG} ]; then
        ${SCRIPTDIR}/show_available_cids.py \
                    ${x}/table.tbl ${x}/copy_and_rotate_do.tbl \
                    3>&1 1> ${AVAILABLE_TXT} 2>&3
    else
        ${SCRIPTDIR}/show_available_cids.py \
                    ${x}/table.tbl ${x}/copy_and_rotate_do.tbl \
                    1> ${AVAILABLE_TXT} 2> ${AVAILABLE_LOG}
        cat ${AVAILABLE_LOG}
    fi
done
