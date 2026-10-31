# EO/SOEO exchange-only robust control — reproducible working report

**Status:** independent technical working draft (1 November 2026). **Not peer reviewed, not a hardware demonstration, not an established novelty claim, and not an all-bond-robust CZ or fault-tolerant QEC result.**

This folder consolidates an exchange-only spin-qubit control investigation covering (i) gauge-safe positive-exchange composite local Clifford gates; (ii) four-spin spin-sector revival and singlet-probe error detection; (iii) a native 43P-to-41P exact six-spin encoded controlled-reflection rewrite; and (iv) restricted physical interface obstructions for EO–EO, EO–SOEO, and SOEO–SOEO.

**Read:** [Technical paper (Markdown)](PAPER.md). The corresponding seven-page typeset PDF is `PAPER.pdf` in the accompanying downloadable research package. The PDF is generated from this same Markdown; it is not currently part of the GitHub commit.

**Reproduce (Python 3 + NumPy; SciPy for mixed-bridge checks):**

```bash
OPENBLAS_NUM_THREADS=1 python code/verify_all_physical.py
OPENBLAS_NUM_THREADS=1 python code/replay_benchmark.py
OPENBLAS_NUM_THREADS=1 python code/permutation_independent.py
OPENBLAS_NUM_THREADS=1 python code/cz43_audit.py sequences/CZ_41P_REWRITE.csv
OPENBLAS_NUM_THREADS=1 python code/single_bridge_no_go.py
```

All pulse CSV files use `X_ij(a) = exp(i*pi*a*P_singlet_ij)`, strictly positive pulse areas, chronological order. EO uses J12/J23 for the local Clifford family; SOEO maps those axes to J12/J13. The 41P file implements a **locally rotated CZ reflection**, not literal computational-basis CZ. No file in this folder claims all-bond first-order cancellation for an encoded two-qubit entangler.

Data limitations: noise ratios depend on a *model* with bond-static fractional gain 0.015 and pulse IID fractional jitter 0.0006. Idle, analog settling, magnetic gradients, readout/reset and full QEC decoding were not included. The physical meaning of H_pb-style coefficients depends on normalization; do not mix raw numbers from unrelated archives.

The included verification scripts and source ZIPs in the downloadable research bundle retain provenance. Additional source optimization scripts can refer to the original working-directory paths and are not asserted to be self-contained.
