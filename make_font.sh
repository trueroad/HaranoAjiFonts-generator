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

case "${SRC_FONTBASE}" in
    SourceHanSans* )
        AI0_SOURCEHAN=${DOWNLOADDIR}/AI0-SourceHanSans
        AJ1X_KANJI=${DOWNLOADDIR}/SourceHanSans/aj16-kanji.txt
        ;;
    SourceHanSerif* )
        AI0_SOURCEHAN=${DOWNLOADDIR}/AI0-SourceHanSerif
        AJ1X_KANJI=${DOWNLOADDIR}/SourceHanSerif/aj16-kanji.txt
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

echo "making conversion table (OpenType feature fwid)..."
${BINDIR}/make_feature_table \
    table01.tbl fwid ${TTXDIR}/${SRC_FONTBASE}.G_S_U_B_.ttx \
    ${DOWNLOADDIR}/aj16-gsub-jp04.txt \
    > table-fwid.tbl 2> table-fwid.log \
   || { echo error; exit 1; }

echo "making conversion table (OpenType feature hwid)..."
${BINDIR}/make_feature_table \
    table01.tbl hwid ${TTXDIR}/${SRC_FONTBASE}.G_S_U_B_.ttx \
    ${DOWNLOADDIR}/aj16-gsub-jp04.txt \
    > table-hwid.tbl 2> table-hwid.log \
   || { echo error; exit 1; }

echo "making conversion table (OpenType feature pwid)..."
${BINDIR}/make_feature_table \
    table01.tbl pwid ${TTXDIR}/${SRC_FONTBASE}.G_S_U_B_.ttx \
    ${DOWNLOADDIR}/aj16-gsub-jp04.txt \
    > table-pwid.tbl 2> table-pwid.log \
   || { echo error; exit 1; }

echo "making conversion table (OpenType feature ruby)..."
${BINDIR}/make_feature_table \
    table01.tbl ruby ${TTXDIR}/${SRC_FONTBASE}.G_S_U_B_.ttx \
    ${DOWNLOADDIR}/aj16-gsub-jp04.txt \
    > table-ruby.tbl 2> table-ruby.log \
   || { echo error; exit 1; }

echo "making conversion table (OpenType feature vert)..."
${BINDIR}/make_feature_table \
    table01.tbl vert ${TTXDIR}/${SRC_FONTBASE}.G_S_U_B_.ttx \
    ${DOWNLOADDIR}/aj16-gsub-jp04.txt \
    > table-vert.tbl 2> table-vert.log \
   || { echo error; exit 1; }

echo "merging convertion tables (OpenType features)..."
${BINDIR}/merge_table \
    table-fwid.tbl table01.tbl \
    > table02.tbl 2> table02.log \
   || { echo error; exit 1; }
${BINDIR}/merge_table \
    table-hwid.tbl table02.tbl \
    > table03.tbl 2> table03.log \
   || { echo error; exit 1; }
${BINDIR}/merge_table \
    table-pwid.tbl table03.tbl \
    > table04.tbl 2> table04.log \
   || { echo error; exit 1; }
${BINDIR}/merge_table \
    table-ruby.tbl table04.tbl \
    > table05.tbl 2> table05.log \
   || { echo error; exit 1; }
${BINDIR}/merge_table \
    table-vert.tbl table05.tbl \
    > table06.tbl 2> table06.log \
   || { echo error; exit 1; }

echo "making conversion table (OpenType feature fwid) pass 2..."
${BINDIR}/make_feature_table \
    table06.tbl fwid ${TTXDIR}/${SRC_FONTBASE}.G_S_U_B_.ttx \
    ${DOWNLOADDIR}/aj16-gsub-jp04.txt \
    > table-fwid2.tbl 2> table-fwid2.log \
   || { echo error; exit 1; }

echo "making conversion table (OpenType feature hwid) pass 2..."
${BINDIR}/make_feature_table \
    table06.tbl hwid ${TTXDIR}/${SRC_FONTBASE}.G_S_U_B_.ttx \
    ${DOWNLOADDIR}/aj16-gsub-jp04.txt \
    > table-hwid2.tbl 2> table-hwid2.log \
   || { echo error; exit 1; }

echo "making conversion table (OpenType feature pwid) pass 2..."
${BINDIR}/make_feature_table \
    table06.tbl pwid ${TTXDIR}/${SRC_FONTBASE}.G_S_U_B_.ttx \
    ${DOWNLOADDIR}/aj16-gsub-jp04.txt \
    > table-pwid2.tbl 2> table-pwid2.log \
   || { echo error; exit 1; }

echo "making conversion table (OpenType feature ruby) pass 2..."
${BINDIR}/make_feature_table \
    table06.tbl ruby ${TTXDIR}/${SRC_FONTBASE}.G_S_U_B_.ttx \
    ${DOWNLOADDIR}/aj16-gsub-jp04.txt \
    > table-ruby2.tbl 2> table-ruby2.log \
   || { echo error; exit 1; }

echo "making conversion table (OpenType feature vert) pass 2..."
${BINDIR}/make_feature_table \
    table06.tbl vert ${TTXDIR}/${SRC_FONTBASE}.G_S_U_B_.ttx \
    ${DOWNLOADDIR}/aj16-gsub-jp04.txt \
    > table-vert2.tbl 2> table-vert2.log \
   || { echo error; exit 1; }

echo "merging convertion tables (OpenType features) pass 2..."
${BINDIR}/merge_table \
    table-fwid2.tbl table06.tbl \
    > table07.tbl 2> table07.log \
   || { echo error; exit 1; }
${BINDIR}/merge_table \
    table-hwid2.tbl table07.tbl \
    > table08.tbl 2> table08.log \
   || { echo error; exit 1; }
${BINDIR}/merge_table \
    table-pwid2.tbl table08.tbl \
    > table09.tbl 2> table09.log \
   || { echo error; exit 1; }
${BINDIR}/merge_table \
    table-ruby2.tbl table09.tbl \
    > table10.tbl 2> table10.log \
   || { echo error; exit 1; }
${BINDIR}/merge_table \
    table-vert2.tbl table10.tbl \
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
    2> CFF.log | sed -f ${BASEDIR}/font_name.sed > CFF.ttx \
   || { echo error; exit 1; }
echo converting VORG table...
${BINDIR}/conv_VORG \
    table.tbl ${TTXDIR}/${SRC_FONTBASE}.V_O_R_G_.ttx \
    > VORG.ttx 2> VORG.log \
   || { echo error; exit 1; }
echo converting hmtx table...
${BINDIR}/conv_mtx \
    table.tbl ${TTXDIR}/${SRC_FONTBASE}._h_m_t_x.ttx \
    > hmtx.ttx 2> hmtx.log \
   || { echo error; exit 1; }
echo converting vmtx table...
${BINDIR}/conv_mtx \
    table.tbl ${TTXDIR}/${SRC_FONTBASE}._v_m_t_x.ttx \
    > vmtx.ttx 2> vmtx.log \
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
