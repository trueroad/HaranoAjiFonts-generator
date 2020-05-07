all: jp
jp: output_otfs
cn: output_otfs_cn

.PHONY: all jp output_otfs cn output_otfs_cn clean


CMAP = UniJIS2004-UTF32-H
CMAP_CN = UniGB-UTF32-H

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


output_otfs: $(OUTPUT_OTFS)
output_otfs_cn: $(OUTPUT_OTFS_CN)


ttx/%.ttx: download/%.otf
	mkdir -p ttx
	$(MAKE) -C ttx $*.ttx

bin/make_conv_table:
	$(MAKE) -C src
	$(MAKE) -C src install

build/$(ORIGINAL_FAMILY_SANS)JP-%/output.otf: \
		ttx/$(ORIGINAL_FAMILY_SANS)JP-%.ttx bin/make_conv_table
	mkdir -p build/$(ORIGINAL_FAMILY_SANS)JP-$*
	./make_font.sh $(ORIGINAL_FAMILY_SANS)JP-$* $(CMAP)
build/$(ORIGINAL_FAMILY_SERIF)JP-%/output.otf: \
		ttx/$(ORIGINAL_FAMILY_SERIF)JP-%.ttx bin/make_conv_table
	mkdir -p build/$(ORIGINAL_FAMILY_SERIF)JP-$*
	./make_font.sh $(ORIGINAL_FAMILY_SERIF)JP-$* $(CMAP)

build/$(ORIGINAL_FAMILY_SANS)CN-%/output.otf: \
		ttx/$(ORIGINAL_FAMILY_SANS)CN-%.ttx bin/make_conv_table
	mkdir -p build/$(ORIGINAL_FAMILY_SANS)CN-$*
	./make_font_cn.sh $(ORIGINAL_FAMILY_SANS)CN-$* $(CMAP_CN)
build/$(ORIGINAL_FAMILY_SERIF)CN-%/output.otf: \
		ttx/$(ORIGINAL_FAMILY_SERIF)CN-%.ttx bin/make_conv_table
	mkdir -p build/$(ORIGINAL_FAMILY_SERIF)CN-$*
	./make_font_cn.sh $(ORIGINAL_FAMILY_SERIF)CN-$* $(CMAP_CN)


$(OUTPUT_FAMILY_SANS)-%.otf: build/$(ORIGINAL_FAMILY_SANS)JP-%/output.otf
	cp $< $@
$(OUTPUT_FAMILY_SERIF)-%.otf: build/$(ORIGINAL_FAMILY_SERIF)JP-%/output.otf
	cp $< $@

$(OUTPUT_FAMILY_SANS)CN-%.otf: build/$(ORIGINAL_FAMILY_SANS)CN-%/output.otf
	cp $< $@
$(OUTPUT_FAMILY_SERIF)CN-%.otf: build/$(ORIGINAL_FAMILY_SERIF)CN-%/output.otf
	cp $< $@


NODELETE_FILES = ttx/%.ttx \
	build/$(ORIGINAL_FAMILY_SANS)JP-%/output.otf \
	build/$(ORIGINAL_FAMILY_SERIF)JP-%/output.otf \
	build/$(ORIGINAL_FAMILY_SANS)CN-%/output.otf \
	build/$(ORIGINAL_FAMILY_SERIF)CN-%/output.otf

.SECONDARY: $(NODELETE_FILES)
.PRECIOUS: $(NODELETE_FILES)


clean:
	$(RM) *~
	$(MAKE) -C src clean
	$(MAKE) -C ttx clean
