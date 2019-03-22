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
LUALATEX = luatex
XELATEX = xetex


PTEX_SOURCES = $(wildcard *.ptex*.tex)
UPTEX_SOURCES = $(wildcard *.uptex*.tex)
PLATEX_SOURCES = $(wildcard *.platex*.tex)
UPLATEX_SOURCES = $(wildcard *.uplatex*.tex)

LUATEX_SOURCES = $(wildcard *.luatex.tex)
XETEX_SOURCES = $(wildcard *.xetex.tex)
LUALATEX_SOURCES = $(wildcard *.lualatex.tex)
XELATEX_SOURCES = $(wildcard *.xelatex.tex)

P_SOURCES = $(PTEX_SOURCES) $(PLATEX_SOURCES)
UP_SOURCES = $(UPTEX_SOURCES) $(UPLATEX_SOURCES)

SOURCES = \
	$(P_SOURCES) $(UP_SOURCES) \
	$(LUATEX_SOURCES) $(XETEX_SOURCES) \
	$(LUALATEX_SOURCES) $(XELATEX_SOURCES)

PTEX_DVIS = $(PTEX_SOURCES:.tex=.dvi)
UPTEX_DVIS = $(UPTEX_SOURCES:.tex=.dvi)
PLATEX_DVIS = $(PLATEX_SOURCES:.tex=.dvi)
UPLATEX_DVIS = $(UPLATEX_SOURCES:.tex=.dvi)

P_PDFS = $(P_SOURCES:.tex=.pdf)
UP_PDFS = $(UP_SOURCES:.tex=.pdf)

LUATEX_PDFS = $(LUATEX_SOURCES:.tex=.pdf)
XETEX_PDFS = $(XETEX_SOURCES:.tex=.pdf)
LUALATEX_PDFS = $(LUALATEX_SOURCES:.tex=.pdf)
XELATEX_PDFS = $(XELATEX_SOURCES:.tex=.pdf)

PDFS = \
	$(P_PDFS) $(UP_PDFS) \
	$(LUATEX_PDFS) $(XETEX_PDFS) \
	$(LUALATEX_PDFS) $(XELATEX_PDFS)


all_pdfs: $(PDFS)

$(PTEX_DVIS): %.dvi: %.tex
	$(PTEX) $<

$(UPTEX_DVIS): %.dvi: %.tex
	$(UPTEX) $<

$(PLATEX_DVIS): %.dvi: %.tex
	$(PLATEX) $<

$(UPLATEX_DVIS): %.dvi: %.tex
	$(UPLATEX) $<

$(filter %tex.pdf,$(P_PDFS)): %tex.pdf: %tex.dvi
	$(DVIPDFMX) -f map/ptex-haranoaji.map $<

$(filter %tex.pdf,$(UP_PDFS)): %tex.pdf: %tex.dvi
	$(DVIPDFMX) -f map/uptex-haranoaji.map $<

$(filter %tex-04.pdf,$(P_PDFS)): %tex-04.pdf: %tex-04.dvi
	$(DVIPDFMX) -f map/ptex-haranoaji-04.map $<

$(filter %tex-04.pdf,$(UP_PDFS)): %tex-04.pdf: %tex-04.dvi
	$(DVIPDFMX) -f map/uptex-haranoaji-04.map $<

$(filter %tex-otf.pdf,$(P_PDFS)): %tex-otf.pdf: %tex-otf.dvi
	$(DVIPDFMX) -f map/otf-haranoaji.map $<

$(filter %tex-otf.pdf,$(UP_PDFS)): %tex-otf.pdf: %tex-otf.dvi
	$(DVIPDFMX) -f map/otf-up-haranoaji.map $<

$(LUATEX_PDFS): %.pdf: %.tex
	$(LUATEX) $<

$(XETEX_PDFS): %.pdf: %.tex
	$(XETEX) $<

$(LUALATEX_PDFS): %.pdf: %.tex
	$(LUALATEX) $<

$(XELATEX_PDFS): %.pdf: %.tex
	$(XELATEX) $<

clean:
	-$(RM) *~ *.aux *.log
