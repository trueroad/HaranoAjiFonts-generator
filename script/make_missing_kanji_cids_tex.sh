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

# https://github.com/adobe-fonts/source-han-serif/pull/123
echo -e "4378\tdummy" >> ${TEXDIR}/table-kanji.mincho.log
echo -e "5224\tdummy" >> ${TEXDIR}/table-kanji.mincho.log

# https://github.com/adobe-fonts/source-han-serif/issues/125
echo -e "13729\tdummy" >> ${TEXDIR}/table-kanji.mincho.log
echo -e "14019\tdummy" >> ${TEXDIR}/table-kanji.mincho.log

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
