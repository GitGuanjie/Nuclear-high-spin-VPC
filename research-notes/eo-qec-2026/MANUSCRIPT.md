---
title: "Exchange-Only Quantum Control and Stabilizer Extraction: A Verified Numerical Research Synthesis"
subtitle: "From simultaneous-exchange noise shaping to coherent multi-EO parity measurements"
date: "1 November 2026"
author: "Working research manuscript — authorship and publication status to be confirmed"
abstract: |
  We synthesize a sequence of computational investigations into exchange-only (EO) spin-qubit control, quasi-static per-physical-bond exchange-gain errors, simultaneous noncommuting exchange pulses, and stabilizer-syndrome extraction. The six-spin gate study demonstrates an exact 30-control, 19-layer encoded CZ with a total quadratic static-gain sensitivity of 32.0119, compared with 37.6681 for a relevant 28-control baseline, while isolated bridge-gain cancellation remains unresolved. A separate six-layer three-spin construction suppresses two independent shot-static exchange-gain channels to fourth order in logical infidelity, but its protection does not carry over to a two-EO encoded entangler because of leakage and non-gauge sector phases. At the measurement level, exact nine-spin parity instruments are constructed from physical exchange-only controls. Exploiting the known ancilla state and the final singlet–triplet measurement reduces the coherent ZZ check from 50 to 48 active controls and 29 to 27 nominal ASAP layers; an alternate ancilla-preparation branch further reduces wrong-syndrome curvature by 8.18%. Under a specified model with 1.5% shot-static bond gains and 0.06% independent control jitter, 750 paired simulations estimate a 9.0% relative reduction in wrong-syndrome probability. Finally, explicit 15-spin state-vector checks establish CZ-factorized, coherence-preserving ZZZZ and XXXX measurement baselines requiring 92 and 116 controls, respectively, on an assumed star-shaped exchange graph. These results are numerical and model-conditional: they do not demonstrate a native non-CZ-factorized four-body primitive, repeated error correction, a logical error threshold, or experimental gate performance.
keywords: [exchange-only qubits, simultaneous exchange, quasi-static noise, leakage, dynamical correction, stabilizer measurement, quantum error correction]
geometry: margin=0.86in
fontsize: 10pt
colorlinks: true
linkcolor: NavyBlue
urlcolor: NavyBlue
header-includes:
- \usepackage{microtype}
- \usepackage{booktabs}
- \usepackage{float}
- \usepackage{placeins}
- \setlength{\emergencystretch}{3em}
---

# Scope and evidence standard

This paper is a **working synthesis of independently packaged numerical research rounds R138–R154**, not a claim of newly completed hardware experiments or an accepted publication. It reorganizes the evidence into a single scientific narrative, and deliberately retains negative results. The included archives contain the original optimized angles, physical exchange schedules, numerical certificates, simulation code, and model assumptions. Numerical endpoints reported as "exact" mean residuals at approximately $10^{-11}$ or better in the specified floating-point physical representations, not symbolic proofs of the angles.

The guiding question is whether *simultaneous exchange* offers a physically efficient path from isolated, noise-shaped EO entanglers to encoded stabilizer measurements with acceptable syndrome error, leakage, and duration. Three distinctions are essential: physical vs. encoded correction, gate vs. measurement-instrument equivalence, and conditional numerical fidelity vs. hardware error rates.

# Exchange-only encoding and physical controls

Each logical EO qubit is carried by three spin-$1/2$ particles. In the total-spin $S=1/2$ manifold, the state of a chosen pair (singlet or triplet) represents a logical degree of freedom, while $S_z=\pm 1/2$ gives a gauge degree of freedom; the $S=3/2$ quartet is leakage. For two triples there are $4\times4=16$ encoded logical--gauge input states within the full six-spin dimension $2^6=64$.

Writing the physical singlet projector on spins $i,j$ as

$$
P_{ij}^{(s)}=\tfrac12(I-\mathrm{SWAP}_{ij}),
$$

our dimensionless positive exchange convention is

$$
X_{ij}(a)=\exp(i\pi a P_{ij}^{(s)}),\qquad 0.15\leq a<2
$$

for active controls in the reported searches. Unlike a sequential pulse decomposition, a simultaneous layer on overlapping bonds must be evaluated with **one matrix exponential**:

$$
U_\ell=\exp\!\left(i\pi\sum_{b\in\mathcal B_\ell}
 a_{\ell b}P_b^{(s)}\right),\quad U=U_L\cdots U_1.
$$

Nonoverlapping exchanges commute; overlapping exchanges usually do not. Every target must be checked on all encoded gauge states, not on a selected logical basis state alone.

If $E$ is the $64\times16$ code isometry, an exact encoded CZ with fixed gauge has $UE=E(CZ\otimes I_g)$, with vanishing component in the orthogonal leakage space. For measurement protocols we also admit a consistent gauge-only transformation and record-dependent overall phase when the **resulting quantum instrument**, not the full unmeasured unitary, is unchanged.

# Noise model and acceptance metrics

The main model samples a fractional static gain $\delta_b$ **once per physical bond per shot** and reuses that value at every occurrence of the bond. A distinct independent fluctuation $\eta_{\ell b}$ perturbs each active control. The representative assumptions are

$$
\delta_b\sim\mathcal N(0,0.015^2),\qquad
\eta_{\ell b}\sim\mathcal N(0,0.0006^2).
$$

These are the assumptions used by the accompanying numerical studies, **not a site-resolved calibration of a particular experimental device**. Separate context-dependent coactivation fluctuations were tested with assumed standard deviations and various correlation times; those values should not be read as experimental measurements.

The input-referred first-order static generator on bond $b$ is

$$
K_b=-iU(0)^\dagger\left.\frac{\partial U}{\partial\delta_b}\right|_0.
$$

We report its gauge-subtracted harmful coefficient, including leakage,

$$
H_b=\frac1{16}\min_{h=h^\dagger}
\left\|K_b E-E(I_{\rm logical}\otimes h_{\rm gauge})\right\|_F^2,
\qquad H_{\rm pb}=\sum_bH_b.
$$

$H_{\rm IID}$ similarly sums the independent-control contributions. For sufficiently weak fluctuations, infidelity begins as a quadratic form in the variances. Gate-level $H_{\rm pb}$, conditional instrument loss, wrong-syndrome probability, and leakage probability are **different observables with different normalizations** and must not be interchanged. "Controls" counts active physical exchange couplings; "ASAP depth" assumes unit-duration compatible layers and is not a calibrated wall-clock time.

# Six-spin simultaneous-exchange CZ: the central constructive result

The short exact CZ reference is the 22-control Fong--Wandzura-derived sequence in the archived linear six-spin encoding [1]. Later rounds explored exact simultaneous replacement, error-generator cones, local spin-sector recurrences, positive-exchange composite loops, and six-spin noncommuting frames.

For the directly comparable 28-control/19-layer R139 baseline, the optimized R143 sequence uses **30 active controls in the same 19 nominal ASAP layers** and gives

$$
H_{\rm pb}:37.668119847\longrightarrow32.011918153
\qquad(15.02\%\ \mathrm{reduction}),
$$

while $H_{\rm IID}$ decreases from $45.7993$ to $43.5393$. The physical gate is validated with full $64$-dimensional exchange propagation and, after translation, with $512$-dimensional propagation of a nine-spin assembly. The encoded residual is on the order of $10^{-13}$. A second 30-control trade-off has $H_{\rm pb}=32.9022$, $H_{34}=8.4960$, and $H_{\rm IID}=41.9486$. Neither eliminates the bridge error at first order.

*Figure available in the companion PDF and reproducibility archive.*

| Certified CZ reference | Active controls | ASAP depth | $H_{\rm pb}$ | $H_{34}$ | $H_{\rm IID}$ |
|:--|--:|--:|--:|--:|--:|
| R139 total-noise baseline | 28 | 19 | 37.6681 | 8.8616 | 45.7993 |
| **R143 optimized static** | **30** | **19** | **32.0119** | 8.9451 | 43.5393 |
| R143 bridge-balanced | 30 | 19 | 32.9022 | 8.4960 | 41.9486 |
| R144 selective bridge | 32 | 20 | 49.7808 | 7.8607 | 42.2649 |
| R149 six-spin coactivation | 35 | 19 | 37.9950 | 8.9451 | 51.3420 |

The improvement is principally a change in **$J_{12}$ logical-error sensitivity**, not a complete bridge-gain correction. Specifically, in the R143 comparison, $J_{12}$ harmful contribution falls from approximately $12.2520$ to $7.4315$, while $J_{34}$ changes from $8.8616$ to $8.9451$. Some additional endpoint Jacobian directions have very small singular values ($\sim10^{-6}$), limiting the physical significance of a simple rank-count argument.

*Figure available in the companion PDF and reproducibility archive.*

### Why straightforward compensation failed

Several carefully bounded negative screens were useful. Adding exact simultaneous identity loops, including four-spin revival blocks, generally worsened $H_{\rm pb}$ because each additional positive exchange accumulates static and IID error. Some optimizations reduce $H_{34}$ at the cost of substantially increasing other bond sensitivities. Introducing $J_{56}$ as an extra control in the old five-spin frame creates new endpoint directions, but their positive-area tangent cone cannot be cancelled by arbitrarily small added pulses near that particular seed. This is **not** a no-go theorem against all six-spin CZ designs.

The six-spin nested commutator

$$
D=[P_{56}^{(s)},[P_{45}^{(s)},P_{34}^{(s)}]]
$$

is nonzero even though $[P_{56}^{(s)},P_{34}^{(s)}]=0$, and a two-bond direction $Q=i[P_{45}^{(s)},P_{34}^{(s)}]$ gives greater reduction of the projected error in *idealized operator-budget screens*. However, the budget coefficients do not correspond to physically executable pulse areas. Later rounds found positive-exchange simultaneous loops with either sign of a $Q$ component, but none gave a lower total-noise exact CZ after insertion. Positive exchange yields semidefinite first-order physical generators, so a pure, unaccompanied traceless $Q$ term is not physically available as a bond-gain derivative.

# A three-spin dual-static-gain corrected exchange: useful but not transferable

On a crossing triple $2,3,4$, a **six-layer, twelve-control** positive simultaneous sequence was synthesized that implements a physical $J_{34}(1)$ SWAP. With two independent bond-static gains,

$$
U_\ell=\exp\{i\pi[a_\ell P_{23}^{(s)}+b_\ell P_{34}^{(s)}]\},
$$

and the first-order generators reduce, numerically, to scalars on the triple's $S=1/2$ sector:

$$
K_{23}=\kappa_{23}\Pi_{234}^{S=1/2},\qquad
K_{34}=\kappa_{34}\Pi_{234}^{S=1/2}.
$$

Consequently, *the isolated three-spin logical operation* has no first-order harmful static-gain rotation. A deterministic noise-amplitude scan gives logical infidelity power-law slopes close to four on both independent error directions, versus approximately two for a direct SWAP. The 15,000-shot isolated-triple simulations yield $3.72\times10^{-4}$ versus $9.88\times10^{-6}$ for direct versus composite SWAP under the static-plus-IID model.

*Figure available in the companion PDF and reproducibility archive.*

**The protection does not carry over to two EO qubits.** The projector $\Pi_{234}^{S=1/2}$ is not gauge-only for the $123|456$ code. Replacing one bridge pulse in an otherwise exact 22-control CZ creates a 31-control exact gate with $H_{\rm pb}=80.276$ and $H_{34}=11.584$, both worse than the original. If simultaneous context noise fluctuates independently every layer rather than being shot-static, the isolated triple's fourth-order benefit also degrades markedly. These observations support *noise correlation-time-aware* compilation rather than a simple claim of universal exchange-gain immunity.

# Measurement-instrument-first design

For a Pauli check $S$ and recorded outcome $m\in\{0,1\}$, the target ideal nondemolition Kraus operator on data is

$$
M_m=P_m^{S}=\frac{I+(-1)^mS}{2}.
$$

Syndrome probabilities alone are insufficient. A valid measurement must preserve arbitrary superpositions **within** each eigenspace of $S$ and must not introduce unwanted logical backaction or leakage. For example, separately measuring $Z_1Z_2$ and $Z_3Z_4$ then multiplying the recorded bits coarse-grains two stronger measurements; it is not the same instrument as measuring $Z_1Z_2Z_3Z_4$. On $|++++\rangle$, conditioning on positive four-body parity gives purity $1$ for the correct projector but only $1/2$ for the fine-grained protocol.

## Nine-spin coherent ZZ and XX checks

Take three consecutive EO triples, data-left $(1,2,3)$, ancilla $(4,5,6)$, and data-right $(7,8,9)$. The exact baseline is

$$
H_A\;CZ_{L,A}\;CZ_{A,R}\;H_A\;\mathrm{ST\ readout}_A,
$$

where each logical $H_A$ is synthesized with **positive exchange only**, not with an assumed physical single-spin magnetic rotation. The 50-control/29-layer ZZ construction and its 62-control XX counterpart are validated by complete physical $512$-dimensional propagation and outcome-conditioned Kraus comparison across all $32$ input logical--gauge states.

## Exact measurement-specific elimination of two controls

An important reduction is **exact for the recorded instrument but not necessarily for the full unmeasured unitary**. At preparation the ancilla is known to be $|0,g\rangle$, with its first pair $(4,5)$ singlet. Thus

$$
X_{45}(a)|0,g\rangle=e^{i\pi a}|0,g\rangle.
$$

At readout the projectors are $M_0=P_{45}^{(s)}$ and $M_1=I-P_{45}^{(s)}$. As $X_{45}(a)$ commutes with both,

$$
M_0X_{45}(a)=e^{i\pi a}M_0,\qquad
M_1X_{45}(a)=M_1.
$$

The initial and final $J_{45}$ controls can therefore be omitted without changing the normalized outcome-conditioned physical data operation (only irrelevant outcome phases remain). This takes the ZZ instrument from **50 controls / 29 ASAP layers to 48 controls / 27 layers**. This exact pruning alone does *not* improve the error statistics, because the discarded controls were physically irrelevant even when miscalibrated.

The additional gain comes from choosing a different legal two-exchange ancilla preparation branch. In chronological order, the optimized preparation uses $J_{56}(0.60817344797)$ followed by $J_{45}(1.69591327602)$, while the readout basis changer retains the archived branch. These operations prepare the same required ancilla input but need not implement the same $H$ on arbitrary ancillary states. Full nine-spin two-outcome Kraus residuals are $\sim10^{-15}$.

| Nine-spin ZZ instrument | Controls | ASAP depth | Static instrument curvature | Static wrong-syndrome curvature |
|:--|--:|--:|--:|--:|
| R153 original | 50 | 29 | 90.1754 | 50.1050 |
| R154 boundary-pruned only | 48 | 27 | 90.1754 | 50.1050 |
| **R154 optimized preparation** | **48** | **27** | **86.0781** | **46.0078** |
| R153 two R143 CZ gates | 66 | 39 | 76.5499 | 46.1944 |

The optimized 48-control choice reduces wrong-syndrome curvature by **8.18%** against the original 50-control instrument, while keeping the average leakage curvature approximately unchanged. A principal sensitivity is the ancilla-adjacent $J_{56}$ bond, whose wrong-syndrome coefficient changes from approximately $20.0460$ to $14.2895$. Thus an instrument-level objective can prioritize a different bond than an isolated CZ compiler.

### Finite-noise assessment

With $750$ **paired** simulations at shot-static gain $1.5\%$ and independent jitter $0.06\%$, the original 50-control instrument has wrong-syndrome probability $0.01103592$, and the optimized 48-control instrument has $0.01004484$. The paired difference is $-0.00099108\pm0.00026945$ (quoted $95\%$ normal confidence-interval halfwidth). Instrument loss changes from $0.01974105$ to $0.01873975$. Leakage differences are statistically inconclusive. These figures do not include calibrated readout errors, waiting dephasing or reset.

*Figure available in the companion PDF and reproducibility archive.*

The 66-control check has lower full-instrument loss and leakage under another matched comparison but requires 18 extra controls and 12 extra ASAP layers relative to 48-control. Its wrong-syndrome advantage is **not statistically established** in that comparison. In particular, one should not merge sample means from separate Monte Carlo batches into a single paired statistical test.

# Fully physical weight-four reference on an explicit star graph

A five-EO reference uses an ancilla triple $(1,2,3)$ and data triples $(4,5,6)$, $(7,8,9)$, $(10,11,12)$, $(13,14,15)$. It **assumes** physical controllable exchange edges $(3,4)$, $(3,7)$, $(3,10)$, and $(3,13)$ plus specified internal bonds. This is **not** a strict one-dimensional nearest-neighbor device and must not be described as one.

Four mapped 22-control FW-derived CZs plus a two-control ancilla preparation and a two-control readout changer yield a **92-control / 56-ASAP-layer** coherent ZZZZ measurement baseline. Applying physical three-exchange logical Hadamards to all four data triples before and after the ZZZZ sequence yields a **116-control / 56-layer** XXXX baseline in the stated unit-time concurrency model.

All 16 data logical patterns multiplied by all 32 combined gauge patterns, i.e. **512 encoded input basis states**, were explicitly propagated in the full $2^{15}=32768$ physical state space. Maximum output vector residuals are approximately $2.45\times10^{-15}$ for ZZZZ and $3.31\times10^{-15}$ for XXXX; selected coherent-superposition checks verify preservation within each parity sector. These are **CZ-factorized constructions**. They do not demonstrate a shorter direct four-body measurement, repeated rounds of correction, or a practical star-chip implementation.

# Interpretation, limitations and open research questions

The trajectory supports three defensible conclusions. First, overlapping simultaneous exchanges provide real noncommuting control and allow nontrivial noise-generator engineering, but a short six-spin, all-bond first-order-corrected exact CZ remains an open problem in these archives. Second, a strong locally corrected crossing triple is not necessarily a corrected multi-EO gate: the code and leakage projectors must be re-evaluated globally. Third, the most tangible system-level saving comes from relaxing unnecessary **intermediate gate constraints** when ancilla initialization and measurement are fixed.

The major limitations are: (i) noise strengths and context covariance are model inputs rather than measured per-device maps; (ii) ASAP depth is not a waveform-calibrated duration and 48 controls do not necessarily imply a smaller total exchange-area time; (iii) no independent noise calibration of the claimed star couplers is provided; (iv) singlet–triplet readout does not separate logical triplet from $S=3/2$ leakage; (v) no repeated syndrome, ancilla reset, hook-error circuit, leakage-reduction unit, decoder, logical error suppression or threshold was evaluated; and (vi) this synthesis is not a full novelty or experimental feasibility review.

The next useful **publication-quality** advance would be a *directly synthesized quantum instrument* with fewer than 48 controls or a materially lower wrong-syndrome/error-plus-duration objective, validated in full nine-spin dynamics. For weight-four checks, the analogous objective must be formulated on an explicitly feasible geometry, include readout/reset/leakage and repeated-cycle propagation, and compare full conditional Kraus maps rather than parity bits alone.

# Reproducibility and research provenance

The accompanying repository package retains selected full-precision sequences and four source-archive ZIPs (R143, R146, R153, R154); an additional all-round archival bundle contains R138–R154. Each source ZIP is treated as a frozen research artifact with its own code, evidence and internal SHA-256 listing. Re-run the corresponding archive verifiers before changing geometry or gauge convention; note that their denominators and definitions differ between gate, isolated triple, and instrument metrics. Exact filenames, command entry points, and hashes are listed in `REPRODUCIBILITY.md` and `SOURCE_MANIFEST.csv`.

# References

[1] B. H. Fong and S. M. Wandzura, "Universal quantum computation and leakage reduction in the 3-qubit decoherence free subsystem," *Quantum Information and Computation* **11**, 1003–1018 (2011). https://doi.org/10.26421/QIC11.11-12-9

[2] G. T. Hickman, X. Wang, J. P. Kestner, and S. Das Sarma, "Dynamically corrected gates for an exchange-only qubit," *Physical Review B* **88**, 161303(R) (2013). https://doi.org/10.1103/PhysRevB.88.161303

[3] I. Heinz *et al.*, "Fast Quantum Gates for Exchange-Only Qubits Using Simultaneous Exchange Pulses," *PRX Quantum* **6**, 030353 (2025). https://doi.org/10.1103/njq3-fcdd

[4] M. T. Mądzik *et al.*, "Operating two exchange-only qubits in parallel," *Nature* **647**, 870–875 (2025). https://doi.org/10.1038/s41586-025-09767-5

[5] Members of the HRL Quantum Team and Collaborators, "A digitally controlled silicon quantum processing unit," *Nature* **655**, 1154–1159 (2026). https://doi.org/10.1038/s41586-026-10754-7

[6] The numerical research archives R138–R154 accompanying this synthesis (October 2026), including reproducibility scripts, pulse CSVs, full-state validation outputs, and model-specific Monte Carlo evidence. These are **internal computational source records**, not independently peer-reviewed publications.