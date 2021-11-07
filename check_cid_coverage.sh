#!/bin/sh

FONTBUILDDIR="$1"

if [ ! -d "${FONTBUILDDIR}" ]; then
    echo "not found ${FONTBUILDDIR}"
    exit
fi

AVAILABLE_TXT=${FONTBUILDDIR}/available.txt

if [ ! -f "${AVAILABLE_TXT}" ]; then
    echo "not found ${AVAILABLE_TXT}"
    exit
fi

DIR=$(cd $(dirname $0); pwd)
BINDIR=${DIR}/bin
SCRIPTDIR=${DIR}/script
COMMONDATADIR=${DIR}/common-data
DOWNLOADDIR=${DIR}/download

case "${FONTBUILDDIR}" in
    *Mincho* )
        AJ16_KANJI=${DOWNLOADDIR}/SourceHanSerif/aj16-kanji.txt
        ;;
    *Gothic* )
        AJ16_KANJI=${DOWNLOADDIR}/SourceHanSans/aj16-kanji.txt
        ;;
    * )
        echo "not font build dir"
        exit 1
        ;;
esac

echo -e "\n*** aj16-kanji ***"
${SCRIPTDIR}/check_aj16-kanji_coverage.py \
            ${AJ16_KANJI} \
            ${AVAILABLE_TXT}

echo -e "\n*** jisx0208 ***"
${SCRIPTDIR}/check_jisx0208_coverage.py \
            ${DOWNLOADDIR}/JISX0208-SourceHan-Mapping.txt \
            ${AVAILABLE_TXT}

echo -e "\n*** Kana ***"
${SCRIPTDIR}/check_kana_coverage.py \
            ${AVAILABLE_TXT}

echo -e "\n*** CMap H ***"
${BINDIR}/check_table_CMap \
         ${FONTBUILDDIR}/table.tbl \
         ${FONTBUILDDIR}/copy_and_rotate_do.tbl \
         ${DOWNLOADDIR}/H \
         2> /dev/null

echo -e "\n*** CMap V ***"
${BINDIR}/check_table_CMap \
         ${FONTBUILDDIR}/table.tbl \
         ${FONTBUILDDIR}/copy_and_rotate_do.tbl \
         ${DOWNLOADDIR}/V \
         2> /dev/null

echo -e "\n*** CMap 2004-H (only JIS X 0208) ***"
${BINDIR}/check_table_CMap --jisx0208 \
         ${FONTBUILDDIR}/table.tbl \
         ${FONTBUILDDIR}/copy_and_rotate_do.tbl \
         ${DOWNLOADDIR}/2004-H \
         2> /dev/null

echo -e "\n*** CMap 2004-V (only JIS X 0208) ***"
${BINDIR}/check_table_CMap --jisx0208 \
         ${FONTBUILDDIR}/table.tbl \
         ${FONTBUILDDIR}/copy_and_rotate_do.tbl \
         ${DOWNLOADDIR}/2004-V \
         2> /dev/null
