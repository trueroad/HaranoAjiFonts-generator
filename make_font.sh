#!/bin/sh

SRC_FONTBASE=$1
CMAP=$2

TTXVER=`ttx --version`
TOOLVER="ttx ${TTXVER}"

cd build/${SRC_FONTBASE}

BASEDIR=../..
BINDIR=${BASEDIR}/bin
SCRIPTDIR=${BASEDIR}/script
COMMONDATADIR=${BASEDIR}/common-data
TTXDIR=${BASEDIR}/ttx
DOWNLOADDIR=${BASEDIR}/download

case "${SRC_FONTBASE}" in
    SourceHanSansJP* )
        FONT_LANG=JP
	FONT_TYPE=Sans
        AI0_SOURCEHAN=${DOWNLOADDIR}/AI0-SourceHanSans
        AJ1X_KANJI=${DOWNLOADDIR}/SourceHanSans/aj16-kanji.txt
        ;;
    SourceHanSerifJP* )
        FONT_LANG=JP
	FONT_TYPE=Serif
        AI0_SOURCEHAN=${DOWNLOADDIR}/AI0-SourceHanSerif
        AJ1X_KANJI=${DOWNLOADDIR}/SourceHanSerif/aj16-kanji.txt
        ;;
    SourceHanSansCN* )
        FONT_LANG=CN
        FONT_TYPE=Sans
        ;;
    SourceHanSerifCN* )
        FONT_LANG=CN
        FONT_TYPE=Serif
        ;;
    * )
	echo invalid font name
	exit 1
	;;
esac

case "${FONT_LANG}" in
    JP )
        ROS_R=Adobe
        ROS_O=Japan1
        ROS_S=7
        ROS=AJ1
        FEATURE_GSUB_FEA=${DOWNLOADDIR}/aj17-gsub-jp04.fea
        FONT_NAME_SED=${BASEDIR}/font_name.sed
        SCRIPT_MAKE_ADJUST=${SCRIPTDIR}/make_adjust.py
        ;;
    CN )
        ROS_R=Adobe
        ROS_O=GB1
        ROS_S=5
        ROS=AG1
        FEATURE_GSUB_FEA=${DOWNLOADDIR}/ag15-gsub.fea
        FONT_NAME_SED=${BASEDIR}/font_name_cn.sed
        SCRIPT_MAKE_ADJUST=${SCRIPTDIR}/make_adjust_center.py
        ;;
    * )
        echo invalid FONT_LANG
        exit 1
        ;;
esac

echo deleting old files...
rm -f *.ttx *.log \
   || { echo error; exit 1; }

echo "making conversion table (from cmap and CMap)..."
${BINDIR}/make_conv_table \
    ${TTXDIR}/${SRC_FONTBASE}._c_m_a_p.ttx ${DOWNLOADDIR}/${CMAP} \
    > table-cmap.tbl 2> table-cmap.log \
   || { echo error; exit 1; }

if [ "${FONT_LANG}" = "JP" ]; then
    echo "making conversion table (from JISX0208-SourceHan-Mapping.txt)..."
    ${BINDIR}/make_jisx0208_table \
        ${DOWNLOADDIR}/JISX0208-SourceHan-Mapping.txt ${FONT_TYPE} \
        > table-jisx0208.tbl 2> table-jisx0208.log \
        || { echo error; exit 1; }

    echo "making conversion table (from AI0-SourceHan and aj16-kanji.txt)..."
    ${BINDIR}/make_kanji_table \
        ${AI0_SOURCEHAN} ${AJ1X_KANJI} \
        > table-kanji.tbl 2> table-kanji.log \
        || { echo error; exit 1; }

    echo merging convertion tables...
    ${BINDIR}/merge_table \
        table-cmap.tbl table-kanji.tbl \
        > table01.tbl 2> table01.log \
        || { echo error; exit 1; }
    ${BINDIR}/merge_table \
        table01.tbl table-jisx0208.tbl \
        > table10.tbl 2> table10.log \
        || { echo error; exit 1; }
else
    echo "skipping language-specific conversion table making and merging..."
    cp table-cmap.tbl table10.tbl
fi

echo "making conversion table (OpenType feature fwid)..."
${BINDIR}/make_feature_table \
    table10.tbl fwid ${TTXDIR}/${SRC_FONTBASE}.G_S_U_B_.ttx \
    ${FEATURE_GSUB_FEA} \
    > table-fwid.tbl 2> table-fwid.log \
   || { echo error; exit 1; }

echo "making conversion table (OpenType feature hwid)..."
${BINDIR}/make_feature_table \
    table10.tbl hwid ${TTXDIR}/${SRC_FONTBASE}.G_S_U_B_.ttx \
    ${FEATURE_GSUB_FEA} \
    > table-hwid.tbl 2> table-hwid.log \
   || { echo error; exit 1; }

echo "making conversion table (OpenType feature pwid)..."
${BINDIR}/make_feature_table \
    table10.tbl pwid ${TTXDIR}/${SRC_FONTBASE}.G_S_U_B_.ttx \
    ${FEATURE_GSUB_FEA} \
    > table-pwid.tbl 2> table-pwid.log \
   || { echo error; exit 1; }

echo "making conversion table (OpenType feature ruby)..."
${BINDIR}/make_feature_table \
    table10.tbl ruby ${TTXDIR}/${SRC_FONTBASE}.G_S_U_B_.ttx \
    ${FEATURE_GSUB_FEA} \
    > table-ruby.tbl 2> table-ruby.log \
   || { echo error; exit 1; }

echo "making conversion table (OpenType feature vert)..."
${BINDIR}/make_feature_table \
    table10.tbl vert ${TTXDIR}/${SRC_FONTBASE}.G_S_U_B_.ttx \
    ${FEATURE_GSUB_FEA} \
    > table-vert.tbl 2> table-vert.log \
   || { echo error; exit 1; }

echo "merging convertion tables (OpenType features)..."
${BINDIR}/merge_table \
    table-fwid.tbl table10.tbl \
    > table11.tbl 2> table11.log \
   || { echo error; exit 1; }
${BINDIR}/merge_table \
    table-hwid.tbl table11.tbl \
    > table12.tbl 2> table12.log \
   || { echo error; exit 1; }
${BINDIR}/merge_table \
    table-pwid.tbl table12.tbl \
    > table13.tbl 2> table13.log \
   || { echo error; exit 1; }
${BINDIR}/merge_table \
    table-ruby.tbl table13.tbl \
    > table14.tbl 2> table14.log \
   || { echo error; exit 1; }
${BINDIR}/merge_table \
    table-vert.tbl table14.tbl \
    > table20.tbl 2> table20.log \
   || { echo error; exit 1; }

echo "making conversion table (OpenType feature fwid) pass 2..."
${BINDIR}/make_feature_table \
    table20.tbl fwid ${TTXDIR}/${SRC_FONTBASE}.G_S_U_B_.ttx \
    ${FEATURE_GSUB_FEA} \
    > table-fwid2.tbl 2> table-fwid2.log \
   || { echo error; exit 1; }

echo "making conversion table (OpenType feature hwid) pass 2..."
${BINDIR}/make_feature_table \
    table20.tbl hwid ${TTXDIR}/${SRC_FONTBASE}.G_S_U_B_.ttx \
    ${FEATURE_GSUB_FEA} \
    > table-hwid2.tbl 2> table-hwid2.log \
   || { echo error; exit 1; }

echo "making conversion table (OpenType feature pwid) pass 2..."
${BINDIR}/make_feature_table \
    table20.tbl pwid ${TTXDIR}/${SRC_FONTBASE}.G_S_U_B_.ttx \
    ${FEATURE_GSUB_FEA} \
    > table-pwid2.tbl 2> table-pwid2.log \
   || { echo error; exit 1; }

echo "making conversion table (OpenType feature ruby) pass 2..."
${BINDIR}/make_feature_table \
    table20.tbl ruby ${TTXDIR}/${SRC_FONTBASE}.G_S_U_B_.ttx \
    ${FEATURE_GSUB_FEA} \
    > table-ruby2.tbl 2> table-ruby2.log \
   || { echo error; exit 1; }

echo "making conversion table (OpenType feature vert) pass 2..."
${BINDIR}/make_feature_table \
    table20.tbl vert ${TTXDIR}/${SRC_FONTBASE}.G_S_U_B_.ttx \
    ${FEATURE_GSUB_FEA} \
    > table-vert2.tbl 2> table-vert2.log \
   || { echo error; exit 1; }

echo "merging convertion tables (OpenType features) pass 2..."
${BINDIR}/merge_table \
    table-fwid2.tbl table20.tbl \
    > table21.tbl 2> table21.log \
   || { echo error; exit 1; }
${BINDIR}/merge_table \
    table-hwid2.tbl table21.tbl \
    > table22.tbl 2> table22.log \
   || { echo error; exit 1; }
${BINDIR}/merge_table \
    table-pwid2.tbl table22.tbl \
    > table23.tbl 2> table23.log \
   || { echo error; exit 1; }
${BINDIR}/merge_table \
    table-ruby2.tbl table23.tbl \
    > table24.tbl 2> table24.log \
   || { echo error; exit 1; }
${BINDIR}/merge_table \
    table-vert2.tbl table24.tbl \
    > table.tbl 2> table.log \
   || { echo error; exit 1; }

echo making glyphorder...
${BINDIR}/make_glyphorder \
    table.tbl \
    > glyphorder.ttx 2> glyphorder.log \
   || { echo error; exit 1; }

echo converting name table...
${BINDIR}/conv_name \
    ${SRC_FONTBASE} "${TOOLVER}" ${TTXDIR}/${SRC_FONTBASE}._n_a_m_e.ttx \
    2> name.log | sed -f ${FONT_NAME_SED} > name.ttx \
   || { echo error; exit 1; }
echo converting cmap table...
${BINDIR}/conv_cmap \
    table.tbl ${TTXDIR}/${SRC_FONTBASE}._c_m_a_p.ttx \
    > cmap.ttx 2> cmap.log \
   || { echo error; exit 1; }
echo converting CFF table...
${BINDIR}/conv_CFF \
    ${ROS_R} ${ROS_O} ${ROS_S} \
    table.tbl ${TTXDIR}/${SRC_FONTBASE}.C_F_F_.ttx \
    2> CFF01.log | sed -f ${FONT_NAME_SED} > CFF01.ttx \
    || { echo error; exit 1; }
if [ -f ${TTXDIR}/${SRC_FONTBASE}.G_D_E_F_.ttx ]; then
    echo converting GDEF table...
    ${BINDIR}/conv_GDEF \
        table.tbl ${TTXDIR}/${SRC_FONTBASE}.G_D_E_F_.ttx \
        > GDEF.ttx 2> GDEF.log \
       || { echo error; exit 1; }
else
    echo no GDEF table...
fi
echo converting GSUB table...
${BINDIR}/conv_GSUB \
    table.tbl ${TTXDIR}/${SRC_FONTBASE}.G_S_U_B_.ttx \
    > GSUB01.ttx 2> GSUB.log \
   || { echo error; exit 1; }
echo converting VORG table...
${BINDIR}/conv_VORG \
    table.tbl ${TTXDIR}/${SRC_FONTBASE}.V_O_R_G_.ttx \
    > VORG.ttx 2> VORG.log \
   || { echo error; exit 1; }
echo converting hmtx table...
${BINDIR}/conv_mtx \
    table.tbl ${TTXDIR}/${SRC_FONTBASE}._h_m_t_x.ttx \
    > hmtx_conv.ttx 2> hmtx_conv.log \
   || { echo error; exit 1; }
echo fixing widths in hmtx table...
${BINDIR}/fix_hmtx \
    ${ROS} table.tbl hmtx_conv.ttx \
    > hmtx_width.ttx 2> hmtx_width.log \
   || { echo error; exit 1; }
echo converting vmtx table...
${BINDIR}/conv_mtx \
    table.tbl ${TTXDIR}/${SRC_FONTBASE}._v_m_t_x.ttx \
    > vmtx_conv.ttx 2> vmtx_conv.log \
   || { echo error; exit 1; }

if [ "${FONT_LANG}" = "JP" ]; then
    echo copying and rotating glyphs in CFF table...
    ${SCRIPTDIR}/copy_and_rotate.py \
        ${COMMONDATADIR}/copy_and_rotate.tbl \
        CFF01.ttx \
        CFF02.ttx \
        > copy_and_rotate.log \
        || { echo error; exit 1; }

    echo calculating letter face for shift table...
    ${SCRIPTDIR}/calc_letter_face.py \
        ${COMMONDATADIR}/shift.lst \
        CFF02.ttx \
        > letter_face01.tbl \
        || { echo error; exit 1; }
else
    echo "skipping language-specific copying and rotating glyphs..."
    cp CFF01.ttx CFF02.ttx
fi

echo making adjust table...
${SCRIPT_MAKE_ADJUST} \
    table.tbl \
    ${TTXDIR}/${SRC_FONTBASE}._h_m_t_x.ttx hmtx_width.ttx \
    > adjust01.tbl 2> make_adjust.log \
    || { echo error; exit 1; }

if [ "${FONT_LANG}" = "JP" ]; then
    echo making shift table...
    ${SCRIPTDIR}/make_shift.py \
        letter_face01.tbl \
        > shift.tbl \
        || { echo error; exit 1; }

    echo adding shift table to adjust table...
    cat adjust01.tbl shift.tbl > adjust02.tbl \
        || { echo error; exit 1; }
else
    echo "skipping language-specific shift table making and merging..."
    cp adjust01.tbl adjust02.tbl
fi

echo adjusting CFF table...
${SCRIPTDIR}/adjust.py \
    adjust02.tbl \
    CFF02.ttx \
    CFF.ttx \
    > adjust.log \
    || { echo error; exit 1; }

if [ "${FONT_LANG}" = "JP" ]; then
    echo "making {h|v}mtx fixing table..."
    cat adjust02.tbl ${COMMONDATADIR}/copy_and_rotate.tbl > fix_mtx.tbl \
        || { echo error; exit 1; }
else
    echo "skipping language-specific {h|v}mtx fixing table making..."
    cp adjust02.tbl fix_mtx.tbl
fi

echo "calculating letter face for fixing {h|v}mtx and GPOS conversion..."
${SCRIPTDIR}/calc_letter_face.py \
    fix_mtx.tbl \
    CFF.ttx \
    > letter_face02.tbl \
    || { echo error; exit 1; }

echo fixing LSB in hmtx table...
${SCRIPTDIR}/fix_mtx.py \
    letter_face02.tbl \
    hmtx_width.ttx \
    hmtx.ttx \
    > hmtx_lsb.log \
    || { echo error; exit 1; }

if [ "${FONT_LANG}" = "JP" ]; then
    echo fixing TSB in vmtx table...
    ${SCRIPTDIR}/fix_mtx.py \
        letter_face02.tbl \
        vmtx_conv.ttx \
        vmtx.ttx \
        > vmtx_tsb.log \
        || { echo error; exit 1; }
else
    echo "skipping language-specific TSB fixing in vmtx table..."
    cp vmtx_conv.ttx vmtx.ttx
fi

echo making conversion table for GPOS...
${SCRIPTDIR}/make_table_for_GPOS.py \
    table.tbl \
    letter_face02.tbl \
    > table_for_GPOS.tbl \
    || { echo error; exit 1; }

echo converting GPOS table...
${BINDIR}/conv_GPOS \
    table_for_GPOS.tbl ${TTXDIR}/${SRC_FONTBASE}.G_P_O_S_.ttx \
    > GPOS.ttx 2> GPOS.log \
   || { echo error; exit 1; }

if [ "${FONT_LANG}" = "JP" ]; then
    echo adding GSUB vert/vrt2 substitution...
    ${SCRIPTDIR}/add_gsub_v.py \
        GSUB01.ttx GSUB.ttx \
        > GSUB_add_v.log \
        || { echo error; exit 1; }
else
    echo "skipping language-specific GSUB vert/vrt2 substitution adding..."
    cp GSUB01.ttx GSUB.ttx
fi

echo symbolic linking other tables...
ln -s ${TTXDIR}/${SRC_FONTBASE}._h_e_a_d.ttx || { echo error; exit 1; }
ln -s ${TTXDIR}/${SRC_FONTBASE}._h_h_e_a.ttx || { echo error; exit 1; }
ln -s ${TTXDIR}/${SRC_FONTBASE}._m_a_x_p.ttx || { echo error; exit 1; }
ln -s ${TTXDIR}/${SRC_FONTBASE}.O_S_2f_2.ttx || { echo error; exit 1; }
ln -s ${TTXDIR}/${SRC_FONTBASE}._p_o_s_t.ttx || { echo error; exit 1; }
ln -s ${TTXDIR}/${SRC_FONTBASE}.B_A_S_E_.ttx || { echo error; exit 1; }
ln -s ${TTXDIR}/${SRC_FONTBASE}._v_h_e_a.ttx || { echo error; exit 1; }

echo converting root ttx file...
sed -f ${BASEDIR}/font_tables.sed ${TTXDIR}/${SRC_FONTBASE}.ttx \
    > output.ttx \
   || { echo error; exit 1; }

ttx -b --recalc-timestamp output.ttx \
   || { echo error; exit 1; }
