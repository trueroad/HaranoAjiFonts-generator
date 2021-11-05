all: all_pdfs

.PHONY: all all_pdfs clean

PTEX = ptex
UPTEX = uptex
PLATEX = platex
UPLATEX = uplatex

DVIPDFMX = dvipdfmx
#DVIPDFMX = dvipdfmx -z 0 -V 4

LUATEX = luatex
XETEX = xetex
LUALATEX = lualatex
XELATEX = xelatex

LATEXMK = latexmk

LATEXMK_LUALATEX = $(LATEXMK) -lualatex


NOEMBED_DIR = noEmbed

PTEX_SOURCES = $(wildcard *.ptex*.tex)
UPTEX_SOURCES = $(wildcard *.uptex*.tex)
PLATEX_SOURCES = $(wildcard *.platex*.tex)
UPLATEX_SOURCES = $(wildcard *.uplatex*.tex)

LUATEX_SOURCES = $(wildcard *.luatex.tex)
XETEX_SOURCES = $(wildcard *.xetex.tex)
LUALATEX_SOURCES = $(wildcard *.lualatex.tex)
XELATEX_SOURCES = $(wildcard *.xelatex.tex)

LATEXMK_LUALATEX_SOURCES = $(wildcard *.latexmk-lualatex.tex)

P_SOURCES = $(PTEX_SOURCES) $(PLATEX_SOURCES)
UP_SOURCES = $(UPTEX_SOURCES) $(UPLATEX_SOURCES)

SOURCES = \
	$(P_SOURCES) $(UP_SOURCES) \
	$(LUATEX_SOURCES) $(XETEX_SOURCES) \
	$(LUALATEX_SOURCES) $(XELATEX_SOURCES) \
	$(LATEXMK_LUALATEX_SOURCES)

PTEX_DVIS = $(PTEX_SOURCES:.tex=.dvi)
UPTEX_DVIS = $(UPTEX_SOURCES:.tex=.dvi)
PLATEX_DVIS = $(PLATEX_SOURCES:.tex=.dvi)
UPLATEX_DVIS = $(UPLATEX_SOURCES:.tex=.dvi)

P_EMBED_PDFS = $(P_SOURCES:.tex=.pdf)
UP_EMBED_PDFS = $(UP_SOURCES:.tex=.pdf)

P_NOEMBED_PDFS = $(addprefix $(NOEMBED_DIR)/, \
		$(filter-out %tex-nomap.pdf,$(P_EMBED_PDFS)))
UP_NOEMBED_PDFS = $(addprefix $(NOEMBED_DIR)/, \
		$(filter-out %tex-nomap.pdf,$(UP_EMBED_PDFS)))

P_PDFS = $(P_EMBED_PDFS) $(P_NOEMBED_PDFS)
UP_PDFS = $(UP_EMBED_PDFS) $(UP_NOEMBED_PDFS)

LUATEX_PDFS = $(LUATEX_SOURCES:.tex=.pdf)
XETEX_PDFS = $(XETEX_SOURCES:.tex=.pdf)
LUALATEX_PDFS = $(LUALATEX_SOURCES:.tex=.pdf)
XELATEX_PDFS = $(XELATEX_SOURCES:.tex=.pdf)
LATEXMK_LUALATEX_PDFS = $(LATEXMK_LUALATEX_SOURCES:.tex=.pdf)

PDFS = \
	$(P_PDFS) $(UP_PDFS) \
	$(LUATEX_PDFS) $(XETEX_PDFS) \
	$(LUALATEX_PDFS) $(XELATEX_PDFS) \
	$(LATEXMK_LUALATEX_PDFS)


all_pdfs: $(NOEMBED_DIR) $(PDFS)

$(NOEMBED_DIR):
	mkdir $@

$(PTEX_DVIS): %.dvi: %.tex
	$(PTEX) $<

$(UPTEX_DVIS): %.dvi: %.tex
	$(UPTEX) $<

$(PLATEX_DVIS): %.dvi: %.tex
	$(PLATEX) $<

$(UPLATEX_DVIS): %.dvi: %.tex
	$(UPLATEX) $<

$(filter %tex.pdf,$(P_EMBED_PDFS)): %tex.pdf: %tex.dvi
	$(DVIPDFMX) -f map/ptex-haranoaji.map $<

$(filter %tex.pdf,$(UP_EMBED_PDFS)): %tex.pdf: %tex.dvi
	$(DVIPDFMX) -f map/uptex-haranoaji.map $<

$(filter %tex-04.pdf,$(P_EMBED_PDFS)): %tex-04.pdf: %tex-04.dvi
	$(DVIPDFMX) -f map/ptex-haranoaji-04.map $<

$(filter %tex-04.pdf,$(UP_EMBED_PDFS)): %tex-04.pdf: %tex-04.dvi
	$(DVIPDFMX) -f map/uptex-haranoaji-04.map $<

$(filter %tex-otf.pdf,$(P_EMBED_PDFS)): %tex-otf.pdf: %tex-otf.dvi
	$(DVIPDFMX) -f map/otf-haranoaji.map $<

$(filter %tex-otf.pdf,$(UP_EMBED_PDFS)): %tex-otf.pdf: %tex-otf.dvi
	$(DVIPDFMX) -f map/otf-up-haranoaji.map $<

$(filter %tex-nomap.pdf,$(P_EMBED_PDFS)): %tex-nomap.pdf: %tex-nomap.dvi
	$(DVIPDFMX) $<

$(filter %tex-nomap.pdf,$(UP_EMBED_PDFS)): %tex-nomap.pdf: %tex-nomap.dvi
	$(DVIPDFMX) $<

$(filter %tex.pdf,$(P_NOEMBED_PDFS)): \
	$(NOEMBED_DIR)/%tex.pdf: %tex.dvi
	$(DVIPDFMX) -f ptex-noEmbed.map $< -o $@

$(filter %tex.pdf,$(UP_NOEMBED_PDFS)): \
	$(NOEMBED_DIR)/%tex.pdf: %tex.dvi
	$(DVIPDFMX) -f uptex-noEmbed.map $< -o $@

$(filter %tex-04.pdf,$(P_NOEMBED_PDFS)): \
	$(NOEMBED_DIR)/%tex-04.pdf: %tex-04.dvi
	$(DVIPDFMX) -f ptex-noEmbed-04.map $< -o $@

$(filter %tex-04.pdf,$(UP_NOEMBED_PDFS)): \
	$(NOEMBED_DIR)/%tex-04.pdf: %tex-04.dvi
	$(DVIPDFMX) -f uptex-noEmbed-04.map $< -o $@

$(filter %tex-otf.pdf,$(P_NOEMBED_PDFS)): \
	$(NOEMBED_DIR)/%tex-otf.pdf: %tex-otf.dvi
	$(DVIPDFMX) -f otf-noEmbed.map $< -o $@

$(filter %tex-otf.pdf,$(UP_NOEMBED_PDFS)): \
	$(NOEMBED_DIR)/%tex-otf.pdf: %tex-otf.dvi
	$(DVIPDFMX) -f otf-up-noEmbed.map $< -o $@

$(LUATEX_PDFS): %.pdf: %.tex
	$(LUATEX) $<

$(XETEX_PDFS): %.pdf: %.tex
	$(XETEX) $<

$(LUALATEX_PDFS): %.pdf: %.tex
	$(LUALATEX) $<

$(XELATEX_PDFS): %.pdf: %.tex
	$(XELATEX) $<

$(LATEXMK_LUALATEX_PDFS): %.pdf: %.tex
	$(LATEXMK_LUALATEX) $<


test-missing-kanji-cids.platex-otf.dvi: \
	missing-kanji-cids-mincho.txt \
	missing-kanji-cids-gothic.txt

missing-kanji-cids-mincho.txt missing-kanji-cids-gothic.txt:
	../script/make_missing_kanji_cids_tex.sh

clean:
	-$(RM) *~ *.aux *.log *.out *.ltjruby *.fdb_latexmk *.fls \
		missing-kanji-cids-mincho.txt missing-kanji-cids-gothic.txt
