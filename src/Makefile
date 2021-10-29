BIN = make_conv_table make_glyphorder make_kanji_table \
	make_feature_table make_ligature_table \
	merge_table \
	conv_name conv_cmap conv_CFF \
	conv_GDEF conv_GPOS conv_GSUB \
	conv_VORG conv_mtx \
	check_table_CMap \
	fix_hmtx \
	palt_to_pwid \
	vpal_to_pwidvert \
	add_cmap \
	ttx_formatter \
	make_kana_pwid_table \
	make_kana_pwidvert_table \
	make_vkana_table \
	make_hkana_table \
	make_gsub_single_table \
	make_gsub_vert_from_pwidvert \
	modify_table_vkana_gpos \

all: version.hh $(BIN)

#
# Libraries
#

PUGIXML_LIBS = -lpugixml
PUGIXML_CFLAGS =

LDLIBS += $(PUGIXML_LIBS)
CXXFLAGS += $(PUGIXML_CFLAGS)


#
# Objects
#

MAKE_CONV_TABLE_OBJS = make_conv_table_main.o \
	fontcmap_reverse.o prefer_unicode.o cmapfile.o
MAKE_GLYPHORDER_OBJS = make_glyphorder_main.o conv_table.o
MAKE_KANJI_TABLE_OBJS = make_kanji_table_main.o \
	AI0-SourceHan.o aj1x-kanji.o
MAKE_FEATURE_TABLE_OBJS = make_feature_table_main.o \
	 conv_table.o gsub_single.o aj1x-gsub.o
MAKE_LIGATURE_TABLE_OBJS = make_ligature_table_main.o \
	 conv_table.o gsub_ligature.o aj1x-gsub-ligature.o
MERGE_TABLE_OBJS = merge_table_main.o \
	conv_table.o
CONV_NAME_OBJS = conv_name_main.o
CONV_CMAP_OBJS = conv_cmap_main.o walker.o walker_conv.o walker_cmap.o \
	conv_table.o
CONV_CFF_OBJS = conv_CFF_main.o walker.o walker_conv.o walker_CFF.o \
	conv_table.o
CONV_GDEF_OBJS = conv_GDEF_main.o conv_table.o
CONV_GPOS_OBJS = conv_GPOS_main.o conv_table.o
CONV_GSUB_OBJS = conv_GSUB_main.o conv_table.o
CONV_VORG_OBJS = conv_VORG_main.o conv_table.o
CONV_MTX_OBJS = conv_mtx_main.o walker.o walker_conv.o conv_table.o
CHECK_TABLE_CMAP_OBJS = check_table_CMap_main.o conv_table.o cmapfile.o
FIX_HMTX_OBJS = fix_hmtx_main.o conv_table.o
PALT_TO_PWID_OBJS = palt_to_pwid_main.o gpos_single.o \
	conv_table.o  aj1x-gsub.o
VPAL_TO_PWIDVERT_OBJS = vpal_to_pwidvert_main.o gpos_single.o \
	conv_table.o aj1x-gsub.o
ADD_CMAP_OBJS = add_cmap_main.o conv_table.o cmapfile.o
TTX_FORMATTER_OBJS = ttx_formatter_main.o
MAKE_KANA_PWID_TABLE_OBJS = make_kana_pwid_table_main.o \
	conv_table.o aj1x-gsub.o
MAKE_KANA_PWIDVERT_TABLE_OBJS = make_kana_pwidvert_table_main.o \
	conv_table.o aj1x-gsub.o
MAKE_VKANA_TABLE_OBJS = make_vkana_table_main.o \
	conv_table.o aj1x-gsub.o gsub_single.o
MAKE_HKANA_TABLE_OBJS = make_hkana_table_main.o \
	conv_table.o aj1x-gsub.o
MAKE_GSUB_SINGLE_TABLE_OBJS = make_gsub_single_table_main.o \
	conv_table.o copy_and_rotate_table.o aj1x-gsub.o gsub_single.o
MAKE_GSUB_VERT_FROM_PWIDVERT_OBJS = make_gsub_vert_from_pwidvert_main.o \
	copy_and_rotate_table.o aj1x-gsub.o gsub_single.o
MODIFY_TABLE_VKANA_GPOS_OBJS = modify_table_vkana_gpos_main.o \
	conv_table.o aj1x-gsub.o

OBJS = $(MAKE_CONV_TABLE_OBJS) $(MAKE_GLYPHORDER_OBJS) \
	$(MAKE_KANJI_TABLE_OBJS) \
	$(MAKE_FEATURE_TABLE_OBJS) \
	$(MERGE_TABLE_OBJS) $(MAKE_LIGATURE_TABLE_OBJS) \
	$(CONV_NAME_OBJS) $(CONV_CMAP_OBJS) $(CONV_CFF_OBJS) \
	$(CONV_GDEF_OBJS) $(CONV_GPOS_OBJS) $(CONV_GSUB_OBJS) \
	$(CONV_VORG_OBJS) $(CONV_MTX_OBJS) \
	$(CHECK_TABLE_CMAP_OBJS) \
	$(FIX_HMTX_OBJS) \
	$(PALT_TO_PWID_OBJS) \
	$(VPAL_TO_PWIDVERT_OBJS) \
	$(ADD_CMAP_OBJS) \
	$(TTX_FORMATTER_OBJS) \
	$(MAKE_KANA_PWID_TABLE_OBJS) \
	$(MAKE_KANA_PWIDVERT_TABLE_OBJS) \
	$(MAKE_VKANA_TABLE_OBJS) \
	$(MAKE_HKANA_TABLE_OBJS) \
	$(MAKE_GSUB_SINGLE_TABLE_OBJS) \
	$(MAKE_GSUB_VERT_FROM_PWIDVERT_OBJS) \
	$(MODIFY_TABLE_VKANA_GPOS_OBJS)


#
# Programs and other settings
#

INSTALL = install
INSTALL_DIR = $(INSTALL) -m 755 -d
INSTALL_FILE = $(INSTALL) -m 644
INSTALL_EXE = $(INSTALL) -m 755

CXXFLAGS_STD = -std=c++11

CXXFLAGS += $(CXXFLAGS_STD)


#
# Dependencies
#

DEPS = $(OBJS:.o=.d)
CPPFLAGS += -MMD -MP -MF $(@:.o=.d) -MT $@
-include $(DEPS)


#
# Rules
#

.PHONY: all install clean

clean:
	$(RM) *~ $(OBJS) $(DEPS) version.hh

make_conv_table: $(MAKE_CONV_TABLE_OBJS)
	$(LINK.cc) $^ $(LOADLIBES) $(LDLIBS) -o $@

make_glyphorder: $(MAKE_GLYPHORDER_OBJS)
	$(LINK.cc) $^ $(LOADLIBES) $(LDLIBS) -o $@

make_kanji_table: $(MAKE_KANJI_TABLE_OBJS)
	$(LINK.cc) $^ $(LOADLIBES) $(LDLIBS) -o $@

make_feature_table: $(MAKE_FEATURE_TABLE_OBJS)
	$(LINK.cc) $^ $(LOADLIBES) $(LDLIBS) -o $@

make_ligature_table: $(MAKE_LIGATURE_TABLE_OBJS)
	$(LINK.cc) $^ $(LOADLIBES) $(LDLIBS) -o $@

merge_table: $(MERGE_TABLE_OBJS)
	$(LINK.cc) $^ $(LOADLIBES) $(LDLIBS) -o $@

conv_name: $(CONV_NAME_OBJS)
	$(LINK.cc) $^ $(LOADLIBES) $(LDLIBS) -o $@

conv_cmap: $(CONV_CMAP_OBJS)
	$(LINK.cc) $^ $(LOADLIBES) $(LDLIBS) -o $@

conv_CFF: $(CONV_CFF_OBJS)
	$(LINK.cc) $^ $(LOADLIBES) $(LDLIBS) -o $@

conv_GDEF: $(CONV_GDEF_OBJS)
	$(LINK.cc) $^ $(LOADLIBES) $(LDLIBS) -o $@

conv_GPOS: $(CONV_GPOS_OBJS)
	$(LINK.cc) $^ $(LOADLIBES) $(LDLIBS) -o $@

conv_GSUB: $(CONV_GSUB_OBJS)
	$(LINK.cc) $^ $(LOADLIBES) $(LDLIBS) -o $@

conv_VORG: $(CONV_VORG_OBJS)
	$(LINK.cc) $^ $(LOADLIBES) $(LDLIBS) -o $@

conv_mtx: $(CONV_MTX_OBJS)
	$(LINK.cc) $^ $(LOADLIBES) $(LDLIBS) -o $@

check_table_CMap: $(CHECK_TABLE_CMAP_OBJS)
	$(LINK.cc) $^ $(LOADLIBES) $(LDLIBS) -o $@

fix_hmtx: $(FIX_HMTX_OBJS)
	$(LINK.cc) $^ $(LOADLIBES) $(LDLIBS) -o $@

palt_to_pwid: $(PALT_TO_PWID_OBJS)
	$(LINK.cc) $^ $(LOADLIBES) $(LDLIBS) -o $@

vpal_to_pwidvert: $(VPAL_TO_PWIDVERT_OBJS)
	$(LINK.cc) $^ $(LOADLIBES) $(LDLIBS) -o $@

add_cmap: $(ADD_CMAP_OBJS)
	$(LINK.cc) $^ $(LOADLIBES) $(LDLIBS) -o $@

ttx_formatter: $(TTX_FORMATTER_OBJS)
	$(LINK.cc) $^ $(LOADLIBES) $(LDLIBS) -o $@

make_kana_pwid_table: $(MAKE_KANA_PWID_TABLE_OBJS)
	$(LINK.cc) $^ $(LOADLIBES) $(LDLIBS) -o $@

make_kana_pwidvert_table: $(MAKE_KANA_PWIDVERT_TABLE_OBJS)
	$(LINK.cc) $^ $(LOADLIBES) $(LDLIBS) -o $@

make_vkana_table: $(MAKE_VKANA_TABLE_OBJS)
	$(LINK.cc) $^ $(LOADLIBES) $(LDLIBS) -o $@

make_hkana_table: $(MAKE_HKANA_TABLE_OBJS)
	$(LINK.cc) $^ $(LOADLIBES) $(LDLIBS) -o $@

make_gsub_single_table: $(MAKE_GSUB_SINGLE_TABLE_OBJS)
	$(LINK.cc) $^ $(LOADLIBES) $(LDLIBS) -o $@

make_gsub_vert_from_pwidvert: $(MAKE_GSUB_VERT_FROM_PWIDVERT_OBJS)
	$(LINK.cc) $^ $(LOADLIBES) $(LDLIBS) -o $@

modify_table_vkana_gpos: $(MODIFY_TABLE_VKANA_GPOS_OBJS)
	$(LINK.cc) $^ $(LOADLIBES) $(LDLIBS) -o $@

VERSION := $(shell cat ../version.txt)

version.hh: version.hh.in ../version.txt
	sed -e 's/@VERSION@/$(VERSION)/g' $< > $@

install: all
	$(INSTALL_DIR) ../bin
	$(INSTALL_EXE) $(BIN) ../bin


#
# Implicit variables (from `make -p`)
#

#CXX = g++
#RM = rm -f
#COMPILE.cc = $(CXX) $(CXXFLAGS) $(CPPFLAGS) $(TARGET_ARCH) -c
#LINK.cc = $(CXX) $(CXXFLAGS) $(CPPFLAGS) $(LDFLAGS) $(TARGET_ARCH)
#OUTPUT_OPTION = -o $@


#
# Implicit rules (from `make -p`)
#

#%.o: %.cc
#	$(COMPILE.cc) $(OUTPUT_OPTION) $<
