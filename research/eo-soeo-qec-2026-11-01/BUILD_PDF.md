# Build the research paper PDF

Requires Pandoc, XeLaTeX and Noto Serif/Noto Sans fonts.

```bash
pandoc PAPER.md -f markdown+tex_math_dollars+yaml_metadata_block \
  --pdf-engine=xelatex -V geometry:margin=0.8in -V fontsize=10pt \
  -V mainfont='Noto Serif' -V sansfont='Noto Sans' \
  -V colorlinks=true -V linkcolor=blue -V urlcolor=blue \
  --number-sections -o PAPER.pdf
```

A PDF rendered for the 1 November 2026 working draft is included in the local downloadable ZIP. GitHub users can regenerate it from `PAPER.md`.
