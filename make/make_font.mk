all: output.otf

.PHONY: all install clean dist-clean

include $(MAKEDIR)/set_variables.mk

clean:
	rm -f *.ttx *.log

dist-clean: clean
	rm -f *.tbl output.otf

install: output.otf
	cp output.otf $(BASEDIR)/$(DEST_FONTBASE).otf


### Make conversion tables ###

# Conversion table from cmap
table-cmap.tbl: $(TTXDIR)/$(SRC_FONTBASE)._c_m_a_p.ttx $(CMAP_FILE)
	@echo "making conversion table (from cmap and CMap)..."
	@$(BINDIR)/make_conv_table \
		$+ \
		> $@ 2> $(addsuffix .log,$(basename $@))

# JP specific conversion table
ifeq ($(FONT_LANG),JP)
table-jisx0208.tbl: $(JISX0208_MAPPING)
	@echo \
	"making conversion table (from JISX0208-SourceHan-Mapping.txt)..."
	@$(BINDIR)/make_jisx0208_table \
		$< $(FONT_TYPE) \
		> $@ 2> $(addsuffix .log,$(basename $@))

table-kanji.tbl: $(AI0_SOURCEHAN) $(AJ1X_KANJI)
	@echo \
	"making conversion table (from AI0-SourceHan and aj16-kanji.txt)..."
	@$(BINDIR)/make_kanji_table \
		$+ \
		> $@ 2> $(addsuffix .log,$(basename $@))

table01.tbl: table-cmap.tbl table-kanji.tbl
	@echo "merging convertion tables (kanji)..."
	@$(BINDIR)/merge_table \
		$+ \
		> $@ 2> $(addsuffix .log,$(basename $@))

table10.tbl: table01.tbl table-jisx0208.tbl
	@echo "merging convertion tables (jisx0208)..."
	@$(BINDIR)/merge_table \
		$+ \
		> $@ 2> $(addsuffix .log,$(basename $@))
else
table10.tbl: table-cmap.tbl
	@echo \
	"skipping language-specific conversion table making and merging..."
	@ln -s $< $@
endif


# Conversion tables from GSUB features pass 1
table-fwid.tbl: table10.tbl $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
		$(FEATURE_GSUB_FEA)
	@echo "making conversion table (OpenType feature fwid)..."
	@$(BINDIR)/make_feature_table \
		$< fwid $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
		$(FEATURE_GSUB_FEA) \
		> $@ 2> $(addsuffix .log,$(basename $@))

table-hwid.tbl: table10.tbl $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
		$(FEATURE_GSUB_FEA)
	@echo "making conversion table (OpenType feature hwid)..."
	@$(BINDIR)/make_feature_table \
		$< hwid $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
		$(FEATURE_GSUB_FEA) \
		> $@ 2> $(addsuffix .log,$(basename $@))

table-pwid.tbl: table10.tbl $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
		$(FEATURE_GSUB_FEA)
	@echo "making conversion table (OpenType feature pwid)..."
	@$(BINDIR)/make_feature_table \
		$< pwid $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
		$(FEATURE_GSUB_FEA) \
		> $@ 2> $(addsuffix .log,$(basename $@))

table-ruby.tbl: table10.tbl $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
		$(FEATURE_GSUB_FEA)
	@echo "making conversion table (OpenType feature ruby)..."
	@$(BINDIR)/make_feature_table \
		$< ruby $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
		$(FEATURE_GSUB_FEA) \
		> $@ 2> $(addsuffix .log,$(basename $@))

table-vert.tbl: table10.tbl $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
		$(FEATURE_GSUB_FEA)
	@echo "making conversion table (OpenType feature vert)..."
	@$(BINDIR)/make_feature_table \
		$< vert $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
		$(FEATURE_GSUB_FEA) \
		> $@ 2> $(addsuffix .log,$(basename $@))

table-ccmp.tbl: table10.tbl $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
		$(FEATURE_GSUB_FEA)
	@echo "making conversion table (OpenType feature ccmp)..."
	@$(BINDIR)/make_ligature_table \
		$< ccmp $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
		$(FEATURE_GSUB_FEA) \
		> $@ 2> $(addsuffix .log,$(basename $@))

table-liga.tbl: table10.tbl $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
		$(FEATURE_GSUB_FEA)
	@echo "making conversion table (OpenType feature liga)..."
	@$(BINDIR)/make_ligature_table \
		$< liga $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
		$(FEATURE_GSUB_FEA) \
		> $@ 2> $(addsuffix .log,$(basename $@))

#table-dlig.tbl: table10.tbl $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
#		$(FEATURE_GSUB_FEA)
#	@echo "making conversion table (OpenType feature dlig)..."
#	@$(BINDIR)/make_ligature_table \
#		$< dlig $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
#		$(FEATURE_GSUB_FEA) \
#		> $@ 2> $(addsuffix .log,$(basename $@))

# Merge conversion tables from GSUB features pass 1
table11.tbl: table-fwid.tbl table10.tbl
	@echo "merging convertion tables (fwid)..."
	@$(BINDIR)/merge_table \
		$+ \
		> $@ 2> $(addsuffix .log,$(basename $@))

table12.tbl: table-hwid.tbl table11.tbl
	@echo "merging convertion tables (hwid)..."
	@$(BINDIR)/merge_table \
		$+ \
		> $@ 2> $(addsuffix .log,$(basename $@))

table13.tbl: table-pwid.tbl table12.tbl
	@echo "merging convertion tables (pwid)..."
	@$(BINDIR)/merge_table \
		$+ \
		> $@ 2> $(addsuffix .log,$(basename $@))

table14.tbl: table-ruby.tbl table13.tbl
	@echo "merging convertion tables (ruby)..."
	@$(BINDIR)/merge_table \
		$+ \
		> $@ 2> $(addsuffix .log,$(basename $@))

table15.tbl: table-vert.tbl table14.tbl
	@echo "merging convertion tables (vert)..."
	@$(BINDIR)/merge_table \
		$+ \
		> $@ 2> $(addsuffix .log,$(basename $@))

table16.tbl: table-ccmp.tbl table15.tbl
	@echo "merging convertion tables (ccmp)..."
	@$(BINDIR)/merge_table \
		$+ \
		> $@ 2> $(addsuffix .log,$(basename $@))

table20.tbl: table-liga.tbl table16.tbl
	@echo "merging convertion tables (liga)..."
	@$(BINDIR)/merge_table \
		$+ \
		> $@ 2> $(addsuffix .log,$(basename $@))

#table20.tbl: table-dlig.tbl table17.tbl
#	@echo "merging convertion tables (dlig)..."
#	@$(BINDIR)/merge_table \
#		$+ \
#		> $@ 2> $(addsuffix .log,$(basename $@))


# Conversion tables from GSUB features pass 2
table-fwid2.tbl: table20.tbl $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
		$(FEATURE_GSUB_FEA)
	@echo "making conversion table (OpenType feature fwid) pass 2..."
	@$(BINDIR)/make_feature_table \
		$< fwid $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
		$(FEATURE_GSUB_FEA) \
		> $@ 2> $(addsuffix .log,$(basename $@))

table-hwid2.tbl: table20.tbl $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
		$(FEATURE_GSUB_FEA)
	@echo "making conversion table (OpenType feature hwid) pass 2..."
	@$(BINDIR)/make_feature_table \
		$< hwid $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
		$(FEATURE_GSUB_FEA) \
		> $@ 2> $(addsuffix .log,$(basename $@))

table-pwid2.tbl: table20.tbl $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
		$(FEATURE_GSUB_FEA)
	@echo "making conversion table (OpenType feature pwid) pass 2..."
	@$(BINDIR)/make_feature_table \
		$< pwid $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
		$(FEATURE_GSUB_FEA) \
		> $@ 2> $(addsuffix .log,$(basename $@))

table-ruby2.tbl: table20.tbl $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
		$(FEATURE_GSUB_FEA)
	@echo "making conversion table (OpenType feature ruby) pass 2..."
	@$(BINDIR)/make_feature_table \
		$< ruby $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
		$(FEATURE_GSUB_FEA) \
		> $@ 2> $(addsuffix .log,$(basename $@))

table-vert2.tbl: table20.tbl $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
		$(FEATURE_GSUB_FEA)
	@echo "making conversion table (OpenType feature vert) pass 2..."
	@$(BINDIR)/make_feature_table \
		$< vert $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
		$(FEATURE_GSUB_FEA) \
		> $@ 2> $(addsuffix .log,$(basename $@))

table-ccmp2.tbl: table20.tbl $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
		$(FEATURE_GSUB_FEA)
	@echo "making conversion table (OpenType feature ccmp) pass 2..."
	@$(BINDIR)/make_ligature_table \
		$< ccmp $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
		$(FEATURE_GSUB_FEA) \
		> $@ 2> $(addsuffix .log,$(basename $@))

table-liga2.tbl: table20.tbl $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
		$(FEATURE_GSUB_FEA)
	@echo "making conversion table (OpenType feature liga) pass 2..."
	@$(BINDIR)/make_ligature_table \
		$< liga $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
		$(FEATURE_GSUB_FEA) \
		> $@ 2> $(addsuffix .log,$(basename $@))

#table-dlig2.tbl: table20.tbl $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
#		$(FEATURE_GSUB_FEA)
#	@echo "making conversion table (OpenType feature dlig) pass 2..."
#	@$(BINDIR)/make_ligature_table \
#		$< dlig $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
#		$(FEATURE_GSUB_FEA) \
#		> $@ 2> $(addsuffix .log,$(basename $@))

# Merge conversion tables from GSUB features pass 2
table21.tbl: table-fwid2.tbl table20.tbl
	@echo "merging convertion tables (fwid) pass 2..."
	@$(BINDIR)/merge_table \
		$+ \
		> $@ 2> $(addsuffix .log,$(basename $@))

table22.tbl: table-hwid2.tbl table21.tbl
	@echo "merging convertion tables (hwid) pass 2..."
	@$(BINDIR)/merge_table \
		$+ \
		> $@ 2> $(addsuffix .log,$(basename $@))

table23.tbl: table-pwid2.tbl table22.tbl
	@echo "merging convertion tables (pwid) pass 2..."
	@$(BINDIR)/merge_table \
		$+ \
		> $@ 2> $(addsuffix .log,$(basename $@))

table24.tbl: table-ruby2.tbl table23.tbl
	@echo "merging convertion tables (ruby) pass 2..."
	@$(BINDIR)/merge_table \
		$+ \
		> $@ 2> $(addsuffix .log,$(basename $@))

table25.tbl: table-vert2.tbl table24.tbl
	@echo "merging convertion tables (vert) pass 2..."
	@$(BINDIR)/merge_table \
		$+ \
		> $@ 2> $(addsuffix .log,$(basename $@))

table26.tbl: table-ccmp2.tbl table25.tbl
	@echo "merging convertion tables (ccmp) pass 2..."
	@$(BINDIR)/merge_table \
		$+ \
		> $@ 2> $(addsuffix .log,$(basename $@))

table30.tbl: table-liga2.tbl table26.tbl
	@echo "merging convertion tables (liga) pass 2..."
	@$(BINDIR)/merge_table \
		$+ \
		> $@ 2> $(addsuffix .log,$(basename $@))

#table30.tbl: table-dlig2.tbl table27.tbl
#	@echo "merging convertion tables (dlig) pass 2..."
#	@$(BINDIR)/merge_table \
#		$+ \
#		> $@ 2> $(addsuffix .log,$(basename $@))


# JP specific conversion table 2
ifeq ($(FONT_LANG),JP)
table-vkana.tbl: table30.tbl \
		$(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx \
		$(FEATURE_GSUB_FEA)
	@echo "making conversion table (from VKana)..."
	@$(BINDIR)/make_vkana_table \
		$+ \
		$@ copy_vkana.tbl feature_vkna.tbl \
		> $(addsuffix .log,$(basename $@)) 2>&1

copy_vkana.tbl: table-vkana.tbl

feature_vkna.tbl: table-vkana.tbl

table.tbl: table-vkana.tbl table30.tbl
	@echo "merging convertion tables (VKana)..."
	@$(BINDIR)/merge_table \
		$+ \
		> $@ 2> $(addsuffix .log,$(basename $@))
else
table.tbl: table30.tbl
	@echo \
	"skipping language-specific conversion table 2 making and merging..."
	@ln -s $< $@

copy_vkana.tbl:
	@touch $@

feature_vkna.tbl:
	@touch $@
endif


# Make conversion table for GPOS
table_for_GPOS.tbl: table.tbl letter_face.tbl
	@echo "making conversion table for GPOS..."
	@$(SCRIPTDIR)/make_table_for_GPOS.py \
		$+ \
		> $@ 2> $(addsuffix .log,$(basename $@))


### Convert ###

# Glyph order
glyphorder.ttx: table.tbl
	@echo "making glyphorder..."
	@$(BINDIR)/make_glyphorder \
		$< \
		> $@ 2> $(addsuffix .log,$(basename $@))

# Convert name table
name.ttx: $(TTXDIR)/$(SRC_FONTBASE)._n_a_m_e.ttx
	@echo "converting name table..."
	@$(BINDIR)/conv_name \
		$(SRC_FONTBASE) \
		"$(TOOLVER)" \
		$< \
		2> $(addsuffix .log,$(basename $@)) | \
		sed -f $(FONT_NAME_SED) > $@

# Convert cmap table
cmap01.ttx: table.tbl $(TTXDIR)/$(SRC_FONTBASE)._c_m_a_p.ttx
	@echo "converting cmap table..."
	@$(BINDIR)/conv_cmap \
		$+ \
		> $@ 2> $(addsuffix .log,$(basename $@))

# Convert CFF table
CFF01.ttx: table.tbl $(TTXDIR)/$(SRC_FONTBASE).C_F_F_.ttx
	@echo "converting CFF table..."
	@$(BINDIR)/conv_CFF \
		$(ROS_R) $(ROS_O) $(ROS_S) \
		$+ \
		2> $(addsuffix .log,$(basename $@)) | \
		sed -f $(FONT_NAME_SED) > $@

# Convert GDEF table
GDEF.ttx: table.tbl $(TTXDIR)/$(SRC_FONTBASE).G_D_E_F_.ttx
	@echo "converting GDEF table..."
	@$(BINDIR)/conv_GDEF \
		$+ \
		> $@ 2> $(addsuffix .log,$(basename $@))

# Convert GPOS table
GPOS.ttx: table_for_GPOS.tbl $(TTXDIR)/$(SRC_FONTBASE).G_P_O_S_.ttx
	@echo "converting GPOS table..."
	@$(BINDIR)/conv_GPOS \
		$+ \
		> $@ 2> $(addsuffix .log,$(basename $@))

# Convert GSUB table
GSUB01.ttx: table.tbl $(TTXDIR)/$(SRC_FONTBASE).G_S_U_B_.ttx
	@echo "converting GSUB table..."
	@$(BINDIR)/conv_GSUB \
		$+ \
		> $@ 2> $(addsuffix .log,$(basename $@))

# Convert VORG table
VORG.ttx: table.tbl $(TTXDIR)/$(SRC_FONTBASE).V_O_R_G_.ttx
	@echo "converting VORG table..."
	@$(BINDIR)/conv_VORG \
		$+ \
		> $@ 2> $(addsuffix .log,$(basename $@))

# Convert hmtx table
hmtx01.ttx: table.tbl $(TTXDIR)/$(SRC_FONTBASE)._h_m_t_x.ttx
	@echo "converting hmtx table..."
	@$(BINDIR)/conv_mtx \
		$+ \
		> $@ 2> $(addsuffix .log,$(basename $@))

# Convert vmtx table
vmtx01.ttx: table.tbl $(TTXDIR)/$(SRC_FONTBASE)._v_m_t_x.ttx
	@echo "converting vmtx table..."
	@$(BINDIR)/conv_mtx \
		$+ \
		> $@ 2> $(addsuffix .log,$(basename $@))


### Fix hmtx ###

# Fix widths in hmtx table
hmtx02.ttx: table.tbl hmtx01.ttx
	@echo "fixing widths in hmtx table..."
	@$(BINDIR)/fix_hmtx \
		$(ROS) $+ \
		> $@ 2> $(addsuffix .log,$(basename $@))

# Set hmtx width for pwid glyphs
hmtx03.ttx: adjust_pwid.tbl hmtx02.ttx
	@echo "setting hmtx width for pwid glyphs..."
	@$(SCRIPTDIR)/set_hmtx_width.py \
		$+ \
		$@ \
		> $(addsuffix .log,$(basename $@)) 2>&1

# Fix LSB in hmtx table
hmtx.ttx: letter_face.tbl hmtx03.ttx
	@echo "fixing LSB in hmtx table..."
	@$(SCRIPTDIR)/fix_mtx.py \
		$+ \
		$@ \
		> $(addsuffix .log,$(basename $@)) 2>&1


### Fix vmtx ###

# Fix TSB in vmtx table
vmtx.ttx: letter_face.tbl vmtx01.ttx
	@echo "fixing TSB in vmtx table..."
	@$(SCRIPTDIR)/fix_mtx.py \
		$+ \
		$@ \
		> $(addsuffix .log,$(basename $@)) 2>&1


### Fix cmap ###

# Add CIDs to cmap table
cmap02.ttx: table.tbl copy_and_rotate_do.tbl ${CMAP_FILE} cmap01.ttx
	@echo "adding glyphs to cmap..."
	@$(BINDIR)/add_cmap $+ $@ \
		> $(addsuffix .log,$(basename $@)) 2>&1

# Truncate cmap table
ifeq ($(FONT_LANG),KR)
TRUNCATE_CMAP_FLAG = 1
endif
ifeq ($(FONT_LANG),TW)
ifeq ($(FONT_TYPE),Sans)
TRUNCATE_CMAP_FLAG = 1
endif
endif
ifdef TRUNCATE_CMAP_FLAG
# cmap table format 4 subtable size exceeds the limit.
cmap.ttx: cmap02.ttx
	@echo "truncating cmap format 4..."
	@$(SCRIPTDIR)/truncate_cmap_format4.py \
		$< $@ \
		> $(addsuffix .log,$(basename $@)) 2>&1
else
cmap.ttx: cmap02.ttx
	@echo "skipping truncating cmap format 4..."
	@ln -s $< $@
endif


### Fix CFF ###

# Copy and rotate glyphs in CFF table
CFF02.ttx: copy_and_rotate_do.tbl CFF01.ttx
	@echo "copying and rotating glyphs in CFF table..."
	@$(SCRIPTDIR)/copy_and_rotate.py \
		$+ \
		$@ \
		> $(addsuffix .log,$(basename $@)) 2>&1

# Adjust CFF table
CFF.ttx: adjust.tbl CFF02.ttx
	@echo "adjusting CFF table..."
	@$(SCRIPTDIR)/adjust.py \
		$+ \
		$@ \
		> $(addsuffix .log,$(basename $@)) 2>&1


### Fix GSUB ###

# Add GSUB pwid substitution
GSUB02.ttx: palt_to_pwid_copy.tbl GSUB01.ttx
	@echo "adding GSUB pwid substitution..."
	@$(SCRIPTDIR)/add_gsub_single.py \
		pwid \
		$+ \
		$@ \
		> $(addsuffix .log,$(basename $@)) 2>&1

# Add GSUB vert/vert2 substitution
ifeq ($(FONT_LANG),JP)
GSUB03.ttx: GSUB02.ttx
	@echo "adding GSUB vert/vrt2 substitution..."
	@$(SCRIPTDIR)/add_gsub_v.py \
		$< \
		$@ \
		> $(addsuffix .log,$(basename $@)) 2>&1
else
GSUB03.ttx: GSUB02.ttx
	@echo \
	"skipping language-specific GSUB vert/vrt2 substitution adding..."
	@ln -s $< $@
endif

# Integrate GSUB vert lookup tables
GSUB04.ttx: GSUB03.ttx
	@echo "integrating GSUB vert lookup tables..."
	@$(SCRIPTDIR)/integrate_gsub_vert.py \
		$< \
		$@ \
		> $(addsuffix .log,$(basename $@)) 2>&1

# Remove VKana from GSUB vert
ifeq ($(FONT_LANG),JP)
GSUB05.ttx: feature_vkna.tbl GSUB04.ttx
	@echo "removing VKana from GSUB vert..."
	@$(SCRIPTDIR)/remove_gsub_single.py \
		vert \
		$+ \
		$@ \
		> $(addsuffix .log,$(basename $@)) 2>&1
else
GSUB05.ttx: GSUB04.ttx
	@echo \
	"skipping language-specific GSUB vert substitution removing..."
	@ln -s $< $@
endif

# Add GSUB substitutes
ifeq ($(FONT_LANG),JP)
feature_expt.tbl: table.tbl copy_and_rotate_do.tbl
	@echo "making GSUB expt table..."
	@$(BINDIR)/make_gsub_single_table \
		expt \
		$+ \
		$(FEATURE_GSUB_FEA) \
		> $@ \
		2> $(addsuffix .log,$(basename $@))

feature_hojo.tbl: table.tbl copy_and_rotate_do.tbl
	@echo "making GSUB hojo table..."
	@$(BINDIR)/make_gsub_single_table \
		hojo \
		$+ \
		$(FEATURE_GSUB_FEA) \
		> $@ \
		2> $(addsuffix .log,$(basename $@))

feature_pkna.tbl: table.tbl copy_and_rotate_do.tbl
	@echo "making GSUB pkna table..."
	@$(BINDIR)/make_gsub_single_table \
		pkna \
		$+ \
		$(FEATURE_GSUB_FEA) \
		> $@ \
		2> $(addsuffix .log,$(basename $@))

feature_trad.tbl: table.tbl copy_and_rotate_do.tbl
	@echo "making GSUB trad table..."
	@$(BINDIR)/make_gsub_single_table \
		trad \
		$+ \
		$(FEATURE_GSUB_FEA) \
		> $@ \
		2> $(addsuffix .log,$(basename $@))

GSUB06.ttx: GSUB05.ttx
	@echo "adding GSUB expt table..."
	@$(SCRIPTDIR)/add_gsub_single_table.py \
		before fwid \
		expt \
		$< \
		$@ \
		> $(addsuffix .log,$(basename $@)) 2>&1

GSUB07.ttx: feature_expt.tbl GSUB06.ttx
	@echo "adding GSUB expt substitutes..."
	@$(SCRIPTDIR)/add_gsub_single.py \
		expt \
		$+ \
		$@ \
		> $(addsuffix .log,$(basename $@)) 2>&1

GSUB08.ttx: GSUB07.ttx
	@echo "adding GSUB hojo table..."
	@$(SCRIPTDIR)/add_gsub_single_table.py \
		before hwid \
		hojo \
		$< \
		$@ \
		> $(addsuffix .log,$(basename $@)) 2>&1

GSUB09.ttx: feature_hojo.tbl GSUB08.ttx
	@echo "adding GSUB hojo substitutes..."
	@$(SCRIPTDIR)/add_gsub_single.py \
		hojo \
		$+ \
		$@ \
		> $(addsuffix .log,$(basename $@)) 2>&1

GSUB10.ttx: GSUB09.ttx
	@echo "adding GSUB pkna table..."
	@$(SCRIPTDIR)/add_gsub_single_table.py \
		before pwid \
		pkna \
		$< \
		$@ \
		> $(addsuffix .log,$(basename $@)) 2>&1

GSUB11.ttx: feature_pkna.tbl GSUB10.ttx
	@echo "adding GSUB pkna substitutes..."
	@$(SCRIPTDIR)/add_gsub_single.py \
		pkna \
		$+ \
		$@ \
		> $(addsuffix .log,$(basename $@)) 2>&1

GSUB12.ttx: GSUB11.ttx
	@echo "adding GSUB trad table..."
	@$(SCRIPTDIR)/add_gsub_single_table.py \
		before vert \
		trad \
		$< \
		$@ \
		> $(addsuffix .log,$(basename $@)) 2>&1

GSUB13.ttx: feature_trad.tbl GSUB12.ttx
	@echo "adding GSUB trad substitutes..."
	@$(SCRIPTDIR)/add_gsub_single.py \
		trad \
		$+ \
		$@ \
		> $(addsuffix .log,$(basename $@)) 2>&1

GSUB14.ttx: GSUB13.ttx
	@echo "adding GSUB vkna table..."
	@$(SCRIPTDIR)/add_gsub_single_table.py \
		after vert \
		vkna \
		$< \
		$@ \
		> $(addsuffix .log,$(basename $@)) 2>&1

GSUB.ttx: feature_vkna.tbl GSUB14.ttx
	@echo "adding GSUB vkna substitutes..."
	@$(SCRIPTDIR)/add_gsub_single.py \
		vkna \
		$+ \
		$@ \
		> $(addsuffix .log,$(basename $@)) 2>&1
else
GSUB.ttx: GSUB05.ttx
	@echo \
	"skipping language-specific GSUB substitution adding..."
	@ln -s $< $@
endif

### palt to pwid ###

palt_to_pwid_kana01.tbl: table.tbl
	@echo "making kana pwid table..."
	@$(BINDIR)/make_kana_pwid_table \
		$+ \
		$(FEATURE_GSUB_FEA) \
		> $@ \
		2> $(addsuffix .log,$(basename $@))

ifeq ($(FONT_LANG),JP)
palt_to_pwid_kana.tbl: palt_to_pwid_kana01.tbl
	@echo "filtering kana pwid table..."
	@cat $+ | grep -v "^#" > $@
else
palt_to_pwid_kana.tbl:
	@touch $@
endif

palt_to_pwid_copy01.tbl adjust_pwid.tbl: \
		table.tbl $(TTXDIR)/$(SRC_FONTBASE).G_P_O_S_.ttx \
		$(FEATURE_GSUB_FEA) $(TTXDIR)/$(SRC_FONTBASE)._h_m_t_x.ttx
	@echo "calculating palt to pwid..."
	@$(BINDIR)/palt_to_pwid \
		$+ \
		palt_to_pwid_copy01.tbl adjust_pwid.tbl \
		> $(addsuffix .log,$(basename $@)) 2>&1

palt_to_pwid_copy.tbl: palt_to_pwid_copy01.tbl palt_to_pwid_kana.tbl \
		${PALT_TO_PWID_FIXED}
	@echo "merging palt_to_copy table..."
	@cat $+ | sort | uniq > $@

copy_and_rotate_do.tbl: ${COPY_AND_ROTATE_TABLE} palt_to_pwid_copy.tbl \
		copy_vkana.tbl
	@echo "merging copy and rotate table..."
	@cat $+ > $@


### letter face ###

# Calc letter face for shift table
letter_face01.tbl: $(SHIFT_LIST) CFF02.ttx
	@echo "calculating letter face for shift table..."
	@$(SCRIPTDIR)/calc_letter_face.py \
		$+ \
		> $@ 2> $(addsuffix .log,$(basename $@))

# Make shift table
shift.tbl: letter_face01.tbl
	@echo "making shift table..."
	@$(SCRIPTDIR)/make_shift.py \
		$< \
		> $@ 2> $(addsuffix .log,$(basename $@))

# Make adjust table
adjust01.tbl: table.tbl $(TTXDIR)/$(SRC_FONTBASE)._h_m_t_x.ttx \
		hmtx03.ttx
	@echo "making adjust table..."
	@$(SCRIPT_MAKE_ADJUST) \
		$+ \
		> $@ 2> $(addsuffix .log,$(basename $@))

# Add shift table to adjust table
adjust.tbl: adjust01.tbl shift.tbl adjust_pwid.tbl
	@echo "adding shift table to adjust table..."
	@cat $+ > $@

# Make {h|v}mtx fixing table
fix_mtx.tbl: adjust.tbl copy_and_rotate_do.tbl
	@echo "making {h|v}mtx fixing table..."
	@cat $+ > $@

# Calc letter face for fixing {h|v}mtx and GPOS conversion
letter_face.tbl: fix_mtx.tbl CFF.ttx
	@echo \
	"calculating letter face for fixing {h|v}mtx and GPOS conversion..."
	@$(SCRIPTDIR)/calc_letter_face.py \
		$+ \
		> $@ 2> $(addsuffix .log,$(basename $@))


### Other tables ###

$(SRC_FONTBASE)._h_e_a_d.ttx: $(TTXDIR)/$(SRC_FONTBASE)._h_e_a_d.ttx
	ln -s $< $@

$(SRC_FONTBASE)._h_h_e_a.ttx: $(TTXDIR)/$(SRC_FONTBASE)._h_h_e_a.ttx
	ln -s $< $@

$(SRC_FONTBASE)._m_a_x_p.ttx: $(TTXDIR)/$(SRC_FONTBASE)._m_a_x_p.ttx
	ln -s $< $@

$(SRC_FONTBASE).O_S_2f_2.ttx: $(TTXDIR)/$(SRC_FONTBASE).O_S_2f_2.ttx
	ln -s $< $@

$(SRC_FONTBASE)._p_o_s_t.ttx: $(TTXDIR)/$(SRC_FONTBASE)._p_o_s_t.ttx
	ln -s $< $@

$(SRC_FONTBASE).B_A_S_E_.ttx: $(TTXDIR)/$(SRC_FONTBASE).B_A_S_E_.ttx
	ln -s $< $@

$(SRC_FONTBASE)._v_h_e_a.ttx: $(TTXDIR)/$(SRC_FONTBASE)._v_h_e_a.ttx
	ln -s $< $@


### Root table ###

output.ttx: $(TTXDIR)/$(SRC_FONTBASE).ttx
	@echo "converting root ttx file..."
	@sed -f $(BASEDIR)/font_tables.sed $< \
		> $@


### Font file ###

DEPEND_TTXS = glyphorder.ttx name.ttx cmap.ttx CFF.ttx \
	GPOS.ttx GSUB.ttx VORG.ttx hmtx.ttx vmtx.ttx \
	$(SRC_FONTBASE)._h_e_a_d.ttx \
	$(SRC_FONTBASE)._h_h_e_a.ttx \
	$(SRC_FONTBASE)._m_a_x_p.ttx \
	$(SRC_FONTBASE).O_S_2f_2.ttx \
	$(SRC_FONTBASE)._p_o_s_t.ttx \
	$(SRC_FONTBASE).B_A_S_E_.ttx \
	$(SRC_FONTBASE)._v_h_e_a.ttx

ifneq ($(wildcard $(TTXDIR)/$(SRC_FONTBASE).G_D_E_F_.ttx),)
DEPEND_TTXS += GDEF.ttx
endif

output.otf: output.ttx $(DEPEND_TTXS)
	ttx -b --recalc-timestamp output.ttx
