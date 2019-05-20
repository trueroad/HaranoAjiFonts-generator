<!-- -*- coding: utf-8 -*- -->
# 原ノ味フォント生成プログラム / Harano Aji Fonts generator

源ノ明朝・源ノ角ゴシック（以下、源ノフォント）を
Adobe-Japan1 （以下、AJ1）フォントになるように組み替えた
「原ノ味フォント（原ノ味明朝、原ノ味角ゴシック）」
生成プログラムです。
CID の対応がとれないため抜けてしまうグリフがありますが、
素の pTeX / pLaTeX で和文フォントとして使う分には
ほぼすべてのグリフが揃っています。

「原ノ味」というのは、
源ノフォントからグリフやテーブルが抜けていることを表すために
「氵（さんずい）」を取り、
AJ1 をもじって AJI にして
音から「味」という字をあてたものです。

## 配布

* 原ノ味フォント生成プログラム
    - [
https://github.com/trueroad/HaranoAjiFonts-generator
](https://github.com/trueroad/HaranoAjiFonts-generator)
* 生成した原ノ味フォント
    - [
https://github.com/trueroad/HaranoAjiFonts
](https://github.com/trueroad/HaranoAjiFonts)

その他、以下のファイルも配布しています。

* [
pTeX / pLaTeX 用マップファイル
](https://github.com/trueroad/HaranoAjiFonts-generator/tree/master/tex/map)
* [
各種 TeX 用テストファイル
](https://github.com/trueroad/HaranoAjiFonts-generator/tree/master/tex)

## Adobe-Japan1 (AJ1) v.s. Adobe-Identity0 (AI0)

源ノフォントは Adobe-Identity0 （以下、AI0）の
Pan-CJK フォントで日本語以外にも対応しています。
一方で AJ1 だと日本語専用になってしまいますが、

* pTeX / pLaTeX で比較的簡単に使うことができる
    - pTeX / pLaTeX で源ノフォント（AI0 フォント）を使うのは少々難しいです
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
              →[
PDF から ToUnicode CMap を削除するツール
](https://github.com/trueroad/pdf-rm-tuc)
              で原ノ味フォントの ToUnicode CMap を削除することもできます

といったメリット？があります。

## 搭載グリフ

源ノフォントが搭載しているグリフ、かつ、
AJ1 への対応が取れたものを搭載します。

* 漢字
    + Adobe-Japan1-6 漢字グリフは以下の 1 グリフを除きすべて搭載
        + \<U+6CE8 U+E0102\> (AJ1 CID+12869) 「注」の異字体
    + JIS X 0208、JIS X 0213 の全漢字グリフを搭載
* 非漢字（ひらがな、カタカナ、英数字、記号類など）
    + JIS X 0208 横書きグリフはすべて搭載
        + JIS90 字形（CMap file `H` を使った場合）すべて搭載
        + JIS2004 字形（CMap file `2004-H` を使った場合）すべて搭載
    + JIS X 0208 縦書きグリフは以下の 4 グリフを除きすべて搭載
        + JIS90 字形（CMap file `V` を使った場合）
            + `‖` 01-34 U+2016 'DOUBLE VERTICAL LINE'
              (AJ1 CID+7895)
        + JIS2004 字形（CMap file `2004-V` を使った場合）
            + `‖` 01-34 U+2016 'DOUBLE VERTICAL LINE'
              (AJ1 CID+7895)
            + `°` 01-75 U+00B0 'DEGREE SIGN'
              (AJ1 CID+8269)
            + `′` 01-76 U+2032 'PRIME'
              (AJ1 CID+8273)
            + `″` 01-77 U+2033 'DOUBLE PRIME'
              (AJ1 CID+8283)
    + JIS X 0213 の非漢字グリフには抜けているものがあります。
    + その他 Adobe-Japan1-6 非漢字グリフには抜けているものがあります。

抜けているグリフのCIDにはダミーグリフ
（.notdef と同じで四角の中に×が入ったような形）が入っています。
上記で具体的に記載した非搭載グリフ（漢字 1 グリフ、非漢字縦書き 4 グリフ）は
いずれも源ノフォントが搭載していないため原ノ味フォントに搭載できないものです。
`H`, `V` は[
Adobe が配布する CMap file
](https://github.com/adobe-type-tools/cmap-resources)
で、TeX Live などにも含まれています。
`2004-H`, `2004-V` は[
Japanese TeX Development Community が配布する CMap file
（のようなもの）
](https://github.com/texjporg/jfontmaps/tree/master/cmap)
で、TeX Live にも含まれています。

## pTeX / pLaTeX

源ノフォントと異なり比較的簡単に使うことができます。
フォントファイルとマップファイルを適切に配置すれば普通に使えます。
ただし搭載しない（抜けている）グリフを使うことはできません。

* OTF パッケージを使わない場合
    + JIS90 字形（マップファイル `ptex-haranoaji.map` を使った場合）
        + 横書きは全グリフ使えます。
        + 縦書きは 1 グリフ `‖` だけ使えません。
    + JIS2004 字形（マップファイル `ptex-haranoaji-04.map` を使った場合）
        + 横書きは全グリフ使えます。
        + 縦書きは 4 グリフ `‖`, `°`, `′`, `″` 使えません。
* OTF パッケージを使う場合
    + Adobe-Japan1-6 全漢字グリフから 1 グリフを除き CID 直接指定などで
      呼び出すことができます。
        + AJ1 CID+12869 （「注」の異字体）だけ使えません。
    + 非漢字（ひらがな、カタカナ、英数字、記号類など）には
      使えないグリフもあります。

詳細は「搭載グリフ」も参照してください。

### ipsj.cls

ipsj.cls の場合は下記のマップファイル

```
rml	H	HaranoAjiMincho-Light.otf
gbm	H	HaranoAjiGothic-Regular.otf
futomin-b	H	HaranoAjiMincho-Regular.otf
futogo-b	H	HaranoAjiGothic-Medium.otf
```

を使い、クラスオプションから `submit` を外すと
[
本物っぽくなると思います
](https://twitter.com/trueroad_jp/status/1111612471763066880)
。

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
また、cmap format 12 も CMap file も異字体セレクタの情報がありませんから、
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
また、上記の配布は Adobe-Japan1-6 までの範囲しか含まれておらず、
Adobe-Japan1-7 で追加されたグリフについては縦書きへの対応が得られません。
そこで
[
AJ17 フォントの「令和」合字
](https://twitter.com/ken_lunde/status/1114141493948633088)
の情報を追加することで対応しています。

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

ほとんどのテーブルを変換しています。

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
欠けている AJ1 CID についてはダミーグリフとして
.notdef の内容をコピーしています。

#### `hmtx`, `vmtx`

`hmtx`, `vmtx` 用の変換プログラムで
CID をすべて AI0 CID から AJ1 CID に変換しています。
対照表が作れずに対応が不明な AI0 CID は削除しています。
欠けている AJ1 CID についてはダミーグリフとして
.notdef の内容をコピーしています。

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
20190501
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20190501)
    + フルセットフォント化
        - これまで AJ1 CID で抜けているグリフは欠番にする
          「サブセットフォント」にしていました。
          これをダミーグリフを入れることにより CID に欠番のない
          「フルセットフォント」にしました。
        - 通常の AJ1 フォントはフルセットフォントなのに対して、
          サブセットフォントだと一部挙動が異なるソフトウェアが
          あるようなのでフルセットに変えることにしました。
            - サブセットフォントだと CID ≠ GID になるのですが、
              これが原因で[
かなり特殊なことをしようとすると変になる
](https://twitter.com/trueroad_jp/status/1123484898386427904)
              ことがあるようです。普通に使う分には問題ありませんでした。
        - これまでは欠番 CID を使用しようとすると警告が出ていたような
          ツールでもフルセット化により警告が出なくなります。
          無警告でダミーグリフが使われることで
          意図しない結果になる恐れがあります。ご注意ください。
        - 原ノ味明朝は Adobe-Japan1-7 を名乗っていますが、
          CID+23058, CID+23059 が無いので実はサブセットフォントです。
          ただし、AJ1-6 の範囲は（ダミーを含めることで）すべて埋まっていて
          CID ＝ GID なので、これが原因で変になることはありません。
    + バージョンアップ
        - ttx 3.41.0
    + グリフ数
        - 変わってないはずですが、
          ダミーグリフの影響でグリフ数を数えるのが難しくなりました。。。
* [
20190413
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20190413)
    + Adobe-Japan1-7 に対応
        - `CFF` テーブルの ROS を Adobe-Japan1-7 に変更しました。
        - あわせて Adobe-Japan1-7 で追加されたグリフの GSUB 情報を
          使うようにしました。
    + 源ノ角ゴシック 2.001 に対応
        - ベースとなる源ノ角ゴシックを 2.000 から 2.001 に変更しました。
        - これにより「令和」の合字 (U+32FF) に対応、
          横書き (AJ1 CID+23058) 縦書き (AJ1 CID+23059) とも搭載。
            - 原ノ味角ゴシックのみです。
            - 原ノ味明朝も Adobe-Japan1-7 フォントになりましたが
              源ノ明朝が搭載しないため搭載していません。
        - 原ノ味角ゴシックのグリフ数は 1 グリフしか増えませんでした。
          これは源ノ角ゴシック 2.000 にはダミーのグリフが含まれており
          原ノ味角ゴシックにもダミーの横書きグリフが含まれていたためです。
          今回のバージョンアップで、横書きグリフはダミーから
          正式なグリフに変更になったためグリフ数が増加せず、
          縦書きは追加の GSUB 情報で紐づけができるようになり
          グリフ数が増加したものです。
    + バージョンアップ
        - 源ノ角ゴシック 2.001
        - ttx 3.40.0
    + グリフ数
        - 原ノ味明朝：16678
        - 原ノ味角ゴシック：16684

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
        - ttx 3.39.0
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
