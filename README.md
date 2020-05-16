<!-- -*- coding: utf-8 -*- -->
# 原ノ味フォント生成プログラム / Harano Aji Fonts generator

[ Japanese （日本語） / [English](README.en.md) ]

源ノ明朝・源ノ角ゴシック（以下、源ノフォント）を
Adobe-Japan1 （以下、AJ1）フォントになるように組み替えた
「原ノ味フォント（原ノ味明朝、原ノ味角ゴシック）」
生成プログラムです。
CID の対応がとれないため抜けてしまうグリフがありますが、
素の pTeX / pLaTeX で和文フォントとして使う分には
すべてのグリフが揃っています。

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
* 生成した原ノ味フォント（日本語版：JP）
    - TeX Live
        - TeX Live 2020 以降に含まれており、
          （ごく一部のエンジンを除き）和文のデフォルトフォントになっています
        - TeX Live 2019 では 2020 年 2 月中旬以降の更新に含まれています
          （デフォルトフォントではありません）
    - W32TeX
        - 2020 年 3 月 23 日以降に含まれています
    - CTAN
        - 主要 7 フォント（各種 TeX 用プリセット設定で使うウェイト）
            - [
https://www.ctan.org/pkg/haranoaji
](https://www.ctan.org/pkg/haranoaji)
        - 追加 7 フォント（プリセットでは使わないウェイト）
            - [
https://www.ctan.org/pkg/haranoaji-extra
](https://www.ctan.org/pkg/haranoaji-extra)
    - GitHub
        - [
https://github.com/trueroad/HaranoAjiFonts
](https://github.com/trueroad/HaranoAjiFonts)

その他、以下のファイルも配布しています。

* [
各種 TeX ファイル
](https://github.com/trueroad/HaranoAjiFonts-generator/tree/master/tex)
    + ドキュメント、サンプル、テストファイルなど
* fontspec 用ファイル
    + [HaranoAjiMincho.fontspec](./tex/HaranoAjiMincho.fontspec),
      [HaranoAjiGothic.fontspec](./tex/HaranoAjiGothic.fontspec)
    + `luatexja-preset` などのプリセット設定を使う場合は不要です

pTeX / pLaTeX 用マップファイルは
[ptex-fontmaps](https://www.ctan.org/pkg/ptex-fontmaps)
20200217.0 以降に入っています。

**実験的**に生成した中国語簡体字、中国語繁体字、韓国語フォントがあります。

* （実験的）中国語簡体字 (CN)：Adobe-GB1 対応
    + [
https://github.com/trueroad/HaranoAjiFontsCN
](https://github.com/trueroad/HaranoAjiFontsCN)
* （実験的）中国語繁体字 (TW)：Adobe-CNS1 対応
    + [
https://github.com/trueroad/HaranoAjiFontsTW
](https://github.com/trueroad/HaranoAjiFontsTW)
* （実験的）韓国語 (KR)：Adobe-KR 対応
    + [
https://github.com/trueroad/HaranoAjiFontsKR
](https://github.com/trueroad/HaranoAjiFontsKR)

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
* 文字幅の食い違いが発生しない
    - 源ノフォントは AI0 なので、文字幅について明確な決まりが無く、
      JFM の文字幅と食い違ってしまい、
      dvipdfmx で後続文字の位置がズレるなど、
      組版結果がおかしくなることがあります。
    - 原ノ味フォントは AJ1 に従った文字幅にしているので、
      後続文字の位置がズレることはありません（20190824 版以降）。

といったメリット？があります。

## 搭載グリフ

源ノフォントが搭載しているグリフ、かつ、
AJ1 への対応が取れたものを搭載します。

* 漢字
    + Adobe-Japan1-6 漢字グリフはすべて搭載
        + \<U+6CE8 U+E0102\> (AJ1 CID+12869) ルビ用の「注」は非搭載
            + これは AJ1 の「漢字グリフ」範囲外で漢字扱いではありません。
    + JIS X 0208、JIS X 0213 の全漢字グリフを搭載
* 非漢字（ひらがな、カタカナ、英数字、記号類など）
    + JIS X 0208 横書きグリフすべて搭載
    + JIS X 0208 縦書きグリフすべて搭載（20200418 版以降）
    + JIS X 0213 の非漢字グリフには抜けているものがあります。
    + その他 Adobe-Japan1-6 非漢字グリフには抜けているものがあります。

以下の縦書きグリフは、横書きグリフを加工したものを搭載しています
（20200418 版以降）。

* `‖` AJ1 CID+7895 U+2016 'DOUBLE VERTICAL LINE'
    + AJ1 CID+666 を右90度回転
* `°` AJ1 CID+8269 U+00B0 'DEGREE SIGN'
    + AJ1 CID+707 を平行移動
* `′` AJ1 CID+8273 U+2032 'PRIME'
    + AJ1 CID+708 を平行移動
* `″` AJ1 CID+8283 U+2033 'DOUBLE PRIME'
    + AJ1 CID+709 を平行移動
* `✂` AJ1 CID+12178 U+2702 'BLACK SCISSORS'
    + AJ1 CID+12176 を右90度回転

抜けているグリフのCIDにはダミーグリフ
（.notdef と同じで四角の中に×が入ったような形）が入っています。
そのほとんどは
源ノフォントが搭載していないため原ノ味フォントに搭載できないものです。

非漢字の搭載グリフの一部で、
源ノフォントの文字幅が AJ1 の文字幅に合わなくて、
強制的に AJ1 に合わせたものがあります（20190824 版以降）。
AJ1 でプロポーショナル幅とされているグリフは変更していません。
さらに、単純に幅を上書きするだけでなく、
グリフによって中央寄せなどの位置調整を行いました（20200215 版以降）。
このため、幅が広くなったグリフは隙間ができたり、
幅が狭くなったグリフは左右がはみ出て前後の文字と重なるなどの現象が発生したり、
不格好な表示になることがあります。
とはいえ、幅としては正しくなっているため、
後続文字の位置がズレるなどといった、組版への影響は発生しません。
以下に該当のグリフを示します。

+ ギリシャ文字
+ キリル文字
+ `¨` AJ1 CID+647 U+00A8 'DIAERESIS'
+ `°` AJ1 CID+707 U+00B0 'DEGREE SIGN'
+ `´` AJ1 CID+645 U+00B4 'ACUTE ACCENT'
+ `′` AJ1 CID+708 U+2032 'PRIME'
+ `″` AJ1 CID+709 U+2033 'DOUBLE PRIME'
+ `‼` AJ1 CID+12111 U+203C 'DOUBLE EXCLAMATION MARK'
+ `⁇` AJ1 CID+16278 U+2047 'DOUBLE QUESTION MARK'
+ `⁈` AJ1 CID+16279 U+2048 'QUESTION EXCLAMATION MARK'
+ `⁉` AJ1 CID+12112 U+2049 'EXCLAMATION QUESTION MARK'
+ `ℓ` AJ1 CID+8025 U+2113 'SCRIPT SMALL L'
+ `№` AJ1 CID+7610 U+2116 'NUMERO SIGN'
+ `−` AJ1 CID+693 U+2212 'MINUS SIGN'
+ `✓` AJ1 CID+16270 U+2713 'CHECK MARK'

以下については、源ノフォントでは幅がゼロの合成用グリフですが、
AJ1 で全角幅の CID に割り当たったため、
幅を全角幅で上書きし（20190824 版以降）位置調整をし（20200215 版以降）
他の AJ1 フォントと同じような位置になるよう再調整しました（20200418 版以降）。
そのため、不格好な表示になることがあります。

+ AJ1 CID+16328 U+20DD 'COMBINING ENCLOSING CIRCLE'
+ AJ1 CID+11035 U+20DE 'COMBINING ENCLOSING SQUARE'
    + CID+11035 は、
      原ノ味角ゴシックのみ幅ゼロの合成用グリフが割り当たったため
      全角幅で上書きおよび位置調整を実施し、
      原ノ味明朝は全角幅グリフが割り当たったため
      幅上書きや位置調整をしていません
+ AJ1 CID+16326 U+3099 'COMBINING KATAKANA-HIRAGANA VOICED SOUND MARK'
+ AJ1 CID+16327 U+309A 'COMBINING KATAKANA-HIRAGANA SEMI-VOICED SOUND MARK'

また、ダミーグリフは全角幅ですが、
これも AJ1 の文字幅で上書きしています。

## pTeX / pLaTeX

源ノフォントと異なり比較的簡単に使うことができます。
TeX Live 2020 以降ではデフォルトフォントになっているので、
何もしなくてもそのままで使えます。
ただし搭載しない（抜けている）グリフを使うことはできません。

* OTF パッケージを使わない場合
    + JIS90 字形 / JIS2004 字形、横書き / 縦書き、
      いずれの組み合わせでも全グリフ使えます（20200418 版以降）。
* OTF パッケージを使う場合
    + Adobe-Japan1-6 全漢字グリフから CID 直接指定などで
      呼び出すことができます。
        + AJ1 CID+12869 （ルビ用の「注」）は使えません。
    + 非漢字（ひらがな、カタカナ、英数字、記号類など）には
      使えないグリフもあります。

詳細は「搭載グリフ」も参照してください。

TeX Live をお使いの場合、
[ptex-fontmaps](https://www.ctan.org/pkg/ptex-fontmaps)
が 20200217.0 以降になっていて sudo で管理者権限が使えるなら、

```
$ sudo kanji-config-updmap-sys --jis2004 haranoaji
```

のようにすることで原ノ味フォントに切り替わります。

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
* Python3
* GNU Make
* GNU sed
* その他 sh など

### ファイル (JP)

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
* AJ1-7 の GSUB 情報
    + [
The Adobe-Japan1-7 Character Collection
](https://github.com/adobe-type-tools/Adobe-Japan1)
      から `aj17-gsub-jp04.fea`
      （GSUB ディレクトリにあります）

注意：
`aj16-kanji.txt` は明朝とゴシックでファイル名が同じですが中身は異なります。
このファイルだけ明朝・ゴシック別のディレクトリに配置してください。
その他のファイルはすべて同じディレクトリに配置してください。

### 生成 (JP)

`make` で生成できます。

### （実験的）他の言語

#### （実験的）ファイル (CN)

* Source Han フォント Region-specific Subset OTFs CN 版
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
* AG1-5 の GSUB 情報
    + [
The Adobe-GB1-5 Character Collection
](https://github.com/adobe-type-tools/Adobe-GB1)
      から `ag15-gsub.fea`
      （GSUB ディレクトリにあります）

#### （実験的）生成 (CN)

`make cn` で生成できます。

#### （実験的）ファイル (TW)

* Source Han フォント Region-specific Subset OTFs TW 版
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
* AC1-7 の GSUB 情報
    + [
The Adobe-CNS1-7 Character Collection
](https://github.com/adobe-type-tools/Adobe-CNS1)
      から `ac17-gsub.fea`
      （GSUB ディレクトリにあります）

#### （実験的）生成 (TW)

`make tw` で生成できます。

#### （実験的）ファイル (KR)

* Source Han フォント Region-specific Subset OTFs KR 版
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
* AKR-9 の GSUB 情報
    + [
The Adobe-KR-9 Character Collection
](https://github.com/adobe-type-tools/Adobe-KR)
      から `akr9-gsub.fea`
      （GSUB ディレクトリにあります）

#### （実験的）生成 (KR)

`make kr` で生成できます。

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

#### 漢字（JP のみ）

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

#### JIS X 0208 （JP のみ）

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

AJ1-7 の GSUB が入手可能です。
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

#### その他の変換方法（JP のみ）

以上でほとんどの CID を対応付けすることができており、
抜けているグリフはもともと源ノフォントが持っていないもの
がほとんどと思っています。

横書き用グリフはあるが縦書き用グリフがなく、
かつ縦横いずれも AJ1 で全角幅になっているものについては、
横書きグリフをもとにして、
右90度回転
(AJ1 CID+7895, AJ1 CID+12178)
もしくは平行移動
(AJ1 CID+8269, AJ1 CID+8273, AJ1 CID+8283)
する加工によって縦書きグリフを作り出しています。
同じように、既存グリフの縮小や変形などの機械的変形で、
組み文字などの抜けているグリフを作って埋めることも可能ですが、
縮小で細くなってしまうなどデザイン的な問題が発生するため、
なかなか難しいです。

また、横組み専用かな、縦組み専用かな、ルビ用かな、などが抜けていますが、
ここに通常のかなのグリフをそのままコピーして搭載する方法も考えられます。
ただ、本来は別のデザインのグリフが必要なのに、
同じグリフにしてしまうことによるデザイン的な問題が発生するため、
こちらもなかなか難しいです。

もともとは、品質が劣るグリフを入れるよりは、
ダミーグリフにして抜けていることがわかりやすい方がよいだろう、
という考え方をしていました。
一方で、品質は劣ってもいいからそれっぽい形のグリフが入っていた方がよい、
という考え方もあり得ると思います。

また、品質のために使用頻度の低いグリフに大きな手間をかけても仕方ありませんが、
上記の加工 5 グリフのうちの 4 グリフ
(AJ1 CID+7895, AJ1 CID+8269, AJ1 CID+8273, AJ1 CID+8283)
は、揃えば素の pTeX 全グリフ搭載を達成できる重要なもので、
右90度回転や平行移動程度であればデザイン的には大きな問題にならないと判断し、
投入したものです。もう一つ
(AJ1 CID+12178)
は、同じ右90度回転で済むため、いわば「ついで」に投入しました。

どこまでやるか、品質も手間も含めて考えていく必要があると思っています。

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

原ノ味フォント 20200516 から、KR のみ format 4 と format 12 に対し、
Unicode コードポイントで一つだけ抜けている
（両隣は存在するが該当箇所は存在しない）ものに
.notdef を割り当てる加工をしています。
これは、何もしないと format 4 のサイズが 64 KB を超えてしまい、
ttx でのフォント生成が例外で落ちてしまったためです。
format 12 はサイズの問題がないし format 4 の情報もすべて含んだ上位互換なので、
format 4 がなくてもいいだろうと削除してみたら落ちなくなりましたが、
Windows がフォントとして認識してくれません。
仕方なく format 4 の仕様書とにらめっこしてサイズを低減する方法を模索し、
上記の処理を入れました。
なお format 12 も BMP の範囲は format 4 と同じである必要があるため、
BMP 範囲内のみ同じ処理を入れてあります。

#### `CFF`

`CFF` 用の変換プログラムで
CID をすべて AI0 CID から AJ1 CID に変換しています。
対照表が作れずに対応が不明な AI0 CID は削除しています。
フォントやサブフォントの名称も変更しています。
欠けている AJ1 CID についてはダミーグリフとして
.notdef の内容をコピーしています。

原ノ味フォント 20200215 から、
横幅を上書きしたグリフについて CharString を書き換え、
左右の位置を調整するようにしています。
これは [@h20y6m](https://github.com/h20y6m) さんのコードによるものです。

原ノ味フォント 20200418 から、
縦書き 5 グリフを、
横書き用グリフの右90度回転もしくは平行移動で作り出しています。
また、ダミーグリフの CharString をサブルーチン化することで
ファイルサイズ低減を図っています。

#### `hmtx`, `vmtx`

`hmtx`, `vmtx` 用の変換プログラムで
CID をすべて AI0 CID から AJ1 CID に変換しています。
対照表が作れずに対応が不明な AI0 CID は削除しています。
欠けている AJ1 CID についてはダミーグリフとして
.notdef の内容をコピーしています。

原ノ味フォント 20190824 から、
源ノフォントの横幅と AJ1 の横幅が食い違ったグリフについて、
`hmtx` に AJ1 の横幅を上書きしています。
AJ1 がプロポーショナル幅の場合は上書きしません。

原ノ味フォント 20200418 から、
幅上書、位置調整、右90度回転、平行移動したグリフについて、
CharString のレンダリングと同様の処理で字面を計算し、
LSB （左サイドベアリング）と TSB （上サイドベアリング）を修正しています。

原ノ味フォント 20200516 から、
KR で AKR の横幅が Monospaced になっているものは全角幅としています。

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

原ノ味フォント 20200418 から、
幅上書、位置調整したグリフについてテーブルから削除しています。

原ノ味フォント 20200516 から、
KR のみ `GPOS` テーブルを削除しています。
これはテーブルの変換がうまくいっていない（ttx でフォント生成はできるが
Windows がフォントとして認識してくれない）ためです。

#### `GSUB`

`GSUB` 用の変換プログラムで
CID をすべて AI0 CID から AJ1 CID に変換しています。
対照表が作れずに対応が不明な AI0 CID は削除しています。
AJ1 用の GSUB 定義を持ってきているわけではなく、
あくまでも源ノフォントの GSUB を変換しています。
とはいえ、「びゃん」や「たいと」などは AJ1 には無いので対応できません。

原ノ味フォント 20200516 から、chain context の変換に対応しました。
chain context があるのは KR のみです。

#### `DSIG`

必須テーブルではないため削除しています。
このテーブルを変換する必要はないと思っています。

## 履歴

* [
20200516
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20200516)
(CN, TW, KR)
    + **実験的に**中国語簡体字、中国語繁体字、韓国語フォントを
      生成できるようにしました
    + 各言語版のフォント名は、サフィックスにベースとした源ノフォントと同じ
      アルファベット 2 文字を付けています
        + 中国語簡体字：Adobe-GB1 対応、サフィックス CN
            + UniGB-UTF32-H 1.016
        + 中国語繁体字：Adobe-CNS1 対応、サフィックス TW
            + UniCNS-UTF32-H 1.019
        + 韓国語：Adobe-KR 対応、サフィックス KR
            + UniAKR-UTF32-H 1.002
    + 日本語は変更なし、今回のリリースもありません
    + 今後は各言語版の略称にサフィックスを使います
        + 日本語版はフォント名にサフィックスありませんが略称 JP とします
    + バージョンアップ
        - ttx 4.10.0
* [
20200418
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20200418)
    + 縦書き用 5 グリフを追加しました
        + 素の pTeX で使用できるすべてのグリフが揃いました
        + いずれも横書き用のグリフを加工（右90度回転または平行移動）
          したものです
            + `‖` AJ1 CID+7895 U+2016 'DOUBLE VERTICAL LINE'
            + `°` AJ1 CID+8269 U+00B0 'DEGREE SIGN'
            + `′` AJ1 CID+8273 U+2032 'PRIME'
            + `″` AJ1 CID+8283 U+2033 'DOUBLE PRIME'
            + `✂` AJ1 CID+12178 U+2702 'BLACK SCISSORS'
    + ファイルサイズを低減しました
        + 14フォント合計で 79.1 MBから 72.3 MB になり 6.8 MB （約 9 %）減
        + CharString でダミーグリフを展開せず、
          サブルーチン呼び出しに変更したことによります
    + 2グリフの描画位置を再調整しました
        + 20200215 版では位置調整の結果ボックス内右上隅に寄っていましたが、
          他の AJ1 フォントではボックス内左上隅に寄っていたため再調整しました
            + AJ1 CID+16326 U+3099
              'COMBINING KATAKANA-HIRAGANA VOICED SOUND MARK'
            + AJ1 CID+16327 U+309A
              'COMBINING KATAKANA-HIRAGANA SEMI-VOICED SOUND MARK'
    + 位置調整したグリフの LSB （左サイドベアリング）を修正しました
        + 20200215 版では、位置調整したグリフについて `hmtx` テーブルの
          LSB も修正すべきでしたが、していませんでした
        + 平行移動や回転したグリフも合わせて LSB と
          `vmtx` テーブルの TSB （上サイドベアリング）
          を計算して修正するようにしました
    + 幅上書き・位置調整したグリフを `GPOS` テーブルから取り除きました
        + 20190824 版で幅上書き、20200215 版で位置調整したグリフが、
          `GPOS` テーブルに上書き・調整前のパラメータのまま残っていたため、
          OpenType feature の指定によっては位置がおかしくなることがありました
        + `GPOS` テーブルから削除したので問題なくなりました
    + バージョンアップ
        - ttx 4.7.0
    + グリフ数
        - 原ノ味明朝：16684
        - 原ノ味角ゴシック：16689
        - 上記 5 グリフ追加に伴い増加しています
* [
20200215
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20200215)
    + 横幅を上書きしたグリフについて、中央揃えにするなどの位置調整をしました
        + [@h20y6m](https://github.com/h20y6m) さんの
          [#2](https://github.com/trueroad/HaranoAjiFonts-generator/issues/2),
          [#3](https://github.com/trueroad/HaranoAjiFonts-generator/pull/3)
          によるものです
            - Python3 が必要になります
    + バージョンアップ
        - ttx 4.3.0, UniJIS2004-UTF32-H 1.021
            - 前の 20190824 では UniJIS2004-UTF32-H のバージョンが
              1.020 のまま変わっていない状態でビルドしていました
            - UniJIS2004-UTF32-H 1.020 から 1.021 への変更により、
              原ノ味明朝では AJ1 CID+127 が増え、
              原ノ味角ゴシックでは AJ1 CID+127 が紐づくグリフが変更
              （AI0 CID+253 から AI0 CID+247）になっています
    + グリフ数
        - 原ノ味明朝：16679
        - 原ノ味角ゴシック：16684
        - 上記 UniJIS2004-UTF32-H のアップデートに伴い、
          原ノ味明朝で 1 グリフ増えています
* [
20190824
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20190824)
    + グリフの横幅を AJ1 の定義に従うようにしました
        + これまで一部のグリフで AJ1 の横幅と食い違っているものがあり、
          [
後続文字の位置がズレて組版結果がおかしくなる
](https://twitter.com/trueroad_jp/status/1164525246319251456)
          ことがありました。
        + 単純に横幅を上書きしただけなので、
          該当のグリフを使うと、左に寄って表示されたり、
          前後の文字に重なったり、不格好な表示になることがありますが、
          他のグリフの位置には影響を及ぼさなくなっているハズです。
    + AJ1-7 の GSUB 情報
        + AJ1-7 の GSUB 情報が公開されたので、
          それを利用するようにしました。
    + バージョンアップ
        - ttx 4.0.0, ~~UniJIS2004-UTF32-H 1.021~~
            - UniJIS2004-UTF32-H は 1.020 のままでした（20200215 追記）
    + グリフ数
        - 原ノ味明朝：16678
        - 原ノ味角ゴシック：16684
        - カウント方法を変更しましたが、数は同じです。
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

Copyright (C) 2019, 2020 Masamichi Hosoda

生成プログラムのライセンスは BSD 2-Clause です。
[LICENSE](./LICENSE)をご覧ください。
生成したフォントは源ノフォントの派生フォントになるため
SIL Open Font License 1.1 です。
