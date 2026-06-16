# IPSJ 論文誌ジャーナル 投稿用 LaTeX テンプレート（和文・submit）

情報処理学会論文誌ジャーナルへの投稿用 LaTeX テンプレート一式です。
Overleaf でそのまま利用できます。

## ファイル構成

| ファイル | 役割 |
|----------|------|
| `main.tex` | 本文（投稿版・1段組） |
| `references.bib` | 参考文献データベース（BibTeX） |
| `latexmkrc` | uplatex + dvipdfmx でのビルド設定 |
| `ipsj.cls` | **要ダウンロード**（学会配布のクラスファイル） |
| `ipsjsort.bst` | **要ダウンロード**（参考文献スタイル） |

## セットアップ手順（Overleaf）

1. 情報処理学会の「LaTeX スタイルファイル」配布ページから
   `ipsj.cls` と `ipsjsort.bst` を入手し、このフォルダにアップロードする。
   - 参考: https://www.ipsj.or.jp/journal/submit/style.html
2. Overleaf の `Menu > Settings` で次を設定する。
   - **Compiler**: `LaTeX`
   - **TeX Live version**: 最新
   - **Main document**: `main.tex`
3. コンパイルすると、`latexmkrc` により
   `uplatex → upbibtex → uplatex(×2) → dvipdfmx` の順で PDF が生成される。

## 注意

- 投稿版は `\documentclass[submit,techrep]{ipsj}` のように `submit` を付ける。
  採録後のカメラレディ版では `submit` を外す（自動で2段組になる）。
- 日本語組版のため、コンパイラは必ず **uplatex（または platex）+ dvipdfmx** を使う。
  pdfLaTeX / XeLaTeX / LuaLaTeX では `ipsj.cls` はコンパイルできない。
- 体裁（用紙サイズ・余白・段組・フォントサイズ・行間など）は `ipsj.cls` が
  規定するため、本文側で指定する必要はない。
