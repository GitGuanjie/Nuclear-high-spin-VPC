# Nuclear High-Spin Virtual Phase Control

Open-source numerical code supporting the manuscript

**“Generating Spin-Squeezed States in High-Spin Nuclear Systems via Optimized Virtual Phase Control”**

by **Guanjie He** and **Peihao Huang**.

This repository contains numerical implementations of virtual phase control (VPC) for generating spin-squeezed states in single high-spin nuclear systems with

\[
I=\frac{3}{2},\quad \frac{5}{2},\quad \frac{7}{2}.
\]

The main reproducible implementation is provided in **Python** using NumPy and SciPy. The original Wolfram Mathematica notebooks used during the development of the project are retained separately for transparency and cross-validation.

The numerical results in the Python implementation are generated directly by the Python code and are **not imported from saved Mathematica notebook outputs**.

---

## Repository structure

```text
Nuclear-high-spin-VPC/
│
├── README.md
│
├── python/
│   ├── requirements.txt
│   ├── TACT python_reproduction.ipynb
│   ├── PYTHON_MIGRATION_NOTES.md
│   ├── vpc/
│   │   ├── __init__.py
│   │   ├── core.py
│   │   └── presets.py
│   ├── scripts/
│   │   ├── validate_core.py
│   │   ├── key_results.py
│   │   ├── search_vpc.py
│   │   ├── search_selected_phases.py
│   │   ├── find_multiple_solutions.py
│   │   ├── density_profile.py
│   │   ├── reproduce_fig2.py
│   │   ├── reproduce_fig3.py
│   │   ├── reproduce_fig6_7.py
│   │   ├── reproduce_fig12.py
│   │   ├── reproduce_fig12_envelope.py
│   │   ├── reproduce_fig13.py
│   │   └── reproduce_all.py
│   └── results/
│       ├── numerical data
│       ├── generated figures
│       ├── optimized phases
│       └── validation files
│
└── mathematica/
    ├── README.md
    └── original Mathematica notebooks
```

The `python/` directory is the recommended entry point for reproducing the numerical results.

The `mathematica/` directory contains the original research notebooks and is not required to run the Python implementation.

---

## Python requirements

Python 3.10 or later is recommended.

The required packages are:

```text
numpy >= 1.24
scipy >= 1.10
matplotlib >= 3.7
pandas >= 2.0
jupyter >= 1.0
```

Install them with

```bash
cd python
pip install -r requirements.txt
```

---

## Quick start

After installing the dependencies, run

```bash
cd python
python scripts/validate_core.py
```

to perform basic numerical consistency checks.

A laptop-friendly reproduction of the main calculations can then be launched with

```bash
python scripts/reproduce_all.py
```

The generated numerical data and figures are written to

```text
python/results/
```

The default `reproduce_all.py` settings are intentionally lightweight. More extensive random-start optimization can be performed with the individual scripts described below.

---

## Physical model

The VPC calculations are performed in the generalized rotating frame for a single spin-\(I\) nucleus.

The phase-controlled Hamiltonian has the transition-chain form implemented in

```text
python/vpc/core.py
```

and the numerical workflow includes:

- spin-\(I\) angular-momentum matrices,
- spin-coherent states,
- phase-dependent VPC Hamiltonians,
- unitary time evolution,
- Kitagawa–Ueda squeezing,
- Wineland squeezing,
- OAT and TACT reference dynamics,
- VPC phase optimization,
- Lindblad decoherence,
- post-preparation \(I_x\) and \(I_y\) rotations,
- state fidelity calculations.

The Python implementation is an independent implementation of the same physical model and optimization objectives used in the original Mathematica calculations.

---

## Corrected TACT benchmark

For

\[
H_{\mathrm{TACT}}
=
\chi\left(I_x^2-I_y^2\right),
\]

the corrected high-efficiency initial state used in the revised comparison is the polar coherent spin state

\[
|CSS_z\rangle=|I,I\rangle.
\]

The previous equatorial TACT result is retained in several plots for comparison, but all revised TACT benchmarks include the corrected \(CSS_z\) initial state.

The Python implementation independently gives the following first minima of the Kitagawa–Ueda squeezing parameter:

| Spin \(I\) | \(t_{\min}\) | \(\xi_{\mathrm{S,min}}^2\) |
| ---: | ---: | ---: |
| \(3/2\) | 0.3022998940 | 0.3333333333 |
| \(5/2\) | 0.2285606357 | 0.2280943573 |
| \(7/2\) | 0.1818400043 | 0.1800911330 |

These values are obtained directly from the Python TACT Hamiltonian initialized in \(CSS_z\).

The corrected comparison reveals a **speed–depth tradeoff** rather than a universal advantage of either protocol:

- for \(I=3/2\), TACT and optimized VPC reach essentially the same squeezing depth, while TACT reaches it earlier;
- for \(I=5/2\) and \(I=7/2\), TACT reaches its optimum earlier, while optimized VPC can reach a lower squeezing parameter at longer evolution times.

Representative independently optimized Python results are stored in

```text
python/results/key_results_python.csv
```

and

```text
python/results/key_results_python.json
```

---

## Squeezing measures

### Kitagawa–Ueda squeezing

The main squeezing quantity is

\[
\xi_{\mathrm S}^{2}
=
\frac{2}{I}
\left(\Delta I_{\mathbf n_\perp}^{2}\right)_{\min}.
\]

For a single spin-\(I\) system, this quantity characterizes the reduction and anisotropy of transverse quantum fluctuations within the spin manifold.

### Wineland squeezing

The Python implementation also evaluates

\[
\xi_{\mathrm R}^{2}
=
\frac{
2I\left(\Delta I_{\mathbf n_\perp}^{2}\right)_{\min}
}{
|\langle\mathbf I\rangle|^2
}.
\]

Unlike the Kitagawa–Ueda parameter alone, the Wineland parameter also accounts for the remaining mean-spin contrast.

For \(I=5/2\) and \(I=7/2\), the phases optimized for \(\xi_{\mathrm S}^{2}\) are not generally identical to those optimized for \(\xi_{\mathrm R}^{2}\). The Python implementation therefore supports direct re-optimization using either squeezing measure as the cost function.

---

## Reproducing individual results

Run the following commands from inside the `python/` directory.

### Core numerical validation

```bash
python scripts/validate_core.py
```

This checks, among other things, the equivalence between direct VPC Hamiltonian propagation and the accelerated phase-gauge implementation.

---

### Key corrected numerical results

```bash
python scripts/key_results.py
```

This reproduces representative corrected TACT and optimized VPC results for both Kitagawa–Ueda and Wineland squeezing.

Outputs:

```text
results/key_results_python.csv
results/key_results_python.json
```

---

### VPC phase optimization

```bash
python scripts/search_vpc.py
```

Additional searches for selected phase configurations and multiple local solutions are available through

```bash
python scripts/search_selected_phases.py
python scripts/find_multiple_solutions.py
```

---

### Fig. 2 — VPC, OAT, and corrected TACT comparison

```bash
python scripts/reproduce_fig2.py
```

The calculation includes:

- optimized VPC,
- OAT with the equatorial coherent spin state,
- TACT with the equatorial initial state for reference,
- corrected TACT with \(CSS_z\).

Generated files include

```text
results/Fig2a_python.png
results/Fig2b_python.png
results/Fig2c_python.png
results/Fig2_I*_python.csv
```

The VPC optimization uses random initial phase configurations. The number of random starts can be increased, for example,

```bash
python scripts/reproduce_fig2.py --spin 2.5 --points 35 --starts 200
```

For high-statistics searches, `--starts` can be increased further. Runs with thousands of initial conditions may require substantial computation time.

---

### Fig. 3 — initial-state dependence

```bash
python scripts/reproduce_fig3.py
```

This calculates the dependence of optimized VPC squeezing on the initial coherent-spin-state orientation.

---

### Density profiles

```bash
python scripts/density_profile.py
```

This reproduces representative phase-space squeezing landscapes corresponding to the density/profile calculations performed in the original Mathematica notebooks.

---

### Figs. 6 and 7 — decoherence and post-preparation rotations

```bash
python scripts/reproduce_fig6_7.py
```

These calculations include:

- VPC squeezing followed by \(I_x\) or \(I_y\) rotation,
- OAT,
- corrected \(CSS_z\)-TACT,
- representative linear decoherence channels,
- quadratic \(I_z^2\) decoherence.

The noise is active from \(t=0\) in the noisy simulations.

The results demonstrate that the relative performance of VPC and TACT depends on spin value, evolution time, and noise channel. The VPC-plus-rotation protocol can maintain a low squeezing parameter over a broader post-preparation time window under the conditions investigated.

---

### Fig. 12 — Wineland squeezing

```bash
python scripts/reproduce_fig12.py
```

This evaluates the time-dependent Wineland squeezing parameter for:

- OAT,
- TACT with the original equatorial initial state,
- corrected TACT with \(CSS_z\),
- VPC,
- VPC followed by \(I_x\) or \(I_y\) rotation,
- representative decoherence channels.

To independently optimize the VPC phases for the Wineland parameter over time, run

```bash
python scripts/reproduce_fig12_envelope.py
```

Generated results include

```text
results/Fig12a_python.png
results/Fig12b_python.png
results/Fig12c_python.png
results/Fig12_envelope_*
```

---

### Fig. 13 — squeezed-state and spin-cat-state fidelity

```bash
python scripts/reproduce_fig13.py
```

This reproduces the fidelity comparison between VPC-generated spin-squeezed states and the corresponding \(z\)-oriented spin-cat states under the considered linear and quadratic decoherence channels.

---

## Optimization settings and reproducibility

The VPC optimization is nonconvex and can contain multiple local optima, particularly for \(I=5/2\) and \(I=7/2\).

The scripts therefore support multiple random initial phase vectors.

For rapid inspection, the default scripts use relatively small random-start ensembles.

For higher-statistics calculations, increase the number of starts using the relevant command-line option, for example

```bash
python scripts/reproduce_fig2.py --starts 2000
```

where applicable.

Random seeds are explicitly specified in the Python scripts so that individual runs can be reproduced.

Because different numerical optimizers or random-start ensembles can converge to different local phase solutions, individual optimized phase vectors need not be identical even when they produce the same or nearly the same squeezing value.

---

## Exact acceleration of VPC propagation

For the open transition-chain Hamiltonian used here, the phase-controlled VPC Hamiltonian can be written as

\[
H_{\mathrm{VPC}}(\boldsymbol{\phi})
=
D I_x D^\dagger,
\]

where \(D\) is a diagonal phase matrix.

Therefore,

\[
e^{-iH_{\mathrm{VPC}}t}
=
D e^{-iI_xt}D^\dagger.
\]

The Python optimizer uses this identity to avoid evaluating a new full matrix exponential at every phase-optimization step.

This is an exact algebraic transformation, not an approximation.

The implementation is checked against direct matrix exponentiation in

```text
scripts/validate_core.py
```

with numerical differences at approximately floating-point precision.

---

## Time and coupling normalization

The comparisons in the manuscript use the nominal dimensionless normalization

\[
\frac{\gamma B_1}{2I}=1
\]

for VPC and

\[
\chi=1
\]

for OAT and TACT.

This normalization provides a common dimensionless scale for comparing the resulting dynamics. It should not be interpreted as implying identical experimental drive power, operator norm, or hardware resource cost for the different protocols.

---

## Validation

The Python implementation was executed independently of the Mathematica kernel.

Saved Mathematica notebook output cells were not used as numerical input for the Python-generated results.

Validation information is available in

```text
python/results/VALIDATION_REPORT.md
python/results/validation_summary.json
python/results/python_environment.json
python/results/python_generation_log.txt
```

The validation includes:

- coherent-spin-state normalization,
- direct versus accelerated VPC propagation,
- corrected \(CSS_z\)-TACT minima,
- representative optimized VPC minima,
- Kitagawa–Ueda squeezing,
- Wineland squeezing,
- Lindblad-based decoherence calculations.

---

## Python / Mathematica correspondence

| Calculation | Python implementation | Original Mathematica implementation |
| --- | --- | --- |
| VPC phase search | `python/scripts/search_vpc.py` | `mathematica/VPC Sequence search *.nb` |
| Phase landscapes | `python/scripts/density_profile.py` | `mathematica/density plot profile *.nb` |
| Fig. 2 / noiseless comparison | `python/scripts/reproduce_fig2.py` | `mathematica/no decoherence and linear plot.nb` |
| Figs. 6–7 / noise calculations | `python/scripts/reproduce_fig6_7.py` | `mathematica/no decoherence and linear plot.nb` |
| TACT / Wineland calculations | `python/scripts/reproduce_fig12.py` | `mathematica/TACT and Wineland plot.nb` |
| Spin-cat fidelity | `python/scripts/reproduce_fig13.py` | `mathematica/Squeeze and Cat state compare Fidelity.nb` |

The Mathematica notebooks are retained to document the original development workflow. The Python implementation is intended to provide an accessible open-source reproduction that does not require Wolfram Mathematica.

---

## Jupyter notebook

A compact interactive reproduction of the corrected TACT benchmark is available in

```text
python/TACT python_reproduction.ipynb
```

This notebook can be opened with

```bash
cd python
jupyter notebook
```

and then selecting `TACT python_reproduction.ipynb`.

---

## Generated data

The `python/results/` directory contains the numerical outputs generated by the Python implementation, including:

- CSV numerical data,
- optimized VPC phase arrays,
- PNG figures,
- validation summaries,
- Python environment information,
- generation logs.

The generated files are provided to facilitate direct comparison and independent verification.

---

## Original Mathematica notebooks

The original Wolfram Mathematica notebooks are retained under

```text
mathematica/
```

They include the original phase searches, density plots, squeezing calculations, noise simulations, TACT/Wineland comparisons, and squeezed-state/spin-cat-state fidelity calculations.

Mathematica is **not required** to reproduce the main results using the Python implementation.

---

## Citation

If you use this code or the associated data, please cite the corresponding manuscript:

> Guanjie He and Peihao Huang,  
> *Generating Spin-Squeezed States in High-Spin Nuclear Systems via Optimized Virtual Phase Control.*

Bibliographic information will be updated after publication.

---

## Contact

For questions about the code or numerical implementation, please contact the authors through the corresponding contact information provided in the manuscript.