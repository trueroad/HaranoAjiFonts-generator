<!-- -*- coding: utf-8 -*- -->
# Harano Aji Fonts generator

[ [Japanese （日本語）](README.md) / English ]

Harano Aji Fonts (Harano Aji Mincho and Harano Aji Gothic)
are fonts obtained by replacing Adobe-Identity-0 (AI0) CIDs
of Source Han fonts (Source Han Serif and Source Han Sans)
with Adobe-Japan1 (AJ1) CIDs.

There are 14 fonts, 7 weights each for Mincho and Gothic.

## Distribution

* Harano Aji Fonts generator
    - [
https://github.com/trueroad/HaranoAjiFonts-generator
](https://github.com/trueroad/HaranoAjiFonts-generator)
* Generated Harano Aji Fonts (Japanese: JP)
    - TeX Live
        - Contained in TeX Live 2020 and later.
          Default font for Japanese except for a few engines.
        - For TeX Live 2019, contained in updates since mid-February 2020.
          (Not the default font.)
    - W32TeX
        - Contained after March 23, 2020.
    - CTAN
        - The major 7 fonts used in the preset settings in some packages.
            - [
https://www.ctan.org/pkg/haranoaji
](https://www.ctan.org/pkg/haranoaji)
        - The remaining 7 fonts.
            - [
https://www.ctan.org/pkg/haranoaji-extra
](https://www.ctan.org/pkg/haranoaji-extra)
    - GitHub
        - [
https://github.com/trueroad/HaranoAjiFonts
](https://github.com/trueroad/HaranoAjiFonts)

The following files are also distributed.

* [
Various TeX files
](https://github.com/trueroad/HaranoAjiFonts-generator/tree/master/tex)
    + Document, samples, test files, etc.
* fontspec file
    + [HaranoAjiMincho.fontspec](./tex/HaranoAjiMincho.fontspec),
      [HaranoAjiGothic.fontspec](./tex/HaranoAjiGothic.fontspec)
    + Not required when using preset settings such as `luatexja-preset`

Map files for pTeX / pLaTeX are contained in
[ptex-fontmaps](https://www.ctan.org/pkg/ptex-fontmaps)
20200217.0 or later.

There are **experimentally** generated Simplified Chinese,
Traditional Chinese, and Korean fonts.

* (Experimental) Simplified Chinese (CN): Adobe-GB1
    + [
https://github.com/trueroad/HaranoAjiFontsCN
](https://github.com/trueroad/HaranoAjiFontsCN)
* (Experimental) Traditional Chinese (TW): Adobe-CNS1
    + [
https://github.com/trueroad/HaranoAjiFontsTW
](https://github.com/trueroad/HaranoAjiFontsTW)
* (Experimental) Korean (KR): Adobe-KR
    + [
https://github.com/trueroad/HaranoAjiFontsKR
](https://github.com/trueroad/HaranoAjiFontsKR)
* (Experimental) Korean (K1): Adobe-Korea1
    + [
https://github.com/trueroad/HaranoAjiFontsK1
](https://github.com/trueroad/HaranoAjiFontsK1)

## Usage

### Required

* ttx
    + [fonttools](https://github.com/fonttools/fonttools)
* C++11 compiler
    + g++ 4.9 and above etc.
* pugixml
    + [https://pugixml.org/](https://pugixml.org/)
* Python3
* GNU Make
* GNU sed
* sh etc.

### Files (JP)

Make `download` directory and put the following files in it.

* Source Han fonts Region-specific Subset OTFs Japanese
    + [Source Han Serif](https://github.com/adobe-fonts/source-han-serif)
        - SourceHanSerifJP-ExtraLight.otf
        - SourceHanSerifJP-Light.otf
        - SourceHanSerifJP-Normal.otf
        - SourceHanSerifJP-Regular.otf
        - SourceHanSerifJP-Medium.otf
        - SourceHanSerifJP-Bold.otf
        - SourceHanSerifJP-Heavy.otf
    + [Source Han Sans](https://github.com/adobe-fonts/source-han-sans)
        - SourceHanSansJP-ExtraLight.otf
        - SourceHanSansJP-Light.otf
        - SourceHanSansJP-Regular.otf
        - SourceHanSansJP-Medium.otf
        - SourceHanSansJP-SemiBold.otf
        - SourceHanSansJP-Bold.otf
        - SourceHanSansJP-Heavy.otf
* Some files of Source Han's Resources
    + [Source Han Serif
](https://github.com/adobe-fonts/source-han-serif/tree/release/Resources)
        - AI0-SourceHanSerif
        - aj16-kanji.txt
            - Only aj16-kanji.txt,
              put it into `download/SourceHanSerif` directory.
    + [Source Han Sans
](https://github.com/adobe-fonts/source-han-sans/tree/release/Resources)
        - AI0-SourceHanSans
        - aj16-kanji.txt
            - Only aj16-kanji.txt,
              put it into `download/SourceHanSans` directory.
* Source Han's JIS X 0208 mapping file
    + [
Adobe-Japan1-6 vs Source Han
](https://ccjktype.fonts.adobe.com/2019/03/aj16-vs-source-han.html)
        - JISX0208-SourceHan-Mapping.txt
* [CMap](https://github.com/adobe-type-tools/cmap-resources)
    + UniJIS2004-UTF32-H
* AJ1-7 GSUB
    + [
The Adobe-Japan1-7 Character Collection
](https://github.com/adobe-type-tools/Adobe-Japan1)
        - aj17-gsub-jp04.fea

Note:
`aj16-kanji.txt` has the same file name in Serif and Sans,
but the contents are different.
Place only this file in a separate directory for Serif and Sans.
Place all other files in the same directory.

### Generate fonts (JP)

`make`

### (Experimental) Other languages

#### (Experimental) File (CN)

* Source Han fonts Region-specific Subset OTFs CN version
    + [Source Han Serif](https://github.com/adobe-fonts/source-han-serif)
        - SourceHanSerifCN-ExtraLight.otf
        - SourceHanSerifCN-Light.otf
        - SourceHanSerifCN-Normal.otf
        - SourceHanSerifCN-Regular.otf
        - SourceHanSerifCN-Medium.otf
        - SourceHanSerifCN-Bold.otf
        - SourceHanSerifCN-Heavy.otf
    + [Source Han Sans](https://github.com/adobe-fonts/source-han-sans)
        - SourceHanSansCN-ExtraLight.otf
        - SourceHanSansCN-Light.otf
        - SourceHanSansCN-Regular.otf
        - SourceHanSansCN-Medium.otf
        - SourceHanSansCN-SemiBold.otf
        - SourceHanSansCN-Bold.otf
        - SourceHanSansCN-Heavy.otf
* [CMap](https://github.com/adobe-type-tools/cmap-resources)
    + UniGB-UTF32-H
* AG1-5 GSUB
    + [
The Adobe-GB1-7 Character Collection
](https://github.com/adobe-type-tools/Adobe-GB1)
        - ag15-gsub.fea

#### (Experimental) Generate fonts (CN)

`make cn`

#### (Experimental) File (TW)

* Source Han fonts Region-specific Subset OTFs TW version
    + [Source Han Serif](https://github.com/adobe-fonts/source-han-serif)
        - SourceHanSerifTW-ExtraLight.otf
        - SourceHanSerifTW-Light.otf
        - SourceHanSerifTW-Normal.otf
        - SourceHanSerifTW-Regular.otf
        - SourceHanSerifTW-Medium.otf
        - SourceHanSerifTW-Bold.otf
        - SourceHanSerifTW-Heavy.otf
    + [Source Han Sans](https://github.com/adobe-fonts/source-han-sans)
        - SourceHanSansTW-ExtraLight.otf
        - SourceHanSansTW-Light.otf
        - SourceHanSansTW-Regular.otf
        - SourceHanSansTW-Medium.otf
        - SourceHanSansTW-SemiBold.otf
        - SourceHanSansTW-Bold.otf
        - SourceHanSansTW-Heavy.otf
* [CMap](https://github.com/adobe-type-tools/cmap-resources)
    + UniCNS-UTF32-H
* AC1-7 GSUB
    + [
The Adobe-CNS1-7 Character Collection
](https://github.com/adobe-type-tools/Adobe-CNS1)
        - ac17-gsub.fea

#### (Experimental) Generate fonts (TW)

`make tw`

#### (Experimental) File (KR)

* Source Han fonts Region-specific Subset OTFs KR version
    + [Source Han Serif](https://github.com/adobe-fonts/source-han-serif)
        - SourceHanSerifKR-ExtraLight.otf
        - SourceHanSerifKR-Light.otf
        - SourceHanSerifKR-Normal.otf
        - SourceHanSerifKR-Regular.otf
        - SourceHanSerifKR-Medium.otf
        - SourceHanSerifKR-Bold.otf
        - SourceHanSerifKR-Heavy.otf
    + [Source Han Sans](https://github.com/adobe-fonts/source-han-sans)
        - SourceHanSansKR-ExtraLight.otf
        - SourceHanSansKR-Light.otf
        - SourceHanSansKR-Regular.otf
        - SourceHanSansKR-Medium.otf
        - SourceHanSansKR-SemiBold.otf
        - SourceHanSansKR-Bold.otf
        - SourceHanSansKR-Heavy.otf
* [CMap](https://github.com/adobe-type-tools/cmap-resources)
    + UniAKR-UTF32-H
* AKR-9 GSUB
    + [
The Adobe-KR-9 Character Collection
](https://github.com/adobe-type-tools/Adobe-KR)
        - akr9-gsub.fea

#### (Experimental) Generate fonts (KR)

`make kr`

#### (Experimental) File (K1)

* Source Han fonts Region-specific Subset OTFs KR version
    + [Source Han Serif](https://github.com/adobe-fonts/source-han-serif)
        - SourceHanSerifKR-ExtraLight.otf
        - SourceHanSerifKR-Light.otf
        - SourceHanSerifKR-Normal.otf
        - SourceHanSerifKR-Regular.otf
        - SourceHanSerifKR-Medium.otf
        - SourceHanSerifKR-Bold.otf
        - SourceHanSerifKR-Heavy.otf
    + [Source Han Sans](https://github.com/adobe-fonts/source-han-sans)
        - SourceHanSansKR-ExtraLight.otf
        - SourceHanSansKR-Light.otf
        - SourceHanSansKR-Regular.otf
        - SourceHanSansKR-Medium.otf
        - SourceHanSansKR-SemiBold.otf
        - SourceHanSansKR-Bold.otf
        - SourceHanSansKR-Heavy.otf
* [CMap](https://github.com/adobe-type-tools/cmap-resources)
    + UniKS-UTF32-H
* AK1-2 GSUB
    + [
AFDKO “features” File Tips & Tricks, Part 2: GSUB Features for Public ROSes
](https://ccjktype.fonts.adobe.com/2012/01/afdko-features-tips-tricks-part-2.html)
        - ak12-gsub.txt (download `gsub-012012.tar` and unpack)

#### (Experimental) Generate fonts (K1)

`make k1`

## Release Notes

* [
20210410
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20210410)
(JP, CN, TW, KR, K1)
    + Based on SourceHanSans 2.003 (JP, CN, TW, KR, K1)
    + Update
        + SourceHanSans 2.003
        + ttx 4.22.0
    + Number of contained glyphs (JP)
        - HaranoAjiMincho: 17554
          (conversion 16862 + glyph processing 691 + .notdef 1)
        - HaranoAjiGothic: 17559
          (conversion 16866 + glyph processing 692 + .notdef 1)
* [
20210130
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20210130)
(JP)
    + Fix GPOS vpal feature for vertical Kana glyphs
    + Fix GSUB vkna feature from [fixing Adobe-Japan1-7
GSUB feature](https://github.com/adobe-type-tools/Adobe-Japan1/pull/4)
    + Update
        + ttx 4.19.1
        + aj17-gsub-jp04.fea (2021-01-25)
    + Number of contained glyphs (JP)
        - HaranoAjiMincho: 17554
          (conversion 16862 + glyph processing 691 + .notdef 1)
        - HaranoAjiGothic: 17559
          (conversion 16867 + glyph processing 691 + .notdef 1)
* [
20210102
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20210102)
(JP)
    + Fix proportional vertical GSUB substitution
    + Fix proportional vertical Kana glyph
    + Number of contained glyphs (JP)
        - HaranoAjiMincho: 17554
          (conversion 16862 + glyph processing 691 + .notdef 1)
        - HaranoAjiGothic: 17559
          (conversion 16867 + glyph processing 691 + .notdef 1)
* [
20210101
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20210101)
(JP, CN, TW, KR, K1)
    + Based on SourceHanSans 2.002 (JP, CN, TW, KR, K1)
    + Add many Kana glyphs (JP)
    + Add many GSUB features and entries (JP)
    + Update
        + SourceHanSans 2.002
        + ttx 4.18.2
    + Number of contained glyphs (JP)
        - HaranoAjiMincho: 17554
          (conversion 16862 + glyph processing 691 + .notdef 1)
        - HaranoAjiGothic: 17559
          (conversion 16867 + glyph processing 691 + .notdef 1)
* [
20200912
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20200912)
(JP)
    + Add glyphs that don't have a single Unicode code point
      and are accessible only by ligature substitute in the `GSUB` table (JP)
    + Update
        + ttx 4.14.0
    + Number of contained glyphs (JP)
        - HaranoAjiMincho: 16904
          (conversion 16693 + glyph processing 210 + .notdef 1)
        - HaranoAjiGothic: 16909
          (conversion 16698 + glyph processing 210 + .notdef 1)
* [
20200612
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20200612)
(JP, CN, TW, KR, K1)
    + Add `cmap` table from CMap such as AJ1
      and change CID in `cmap` table according to CMap (JP, CN, TW, KR, K1)
    + Add AJ1 CID+151 by copying from AJ1 CID+14 (JP)
    + Change size reducing method for size exceeded `cmap` table format 4
      (TW, KR)
    + Add `GPOS` table (KR)
    + Improve generator
    + Update
        + ttx 4.12.0
    + Number of contained glyphs (JP)
        - HaranoAjiMincho: 16888
          (conversion 16678 + glyph processing 209 + .notdef 1)
        - HaranoAjiGothic: 16893
          (conversion 16683 + glyph processing 209 + .notdef 1)
* [
20200524
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20200524)
(JP, CN, TW, KR, K1)
    + Add proportional Kana glyphs (JP)
    + Add some space glyphs (JP, KR)
    + Fix broken `GPOS` table such as palt (JP, CN, TW, KR)
    + Change width of Monospaced glyphs in **experimental** Korean font (KR)
    + Add **experimental** Korean font variation (K1)
        + Korean: Adobe-Korea1, suffix K1
            + UniKS-UTF32-H 1.008
    + Update
        + ttx 4.10.2
    + Number of contained glyphs (JP)
        - HaranoAjiMincho: 16887
          (conversion 16678 + glyph processing 208 + .notdef 1)
        - HaranoAjiGothic: 16892
          (conversion 16683 + glyph processing 208 + .notdef 1)
* [
20200516
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20200516)
(CN, TW, KR)
    + The generator can now generate **experimental**
      Simplified Chinese, Traditional Chinese, and Korean fonts.
    + The font name for each langulage has the two letter suffix
      same as Source Han fonts.
        + Simplified Chinese: Adobe-GB1, suffix CN
            + UniGB-UTF32-H 1.016
        + Traditional Chinese: Adobe-CNS1, suffix TW
            + UniCNS-UTF32-H 1.019
        + Korean: Adobe-KR, suffix KR
            + UniAKR-UTF32-H 1.002
    + No change for Japanese version, no release this time.
    + The suffix is used as an abbreviation for each language font.
        + The Japanese font name has no suffix,
          but the abbreviation is JP.
    + Update
        - ttx 4.10.0
* [
20200418
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20200418)
    + Add 5 glyphs for vertical writing
    + Reduce file size
    + Readjust the drawing position of 2 glyphs
    + Fix LSB/TSB of adjusted glyphs
    + Remove adjusted glyphs from `GPOS` table
    + Update
        - ttx 4.7.0
    + Number of contained glyphs
        - HaranoAjiMincho: 16684
        - HaranoAjiGothic: 16689
* [
20200215
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20200215)
    + For glyphs with overwritten width, position adjustment such as centering
        + Contribution from [@h20y6m](https://github.com/h20y6m)
    + Update
        - ttx 4.3.0, UniJIS2004-UTF32-H 1.021
    + Number of contained glyphs
        - HaranoAjiMincho: 16679
        - HaranoAjiGothic: 16684
* [
20190824
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20190824)
    + Overwrite glyph width with AJ1 definition
    + Use AJ1-7 GSUB
    + Update
        - ttx 4.0.0, ~~UniJIS2004-UTF32-H 1.021~~
    + Number of contained glyphs
        - HaranoAjiMincho: 16678
        - HaranoAjiGothic: 16684
        - Changed counting method
* [
20190501
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20190501)
    + Become full set fonts with dummy glyph
    + Update
        - ttx 3.41.0
    + Number of contained glyphs
        - It shouldn't change, but it's difficult to count
          the number of glyphs due to the effect of dummy glyphs...
* [
20190413
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20190413)
    + Support Adobe-Japan1-7
    + Based on SourceHanSans 2.001
    + Update
        - SourceHanSans 2.001
        - ttx 3.40.0
    + Number of contained glyphs
        - HaranoAjiMincho: 16678
        - HaranoAjiGothic: 16684

* [
20190324
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20190324)
    + Support Variation Selector
    + Support OpenType feature
    + Support JIS X 0208 glyphs
    + Add [map files for pTeX / pLaTeX](./tex/map) and [.tex files](./tex)
    + Update
        - ttx 3.39.0
    + Number of contained glyphs
        - HaranoAjiMincho: 16678
        - HaranoAjiGothic: 16683

* [
20190310
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20190310)
    + Add some glyphs for vertical writing etc.
    + Number of contained glyphs
        - HaranoAjiMincho: 16678
        - HaranoAjiGothic: 16683

* [
20190309
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20190309)
    + Contain all Adobe-Japan1-6 kanji glyphs
    + Add `BASE`, `VORG`, `vhea`, `vmtx` tables
    + Number of contained glyphs
        - HaranoAjiMincho: 16425
        - HaranoAjiGothic: 16429

* [
20190303
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20190303)
    + First release
        - Based on SourceHanSerif 1.001, SourceHanSans 2.000
        - ttx 3.38.0, UniJIS2004-UTF32-H 1.020
    + Number of contained glyphs
        - HaranoAjiMincho: 15213
        - HaranoAjiGothic: 15215

## LICENSE

Copyright (C) 2019-2021 Masamichi Hosoda

The license of the generator is BSD 2-Clause. See [LICENSE](./LICENSE).
The license of the generated fonts is SIL Open Font License 1.1.
