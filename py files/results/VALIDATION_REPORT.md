# Python conversion validation report

The Python implementation was executed independently of the Mathematica kernel. Saved Mathematica output cells were not loaded as numerical input.

## Core equivalence check

For random phase vectors, direct propagation with the Python `H_VPC` matrix and the exact diagonal-gauge accelerated propagation agree to approximately `1e-16` for `I=3/2, 5/2, 7/2`. See `validation_summary.json`.

A coherent spin state returns `xi_S^2 = xi_R^2 = 1` to floating-point precision.

## Corrected TACT(CSS_z) benchmark required by Reviewer 2

| I | first minimum time | minimum KU squeezing |
|---:|---:|---:|
| 3/2 | 0.3022998940 | 0.3333333333 |
| 5/2 | 0.2285606357 | 0.2280943573 |
| 7/2 | 0.1818400043 | 0.1800911330 |

These values are produced by the Python TACT Hamiltonian `Ix@Ix - Iy@Iy` initialized in `|I,I>`.

## Python VPC speed-depth check

Independent Python phase optimization gives the following representative longer-time KU results (see `key_results_python.csv`):

| I | corrected TACT min | VPC representative deeper value | interpretation |
|---:|---:|---:|---|
| 3/2 | 0.3333333 | 0.3333333 | same depth; TACT earlier |
| 5/2 | 0.2280944 | 0.2000005 | VPC deeper at longer time |
| 7/2 | 0.1800911 | 0.1430688 | VPC deeper at longer time |

This supports the revised **speed vs attainable-depth tradeoff** rather than a universal VPC-over-TACT claim.

## Wineland check

The Python implementation separately optimizes the Wineland cost. Representative long-time values are lower than the corrected TACT(CSS_z) Wineland minima for `I=5/2` and `I=7/2`; the numerical values are in `key_results_python.csv` and the time-resolved Python outputs are in `Fig12_envelope_*`.

## Noise / rotation calculations

`Fig6_*_python.csv`, `Fig7_*_python.csv` and `Fig12_*_python.csv` are produced by an explicit Lindblad superoperator. The noisy TACT curves use the corrected `CSS_z` initial state, and the noise is active from `t=0`. The VPC curves switch from the squeezing Hamiltonian to `Ix` or `Iy` at the selected `t1`.
