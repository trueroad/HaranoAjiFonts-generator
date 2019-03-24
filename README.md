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
    - pTeX / pLaTeX で源ノフォント（AI0 フォント）を使うのは少々難しいです
    - 原ノ味フォントでは
        + OTF パッケージを使わない場合
            + 縦書きグリフも含め pTeX / pLaTeX で使えるすべての
              和文グリフに対応しているつもりです
        + OTF パッケージを使う場合
            + Adobe-Japan1-6 漢字グリフを CID 直接指定で
              呼び出すことができます
            + 非漢字（ひらがな、カタカナ、英数字、記号類など）には
              抜けているグリフもあります
    - [マップファイルを配布しています](./tex/map)
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
            + dvipdfmx / xdvipdfmx は AJ1 なら ToUnicode CMap を生成せず
              埋め込みもしないため文字化けが発生しにくくなります
            + ただし LuaTeX は AJ1 でも逆変換で ToUnicode CMap を
              生成して埋め込むため一部で文字化けが発生することがあるようです

といったメリット？があります。

## 生成プログラムの使い方

まず、源ノフォントの OTF ファイルを ttx で xml にし、
C++ で xml や CMap などから CID の対照表を作り、 C++ や sed で変換、
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
* 源ノフォント Resources の一部ファイル
    + [源ノ明朝
](https://github.com/adobe-fonts/source-han-serif/tree/release/Resources)
        - AI0-SourceHanSerif
        - aj16-kanji.txt
            - aj16-kanji.txt のみ
              `download/SourceHanSerif` ディレクトリに格納してください。
    + [源ノ角ゴシック
](https://github.com/adobe-fonts/source-han-sans/tree/release/Resources)
        - AI0-SourceHanSans
        - aj16-kanji.txt
            - aj16-kanji.txt のみ
              `download/SourceHanSans` ディレクトリに格納してください。
* 源ノフォントの JIS X 0208 mapping ファイル
    + [
Adobe-Japan1-6 vs Source Han
](https://blogs.adobe.com/CCJKType/2019/03/aj16-vs-source-han.html)
      から `JISX0208-SourceHan-Mapping.txt`
      （本文中最初のパラグライフの最初の文中 maping file と
      と書いてあるところにリンクがあります）
* [CMap](https://github.com/adobe-type-tools/cmap-resources)
    + UniJIS2004-UTF32-H
* AJ1-6 の GSUB 情報
    + [
AFDKO “features” File Tips & Tricks, Part 2: GSUB Features for Public ROSes
](http://blogs.adobe.com/CCJKType/2012/01/afdko-features-tips-tricks-part-2.html)
      から `gsub-012012.tar` をダウンロードし
      （本文中第 2 パラグラフの下から 2 番目の文中
      here と書いてあるところにリンクがあります）解凍すると得られる
      `aj16-gsub-jp04.txt`

注意：
`aj16-kanji.txt` は明朝とゴシックでファイル名が同じですが中身は異なります。
このファイルだけ明朝・ゴシック別のディレクトリに配置してください。
その他のファイルはすべて同じディレクトリに配置してください。

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
その場合には、それぞれの AI0 CID に対応した
Unicode のコードポイントを使い
cmap テーブルの逆変換と同様の方法で優先する方を決めています。
なお、源ノフォントは JIS2004 字形のフォントということなので、
CMap file には JIS2004 用のものを使用しています。

cmap テーブルの format 12 には
横書き用のグリフしか登録されていませんし、
`UniJIS2004-UTF32-H` も横書き用ですので、
縦書きのグリフは対応が取れずに失われます。
また、cmap format 12 には異字体セレクタの情報がありませんから、
異字体セレクタを要するグリフも対応が取れずに失われます。

#### 漢字

cmap テーブルと CMap file による方法は源ノフォントに限らず、
AI0 の OpenType フォントであればどのフォントでも使うことができる方法です。
しかし、この方法では異字体に対応することができません。
フォントの cmap format 14 を読み込むことで、
異字体セレクタを使った Unicode → AI0 CID
の変換表を得ることはできるのですが、
異字体セレクタを使った CMap file が無いので、
異字体セレクタを使った Unicode → AJ1 CID
の変換ができません。

でも、源ノフォントには `aj16-kanji.txt` という、
AJ1 CID と源ノフォントのグリフ名の対応表が配布されています。
さらに `AI0-SourceHanSerif` `AI0-SourceHanSans` という、
AI0 CID と源ノフォントのグリフ名の対応表も配布されています。
これらをつなげれば
AI0 CID → AJ1 CID
の対照表が作れます。
ただし、残念ながら漢字しか含まれていません。
非漢字、すなわち、ひらがな・カタカナ・英数字・記号類などについては、
この方法では対照表が得られないということです。
漢字だけと言わずに非漢字の対応表も作ってくれていれば簡単だったのですが。。。
とはいえ、グリフ数の大部分は漢字ですから、
この方法でかなりカバーできているはずです。

#### JIS X 0208

前節で非漢字の対応表が無いと書きましたが、
原ノ味フォントを作ってしばらくしたら
[
JIS X 0208 の範囲での対応表を作っていただいてしまい
](https://twitter.com/ken_lunde/status/1105486635079098369)
、その後アップデートされて
[
JIS90 のグリフも追加されました
](https://twitter.com/ken_lunde/status/1106259919748030464)
。
漢字グリフは元々すべて AJ1 との対応が取れていましたが、
これで JIS X 0208 の範囲に限り非漢字グリフについても AJ1 との対応が取れます
（ただし縦書きは入っておらず横書きのみのようですしルビなども無さそうです）。
この範囲は元々 Unicode を介した変換でも対応できていましたが、
ちゃんとした対応表があるならそれを使った方がよいので、
利用させていただくことにしました。

#### 縦書きなど

源ノフォントに含まれる `GSUB` テーブルから、
縦書き用の OpenType feature である `vert` の部分を読み込むことで、
源ノフォントの横書き用・縦書き用 AI0 CID の対照表が得られます。つまり、
横書き用 AI0 CID →縦書き用 AI0 CID
という変換ができるので、これの逆変換となる
縦書き用 AI0 CID →横書き用 AI0 CID
を作ります。ここに、これまで作った対照表を重ねると、
縦書き用 AI0 CID →横書き用 AI0 CID →横書き用 AJ1 CID
という変換ができます。

また、原ノ味フォント初版リリース後に
[
AJ1 の GSUB は Adobe で配布されている
](https://twitter.com/o_tamon/status/1102231709951483906)
ということを教えていただきました。
このファイルから `vert` をパースすると横書き用・縦書き用 AJ1 CID
の対照表が得られるので、これをさらに重ねることで、
縦書き用 AI0 CID →横書き用 AI0 CID →横書き用 AJ1 CID →縦書き用 AJ1 CID
となって、縦書き用の対照表を作ることができます。

縦書き `vert` 以外にも、CID が 1 対 1 で対応している
`fwid`, `hwid`, `pwid`, `ruby`  についても同様の方法で
対照表を作ることができます。
さらに、1 回これをやって AI0 CID → AJ1 CID の対応を増やしてから、
もう 1 回同じことをするとさらに対応付けできる CID の数が増えるため、
2 回実施しています。

#### その他の変換方法

さらに対照表を充実させる方法も検討しています。

##### OpenType feature

縦書き `vert` など CID が 1 対 1 で対応している OpenType feature
については対照表の作成ができていますが、
1 対 1 対応でないものについても対照表が作れないか考えています。

##### AJ1 CID からの逆探索

現状は、源ノフォントの AI0 CID を出発点として
関連のあるものを辿って AJ1 CID を見つけるというロジックにしています。
しかし、これでは対応が取れない AJ1 CID がどうしても出てきてしまいます。
そこで、対応が取れていなかった AJ1 CID について
AJ1 の 逆変換 CMap である Adobe-Japan1-UCS2 を使い、
AJ1 CID → Unicode
の変換をしてから源ノフォントの cmap を辿ることで、
AJ1 CID → Unicode → AI0 CID
が得られるはずです。
この方法なら、今まで対応が取れていなかった AJ1 CID について
何かしらのグリフを割り当てることができるはずです。

ただし、 Adobe-Japan1-UCS2 は横書き用か、縦書き用か、ルビ用かなどの
情報が失われてしまうため、もしかしたらふさわしくないグリフを
割り当ててしまうかもしれません。
また、この方法だとどこか別の AJ1 CID に割り当て済の AI0 CID を
再度重複して割り当てなければならなくなる可能性が高いと思っています。
一つの AI0 CID を複数の AJ1 CID に割り当てなければならないとなると、
単純に CID を書き換えるだけでは済まなくて、
複製が必要となり難易度が高くなります。

### OpenType テーブル

現状では一部のテーブルが変換できていません。

#### `head`, `hhea`, `maxp`, `OS/2`, `post`, `BASE`, `vhea`

何も変換せずにそのまま流用しています。

#### `name`

`name` 用の変換プログラムで
名称などを変更しています。

#### `cmap`

`cmap` 用の変換プログラムで
CID をすべて AI0 CID から AJ1 CID に変換しています。
対照表が作れずに対応が不明な AI0 CID は削除しています。
format 14 も変換するようにしたため異字体セレクタを使うことができます。
ttx の出力で中身が無かった format 6 は削除しています。
これは本当に中身が無いのか ttx が format 6 のパースに対応していないのか、
どちらなのかはわかりません。

#### `CFF`

`CFF` 用の変換プログラムで
CID をすべて AI0 CID から AJ1 CID に変換しています。
対照表が作れずに対応が不明な AI0 CID は削除しています。
フォントやサブフォントの名称も変更しています。

#### `hmtx`, `vmtx`

`hmtx`, `vmtx` 用の変換プログラムで
CID をすべて AI0 CID から AJ1 CID に変換しています。
対照表が作れずに対応が不明な AI0 CID は削除しています。

#### `VORG`

`VORG` 用の変換プログラムで
CID をすべて AI0 CID から AJ1 CID に変換しています。
対照表が作れずに対応が不明な AI0 CID は削除しています。

#### `GDEF`

原ノ味角ゴシック向けに `GDEF` 用の変換プログラムで
CID をすべて AI0 CID から AJ1 CID に変換しています。
対照表が作れずに対応が不明な AI0 CID は削除しています。
なお、源ノ明朝には `GDEF` が存在しないため、
原ノ味明朝向けには変換せず `GDEF` は存在しません。

#### `GPOS`

`GPOS` 用の変換プログラムで
CID をすべて AI0 CID から AJ1 CID に変換しています。
対照表が作れずに対応が不明な AI0 CID は削除しています。

#### `GSUB`

`GSUB` 用の変換プログラムで
CID をすべて AI0 CID から AJ1 CID に変換しています。
対照表が作れずに対応が不明な AI0 CID は削除しています。
AJ1 用の GSUB 定義を持ってきているわけではなく、
あくまでも源ノフォントの GSUB を変換しています。
とはいえ、「びゃん」や「たいと」などは AJ1 には無いので対応できません。

#### `DSIG`

必須テーブルではないため削除しています。
このテーブルを変換する必要はないと思っています。

## 履歴

* [
20190324
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20190324)
    + 異字体セレクタ に対応
        - cmap format 14 を変換するようにしたため
          異字体セレクタを使うことができるようになりました。
    + OpenType feature に対応
        - `GDEF`, `GPOS`, `GSUB` を変換するようにしたため
          OpenType feature を使うことができるようになりました。
    + JIS X 0208 グリフに対応
        - JISX0208-SourceHan-Mapping.txt 2019-03-14
        - 元々この範囲のグリフには対応できていましたが、
          マッピングファイルを作っていただいたのでそれを使って
          生成するようにしました。
          本件によるグリフ数の増加や変更はありません。
    + [pTeX / pLaTeX 用マップファイルを配布](./tex/map)
        - [各種 TeX 用テストファイル](./tex)もあります。
    + バージョンアップ
        - ttx 0.39.0
    + グリフ数
        - 原ノ味明朝：16678
        - 原ノ味角ゴシック：16683

* [
20190310
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20190310)
    + 縦書きなどのグリフに対応
        - OpenType feature `fwid`, `hwid`, `pwid`, `ruby`, `vert`
          を読み込んで対応付けするグリフを増やしました。
          ただし OpenType feature そのものには対応していませんので、
          今回追加されたグリフにアクセスするには
          CID を直接指定する、 V 系の CMap ファイルを経由する、
          などの必要があります。
    + グリフ数
        - 原ノ味明朝：16678
        - 原ノ味角ゴシック：16683

* [
20190309
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20190309)
    + Adobe-Japan1-6 全漢字グリフに対応
        - 異字体セレクタや OpenType feature には対応していませんので、
          今回追加されたグリフにアクセスするには
          CID を直接指定する必要があります。
    + `BASE`, `VORG`, `vhea`, `vmtx` テーブルを追加
    + グリフ数
        - 原ノ味明朝：16425
        - 原ノ味角ゴシック：16429

* [
20190303
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20190303)
    + 初版
        - 源ノ明朝 1.001、源ノ角ゴシック 2.000
        - ttx 3.38.0, UniJIS2004-UTF32-H 1.020
    + グリフ数
        - 原ノ味明朝：15213
        - 原ノ味角ゴシック：15215

## ライセンス

Copyright (C) 2019 Masamichi Hosoda

生成プログラムのライセンスは BSD 2-Clause です。
生成したフォントは源ノフォントの派生フォントになるため
SIL Open Font License 1.1 です。
