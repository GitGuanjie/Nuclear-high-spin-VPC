# Generate the paper-style PDF

The GitHub version of `MANUSCRIPT.md` omits embedded figures that are supplied in the separate PDF/data archive. It is otherwise self-contained.

On Linux with Pandoc and XeLaTeX installed:

```bash
pandoc MANUSCRIPT.md \
  -f markdown+tex_math_dollars+pipe_tables+link_attributes \
  -o EO_Exchange_QEC_Working_Paper.pdf \
  --pdf-engine=xelatex \
  --toc --toc-depth=2 --number-sections \
  -V papersize=letter \
  -V mainfont='Noto Serif' \
  -V sansfont='Noto Sans' \
  -V monofont='DejaVu Sans Mono'
```

The original typeset nine-page PDF **including figures**, source code, full-precision control CSVs, and frozen research archives are available in the associated conversation download package. The Markdown alone is not a standalone source-code reproduction of the numerical optimizers.
