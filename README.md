<!-- -*- coding: utf-8 -*- -->
# 原ノ味フォント生成プログラム / Harano Aji Fonts generator

源ノ明朝・源ノ角ゴシック（以下、源ノフォント）を
Adobe-Japan1 （以下、AJ1）フォントになるように組み替えた
「原ノ味フォント（原ノ味明朝、原ノ味角ゴシック）」
生成プログラムです。
CID の対応がとれないため抜けてしまうグリフがある、
いくつかの OpenType テーブルを落としている、
などがあるため実験的なフォントにとどまっています。

* 原ノ味フォント生成プログラム
    - [
https://github.com/trueroad/HaranoAjiFonts-generator
](https://github.com/trueroad/HaranoAjiFonts-generator)
* 生成した原ノ味フォント
    - [
https://github.com/trueroad/HaranoAjiFonts
](https://github.com/trueroad/HaranoAjiFonts)

「原ノ味」というのは、
源ノフォントからグリフやテーブルが抜けていることを表すために
「氵（さんずい）」を取り、
AJ1 をもじって AJI にして
音から「味」という字をあてたものです。

## Adobe-Japan1 (AJ1) v.s. Adobe-Identity0 (AI0)

源ノフォントは Adobe-Identity0 （以下、AI0）の
Pan-CJK フォントで日本語以外にも対応しています。
一方で AJ1 だと日本語専用になってしまいますが、

* pTeX / pLaTeX で比較的簡単に使うことができる
* PDF に埋め込む際に ToUnicode CMap が必要ない
    - AI0 だと ToUnicode CMap を用意して PDF に埋め込んでおかないと
      PDF からテキスト抽出できない
        + AI0 フォントの cmap テーブルから ToUnicode CMap を生成するには
          逆変換が必要
        + 逆変換すると重複が問題になりテキスト抽出で意図しない文字に化ける
          ことがある
    - AJ1 だと PDF ビュアーがあらかじめ持っている CMap を使うことで
      PDF からテキスト抽出できる
        + 逆変換の問題が発生しないように調整されたものなので
          意図しない文字化けが発生しにくい

といったメリット？があります。

## 生成プログラムの使い方

まず、源ノフォントの OTF ファイルを ttx で xml にし、
C++ で xml や CMap から CID の対照表を作り、 C++ や sed で変換、
最後に再び ttx で OTF ファイルを生成する、という方法を採っています。

### 環境

* ttx
    + [fonttools](https://github.com/fonttools/fonttools)
* C++11 対応コンパイラ
    + g++ 4.9 以降など
* pugixml
    + [https://pugixml.org/](https://pugixml.org/)
* GNU Make
* sed
* その他 sh など

### ファイル

`download` ディレクトリを掘り、以下のファイルを置いてください。

* 源ノフォント Region-specific Subset OTFs 日本語版
    + [源ノ明朝](https://github.com/adobe-fonts/source-han-serif)
        - SourceHanSerifJP-ExtraLight.otf
        - SourceHanSerifJP-Light.otf
        - SourceHanSerifJP-Normal.otf
        - SourceHanSerifJP-Regular.otf
        - SourceHanSerifJP-Medium.otf
        - SourceHanSerifJP-Bold.otf
        - SourceHanSerifJP-Heavy.otf
    + [源ノ角ゴシック](https://github.com/adobe-fonts/source-han-sans)
        - SourceHanSansJP-ExtraLight.otf
        - SourceHanSansJP-Light.otf
        - SourceHanSansJP-Regular.otf
        - SourceHanSansJP-Medium.otf
        - SourceHanSansJP-SemiBold.otf
        - SourceHanSansJP-Bold.otf
        - SourceHanSansJP-Heavy.otf
* [CMap](https://github.com/adobe-type-tools/cmap-resources)
    + UniJIS2004-UTF32-H

### 生成

`make` で生成できます。

## 詳細

### CID の対応

源ノフォントは Adobe-Identity0 (AI0) のフォントであり、
CID の並び方が Adobe-Japan1 (AJ1) とは異なります。
そのため AJ1 化するためには AI0 CID → AJ1 CID 対照表が必要となります。
源ノフォントは日本語用 (Region-specific Subset OTF) であっても、
2 万近い数のグリフがあるため、人手で対照表を作っていたら大変です。
そこで、自動的に対照表を作るようにしています。

#### Unicode を介した変換

源ノフォントをはじめとする OpenType フォントには
cmap テーブルというものが入っていて、
Unicode から CID へ変換ができるようになっています。
源ノフォントは AI0 フォントなので、
Unicode → AI0 CID
の変換となっています。
一方 Adobe は CMap file を配布していて、
このうち `UniJIS2004-UTF32-H` というファイルは、
Unicode → AJ1 CID
の変換表になっています。

本プログラムでは、
源ノフォントの cmap テーブルから逆変換して、
AI0 CID → Unicode
とし、さらに CMap file による変換を重ねて、
AI0 CID → Unicode → AJ1 CID
という変換にすることで、
AI0 CID → AJ1 CID
の対照表を作っています。
本プログラムで参照している cmap テーブルは
format 12 で Unicode 全域を含んでいるもの、
CMap も UTF-32 用のものを使用しているため、
BMP 外のグリフも紐づけることができています。

cmap テーブルは、本来
Unicode → AI0 CID
の変換テーブルであるため、複数の Unicode が
同一の CID にマップされているものがあります。
ここから逆変換すると、一つの AI0 CID から
複数の Unicode に変換できることになってしまいますが、
逆変換表を作るにあたっては一つに絞る必要があります。
本プログラムでは基本的に Unicode のコードポイントが小さい方を優先として、
dvipdfmx の ToUnicode CMap 生成を参考に、
部首などのブロックの優先度を下げるようにしています。
この方法にはブロックごとの優先度を調整するなど改良の余地があるかもしれません。

CMap file は逆変換不要ですが、
やはり複数の Unicode が同一の CID にマップされているものがあります。
この際、別々の AI0 CID が別々の Unicode にマップされていても、
CMap file によって
最終的に同じ AJ1 CID になってしまうケースが発生します。
その場合には、小さい方の AI0 CID を選択しています。
この方法も、CID が小さい方ではなくて、
Unicode のコードポイントを使い
cmap テーブルの逆変換と同様の方法で優先する方を決めるなど
改良の余地があるかもしれません。
なお、源ノフォントは JIS2004 字形のフォントということなので、
CMap file には JIS2004 用のものを使用しています。

cmap テーブルの format 12 には
横書き用のグリフしか登録されていませんし、
`UniJIS2004-UTF32-H` も横書き用ですので、
縦書きのグリフは対応が取れずに失われます。
また、cmap format 12 には異字体セレクタの情報がありませんから、
異字体セレクタを要するグリフも対応が取れずに失われます。

#### その他の変換方法

今後、いくつかの方法で対照表を充実させることを検討したいと思います。

##### 縦書き

源ノフォントに含まれる `GSUB` テーブルから、
縦書き用の OpenType feature である `vert` の部分を読み込むことで、
源ノフォントの横書き用・縦書き用 AI0 CID の対照表が得られます。つまり、
Unicode →横書き用 AI0 CID →縦書き用 AI0 CID
という変換ができるようになります。
これを逆変換にすれば、
縦書き用 AI0 CID → Unicode
ができるようになるはずです。
ここに、縦書き用の CMap file `UniJIS2004-UTF32-V` にある
Unicode →縦書き用 AJ1 CID
を重ねることで、
縦書き用 AI0 CID → Unicode →縦書き用 AJ1 CID
ということができるようになります。これらにより、
縦書き用 AI0 CID →縦書き用 AJ1 CID
の対照表を作ることができ、
縦書きグリフに対応できるようになるのではないかと考えています。

##### 漢字

ここまでの方法は源ノフォントに限らず、
AI0 の OpenType フォントであればどのフォントでも使うことができる方法です。
しかし、ここまでの方法では異字体に対応することができません。
フォントの cmap format 14 を読み込むことで、
異字体セレクタを使った Unicode → AI0 CID
の変換表を得ることはできるのですが、
異字体セレクタを使った CMap が無いので、
異字体セレクタを使った Unicode → AJ1 CID
の変換ができません。

でも、源ノフォントには `aj16-kanji.txt` という、
AJ1 CID と源ノフォントのグリフ名の対応表が配布されています。
さらに `AI0-SourceHanSans` という、
AI0 CID と源ノフォントのグリフ名の対応表も配布されています。
これらをつなげれば
AI0 CID → AJ1 CID
の対照表が作れるはず、というわけです。
ただし、残念ながら漢字しか含まれていません。
非漢字、すなわち、ひらがな・カタカナ・英数字・記号類などについては、
この方法では対照表が得られないということです。
漢字だけと言わずに非漢字の対応表も作ってくれていれば簡単だったのですが。。。
とはいえ、グリフ数の大部分は漢字ですから、
この方法でかなりカバーできるのではないかと思っています。

### OpenType テーブル

現状ではフォントとして体裁が整う最低限のテーブルしか変換していません。

#### `head`, `hhea`, `maxp`, `OS/2`, `post`

何も変換せずにそのまま流用しています。

#### `name`

名称などを変更しています。

#### `cmap`

CID をすべて AI0 CID から AJ1 CID に変換しています。
対照表が作れずに対応が不明な AI0 CID は削除しています。
そして、異字体セレクタを要するグリフも失われているため
format 14を削除しています。
全漢字グリフの対照表ができたら format 14 の変換も考えたいと思います。
また、 ttx の出力で中身が無かった format 6 も削除しています。
これは本当に中身が無いのか ttx が format 6 のパースに対応していないのか、
どちらなのかはわかりません。

#### `CFF`

CID をすべて AI0 CID から AJ1 CID に変換しています。
対照表が作れずに対応が不明な AI0 CID は削除しています。
フォントやサブフォントの名称も変更しています。

#### `hmtx`

CID をすべて AI0 CID から AJ1 CID に変換しています。
対照表が作れずに対応が不明な AI0 CID は削除しています。

#### `BASE`, `vhea`

必須テーブルではないため削除しています。
とはいえ特に変換が必要な内容ではなさそうなので、
いずれそのまま流用するようにしたいと思っています。

#### `vmtx`

必須テーブルではないため削除しています。
既に変換している `hmtx` と同じような変換で済みそうなので、
いずれ変換して含めるようにしたいと思っています。

#### `VORG`

必須テーブルではないため削除しています。
変換するならば CID の置き換えが必要で、
`VORG` 専用の変換が必要そうに見えるため、ひと手間かかりそうですが、
いずれ変換して含めるようにしたいと思っています。

#### `GDEF`, `GPOS`, `GSUB`

必須テーブルではないため削除しています。
変換するならば CID の置き換えが必要で、
それなりに複雑な変換を考慮する必要がありそうに見えます。。。
縦書きグリフの対照表ができたら、
OpenType feature の縦書き `vert`, `vrt2` の対応を考えた方がよいでしょうし、
全漢字グリフの対照表ができたら `jp78`, `jp83`, `jp90` の
対応を考えた方がいいんだろう、、、と思っていますので、
そうすると変換が必要となります。
その他の OpenType feature は AJ1 側の CID がわかりませんので、
対応はかなり困難だと思っています。
また、「びゃん」や「たいと」などは AJ1 には無いでしょうから、
対応のしようが無いと思います。

#### `DSIG`

必須テーブルではないため削除しています。
このテーブルを変換する必要はないと思っています。

## 履歴

* [
20190303
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20190303)
    + 初版
        - 源ノ明朝 1.001、源ノ角ゴシック 2.000
        - ttx 3.38.0, UniJIS2004-UTF32-H 1.020

## ライセンス

Copyright (C) 2019 Masamichi Hosoda

生成プログラムのライセンスは BSD 2-Clause です。
生成したフォントは源ノフォントの派生フォントになるため
SIL Open Font License 1.1 です。
