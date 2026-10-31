# Exchange-only quantum control and stabilizer extraction (working research notes)

**Status: numerical working manuscript, not peer reviewed.** This directory was staged in an isolated GitHub branch because the connected account currently exposes only the unrelated `Nuclear-high-spin-VPC` repository. **Please do not merge into the VPC project without intentionally choosing that destination.** A dedicated EO-QEC repository is recommended.

## Contents

- [Paper-style Markdown manuscript](MANUSCRIPT.md) — model, detailed quantitative results, derivations, limitations and source references.
- [Round-by-round research ledger](RESULTS_LEDGER.md) — concise evidence from R138–R154.
- [Reproducibility](REPRODUCIBILITY.md) — metrics, noise conventions, and exact source ZIP verification commands.
- [PDF build instructions](BUILD_PDF.md) — create a local typeset PDF from the Markdown source.

## Principal results

| Research milestone | Supported result |
|---|---|
| 6-spin simultaneous CZ | Exact numerical 30-control / 19-layer CZ: `Hpb=32.0119` versus 37.6681 for the relevant 28-control baseline (15.0% lower). J34 is **not** first-order corrected. |
| Isolated 3-spin dual-static correction | 6 simultaneous layers, 12 positive exchange controls, fourth-order logical infidelity under two independently shot-static gains; **not** protected when transplanted into a two-EO CZ. |
| 9-spin ZZ check | Measurement-specific optimization reduces 50 controls / 29 layers to **48 controls / 27 layers**, wrong-syndrome quadratic curvature 50.1050 to 46.0078. |
| Paired simulated syndrome | With static 1.5%, IID 0.06%, 750 paired samples: wrong-syndrome fraction 0.01103592 to 0.01004484. Model results, not measured device rates. |
| 5-EO weight-4 references | Validated 15-spin star-graph **ZZZZ 92-control** and **XXXX 116-control** coherent measurement references, both composed of CZs and **not realizations on a strict linear nearest-neighbor graph**. |

No QEC threshold, repeated rounds, experimentally calibrated error rate, native non-CZ four-body sequence or universal first-order gain-corrected two-EO entangler is claimed.

The original frozen research archive and a downloadable nine-page PDF are provided separately through the associated ChatGPT conversation; those binary files have not been committed to this draft branch.
