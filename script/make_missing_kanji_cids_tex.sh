#!/bin/sh

DIR=$(cd $(dirname $0); pwd)
TEXDIR=${DIR}/../tex
BINDIR=${DIR}/../bin
SCRIPTDIR=${DIR}/../script
DOWNLOADDIR=${DIR}/../download

${BINDIR}/make_kanji_table \
    ${DOWNLOADDIR}/AI0-SourceHanSerif \
    ${DOWNLOADDIR}/SourceHanSerif/aj16-kanji.txt \
    > /dev/null 2> ${TEXDIR}/table-kanji.mincho.log

${SCRIPTDIR}/missing_kanji_to_tex.py \
            ${TEXDIR}/table-kanji.mincho.log \
            > ${TEXDIR}/missing-kanji-cids-mincho.txt

${BINDIR}/make_kanji_table \
    ${DOWNLOADDIR}/AI0-SourceHanSans \
    ${DOWNLOADDIR}/SourceHanSans/aj16-kanji.txt \
    > /dev/null 2> ${TEXDIR}/table-kanji.gothic.log

${SCRIPTDIR}/missing_kanji_to_tex.py \
            ${TEXDIR}/table-kanji.gothic.log \
            > ${TEXDIR}/missing-kanji-cids-gothic.txt
