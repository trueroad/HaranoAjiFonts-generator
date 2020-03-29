#!/bin/sh

SRC_FONTBASE=$1
CMAP=$2

TTXVER=`ttx --version`
TOOLVER="ttx ${TTXVER}"

cd build/${SRC_FONTBASE}

BASEDIR=../..
BINDIR=${BASEDIR}/bin
TTXDIR=${BASEDIR}/ttx
DOWNLOADDIR=${BASEDIR}/download
SCRIPTDIR=${BASEDIR}/script

case "${SRC_FONTBASE}" in
    SourceHanSans* )
        AI0_SOURCEHAN=${DOWNLOADDIR}/AI0-SourceHanSans
        AJ1X_KANJI=${DOWNLOADDIR}/SourceHanSans/aj16-kanji.txt
	FONT_TYPE=Sans
        ;;
    SourceHanSerif* )
        AI0_SOURCEHAN=${DOWNLOADDIR}/AI0-SourceHanSerif
        AJ1X_KANJI=${DOWNLOADDIR}/SourceHanSerif/aj16-kanji.txt
	FONT_TYPE=Serif
        ;;
    * )
	echo invalid font name
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

echo "making conversion table (OpenType feature fwid)..."
${BINDIR}/make_feature_table \
    table10.tbl fwid ${TTXDIR}/${SRC_FONTBASE}.G_S_U_B_.ttx \
    ${DOWNLOADDIR}/aj17-gsub-jp04.fea \
    > table-fwid.tbl 2> table-fwid.log \
   || { echo error; exit 1; }

echo "making conversion table (OpenType feature hwid)..."
${BINDIR}/make_feature_table \
    table10.tbl hwid ${TTXDIR}/${SRC_FONTBASE}.G_S_U_B_.ttx \
    ${DOWNLOADDIR}/aj17-gsub-jp04.fea \
    > table-hwid.tbl 2> table-hwid.log \
   || { echo error; exit 1; }

echo "making conversion table (OpenType feature pwid)..."
${BINDIR}/make_feature_table \
    table10.tbl pwid ${TTXDIR}/${SRC_FONTBASE}.G_S_U_B_.ttx \
    ${DOWNLOADDIR}/aj17-gsub-jp04.fea \
    > table-pwid.tbl 2> table-pwid.log \
   || { echo error; exit 1; }

echo "making conversion table (OpenType feature ruby)..."
${BINDIR}/make_feature_table \
    table10.tbl ruby ${TTXDIR}/${SRC_FONTBASE}.G_S_U_B_.ttx \
    ${DOWNLOADDIR}/aj17-gsub-jp04.fea \
    > table-ruby.tbl 2> table-ruby.log \
   || { echo error; exit 1; }

echo "making conversion table (OpenType feature vert)..."
${BINDIR}/make_feature_table \
    table10.tbl vert ${TTXDIR}/${SRC_FONTBASE}.G_S_U_B_.ttx \
    ${DOWNLOADDIR}/aj17-gsub-jp04.fea \
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
    ${DOWNLOADDIR}/aj17-gsub-jp04.fea \
    > table-fwid2.tbl 2> table-fwid2.log \
   || { echo error; exit 1; }

echo "making conversion table (OpenType feature hwid) pass 2..."
${BINDIR}/make_feature_table \
    table20.tbl hwid ${TTXDIR}/${SRC_FONTBASE}.G_S_U_B_.ttx \
    ${DOWNLOADDIR}/aj17-gsub-jp04.fea \
    > table-hwid2.tbl 2> table-hwid2.log \
   || { echo error; exit 1; }

echo "making conversion table (OpenType feature pwid) pass 2..."
${BINDIR}/make_feature_table \
    table20.tbl pwid ${TTXDIR}/${SRC_FONTBASE}.G_S_U_B_.ttx \
    ${DOWNLOADDIR}/aj17-gsub-jp04.fea \
    > table-pwid2.tbl 2> table-pwid2.log \
   || { echo error; exit 1; }

echo "making conversion table (OpenType feature ruby) pass 2..."
${BINDIR}/make_feature_table \
    table20.tbl ruby ${TTXDIR}/${SRC_FONTBASE}.G_S_U_B_.ttx \
    ${DOWNLOADDIR}/aj17-gsub-jp04.fea \
    > table-ruby2.tbl 2> table-ruby2.log \
   || { echo error; exit 1; }

echo "making conversion table (OpenType feature vert) pass 2..."
${BINDIR}/make_feature_table \
    table20.tbl vert ${TTXDIR}/${SRC_FONTBASE}.G_S_U_B_.ttx \
    ${DOWNLOADDIR}/aj17-gsub-jp04.fea \
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
    2> name.log | sed -f ${BASEDIR}/font_name.sed > name.ttx \
   || { echo error; exit 1; }
echo converting cmap table...
${BINDIR}/conv_cmap \
    table.tbl ${TTXDIR}/${SRC_FONTBASE}._c_m_a_p.ttx \
    > cmap.ttx 2> cmap.log \
   || { echo error; exit 1; }
echo converting CFF table...
${BINDIR}/conv_CFF \
    table.tbl ${TTXDIR}/${SRC_FONTBASE}.C_F_F_.ttx \
    2> CFF01.log | sed -f ${BASEDIR}/font_name.sed > CFF01.ttx \
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
echo converting GPOS table...
${BINDIR}/conv_GPOS \
    table.tbl ${TTXDIR}/${SRC_FONTBASE}.G_P_O_S_.ttx \
    > GPOS.ttx 2> GPOS.log \
   || { echo error; exit 1; }
echo converting GSUB table...
${BINDIR}/conv_GSUB \
    table.tbl ${TTXDIR}/${SRC_FONTBASE}.G_S_U_B_.ttx \
    > GSUB.ttx 2> GSUB.log \
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
    table.tbl hmtx_conv.ttx \
    > hmtx.ttx 2> hmtx.log \
   || { echo error; exit 1; }
echo converting vmtx table...
${BINDIR}/conv_mtx \
    table.tbl ${TTXDIR}/${SRC_FONTBASE}._v_m_t_x.ttx \
    > vmtx.ttx 2> vmtx.log \
   || { echo error; exit 1; }

echo making adjust table...
${SCRIPTDIR}/make_adjust.py \
    table.tbl \
    ${TTXDIR}/${SRC_FONTBASE}._h_m_t_x.ttx hmtx.ttx \
    > adjust.tbl 2> make_adjust.log \
    || { echo error; exit 1; }
echo adjusting CFF table...
${SCRIPTDIR}/adjust.py \
    adjust.tbl \
    CFF01.ttx \
    CFF.ttx \
    > adjust.log \
    || { echo error; exit 1; }

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
