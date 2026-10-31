# Build the PDF

The paper source is [PAPER.md](PAPER.md). A branch-specific GitHub Actions workflow renders the paper and commits the resulting `PAPER.pdf` when permissions allow.

To generate locally on Linux with Pandoc, XeLaTeX and `rsvg-convert` installed:

```sh
pandoc PAPER.md -o PAPER.pdf --pdf-engine=xelatex --resource-path=. -V geometry:margin=0.85in -V fontsize=10pt -V mainfont="DejaVu Serif"
```

The original seven-page PDF assembled during research remains available as an independent ChatGPT downloadable artifact. The GitHub CI rendering may have different pagination. All numerical outcomes are preliminary and model-limited; see [EVIDENCE_LEDGER.md](EVIDENCE_LEDGER.md).
