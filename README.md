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
* （実験的）韓国語 (K1)：Adobe-Korea1 対応
    + [
https://github.com/trueroad/HaranoAjiFontsK1
](https://github.com/trueroad/HaranoAjiFontsK1)

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

非漢字のうち、かなグリフ（ひらがな、カタカナ）は以下のようになっています。
分類は AJ1-7 によります。
全角とプロポーショナルで搭載していない
小書き「こ」と小書き「コ」は源ノフォントに存在せず、
加工元にできるグリフがありません。

* 半角かな
    + 横組み用
        - 濁点・半濁点のつかないカタカナなどを搭載
        - ひらがな、濁点・半濁点付きなどは非搭載
    + 縦組み用
        - すべて非搭載
* （通常の）全角かな
    + 横組み用
        - 2 グリフのみ非搭載（小書き「こ」小書き「コ」）
        - 他はすべて搭載
        - 源ノの横組み用かなグリフを割り当てている
        - 源ノの横組み用かなの GPOS 情報を割り当てている
        - 注：AJ1 の「（通常の）全角かな横組み用」は小書き等を除き縦横両用
        - GSUB feature 無しで選択できる
        - GPOS feature の palt などを利用できる（今後変更の可能性あり）
    + 縦組み用
        - 2 グリフのみ非搭載（小書き「こ」小書き「コ」）
        - 他はすべて搭載
        - 源ノの縦組み用かなグリフを割り当てている
        - 源ノの縦組み用かなの GPOS 情報は割り当てていない（20210130 版以降）
        - 注：AJ1 の「（通常の）全角かな縦組み用」は
          小書き等の横組み用ではマズい一部のグリフのみが存在し、
          それ以外は「（通常の）全角かな横組み用」を使うようになっている
        - GSUB feature の vert または vrt2 で選択できる
        - GPOS feature の vpal などは利用できない
* 組方向ごとに最適化した全角かな
    + 横組み用（20210101 版以降）
        - 2 グリフのみ非搭載（小書き「こ」小書き「コ」）
        - 他はすべて搭載
        - 源ノの横組み用かなグリフを割り当てている
        - 源ノの横組み用かなの GPOS 情報を割り当てていない
          （今後変更の可能性あり）
        - そのため「（通常の）全角かな横組み用」と同じグリフを搭載
          （ただし GPOS 情報は無し）
        - GSUB feature の hkna で選択できる
        - GPOS feature の palt などは利用できない（今後変更の可能性あり）
    + 縦組み用（20210101 版以降）
        - 2 グリフのみ非搭載（小書き「こ」小書き「コ」）
        - 他はすべて搭載
        - 源ノの縦組み用かなグリフを割り当てている
        - 源ノの縦組み用かなの GPOS 情報を割り当てている
        - そのため、小書き等の「（通常の）全角かな縦組み用」に
          存在するもののみ同じグリフを搭載、それ以外は別グリフを搭載
        - GSUB feature の vert と vkna を併用すると選択できる
        - GPOS feature の vpal などを利用できる
* プロポーショナルかな
    + 横組み用（20210101 版以降、一部は 20200524 版以降）
        - 2 グリフのみ非搭載（小書き「こ」小書き「コ」）
        - 他はすべて搭載
        - 源ノの横組み用かなで palt があるものは加工し、
          ないものはそのまま搭載
        - GSUB feature の pwid で選択できる
        - GPOS feature は利用できない
    + 縦組み用（20210102 版以降）
        - 2 グリフのみ非搭載（小書き「こ」小書き「コ」）
        - 他はすべて搭載
        - 源ノの縦組み用かなで vpal があるものは加工し、
          ないものはそのまま搭載
        - GSUB feature の pwid と vert を併用すると選択できる
        - GPOS feature は利用できない
* ルビかな
    + 横組み用
        - すべて非搭載
    + 縦組み用
        - すべて非搭載
* U-PRESSかな
    + 横組み用
        - すべて非搭載

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

以下のグリフは、他のグリフを加工したものを搭載しています
（20220220 版以降）。

* `✂` AJ1 CID+12175 U+2702 'BLACK SCISSORS'
    + AJ1 CID+12176 を180度回転
* `✂` AJ1 CID+12177 U+2702 'BLACK SCISSORS'
    + AJ1 CID+12176 を270 (-90)度回転
* `〝` AJ1 CID+12169 U+301D 'REVERSED DOUBLE PRIME QUOTATION MARK'
    + AJ1 CID+7608 をそのままコピー
        - 組み合わせて使う AJ1 CID+12170 は以前より存在し、
          小塚とは微妙に角度が違いますがCID+12169, CID+12170 でほぼ線対称の
          グリフにできたためその状態で収録します
* `‘` AJ1 CID+12171 U+2018 'LEFT SINGLE QUOTATION MARK'
    + AJ1 CID+12173 を270 (-90)度回転
* `’` AJ1 CID+12172 U+2019 'RIGHT SINGLE QUOTATION MARK'
    + AJ1 CID+12174 を270 (-90)度回転

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

以下については、
源ノ明朝では
[
縦書きグリフも横書きグリフも左上に配置されています
](https://github.com/adobe-fonts/source-han-serif/issues/157)
が、
AJ1 の縦書きグリフでは右下に配置されるのが普通のようなので
平行移動して位置調整しました（20220130 版以降）。
源ノ角ゴシックにはこの問題はありませんので調整していません。

+ CID+8271 (GSUB vert/vrt2,
  `゜` U+309C 'KATAKANA-HIRAGANA SEMI-VOICED SOUND MARK')
+ CID+8272 (GSUB vert/vrt2,
  `゛` U+309B 'KATAKANA-HIRAGANA VOICED SOUND MARK')

原ノ味フォント 20200524 からプロポーショナルかな横組み用を搭載しています。
源ノフォントの palt に従って幅と位置を調整したものです。
原ノ味フォント 20210102 からプロポーショナルかな縦組み用を搭載しています。
源ノフォントの vpal に従って高さと位置を調整したものです。

原ノ味フォント 20210101 から AJ1 「組方向ごとに最適化した全角かな」
を搭載しています。
源ノフォントは、
全角かなには横組み用と縦組み用で別々のグリフが用意されていますが、
AJ1 のような「（通常の）全角かな」と「組方向ごとに最適化した全角かな」
の区別はありません。そこで、源ノの横組み用を
「（通常の）全角かな横組み用」と「組方向ごとに最適化した全角かな横組み用」に、
源ノの縦組み用を
「（通常の）全角かな縦組み用」と「組方向ごとに最適化した全角かな縦組み用」に、
それぞれ割り当てました。

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
* [CMap](https://github.com/adobe-type-tools/cmap-resources)
    + UniJIS2004-UTF32-H
* AJ1-7 の GSUB 情報
    + [
The Adobe-Japan1-7 Character Collection
](https://github.com/adobe-type-tools/Adobe-Japan1)
      から `aj17-gsub-jp04.fea`
      （GSUB ディレクトリにあります）
* AJ1-7 の Variation Selector 情報
    + [
The Adobe-Japan1-7 Character Collection
](https://github.com/adobe-type-tools/Adobe-Japan1)
      から `Adobe-Japan1_sequences.txt`

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
* AG1-5 の Variation Selector 情報
    + [
The Adobe-GB1-5 Character Collection
](https://github.com/adobe-type-tools/Adobe-GB1)
      から `Adobe-GB1_sequences.txt`

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
* AC1-7 の Variation Selector 情報
    + [
The Adobe-CNS1-7 Character Collection
](https://github.com/adobe-type-tools/Adobe-CNS1)
      から `Adobe-CNS1_sequences.txt`

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
* AKR-9 の Variation Selector 情報
    + [
The Adobe-KR-9 Character Collection
](https://github.com/adobe-type-tools/Adobe-KR)
      から `Adobe-KR_sequences.txt`

#### （実験的）生成 (KR)

`make kr` で生成できます。

#### （実験的）ファイル (K1)

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
    + UniKS-UTF32-H
* AK1-2 の GSUB 情報
    + [
AFDKO “features” File Tips & Tricks, Part 2: GSUB Features for Public ROSes
](https://ccjktype.fonts.adobe.com/2012/01/afdko-features-tips-tricks-part-2.html)
      からダウンロードできる `gsub-012012.tar` を解凍して得られる
      `ak12-gsub.txt`

#### （実験的）生成 (K1)

`make k1` で生成できます。

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
原ノ味フォント 20220211 版から CMap file に存在する
Unicode コードポイントを優先するようにしています。

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

しかし、源ノ明朝 2.000 （2021 年 10 月 25 日リリース）では
[
CID がリナンバリングされたようで、この対応表が役に立たなくなりました。
](https://twitter.com/trueroad_jp/status/1454092013293367301)
そのため、原ノ味 20211003 から使用しないようにしました。

#### 縦書き・リガチャなど

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
さらに CID が多対 1 で対応している `ccmp`, `liga` についても
似たような方法で対照表を作ることができ、
これによって
[小書きの「プ」](https://twitter.com/zr_tex8r/status/1303694108465135616)
のような、
[単独の Unicode コードポイントを持たず、
リガチャ置き換えのみでアクセス可能な
CID](https://twitter.com/trueroad_jp/status/1304001557822730241)
についても対照表を作ることができます。
なお、`dlig` でもリガチャ置き換えで対照表を作ることができるのですが、
残念ながら割り当たるグリフの形が微妙に異なる
（AJ1 は枠のあるグリフだが源ノは枠がない）ため使いません。

そして、これらを 1 回やって AI0 CID → AJ1 CID の対応を増やしてから、
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

プロポーショナルかなについては、
機械的変形とは異なった方法で搭載しています。
源ノフォントのかなグリフは全角のものしかありませんが、
GPOS テーブルに palt （プロポーショナルメトリクス）があります。
そこで、全角かなグリフを palt のパラメータに従って幅と位置を調整した上で、
AJ1 GSUB pwid 情報に従ってプロポーショナルかな横組み用のCIDに配置し、
原ノ味フォントの pwid にも追加しています。
これによって[
palt 指定時と pwid 指定時のかな出力が同じになります
](https://twitter.com/zr_tex8r/status/1262022045740625920)
。
同じく源ノ の GPOS には vpal （縦組みプロポーショナルメトリクス）があります。
こちらも vpal のパラメータに従って高さと位置を調整し、
AJ1 GSUB pwid および vert に従ってプロポーショナルかな縦組み用のCIDに配置し、
原ノ味フォントの vert にも追加しています。

また、源ノフォントの全角かなは横組み用と縦組み用に別々のグリフが
用意されている（見た目はほぼ同じですがサイズが微妙に違うようです）ので、
原ノ味フォント 20210101 以降では、
源ノの横組み用を
「（通常の）全角かな横組み用」と「組方向ごとに最適化した全角かな横組み用」に、
源ノの縦組み用を
「（通常の）全角かな縦組み用」と「組方向ごとに最適化した全角かな縦組み用」に、
それぞれ割り当てています。
重複するものはグリフをコピーして同じものを搭載しています。
横組み用は双方すべて重複です。
縦組み用については、
AJ1「（通常の）全角かな縦組み用」は小書き等の一部だけ定義されていて、
その他の多数のグリフは名前に反し「（通常の）全角かな横組み用」を使うため、
重複するものは少なくなっています。
なお、そのため原ノ味で普通に縦書きすると、
小書き等は源ノの縦書き用グリフ、
それ以外の多数のグリフは源ノの横書き用グリフが使われてしまい、
細かいことを言えば食い違ってしまいます
（見た目は同じようですし、
サイズの違いもごくわずかなので違和感はないと思います）。
原ノ味 20210101 以降なら「組方向ごとに最適化した全角かな縦組み用」を使えば、
小書きもそれ以外もすべて源ノの縦書き用グリフが使われるようになる、
ということです。

ルビ用かな、などは抜たままですが、
ここに通常のかなのグリフをそのままコピーして搭載する方法も考えられます。
ただ、本来は別のデザインのグリフが必要なのに、
同じグリフにしてしまうことによるデザイン的な問題が発生するため、
こちらはなかなか難しいです。

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

原ノ味フォント 20200612 から、
AJ1 の CMap と比較して不足しているところを追加、
食い違っているところを修正するようにしました。
これにより `cmap` テーブルに U+FF0D 'FULLWIDTH HYPHEN-MINUS'
が搭載されていない[
問題
](https://github.com/trueroad/HaranoAjiFonts/issues/4)が修正され、
pTeX/upTeX のように CMap を使う場合と、
LuaTeX/XeTeX のように cmap テーブルを使う場合とで、
同じグリフが使えるようになります。
また、KR で入れていた[
Unicode コードポイントで一つだけ抜けているものに .notdef を割り当てる加工
](https://github.com/trueroad/HaranoAjiFonts-generator/commit/3eb47da6025e58d228c9d3f2bef54e87904e8e39)
をやめ、代わりに[
Adobe-KR
](https://github.com/adobe-type-tools/Adobe-KR)
のドキュメントに記載されている format 4 から
CJK Unified Ideographs (U+4E00..U+9FFF) と
CJK Compatibility Ideographs (U+F900..U+FAFF)
のブロックを削除する方法に変更しました。
これは .notdef を割り当てる加工をしていて、
かつ（関係ないはずの） `GPOS` テーブルが存在すると、
なぜか Windows がフォントを認識してくれないことが分かったためです。
OpenType 仕様的には（というか Windows 向けとしては）
format 4 と format 12 の BMP 部分は一致するようにするのが推奨されていますが、
サイズ的に収まらないので仕方がなく
Adobe お勧めの対処法に従った処理を行ったものです。
通常は format 4 ではなく、該当のブロックを含めすべての使用可能な
Unicode コードポイントが搭載されている format 12 が使われるため問題ありません。
また、前バージョンまでは KR のみ format 4
サイズが超過したため対策していましたが、今回は上記 `cmap` 追加に伴い、
TW の HaranoAjiGothicTW でもサイズ超過したため対策しています。
TW の HaranoAjiMinchoTW では超過しなかったため対策していません。

原ノ味フォント 20211103 から、
format 14 の Variation Selector について、
AJ1 などの定義と比較して不足しているところを追加、
食い違っているところを修正するようにしました。
これにより[
源ノ明朝 2.000 で \<U+2E569 U+E0100\> および U+884B が違う文字になる
](https://github.com/adobe-fonts/source-han-serif/issues/126)
現象を継承してしまい原ノ味明朝の \<U+2E569 U+E0100\>
が違う文字になってしまうことを防いでいます。
また、この源ノ明朝のマッピング間違いと原ノ味フォント 20200612 で導入した
cmap テーブルを CMap で修正する機能の結果、U+884B は修正できたので正しいが、
\<U+884B U+E0101\> が U+884B に引きずられて
同じグリフへ間違って変わってしまう現象も防ぐことができます。
原ノ味明朝だけではなく原ノ味角ゴシックでも同様に
\<U+884B U+E0101\> が間違っていたのを修正できています。
また、前バージョンまでは KR と TW の HaranoAjiGothicTW で
format 4 のサイズ超過があったため対策していましたが、
TW の HaranoAjiMinchoTW では超過していなかったため対策していませんでした。
今回は源ノ明朝 2.000 ベースへ切り替えた結果、
グリフ数が増加してサイズ超過してしまったため
HaranoAjiMinchoTW にも同様の対策を入れました。
これにより、format 4 サイズ超過対策をしているのは KR と TW になります。
JP, CN, K1 はサイズ超過しなかったため対策を入れていません。

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

原ノ味フォント 20200524 から、
AJ1, AKR 規格にあるスペースのグリフを一部追加しています (JP, KR)。
これは、AJ1 や AKR に規定のあるスペースのグリフで、
これまで搭載されていなかったグリフを追加したものです。
なお、回転やイタリックなど、
他の関連グリフが存在していないものについては追加していません。
また、プロポーショナルかななどの追加をしています (JP)。
これは、全角かなグリフを palt に従って調整し、
プロポーショナルかなのCIDに配置したものです。

原ノ味フォント 20200612 から、
AJ1 CID+151 を AJ1 CID+14 からのコピーで追加しました (JP)。
源ノフォントでは U+002D 'HYPHEN-MINUS' と U+00AD 'SOFT HYPHEN'
が同じ AI0 CID にマップされているのに対して、AJ1 では別になっており
それぞれ AJ1 CID+14 と AJ1 CID+151 にマップされています。
これまで原ノ味フォントは AJ1 CID+14 のみ搭載していましたが、
源ノでは同じグリフなので AJ1 CID+151 にコピーすることにしました。
これにより U+00AD が使えるようになりました。

原ノ味フォント 20210101/20210102 から、
かなグリフを大幅強化して追加しています (JP)。
AJ1-7
「組方向ごとに最適化した全角かな横組み用」
「組方向ごとに最適化した全角かな縦組み用」
「プロポーショナルかな横組み用」
「プロポーショナルかな縦組み用」
の大部分を搭載しました。以前より
AJ1-7
「（通常の）全角横組み用」
「（通常の）全角縦組み用」
の大部分を搭載していましたので、
全角とプロポーショナルのかなは、これでほとんど揃い、
搭載していないのは、それぞれ小書き「こ」と小書き「コ」だけとなりました。
うち「組方向ごとに最適化した全角かな横組み用」
「組方向ごとに最適化した全角かな縦組み用」は、
源ノの全角かな横組み用と全角かな縦組み用をそれぞれ割り当てたものです
（一部は通常の全角と重複しますが、縦組み用の多くは新規）。
「プロポーショナルかな縦組み用」は vpal を使って
全角グリフを調整して配置したものです。

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

原ノ味フォント 20200524 から、
KR で AKR の横幅が Monospaced になっているものは、
AKR CID+221 （U+AC00、[
akr-hangul.txt
](https://github.com/adobe-type-tools/Adobe-KR/blob/master/akr9-hangul.txt)
の最初に出てくる CID） の横幅に揃えました。
その他、KR で追加したスペースのグリフについて、横幅を
AKR CID+221 の幅や数字グリフの幅を元に設定しています。

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

原ノ味フォント 20211103 から、
ベースとなる源ノ明朝 2.000 には `GDEF` が存在するため、
原ノ味明朝向けにもゴシックと同様の変換をするようにしています。

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

原ノ味フォント 20200524 で、
palt などの `GPOS` が壊れていたものを修正しています。

原ノ味フォント 20200612 で、
KR に搭載していなかった `GPOS` を搭載するようにしました。
これは、`cmap` での format 4 のサイズ制限対策をしていて、
かつ `GPOS` テーブルが存在すると、関係ないはずなのになぜか
Windows がフォントを認識しないということがわかったため、
`cmap` の対策を別の方法に変更したことによるものです。

原ノ味フォント 20210130 で、
vpal など縦組みのかなに対する GPOS を修正しました (JP)。
これまで縦組みのかなでは、小書き文字などは「（通常の）全角かな」縦組み用、
その他は「組方向ごとに最適化した全角かな」縦組み用のグリフに
源ノの GPOS 情報を割り当てていました。
しかし、これだと縦組みのかなで統一的に GPOS feature を使うことができないため、
すべて「組方向ごとに最適化した全角かな」縦組み用のグリフに
割り当てるように変更しました。
そのため、縦組みのかなで vpal などの GPOS feature を使いたいときは
vert, vkna を併用してください。
逆に、横組みのかなでは今のところ「（通常の）全角かな」横組み用のグリフに
源ノの GPOS 情報を割り当てていて、
「組方向ごとに最適化した全角かな」横組み用のグリフには
GPOS 情報がありません（これはこれまでと同じですが変更する可能性はあります）。
そのため、（今のところ）横組みのかなで palt などの GPOS feature を使うときは
hkna を併用しないでください。

#### `GSUB`

`GSUB` 用の変換プログラムで
CID をすべて AI0 CID から AJ1 CID に変換しています。
対照表が作れずに対応が不明な AI0 CID は削除しています。
AJ1 用の GSUB 定義を持ってきているわけではなく、
あくまでも源ノフォントの GSUB を変換しています。
とはいえ、「びゃん」や「たいと」などは AJ1 には無いので対応できません。

原ノ味フォント 20200516 から、chain context の変換に対応しました。
chain context があるのは KR のみです。

原ノ味フォント 20210101/20210102 から、対応を強化しました (JP)。
expt, hojo, trad を追加しました。AJ1-7 の GSUB と同内容です。
pkna, hkna, vkna を追加しました。AJ1-7 の GSUB とほぼ同内容
（欠けているものがあるのでサブセット）です。
vert に「プロポーショナルかな縦組み用」を追加しました。
追加したのは AJ1-7 の GSUB とほぼ同内容
（欠けているものがあるのでサブセット）です。
先に pwid または pkna を適用してから vert を適用することで
「プロポーショナルかな縦組み用」グリフが選択できます
（これは AJ1-7 GSUB と同じです）。
また、OpenType 規格で GSUB feature は Lookup テーブルの順番で
適用することになっており、それにあわせ pwid や pkna が
vert より先にくるようにしています
（これも AJ1-7 GSUB と同じです）。
また、Issue [縦組み 「：」が倒れていない
](https://github.com/trueroad/HaranoAjiFonts/issues/6)
に対応しました。
源ノの vert には複数のテーブルがあり、
そのうちの 1 つだけが vrt2 に入っているため、
vrt2 が vert のサブセットになっていました。
OpenType 規格的にはサブセットではマズいのですが、
vrt2 は単一テーブルでなければならないという制約があること、
vrt2 が無いと一部アプリの縦組みで問題が発生することから、
妥協してわざと規格に反する状態にしているようでした
（詳細はリンク先の Issue や、そこからリンクが張られている源ノの
Issue を参照してください）。
そこで原ノ味では、複数の vert テーブルを 1 つに統合し、
vrt2 が vert と同じ内容になるようにしました。

原ノ味フォント 20210130 で vkna を修正しました (JP)。
 [Adobe-Japan1-7 GSUB
情報の修正](https://github.com/adobe-type-tools/Adobe-Japan1/pull/4)
を取り込み、小書き「ク」などの vkna を修正したものです。

原ノ味フォント 20220220 で vert を修正しました (JP, CN, TW, KR)。
[
グリフが存在するのに GSUB vert が無い
](https://github.com/trueroad/HaranoAjiFontsTW/issues/1)
ことがあったので、JP のみ CID 個別指定で実施していた vert 追加を、
AJ17 などの GSUB を読み込んで反映するよう汎用化して多言語対応しました。

#### `DSIG`

必須テーブルではないため削除しています。
このテーブルを変換する必要はないと思っています。

## 履歴

* [
20230223
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20230223)
(JP, KR)
    + CMap を更新 (JP, KR)
        - [
AJ1-7 に U+31350 が追加された
](https://github.com/trueroad/HaranoAjiFonts/issues/9)
          ので、これを反映しました。
        - AKR も更新されているので反映しました。
        - 収録 CID には変更ありません。
    + バージョンアップ
        + UniJIS2004-UTF32-H 1.022
        + Adobe-Japan1_sequences.txt 2022-09-14
        + UniAKR-UTF32-H 1.003
        + ttx 4.38.0
* [
20220220
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20220220)
(JP, CN, TW, KR, K1)
    + 180 度 270 度（-90 度）回転・コピーによるグリフ追加 (JP)
        + AJ1 CID+12175 (`✂` U+2702 'BLACK SCISSORS')
          180 度回転
          （無回転 CID+12176, 90 度回転 CID+12178 は以前より存在）
        + AJ1 CID+12177 (`✂` U+2702 'BLACK SCISSORS')
          270 (-90) 度回転
          （無回転 CID+12176, 90 度回転 CID+12178 は以前より存在）
        + AJ1 CID+12169 (`〝` U+301D 'REVERSED DOUBLE PRIME QUOTATION MARK')
          無回転
          （組み合わせて使う CID+12170 は以前より存在）
        + AJ1 CID+12171 (`‘` U+2018 'LEFT SINGLE QUOTATION MARK')
          270 (-90) 度回転
        + AJ1 CID+12172 (`’` U+2019 'RIGHT SINGLE QUOTATION MARK')
          270 (-90) 度回転
    + かなに類似するプロポーショナルグリフ追加 (JP)
        + AJ1 CID+15453 (`〃` U+3003 'DITTO MARK') 横組み
        + AJ1 CID+15980 (`〃` U+3003 'DITTO MARK') 縦組み
        + AJ1 CID+15981 (`〆`  U+3006 'IDEOGRAPHIC CLOSING MARK') 縦組み
          （横組み CID+15454 は以前より存在）
    + GSUB による変換テーブル作成を修正 (CN, K1)
        + [
GSUB 紐づけが重複により欠落する問題
](https://github.com/trueroad/HaranoAjiFontsK1/issues/2)
          があったのを修正しました。
        + CN, K1 はこれにより収録 CID が増加しました。
    + GSUB vert 追加の改良 (JP, CN, TW, KR)
        + [
グリフが存在するのに GSUB vert が無い
](https://github.com/trueroad/HaranoAjiFontsTW/issues/1)
      ことがあったので JP のみ CID 個別指定で実施していた vert 追加を、
      汎用化して多言語対応しました。
    + バージョンアップ
        + ttx 4.29.1
    + グリフ数 (JP)
        + 原ノ味明朝：17567
          （変換 16867 ＋グリフ加工 699 ＋ .notdef 1）
        + 原ノ味角ゴシック：17567
          （変換 16866 ＋グリフ加工 700 ＋ .notdef 1）
        + 上記により変換 8 増です。
* [
20220211
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20220211)
(CN, TW, KR, K1)
    + 変換テーブル作成を改良 (CN, TW, KR, K1)
        - [
源ノの cmap テーブルで複数の Unicode コードポイントから同一の AI0 CID
へマッピングされている際に CMap に存在しない方を優先して
グリフが欠けることがある
](https://github.com/trueroad/HaranoAjiFontsK1/issues/1)
          という事象を解決するため、
          CMap に存在する方を優先するよう変更しました。
        - JP は本変更を行っても収録 CID 等が変わらなかったので
          今回はリリースしません。
        - CN, TW, KR, K1 はこれにより収録 CID が増えました。
    + バージョンアップ
        + ttx 4.29.1
* [
20220130
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20220130)
(JP, CN, TW, KR, K1)
    + 源ノ明朝 2.001 に対応 (JP, CN, TW, KR, K1)
        - ベースとなる源ノ明朝を 2.000 から 2.001 に変更しました。
        - JP: [
源ノ明朝 2.000 JP 版で 2 グリフが欠けている問題
](https://github.com/adobe-fonts/source-han-serif/issues/125)
          が修正されたため
          CID+13729
          （U+2EA9 "⺩" / \<U+738B U+E0101\> "王󠄁" --- "王" の異体字）,
          CID+14019
          （\<U+5305 U+E0101\> "包󠄁" --- "包" の異体字）
          が復活し、再び AJ16 全漢字グリフを搭載しています。
        - JP: [
源ノ明朝 2.000 で aj16-kanji.txt が更新されていない問題
](https://github.com/adobe-fonts/source-han-serif/pull/123)
          が修正されたため原ノ味独自の修正をやめました。
        - JP: 原ノ味明朝 20211103 版からですが、
          [
全角ダッシュを並べてもつながらなくなっています
](https://twitter.com/trueroad_jp/status/1460557464349253635)
          。
          源ノ明朝 2.000 で全角ダッシュが単独のグリフを並べても
          つながらないタイプのものになったためです。
          源ノ角ゴシックは以前（少なくとも最初の原ノ味のベースにした
          源ノ角ゴシック 2.000 の頃）からそうだったので
          原ノ味角ゴシックは最初からつながりませんでした。
          源ノフォントはいずれも全角ダッシュを複数並べると
          GSUB で 2 倍角や 3 倍角のダッシュに置き換えるようになったため、
          単独のグリフをつながるタイプにするつもりはないだろうと思っています。
          また、他の AJ1 フォントの全角ダッシュは
          つながるものとつながらないものが混在しているようなので、
          原ノ味フォントではつながらないものとして
          特にグリフの加工はしていません。
    + 原ノ味明朝のグリフ位置修正
        - [
源ノ明朝 2.001 で縦書き用の濁点、半濁点の位置がおかしい問題
](https://github.com/adobe-fonts/source-han-serif/issues/157)
          に起因する位置の問題を修正しました。
        - CID+8271 (GSUB vert/vrt2,
          "゜" U+309C 'KATAKANA-HIRAGANA SEMI-VOICED SOUND MARK'),
          CID+8272 (GSUB vert/vrt2,
          "゛" U+309B 'KATAKANA-HIRAGANA VOICED SOUND MARK')
          を平行移動して位置調整しています。
        - 本件は以前からあったようですが今回発見して修正したものです。
    + バージョンアップ
        + 源ノ明朝 2.001
        + ttx 4.29.0
        + Python 3.9.10
    + グリフ数 (JP)
        + 原ノ味明朝：17559
          （変換 16867 ＋グリフ加工 691 ＋ .notdef 1）
        + 原ノ味角ゴシック：17559
          （変換 16866 ＋グリフ加工 692 ＋ .notdef 1）
        + 上記により原ノ味明朝で変換 2 増です。
        + 明朝とゴシックで収録 CID が同じになりました。
* [
20211103
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20211103)
(JP, CN, TW, KR, K1) 試験的リリース
    + 本バージョンは試験的リリースです
        - 源ノ明朝のメジャーバージョンアップにより大幅な変更があります。
        - JP: CID+13729, CID+14019 が欠けています（詳細は下記参照）。
        - その他にも大幅な変更があるようなので、
          試験的にお使いいただいておかしなところなどをご指摘いただけると
          助かります。
        - CTAN （や TeX Live）へのアップロードはしません。
    + 源ノ明朝 2.000 に対応 (JP, CN, TW, KR, K1)
        - ベースとなる源ノ明朝を 1.001 から 2.000 に変更しました。
        - 全角ダッシュを並べてもつながらなくなりました
          （ゴシックは以前からつながりませんでした）。
        - JP: [
源ノ明朝 2.000 JP 版で 2 グリフが欠けている問題
](https://github.com/adobe-fonts/source-han-serif/issues/125)
          により
          CID+13729
          （U+2EA9 "⺩" / \<U+738B U+E0101\> "王󠄁" --- "王" の異体字）,
          CID+14019
          （\<U+5305 U+E0101\> "包󠄁" --- "包" の異体字）
          が欠けています。
          本件修正は源ノ明朝の次期バーションで修正されるのを待つつもりです。
        - JP: [
源ノ明朝 2.000 で aj16-kanji.txt が更新されていない問題
](https://github.com/adobe-fonts/source-han-serif/pull/123)
          については源ノ明朝の次期バージョンで修正されるのを待たず、
          原ノ味での修正を試みました（[
その 1
](https://github.com/trueroad/HaranoAjiFonts-generator/commit/aac4c985b3dee9ced9670ad04439e1c0cfa35310)
          , [
その 2
](https://github.com/trueroad/HaranoAjiFonts-generator/commit/5f3ba45054b612c82b5a25fee293ac84a4d6badd)
          ）が、不十分である可能性が残っています。
        - JP: [
源ノ明朝 2.000 でマッピングに誤りがある問題
](https://github.com/adobe-fonts/source-han-serif/issues/126)
          については原ノ味で修正しています（[
その 1
](https://github.com/trueroad/HaranoAjiFonts-generator/commit/778f5afbda5adf259088d30459f7e2dd6d873e91)
          , [
その 2
](https://github.com/trueroad/HaranoAjiFonts-generator/commit/eb40dc384ce4d4f42363899ad02e25cda2e159b3)
          ）。
    + 源ノ角ゴシック 2.004 に対応 (JP, CN, TW, KR, K1)
        - ベースとなる源ノ角ゴシックを 2.003 から 2.004 に変更しました。
    + 明朝・ゴシックともに設定ミスで CID+515 （半角ひらがなスペース）を
      搭載していなかったのを[
修正しました
](https://github.com/trueroad/HaranoAjiFonts-generator/commit/f821f1b05ae9768bcdc9b991e5a9790e3bfa7c9c)
      。 (JP)
    + \<U+884B U+E0101\>
      （"衋󠄁" --- "衋" の異体字）で選択される CID
      が誤っているのを修正しました。上記マッピング誤りの修正に関連します。
      (JP)
    + 生成に JIS X 0208 マッピングを[
使用しないようにしました
](https://github.com/trueroad/HaranoAjiFonts-generator/commit/056b398ed30a0be0f5c3948f45dde4c50c2e04d3)
      。 (JP)
    + HaranoAjiSerifTW で `cmap` テーブル format4 がサイズ超過したため[
対策を追加しました
](https://github.com/trueroad/HaranoAjiFonts-generator/commit/5815efc124dc688f628cca62eff6491fe7f914b8)
      。 (TW)
    + バージョンアップ
        + 源ノ明朝 2.000
        + 源ノ角ゴシック 2.004
        + ttx 4.27.1
    + グリフ数 (JP)
        + 原ノ味明朝：17557
          （変換 16865 ＋グリフ加工 691 ＋ .notdef 1）
        + 原ノ味角ゴシック：17559
          （変換 16866 ＋グリフ加工 692 ＋ .notdef 1）
        + 原ノ味フォント 20200524 から 20210410 まで CID+515 ミスの影響で、
          グリフ総数および加工数を 1 つ余計にカウントしていました。
          カウント方法を改良しました。
        + 原ノ味明朝は上記 2 グリフ欠け以外は
          原ノ味ゴシックと同等になりました。
        + 原ノ味角ゴシックは CID+515 搭載により加工 1 増ですが、
          原ノ味角ゴシック 20200524 以降で余計にカウントしていたため
          数字上は増えていません。
* [
20210410
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20210410)
(JP, CN, TW, KR, K1)
    + 源ノ角ゴシック 2.003 に対応 (JP, CN, TW, KR, K1)
        - ベースとなる源ノ角ゴシックを 2.002 から 2.003 に変更しました。
        - 源ノ角ゴシック 2.003 では
          U+4E08 U+E0101（AJ1 CID+13463相当）の
          グリフ（グリフ名uni4E08uE0101-JP）がなくなりました。
          これは U+4E08（丈、AJ1 CID+2510相当）の
          グリフ（グリフ名uni4E08-CN）と統合されたものと思われます。
          これらは源ノ明朝ではヒゲの有無が異なるグリフですが、
          源ノ角ゴシック 2.002 ではどちらもヒゲ無しのよく似たグリフでした。
          そこで、原ノ味角ゴシックでは CID+2510 を CID+13463 へコピーする
          ことにしました。原ノ味明朝ではこれまで通り変更ありません。
    + バージョンアップ
        + 源ノ角ゴシック 2.003
        + ttx 4.22.0
    + グリフ数 (JP)
        + 原ノ味明朝：17554
          （変換 16862 ＋グリフ加工 691 ＋ .notdef 1）
        + 原ノ味角ゴシック：17559
          （変換 16866 ＋グリフ加工 692 ＋ .notdef 1）
        + 上記により原ノ味角ゴシックで変換 1 減、加工 1 増です
* [
20210130
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20210130)
(JP)
    + vpal など縦組みのかなに対する GPOS を修正しました
        - これまで縦組みのかなでは、
          小書き文字などは「（通常の）全角かな」縦組み用、
          その他は「組方向ごとに最適化した全角かな」縦組み用のグリフに
          源ノの GPOS 情報を割り当てていました。
          しかし、これだと縦組みのかなで統一的に GPOS feature
          を使うことができないため、
          すべて「組方向ごとに最適化した全角かな」縦組み用のグリフに
          割り当てるように変更しました。
        - そのため、縦組みのかなで vpal などの GPOS feature を使いたいときは
          vert, vkna を併用してください。
        - 逆に、横組みのかなでは今のところ
          「（通常の）全角かな」横組み用のグリフに
          源ノの GPOS 情報を割り当てていて、
          「組方向ごとに最適化した全角かな」横組み用のグリフには
          GPOS 情報がありません（これはこれまでと同じですが、
          変更する可能性はあります）。
        - そのため、（今のところ）
          横組みのかなで palt などの GPOS feature を使うときは
          hkna を併用しないでください。
    + vkna を修正しました
        - [Adobe-Japan1-7 GSUB
          情報の修正](https://github.com/adobe-type-tools/Adobe-Japan1/pull/4)
          を取り込み、小書き「ク」などの vkna を修正しました。
    + バージョンアップ
        + ttx 4.19.1
        + aj17-gsub-jp04.fea (2021-01-25)
    + グリフ数 (JP)
        + 原ノ味明朝：17554
          （変換 16862 ＋グリフ加工 691 ＋ .notdef 1）
        + 原ノ味角ゴシック：17559
          （変換 16867 ＋グリフ加工 691 ＋ .notdef 1）
        + 20210102 から変更ありません
* [
20210102
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20210102)
(JP)
    + 「プロポーショナルかな縦組み用」GSUB 置き換えを修正
        - Issue [pwid が間違っている？
          ](https://github.com/trueroad/HaranoAjiFonts/issues/7)
          に対応しました。
        - 20210101 版は vert へ追加すべき置き換えを
          誤って pwid へ追加していましたので、修正しました。
        - これにより LuaTeX や XeTeX で動作確認できるようになりました。
    + 「プロポーショナルかな縦組み用」グリフを修正
        - 20210101 版は vpal によるグリフの位置計算が誤っていたため、
          修正しました
    + グリフ数 (JP)
        + 原ノ味明朝：17554
          （変換 16862 ＋グリフ加工 691 ＋ .notdef 1）
        + 原ノ味角ゴシック：17559
          （変換 16867 ＋グリフ加工 691 ＋ .notdef 1）
        + 20210101 から変更ありません
* [
20210101
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20210101)
(JP, CN, TW, KR, K1)
    + 源ノ角ゴシック 2.002 に対応 (JP, CN, TW, KR, K1)
        - ベースとなる源ノ角ゴシックを 2.001 から 2.002 に変更しました。
    + かなグリフを大幅強化 (JP)
        - AJ1-7 「組方向ごとに最適化した全角かな横組み用」グリフの
          大部分となる 211 グリフを搭載しました（非搭載は 2 グリフ）。
          これはすべて通常の全角かな横組み用と同じもので、
          今回新たに搭載したものです。
        - AJ1-7 「組方向ごとに最適化した全角かな縦組み用」グリフの
          大部分となる 211 グリフを搭載しました（非搭載は 2 グリフ）。
          これは、源ノが持っている全角かな縦組み用グリフで、
          これまで原ノ味のグリフに割り当てていなかった 169 グリフ
          を今回新たに割り当てました。
          残り 42 グリフは、
          通常の全角かな縦組み用と同じグリフを今回新たに搭載しました。
        - AJ1-7 「プロポーショナルかな横組み用」グリフの
          大部分となる 213 グリフを搭載しました（非搭載は 2 グリフ）。
          これまで、palt を持つ全角グリフについて palt で幅と横位置を加工して
          プロポーショナルなグリフとして搭載していました。
          また、palt を持たない全角グリフでも、
          同じ CID が別のウェイトで palt を持っていれば、
          全角と同じグリフをプロポーショナルとして搭載していました。
          しかし、全ウェイトで palt を持たない
          全角かな横組み用グリフが 15 あったため、
          これらについても同じグリフを今回新たに搭載しました。
        - AJ1-7 「プロポーショナルかな縦組み用」グリフの
          大部分となる 213 グリフを搭載しました（非搭載は 2 グリフ）。
          これは、横組み用と同様に vpal を持つ全角グリフについて
          vpal で高さと縦位置を加工して
          プロポーショナルなグリフとして今回新たに搭載しました。
          また、vpal を持たない全角グリフについても
          プロポーショナルかな縦組みに紐づけられるものは
          全角と同じグリフをプロポーショナルとして今回新たに搭載しました。
          両方あわせて 213 グリフです。
    + GSUB による OpenType feature 対応を強化 (JP)
        - expt, hojo, trad を追加しました。AJ1-7 の GSUB と同内容です。
        - pkna, hkna, vkna を追加しました。AJ1-7 の GSUB とほぼ同内容
          （欠けているものがあるのでサブセット）です。
        - vert に「プロポーショナルかな縦組み用」を追加しました。
          追加したのは AJ1-7 の GSUB とほぼ同内容
          （欠けているものがあるのでサブセット）です。
          先に pwid または pkna を適用してから vert を適用することで
          「プロポーショナルかな縦組み用」グリフが選択できます
          （これは AJ1-7 GSUB と同じです）。
          また、OpenType 規格で GSUB feature は Lookup テーブルの順番で
          適用することになっており、それにあわせ pwid や pkna が
          vert より先にくるようにしています
          （これも AJ1-7 GSUB と同じです）。
        - Issue [縦組み 「：」が倒れていない
          ](https://github.com/trueroad/HaranoAjiFonts/issues/6)
          に対応しました。
          源ノの vert には複数のテーブルがあり、
          そのうちの 1 つだけが vrt2 に入っているため、
          vrt2 が vert のサブセットになっていました。
          OpenType 規格的にはサブセットではマズいのですが、
          vrt2 は単一テーブルでなければならないという制約があること、
          vrt2 が無いと一部アプリの縦組みで問題が発生することから、
          妥協してわざと規格に反する状態にしているようでした
          （詳細はリンク先の Issue や、そこからリンクが張られている源ノの
          Issue を参照してください）。
          そこで原ノ味では、複数の vert テーブルを 1 つに統合し、
          vrt2 が vert と同じ内容になるようにしました。
    + バージョンアップ
        + 源ノ角ゴシック 2.002
        + ttx 4.18.2
    + グリフ数 (JP)
        + 原ノ味明朝：17554
          （変換 16862 ＋グリフ加工 691 ＋ .notdef 1）
        + 原ノ味角ゴシック：17559
          （変換 16867 ＋グリフ加工 691 ＋ .notdef 1）
        + 上記により、変換 169 グリフ、加工 481 グリフ、
          計 650 グリフ増加しています
* [
20200912
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20200912)
(JP)
    + [
小書きの「プ」
](https://twitter.com/zr_tex8r/status/1303694108465135616)、
半濁点のか行、カ行、「セ」、「ツ」、「ト」のグリフを追加しました
        + 小書きの「プ」は、縦書き用と pwid （加工）も追加しています
        + これは[単独の Unicode コードポイントを持たず、
リガチャ置き換えのみでアクセス可能な
CID](https://twitter.com/trueroad_jp/status/1304001557822730241)
の変換に対応したことによるものです
        + この対応で JP 以外はグリフ変更ありませんでした
    + バージョンアップ
        + ttx 4.14.0
    + グリフ数 (JP)
        + 原ノ味明朝：16904
          （変換 16693 ＋グリフ加工 210 ＋ .notdef 1）
        + 原ノ味角ゴシック：16909
          （変換 16698 ＋グリフ加工 210 ＋ .notdef 1）
        + 上記により、変換 15 グリフ、加工 1 グリフ、
          計 16 グリフ増加しています
* [
20200612
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20200612)
(JP, CN, TW, KR, K1)
    + `cmap` テーブルが AJ1 などの CMap と比較して不足しているところを追加、
      食い違っていたところを修正しました
      (JP, CN, TW, KR, K1)
        + これにより `cmap` テーブルに U+FF0D 'FULLWIDTH HYPHEN-MINUS'
          が搭載されていない[
問題
](https://github.com/trueroad/HaranoAjiFonts/issues/4)が修正されました
        + これまでと同じくグリフを搭載していない（ダミーグリフの）
          CID に紐づく Unicode コードポイントは `cmap` に搭載していません
    + AJ1 CID+151 を AJ1 CID+14 からのコピーで追加しました (JP)
    + `cmap` テーブル format 4 がサイズ制限を超える場合の対策を変更しました
      (TW, KR)
    + `GPOS` テーブルを搭載しました (KR)
    + 生成プログラムの改良をしました
        + 各フォントの生成をシェルスクリプトから make に変更しました
        + ビルドディレクトリ、ログファイル、中間ファイルの名称を変更しました
    + バージョンアップ
        + ttx 4.12.0
    + グリフ数 (JP)
        + 原ノ味明朝：16888
          （変換 16678 ＋グリフ加工 209 ＋ .notdef 1）
        + 原ノ味角ゴシック：16893
          （変換 16683 ＋グリフ加工 209 ＋ .notdef 1）
        + 上記 1 グリフ追加に伴い増加しています
* [
20200524
](https://github.com/trueroad/HaranoAjiFonts-generator/releases/tag/20200524)
(JP, CN, TW, KR, K1)
    + プロポーショナルかなのグリフを追加しました (JP)
    + 一部のスペースグリフを追加しました (JP, KR)
    + palt などの `GPOS` テーブルが壊れていたのを修正しました (JP, CN, TW, KR)
    + **実験的な**韓国語フォントで Monospaced グリフの幅を変更しました (KR)
    + **実験的に**韓国語フォントのバリエーションを追加しました (K1)
    + これまで Adobe-KR 対応でサフィックス KR のフォントがありましたが、
      Adobe-Korea1 対応でサフィックス K1 のフォントを追加しました
        + 韓国語：Adobe-Korea1 対応、サフィックス K1
            + UniKS-UTF32-H 1.008
    + バージョンアップ
        - ttx 4.10.2
    + グリフ数 (JP)
        - 原ノ味明朝：16887
          （変換 16678 ＋グリフ加工 208 ＋ .notdef 1）
        - 原ノ味角ゴシック：16892
          （変換 16683 ＋グリフ加工 208 ＋ .notdef 1）
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

Copyright (C) 2019-2023 Masamichi Hosoda

生成プログラムのライセンスは BSD 2-Clause です。
[LICENSE](./LICENSE)をご覧ください。
生成したフォントは源ノフォントの派生フォントになるため
SIL Open Font License 1.1 です。
