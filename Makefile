all: jp
jp: output_otfs
cn: output_otfs_cn
tw: output_otfs_tw
kr: output_otfs_kr
k1: output_otfs_k1

.PHONY: all clean \
	jp output_otfs \
	cn output_otfs_cn \
	tw output_otfs_tw \
	kr output_otfs_kr \
	k1 output_otfs_k1


ORIGINAL_FAMILY_SANS = SourceHanSans
ORIGINAL_FAMILY_SERIF = SourceHanSerif
OUTPUT_FAMILY_SANS = HaranoAjiGothic
OUTPUT_FAMILY_SERIF = HaranoAjiMincho

WEIGHT_SANS = ExtraLight Light Normal Regular Medium Bold Heavy
WEIGHT_SERIF = ExtraLight Light Regular Medium SemiBold Bold Heavy
#WEIGHT_SANS = Regular
#WEIGHT_SERIF  = Medium

OUTPUT_FONTS = $(addprefix $(OUTPUT_FAMILY_SANS)-,$(WEIGHT_SANS)) \
	$(addprefix $(OUTPUT_FAMILY_SERIF)-,$(WEIGHT_SERIF))
OUTPUT_OTFS = $(addsuffix .otf,$(OUTPUT_FONTS))

OUTPUT_FONTS_CN = $(addprefix $(OUTPUT_FAMILY_SANS)CN-,$(WEIGHT_SANS)) \
	$(addprefix $(OUTPUT_FAMILY_SERIF)CN-,$(WEIGHT_SERIF))
OUTPUT_OTFS_CN = $(addsuffix .otf,$(OUTPUT_FONTS_CN))

OUTPUT_FONTS_TW = $(addprefix $(OUTPUT_FAMILY_SANS)TW-,$(WEIGHT_SANS)) \
	$(addprefix $(OUTPUT_FAMILY_SERIF)TW-,$(WEIGHT_SERIF))
OUTPUT_OTFS_TW = $(addsuffix .otf,$(OUTPUT_FONTS_TW))

OUTPUT_FONTS_KR = $(addprefix $(OUTPUT_FAMILY_SANS)KR-,$(WEIGHT_SANS)) \
	$(addprefix $(OUTPUT_FAMILY_SERIF)KR-,$(WEIGHT_SERIF))
OUTPUT_OTFS_KR = $(addsuffix .otf,$(OUTPUT_FONTS_KR))

OUTPUT_FONTS_K1 = $(addprefix $(OUTPUT_FAMILY_SANS)K1-,$(WEIGHT_SANS)) \
	$(addprefix $(OUTPUT_FAMILY_SERIF)K1-,$(WEIGHT_SERIF))
OUTPUT_OTFS_K1 = $(addsuffix .otf,$(OUTPUT_FONTS_K1))


output_otfs: $(OUTPUT_OTFS)
output_otfs_cn: $(OUTPUT_OTFS_CN)
output_otfs_tw: $(OUTPUT_OTFS_TW)
output_otfs_kr: $(OUTPUT_OTFS_KR)
output_otfs_k1: $(OUTPUT_OTFS_K1)


ttx/%.ttx: download/%.otf
	mkdir -p ttx
	$(MAKE) -C ttx $*.ttx

bin/make_conv_table:
	$(MAKE) -C src
	$(MAKE) -C src install

build/$(OUTPUT_FAMILY_SANS)-%/output.otf: \
		ttx/$(ORIGINAL_FAMILY_SANS)JP-%.ttx bin/make_conv_table
	mkdir -p $(dir $@)
	-ln -s ../../make/Makefile.in $(dir $@)Makefile
	$(MAKE) -C $(dir $@)

build/$(OUTPUT_FAMILY_SERIF)-%/output.otf: \
		ttx/$(ORIGINAL_FAMILY_SERIF)JP-%.ttx bin/make_conv_table
	mkdir -p $(dir $@)
	-ln -s ../../make/Makefile.in $(dir $@)Makefile
	$(MAKE) -C $(dir $@)

build/$(OUTPUT_FAMILY_SANS)CN-%/output.otf: \
		ttx/$(ORIGINAL_FAMILY_SANS)CN-%.ttx bin/make_conv_table
	mkdir -p $(dir $@)
	-ln -s ../../make/Makefile.in $(dir $@)Makefile
	$(MAKE) -C $(dir $@)

build/$(OUTPUT_FAMILY_SERIF)CN-%/output.otf: \
		ttx/$(ORIGINAL_FAMILY_SERIF)CN-%.ttx bin/make_conv_table
	mkdir -p $(dir $@)
	-ln -s ../../make/Makefile.in $(dir $@)Makefile
	$(MAKE) -C $(dir $@)

build/$(OUTPUT_FAMILY_SANS)TW-%/output.otf: \
		ttx/$(ORIGINAL_FAMILY_SANS)TW-%.ttx bin/make_conv_table
	mkdir -p $(dir $@)
	-ln -s ../../make/Makefile.in $(dir $@)Makefile
	$(MAKE) -C $(dir $@)

build/$(OUTPUT_FAMILY_SERIF)TW-%/output.otf: \
		ttx/$(ORIGINAL_FAMILY_SERIF)TW-%.ttx bin/make_conv_table
	mkdir -p $(dir $@)
	-ln -s ../../make/Makefile.in $(dir $@)Makefile
	$(MAKE) -C $(dir $@)

build/$(OUTPUT_FAMILY_SANS)KR-%/output.otf: \
		ttx/$(ORIGINAL_FAMILY_SANS)KR-%.ttx bin/make_conv_table
	mkdir -p $(dir $@)
	-ln -s ../../make/Makefile.in $(dir $@)Makefile
	$(MAKE) -C $(dir $@)

build/$(OUTPUT_FAMILY_SERIF)KR-%/output.otf: \
		ttx/$(ORIGINAL_FAMILY_SERIF)KR-%.ttx bin/make_conv_table
	mkdir -p $(dir $@)
	-ln -s ../../make/Makefile.in $(dir $@)Makefile
	$(MAKE) -C $(dir $@)

build/$(OUTPUT_FAMILY_SANS)K1-%/output.otf: \
		ttx/$(ORIGINAL_FAMILY_SANS)KR-%.ttx bin/make_conv_table
	mkdir -p $(dir $@)
	-ln -s ../../make/Makefile.in $(dir $@)Makefile
	$(MAKE) -C $(dir $@)

build/$(OUTPUT_FAMILY_SERIF)K1-%/output.otf: \
		ttx/$(ORIGINAL_FAMILY_SERIF)KR-%.ttx bin/make_conv_table
	mkdir -p $(dir $@)
	-ln -s ../../make/Makefile.in $(dir $@)Makefile
	$(MAKE) -C $(dir $@)

%.otf: build/%/output.otf
	$(MAKE) -C $(dir $<) install


NODELETE_FILES = ttx/%.ttx build/%/output.otf %.otf \
		build/$(OUTPUT_FAMILY_SANS)-%/output.otf \
		build/$(OUTPUT_FAMILY_SERIF)-%/output.otf \
		build/$(OUTPUT_FAMILY_SANS)CN-%/output.otf \
		build/$(OUTPUT_FAMILY_SERIF)CN-%/output.otf \
		build/$(OUTPUT_FAMILY_SANS)TW-%/output.otf \
		build/$(OUTPUT_FAMILY_SERIF)TW-%/output.otf \
		build/$(OUTPUT_FAMILY_SANS)KR-%/output.otf \
		build/$(OUTPUT_FAMILY_SERIF)KR-%/output.otf \
		build/$(OUTPUT_FAMILY_SANS)K1-%/output.otf \
		build/$(OUTPUT_FAMILY_SERIF)K1-%/output.otf

.SECONDARY: $(NODELETE_FILES)
.PRECIOUS: $(NODELETE_FILES)


clean:
	$(RM) *~
	$(MAKE) -C src clean
	$(MAKE) -C ttx clean
