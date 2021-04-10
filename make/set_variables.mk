GET_MAKE_VARIABLE=$(MAKEDIR)/get_make_variable.sh

FONT_TYPE := $(shell $(GET_MAKE_VARIABLE) FONT_TYPE)
FONT_LANG := $(shell $(GET_MAKE_VARIABLE) FONT_LANG)
FONT_WEIGHT := $(shell $(GET_MAKE_VARIABLE) FONT_WEIGHT)

TTXVER := $(shell ttx --version)

BINDIR = $(BASEDIR)/bin
SCRIPTDIR = $(BASEDIR)/script
COMMONDATADIR = $(BASEDIR)/common-data
TTXDIR = $(BASEDIR)/ttx
DOWNLOADDIR = $(BASEDIR)/download

TOOLVER = ttx $(TTXVER)

DEST_NAME = HaranoAji

# JP
ifeq ($(FONT_LANG),JP)
CMAP = UniJIS2004-UTF32-H
ROS_R = Adobe
ROS_O = Japan1
ROS_S = 7
ROS = AJ1
SRC_LANG = JP

# JP Sans
ifeq ($(FONT_TYPE),Sans)
AI0_SOURCEHAN = $(DOWNLOADDIR)/AI0-SourceHanSans
AJ1X_KANJI = $(DOWNLOADDIR)/SourceHanSans/aj16-kanji.txt
PALT_TO_PWID_FIXED = $(COMMONDATADIR)/palt_to_pwid_fixed_sans.tbl
VPAL_TO_PWIDVERT_FIXED = $(COMMONDATADIR)/vpal_to_pwidvert_fixed_sans.tbl
COPY_AND_ROTATE_TABLE = $(COMMONDATADIR)/copy_and_rotate_sans.tbl
SHIFT_LIST = $(COMMONDATADIR)/shift_sans.lst
DEST_FONTBASE = $(DEST_NAME)Gothic-$(FONT_WEIGHT)
endif

# JP Serif
ifeq ($(FONT_TYPE),Serif)
AI0_SOURCEHAN = $(DOWNLOADDIR)/AI0-SourceHanSerif
AJ1X_KANJI = $(DOWNLOADDIR)/SourceHanSerif/aj16-kanji.txt
PALT_TO_PWID_FIXED = $(COMMONDATADIR)/palt_to_pwid_fixed_serif.tbl
VPAL_TO_PWIDVERT_FIXED = $(COMMONDATADIR)/vpal_to_pwidvert_fixed_serif.tbl
COPY_AND_ROTATE_TABLE = $(COMMONDATADIR)/copy_and_rotate_serif.tbl
SHIFT_LIST = $(COMMONDATADIR)/shift_serif.lst
DEST_FONTBASE = $(DEST_NAME)Mincho-$(FONT_WEIGHT)
endif

# JP Common
FEATURE_GSUB_FEA = $(DOWNLOADDIR)/aj17-gsub-jp04.fea
FONT_NAME_SED = $(BASEDIR)/font_name.sed
SCRIPT_MAKE_ADJUST=$(SCRIPTDIR)/make_adjust.py
JISX0208_MAPPING=$(DOWNLOADDIR)/JISX0208-SourceHan-Mapping.txt
endif

# CN
ifeq ($(FONT_LANG),CN)
CMAP = UniGB-UTF32-H
ROS_R = Adobe
ROS_O = GB1
ROS_S = 5
ROS = AG1
SRC_LANG = CN

# CN Sans
ifeq ($(FONT_TYPE),Sans)
PALT_TO_PWID_FIXED=$(COMMONDATADIR)/palt_to_pwid_fixed_sans_CN.tbl
VPAL_TO_PWIDVERT_FIXED=$(COMMONDATADIR)/vpal_to_pwidvert_fixed_sans_CN.tbl
COPY_AND_ROTATE_TABLE = $(COMMONDATADIR)/copy_and_rotate_serif_CN.tbl
SHIFT_LIST = $(COMMONDATADIR)/shift_sans_CN.lst
DEST_FONTBASE = $(DEST_NAME)Gothic$(FONT_LANG)-$(FONT_WEIGHT)
endif

# CN Serif
ifeq ($(FONT_TYPE),Serif)
PALT_TO_PWID_FIXED=$(COMMONDATADIR)/palt_to_pwid_fixed_serif_CN.tbl
VPAL_TO_PWIDVERT_FIXED=$(COMMONDATADIR)/vpal_to_pwidvert_fixed_serif_CN.tbl
COPY_AND_ROTATE_TABLE = $(COMMONDATADIR)/copy_and_rotate_serif_CN.tbl
SHIFT_LIST = $(COMMONDATADIR)/shift_serif_CN.lst
DEST_FONTBASE = $(DEST_NAME)Mincho$(FONT_LANG)-$(FONT_WEIGHT)
endif

# CN Common
FEATURE_GSUB_FEA = $(DOWNLOADDIR)/ag15-gsub.fea
FONT_NAME_SED = $(BASEDIR)/font_name_cn.sed
SCRIPT_MAKE_ADJUST = $(SCRIPTDIR)/make_adjust_center.py
endif

# TW
ifeq ($(FONT_LANG),TW)
CMAP = UniCNS-UTF32-H
ROS_R = Adobe
ROS_O = CNS1
ROS_S = 7
ROS = AC1
SRC_LANG = TW

# TW Sans
ifeq ($(FONT_TYPE),Sans)
PALT_TO_PWID_FIXED=$(COMMONDATADIR)/palt_to_pwid_fixed_sans_TW.tbl
VPAL_TO_PWIDVERT_FIXED=$(COMMONDATADIR)/vpal_to_pwidvert_fixed_sans_TW.tbl
COPY_AND_ROTATE_TABLE = $(COMMONDATADIR)/copy_and_rotate_sans_TW.tbl
SHIFT_LIST = $(COMMONDATADIR)/shift_sans_TW.lst
DEST_FONTBASE = $(DEST_NAME)Gothic$(FONT_LANG)-$(FONT_WEIGHT)
endif

# TW Serif
ifeq ($(FONT_TYPE),Serif)
PALT_TO_PWID_FIXED=$(COMMONDATADIR)/palt_to_pwid_fixed_serif_TW.tbl
VPAL_TO_PWIDVERT_FIXED=$(COMMONDATADIR)/vpal_to_pwidvert_fixed_serif_TW.tbl
COPY_AND_ROTATE_TABLE = $(COMMONDATADIR)/copy_and_rotate_serif_TW.tbl
SHIFT_LIST = $(COMMONDATADIR)/shift_serif_TW.lst
DEST_FONTBASE = $(DEST_NAME)Mincho$(FONT_LANG)-$(FONT_WEIGHT)
endif

# TW Common
FEATURE_GSUB_FEA = $(DOWNLOADDIR)/ac17-gsub.fea
FONT_NAME_SED = $(BASEDIR)/font_name_tw.sed
SCRIPT_MAKE_ADJUST = $(SCRIPTDIR)/make_adjust_center.py
endif

# KR
ifeq ($(FONT_LANG),KR)
CMAP = UniAKR-UTF32-H
ROS_R = Adobe
ROS_O = KR
ROS_S = 9
ROS = AKR
SRC_LANG = KR

# KR Sans
ifeq ($(FONT_TYPE),Sans)
PALT_TO_PWID_FIXED=$(COMMONDATADIR)/palt_to_pwid_fixed_sans_KR.tbl
VPAL_TO_PWIDVERT_FIXED=$(COMMONDATADIR)/vpal_to_pwidvert_fixed_sans_KR.tbl
COPY_AND_ROTATE_TABLE = $(COMMONDATADIR)/copy_and_rotate_sans_KR.tbl
SHIFT_LIST = $(COMMONDATADIR)/shift_sans_KR.lst
DEST_FONTBASE = $(DEST_NAME)Gothic$(FONT_LANG)-$(FONT_WEIGHT)
endif

# KR Serif
ifeq ($(FONT_TYPE),Serif)
PALT_TO_PWID_FIXED=$(COMMONDATADIR)/palt_to_pwid_fixed_serif_KR.tbl
VPAL_TO_PWIDVERT_FIXED=$(COMMONDATADIR)/vpal_to_pwidvert_fixed_serif_KR.tbl
COPY_AND_ROTATE_TABLE = $(COMMONDATADIR)/copy_and_rotate_serif_KR.tbl
SHIFT_LIST = $(COMMONDATADIR)/shift_serif_KR.lst
DEST_FONTBASE = $(DEST_NAME)Mincho$(FONT_LANG)-$(FONT_WEIGHT)
endif

# KR Common
FEATURE_GSUB_FEA = $(DOWNLOADDIR)/akr9-gsub.fea
FONT_NAME_SED = $(BASEDIR)/font_name_kr.sed
SCRIPT_MAKE_ADJUST = $(SCRIPTDIR)/make_adjust_center.py
endif

# K1
ifeq ($(FONT_LANG),K1)
CMAP = UniKS-UTF32-H
ROS_R = Adobe
ROS_O = Korea1
ROS_S = 2
ROS = AK1
SRC_LANG = KR

# K1 Sans
ifeq ($(FONT_TYPE),Sans)
PALT_TO_PWID_FIXED=$(COMMONDATADIR)/palt_to_pwid_fixed_sans_K1.tbl
VPAL_TO_PWIDVERT_FIXED=$(COMMONDATADIR)/vpal_to_pwidvert_fixed_sans_K1.tbl
COPY_AND_ROTATE_TABLE = $(COMMONDATADIR)/copy_and_rotate_sans_K1.tbl
SHIFT_LIST = $(COMMONDATADIR)/shift_sans_K1.lst
DEST_FONTBASE = $(DEST_NAME)Gothic$(FONT_LANG)-$(FONT_WEIGHT)
endif

# K1 Serif
ifeq ($(FONT_TYPE),Serif)
PALT_TO_PWID_FIXED=$(COMMONDATADIR)/palt_to_pwid_fixed_serif_K1.tbl
VPAL_TO_PWIDVERT_FIXED=$(COMMONDATADIR)/vpal_to_pwidvert_fixed_serif_K1.tbl
COPY_AND_ROTATE_TABLE = $(COMMONDATADIR)/copy_and_rotate_serif_K1.tbl
SHIFT_LIST = $(COMMONDATADIR)/shift_serif_K1.lst
DEST_FONTBASE = $(DEST_NAME)Mincho$(FONT_LANG)-$(FONT_WEIGHT)
endif

# K1 Common
FEATURE_GSUB_FEA = $(DOWNLOADDIR)/ak12-gsub.txt
FONT_NAME_SED = $(BASEDIR)/font_name_k1.sed
SCRIPT_MAKE_ADJUST = $(SCRIPTDIR)/make_adjust_center.py
endif

CMAP_FILE = $(DOWNLOADDIR)/$(CMAP)
SRC_FONTBASE = SourceHan$(FONT_TYPE)$(SRC_LANG)-$(FONT_WEIGHT)

.PHONY: debug

debug:
	@echo "FONT_TYPE              $(FONT_TYPE)"
	@echo "FONT_LANG              $(FONT_LANG)"
	@echo "FONT_WEIGHT            $(FONT_WEIGHT)"
	@echo ""
	@echo "TTXVER                 $(TTXVER)"
	@echo "TOOLVER                $(TOOLVER)"
	@echo ""
	@echo "CMAP                   $(CMAP)"
	@echo "ROS_R-ROS_O-ROS_S      $(ROS_R)-$(ROS_O)-$(ROS_S)"
	@echo "ROS                    $(ROS)"
	@echo "SRC_LANG               $(SRC_LANG)"
	@echo ""
	@echo "AI0_SOURCEHAN          $(AI0_SOURCEHAN)"
	@echo "AJ1X_KANJI             $(AJ1X_KANJI)"
	@echo "PALT_TO_PWID_FIXED     $(PALT_TO_PWID_FIXED)"
	@echo "VPAL_TO_PWIDVERT_FIXED $(VPAL_TO_PWIDVERT_FIXED)"
	@echo ""
	@echo "FEATURE_GSUB_FEA       $(FEATURE_GSUB_FEA)"
	@echo "FONT_NAME_SED          $(FONT_NAME_SED)"
	@echo "COPY_AND_ROTATE_TABLE  $(COPY_AND_ROTATE_TABLE)"
	@echo "SHIFT_LIST             $(SHIFT_LIST)"
	@echo "SCRIPT_MAKE_ADJUST     $(SCRIPT_MAKE_ADJUST)"
	@echo "JISX0208_MAPPING       $(JISX0208_MAPPING)"
	@echo ""
	@echo "CMAP_FILE              $(CMAP_FILE)"
	@echo "SRC_FONTBASE           $(SRC_FONTBASE)"
	@echo "DEST_FONTBASE          $(DEST_FONTBASE)"
