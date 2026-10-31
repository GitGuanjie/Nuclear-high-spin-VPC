# Reproducibility, gauge conventions, and audit checklist

## Inputs and environment

This package is a synthesis; it does not rewrite the optimizers. Original full-precision sequences, run logs, source code and numerical evidence are maintained in the frozen ZIPs under `source_archives/` and in the optional `EO_Exchange_QEC_All_Rounds_Archive.zip` companion.

Recommended environment: Python 3.10+ with `numpy` and `scipy` (and `matplotlib` for plotting), running with `OPENBLAS_NUM_THREADS=1` and `OMP_NUM_THREADS=1`. Some heavier 15-spin programs process basis columns in batches: use a machine with sufficient RAM and confirm archived script flags before changing parameters.

## Independent verification commands

Extract *one* source ZIP to its own empty directory; change into the extracted round root before running:

```bash
# R143: exact six-spin CZ, nine-spin translation, noise derivatives
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python code/verify_r143.py
python code/error_anatomy.py
python code/mc143.py 1000

# R146: isolated three-spin gain correction and failed six-spin embedding
OPENBLAS_NUM_THREADS=1 python code/verify_and_mc.py
python code/verify_64_512.py
python code/context_stress.py

# R154: 48-control nine-spin instrument and 15-spin star stabilizers
OPENBLAS_NUM_THREADS=1 python code/smoke_test.py
OPENBLAS_NUM_THREADS=1 python code/variant_screen.py
OPENBLAS_NUM_THREADS=1 python code/paired_mc.py
OPENBLAS_NUM_THREADS=1 python code/star4.py
OPENBLAS_NUM_THREADS=1 python code/star4xx.py
```

**Caution:** these command blocks refer to **different extracted folders**; do not run all commands from one project root. Full Monte Carlo reproduction is more expensive than baseline analytic checks. For the exact archived flags and expected results, consult each round's own `README.md` and `REPORT_EN.md`. This synthesis has validated its extracted textual metrics against those reports, but has *not* independently rerun every historical search in the current packaging step.

## Metric conventions

- `control`: one nonzero physical exchange amplitude $a_{\ell b}$, even when combined with another amplitude in a simultaneous layer.
- `simultaneous layer`: the exponential of the **sum** of active exchange projectors. Factorization into serial terms is invalid for overlapping bonds.
- `ASAP depth`: idealized scheduling of layers with resource conflicts and equal unit durations. This is **not** experimental pulse time.
- `Hpb`: sum of second-order *gauge-subtracted* per-physical-bond static-gain coefficients for the encoded gate. It includes harmful logical and leakage components.
- `H34`: contribution of a **single physical bond** (J34), not total error and not always the measurement-dominant bond.
- `Hiid`: sum of independent-control perturbative sensitivity coefficients; not a noise rate.
- `instrument loss`: outcome-resolved Kraus overlap metric of a complete measurement.
- `wrong syndrome`: conditional measurement bit error averaged over specified logical/gauge inputs. It is *not* necessarily equal to instrument loss or leakage.
- `leakage`: final probability outside all declared EO $S=1/2$ triple code subspaces; physical singlet–triplet readout alone does not necessarily flag it.

## Required checks before reusing sequences

1. Confirm the triples and encoded basis order, the temporal order convention, which pair defines the singlet, and whether gauge phases are fixed or allowed.
2. For a *gate*, verify the full encoded target on every logical×gauge column and the orthogonal leakage block; do not verify only the logical $4\times4$ block.
3. For a *measurement*, compare the two complete outcome-conditioned Kraus maps up to allowable outcome phases and gauge-only action. Test superpositions **within** parity sectors.
4. For static noise, draw each physical bond's gain **once per shot**; do not redraw it for every pulse. Independently sample the per-control IID term. Preserve the declared covariance model for coactivation context errors.
5. Keep the physical graph fixed. In particular, the five-EO four-body baseline relies on a star-shaped graph not present in a strict linear six-spin test chain.
6. Record controls, ASAP depth, total exchange area, and any actual amplitude-dependent time model separately.
7. Report negative results as bounded by the exact tested family or finite optimizer campaign, not as universal impossibility theorems.

## Representative full-precision sequences

- `selected_sequences/CZ30C_R143_STATIC_OPT.csv`: exact CZ with lower total quasi-static per-bond curvature, original source R143 archive.
- `selected_sequences/THREE_SPIN_6L_DUAL_GAIN.csv`: three-spin 6-layer isolated two-axis static-gain-corrected SWAP; **not** a corrected two-EO CZ.
- `selected_sequences/ZZ_48C_P1R0.csv`: nine-spin exact syndrome extraction with optimized ancilla preparation branch.

Their companion code and original internal evidence remain in the respective frozen source archives.

## Integrity

`SOURCE_MANIFEST.csv` includes names, sizes and SHA-256 digests for the paper, Markdown, selected full-precision sequences and source ZIPs. To compare values after transfer:

```bash
python - <<'PY'
import csv, hashlib, pathlib
root=pathlib.Path('.')
for row in csv.DictReader((root/'SOURCE_MANIFEST.csv').open()):
    if not (root/row['relative_path']).exists():
        print('MISSING',row['relative_path']); continue
    h=hashlib.sha256((root/row['relative_path']).read_bytes()).hexdigest()
    print('OK' if h == row['sha256'] else 'FAIL',row['relative_path'])
PY
```

PDF/Markdown manuscript figures are generated or copied from the authors' R143/R146/R154 archives, not from external journal PDFs.