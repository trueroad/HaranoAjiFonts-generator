all: jp
jp: output_otfs
cn: output_otfs_cn
tw: output_otfs_tw

.PHONY: all clean \
	jp output_otfs \
	cn output_otfs_cn \
	tw output_otfs_tw


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


output_otfs: $(OUTPUT_OTFS)
output_otfs_cn: $(OUTPUT_OTFS_CN)
output_otfs_tw: $(OUTPUT_OTFS_TW)


ttx/%.ttx: download/%.otf
	mkdir -p ttx
	$(MAKE) -C ttx $*.ttx

bin/make_conv_table:
	$(MAKE) -C src
	$(MAKE) -C src install

build/%/output.otf: ttx/%.ttx bin/make_conv_table
	mkdir -p build/$*
	./make_font.sh $*


$(OUTPUT_FAMILY_SANS)-%.otf: build/$(ORIGINAL_FAMILY_SANS)JP-%/output.otf
	cp $< $@
$(OUTPUT_FAMILY_SERIF)-%.otf: build/$(ORIGINAL_FAMILY_SERIF)JP-%/output.otf
	cp $< $@

$(OUTPUT_FAMILY_SANS)CN-%.otf: build/$(ORIGINAL_FAMILY_SANS)CN-%/output.otf
	cp $< $@
$(OUTPUT_FAMILY_SERIF)CN-%.otf: build/$(ORIGINAL_FAMILY_SERIF)CN-%/output.otf
	cp $< $@

$(OUTPUT_FAMILY_SANS)TW-%.otf: build/$(ORIGINAL_FAMILY_SANS)TW-%/output.otf
	cp $< $@
$(OUTPUT_FAMILY_SERIF)TW-%.otf: build/$(ORIGINAL_FAMILY_SERIF)TW-%/output.otf
	cp $< $@


NODELETE_FILES = ttx/%.ttx build/%/output.otf

.SECONDARY: $(NODELETE_FILES)
.PRECIOUS: $(NODELETE_FILES)


clean:
	$(RM) *~
	$(MAKE) -C src clean
	$(MAKE) -C ttx clean
