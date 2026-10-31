---
title: 'Exchange-Only Native Stabilizer Extraction with Flagged Logical-Fault Suppression'
subtitle: 'A numerically supported working manuscript on four-body parity checks in encoded silicon spin qubits'
date: '1 November 2026'
abstract: |
  We assemble and critically assess a set of native, exchange-only constructions for four-body parity extraction on three-spin exchange-only (EO) qubits. Under a proposed degree-four planar coupling graph, 92 exchange pulses implement an encoded $Z^{\otimes4}$ measurement and another 92-pulse sequence measures a uniformly rotated $\widetilde X^{\otimes4}$ operator. A 140-pulse, 18-spin construction adds an encoded flag ancilla to one rotated-$X$ check. We examine ideal gauge-sector correctness, single-pulse exchange-angle faults, and a limited three-check memory experiment in which persistent physical-bond gain errors coexist with pulse-wise jitter. For one encoded input state and gauge configuration, a 324-pulse flagged $\widetilde X\to Z\to\widetilde X$ history reduces accepted-conditioned encoded logical error from $6.682\times10^{-4}$ to $3.744\times10^{-4}$ relative to a 276-pulse unflagged history, while decreasing acceptance from 88.70% to 86.24% in 50 paired gain realizations. The results establish specific *numerical constructions* and a restricted fault-suppression observation, not a fault-tolerance certificate, a distance-three decoder result, a physical-device demonstration, or a logical-error threshold.
keywords: 'exchange-only qubits; stabilizer extraction; syndrome measurement; flag qubits; gauge leakage; correlated exchange noise'
---

> **Status and provenance.** Working research synthesis, **not peer reviewed**. All results described as numerical are transcribed from the project archives `EO_QEC_NATIVE_92P_100P_53P_RESULTS_20261030.zip`, `EO_ROTATED_CHECK_92P_GAUGE_ROBUST_20261030.zip`, `EO_QEC_140P_FLAG_NATIVE_RESULTS_20261031.zip`, and `EO_QEC_FLAGGED_LOGICAL_AUDIT_20261031.zip`. This manuscript audits the reported evidence and provides selected source sequences; it does **not** claim a fresh independent full-Hilbert-space rerun of every simulation. Authors and priority/novelty claims require verification before journal submission.

# 1. Motivation and scope

Three-spin exchange-only (EO) qubits admit encoded logical control using isotropic Heisenberg exchange without local physical-spin $H$, $X$, or $Z$ rotations. The challenge is not merely to compile an accurate two-EO controlled gate but to realize *non-demolition parity-measurement instruments* compatible with repeated syndrome extraction, including gauge-sector consistency, physical leakage, correlated exchange calibration error, and measurement/reset overhead.

The motivating reference is Heinz, Sharma and Kattemölle, *Exchange-only qubit stabilized by a single-spin qubit*, arXiv:2608.14214v1 (2026). Their singlet-only EO (SOEO) proposal combines four-spin encoded data with individually controllable Loss--DiVincenzo (LD) ancillas, enabling flagged physical-spin $XXXX$ and $ZZZZ$ detection. Our architecture is **different**: it retains three-spin EO data and ancillas and measures four-*logical*-EO stabilizers using exchange alone. The two $XXXX$ symbols act on distinct encoding layers and should not be equated.

The scope is deliberately narrow: exact ideal encoded operations and partial numerical fault/finite-noise evidence. We do not assert complete fault-tolerant quantum error correction (QEC). In particular, the $[[4,2,2]]$ construction is a detection code, not deterministic correction of arbitrary single errors.

# 2. Physical model and target measurement

For $n$ physical spin-$1/2$ electrons the control is

$$
H(t)=\sum_{(i,j)\in E}J_{ij}(t)\bigl(\mathbf S_i\!\cdot\!\mathbf S_j-\tfrac14\bigr),
\qquad J_{ij}(t)\ge0.
$$

A normalized exchange-area pulse is

$$
U_{ij}(a)=\exp\!\left[i\pi a P_{ij}^{(s)}\right],\qquad
P_{ij}^{(s)}=\tfrac14-\mathbf S_i\!\cdot\!\mathbf S_j.
$$

The native sequences are strictly one physical bond per *chronological* step. Reported depth permits disjoint bonds to operate in parallel; it is not equal to the number of serial steps and excludes measurement/reset latency. Each EO block has three spins, a logical qubit within the total-$S=1/2$ manifold, an unused gauge degree of freedom, and a $S=3/2$ leakage sector.

For four encoded data EO blocks $D_1,\ldots,D_4$ we wish to measure

$$
S_Z=\prod_{j=1}^{4} Z_{L,j},\qquad
S_{\widetilde X}=\prod_{j=1}^{4}\widetilde X_{L,j},\qquad
\widetilde X_L=-\frac{X_L}{\sqrt3}+\sqrt{\frac23}\,Y_L.
$$

Since $\widetilde X_L^2=I$ and $\{\widetilde X_L,Z_L\}=0$, the two four-body operators commute and define a rotated logical Pauli frame equivalent to the familiar $[[4,2,2]]$ generators. This is **not** the original-frame $X_L^{\otimes4}$; conversions between frames in an end-to-end circuit carry real resources and must be accounted for.

An ideal binary measurement of a stabilizer $S$ must realize the instrument

$$
\mathcal M_{\pm}(\rho)=K_\pm\rho K_\pm^\dagger,\qquad
K_\pm=e^{i\phi_\pm}\frac{I\pm S}{2}\otimes I_g
$$

on the encoded input, with no nominal leakage and a gauge-independent action. Merely matching the expectation value $\langle S\rangle$ is insufficient. Conditional branch phases are permissible when known and physically immaterial for the measured parity.

![Proposed six-EO, 18-spin planar graph for the flagged rotated-X check. Blocks D1--D4 carry data; S is the syndrome EO; F is the flag EO. Lines depict the physical nearest-neighbor geometry, not a fabricated chip.](figures/eo_flag_geometry.png){ width=77% }

# 3. Native constructions and resource accounting

The starting point is a Fong--Wandzura-derived 22-pulse encoded controlled-reflection whose action on the EO ancilla has a consistent logical reflection axis across four data interfaces. The ancilla is prepared and unprepared with native EO rotations. Conjugating an encoded control axis can transform $Z$ checks into $X$ checks without any physical single-spin Hadamard. A rotated $\widetilde X$ direction allows local basis rotations to merge into existing controlled-gate bonds.

| Native instrument or check history | Physical spins | Pulses | Ideal ASAP depth | Interpretation |
|:--|--:|--:|--:|:--|
| Two-data $X_AX_C$ | 9 | 59 | 29 | Exact fixed-frame $XX$ instrument; 53P/26D alternative exists with less favorable static-gain coefficient. |
| Four-data $S_Z$ | 15 | 92 | 44 | Unflagged logical $ZZZZ$ parity extraction. |
| Four-data fixed-frame $X_L^{\otimes4}$ | 15 | 100 | 45 | Exact unflagged instrument; 116P alternate with different noise response. |
| Four-data rotated $S_{\widetilde X}$ | 15 | 92 | 44 | Same code up to local frame conventions. |
| Flagged rotated $S_{\widetilde X}$ | 18 | 140 | 60 | First-check logical fault flag, not complete FT certification. |
| $S_{\widetilde X}\to S_Z$ | 15 | 184 | Not separately benchmarked | Two-check detection cycle; midcircuit ancilla read/reset assumed. |
| $S_{\widetilde X}\to S_Z\to S_{\widetilde X}$ | 15 | 276 | 132 | Unflagged three-check fault-history benchmark. |
| $F S_{\widetilde X}\to S_Z\to S_{\widetilde X}$ | 18 | 324 | 148 | Only the first $S_{\widetilde X}$ check is flagged. |

The 92P $S_Z$ and $S_{\widetilde X}$ instruments are reported gauge-independent and nominally leakage-free in full 15-spin propagation. The construction of the flagged 140P gadget follows a $92+2\times22+4=140$ pulse decomposition: original rotated-$X$ check, two additional syndrome--flag controlled reflections, and four flag-local preparation/unpreparation pulses. The flag is attached to an unused fourth nearest-neighbor interface of a syndrome-EO target-pair spin, avoiding a fifth connection on the four-arm core. The maximum degree of the proposed 18-dot graph is four. A rejected 148P variant needed two extra 4P axis-matching wrappers.

For the 140P no-fault construction, the prior archive reports 96 representative 18-spin state-propagation tests including all 64 gauge patterns for one selected data state and additional logical inputs, with maximum full-state residual $2.70\times10^{-15}$. These are **not** a full exhaustive 1024-column test across all six EO blocks; the operator-level argument also uses encoded controlled-reflection identities.

# 4. Flag mechanism and the single-fault question

Represent each data--syndrome interaction schematically by

$$
C_j=P^{(\widetilde X_j)}_+\otimes I_A+P^{(\widetilde X_j)}_-\otimes R_A,\qquad R_A^2=I_A.
$$

When a syndrome logical fault $E_A$ anticommutes with $R_A$,

$$
C_j(I\otimes E_A)C_j=\widetilde X_j\otimes E_A.
$$

A single syndrome fault can therefore propagate to several data EO blocks, creating a hook fault. Two controlled interactions with a flag EO are arranged so that a targeted $E_A$ is detected by a nontrivial flag outcome while the flag returns to its nominal state in the no-fault circuit. Prior full-spin fault-injection tests found 100% flag alarm for the chosen logical $Y_A$ and the specific anticommuting axis $E_\perp$, versus zero for the commuting axis $E_\parallel$. These figures do **not** establish detection of arbitrary exchange-pulse faults or leakage.

A single parity check cannot by itself classify every data error: an error commuting with that check may trigger its complementary check in a later round. Therefore the correct fault objective is a *detector history* and an accepted logical transition after complementary checks, not the flag rate or first-check wrong-record rate alone.

The archived first-gadget single-pulse tangent scan uses

$$
\partial_k |\psi_{\rm out}\rangle = U_N\cdots U_{k+1}
\bigl(i\pi a_kP_{b_k}^{(s)}\bigr)U_k\cdots U_1 |\psi_{\rm in}\rangle,
$$

followed by ideal later-check projections and a decomposition into codeword transitions versus outside-code/leaked states. Under one initial codeword/gauge setting, 32 of 92 unflagged first-check pulse positions led to a nonzero accepted encoded transition after the entire $\widetilde X\to Z\to\widetilde X$ history; the summed independent-pulse coefficient was $0.487873932$. Replacing that first check with the 140P flag reduced this *specific* accepted encoded-codeword-transition coefficient to numerical zero across all 140 first-check pulse positions, verified for **two** selected codeword/gauge settings. The accepted outside-code derivative coefficient remained nonzero ($0.699659$ in one tested input). This is a restricted single-fault finding, **not** $\sigma^4$ cancellation for arbitrary physical noise.

A separate set of $7\times15=105$ two-spin Pauli faults, covering seven selected physical pulse positions, also showed no accepted encoded-codeword transition on the tested state/gauge. It is not exhaustive over all pulses or all fault locations, and it does not establish absence of undetected leakage.

# 5. Persistent correlated-noise comparison

The model assigns an independent static fractional gain to each physical exchange bond and a separate pulse-specific fluctuation:

$$
a_k^{\rm actual}=a_k(1+\delta_{b_k}+\eta_k),\qquad
\delta_b\sim\mathcal N(0,0.015^2),\quad
\eta_k\sim\mathcal N(0,0.0006^2).
$$

Each $\delta_b$ persists across the **entire three-check history**, and the candidate histories use paired static-gain draws. This is a project-level HRL-*motivated* model, not a claim that these per-bond values were measured individually on a particular device. The published archive used one initial encoded codeword and gauge configuration, 50 paired gain draws, ideal readout/reset, no separate storage noise, and no decoder.

| Quantity (per attempted three-check history unless noted) | 276P unflagged | 324P flagged |
|:--|--:|--:|
| All-check acceptance | **88.7015%** | 86.2357% |
| Undetected encoded logical error, per attempt | 0.05927% | **0.03229%** |
| Undetected encoded logical error, conditional on acceptance | 0.06682% | **0.03744%** |
| Accepted but outside intended code space | 1.60875% | 1.53537% |
| Pulse count | **276** | 324 |
| ASAP depth proxy, excluding measurements | **132** | 148 |

![Comparison of conditioned encoded logical error and acceptance for the two three-check histories. Data are a limited model simulation with 50 paired static-gain draws, not a device measurement or decoded QEC threshold.](figures/three_check_comparison.png){ width=90% }

The flagged candidate reduces accepted-conditioned encoded logical error from $6.68235\times10^{-4}$ to $3.74410\times10^{-4}$, a **43.97% relative reduction**. A 5,000-resample paired bootstrap gave a **model-conditional sampling** interval of approximately 36.1--51.4% for that relative reduction. This interval does not cover experimental calibration, modeling errors or untested gauge settings. Acceptance falls from 88.70% to 86.24%, and pulse-cost per accepted history rises by approximately 20.7%. Including readout and reset time may change the ranking further.

**Interpretation:** the flag offers a credible *restricted* suppression mechanism for accepted logical transitions, but whether it improves useful quantum-memory or decoded computation performance is an open systems question. Optimizing only a one-round wrong-syndrome statistic would miss this distinction.

# 6. Exchange-only SOEO spin-sector alternative

An orthogonal proposal uses a four-spin singlet-only EO data block and a two-spin singlet ancilla. For uniform simultaneous exchange between one ancilla spin and four data spins,

$$
H_\star=J\sum_{j=1}^{4}\mathbf S_j\cdot\mathbf S_a
=J\mathbf S_D\cdot\mathbf S_a,
$$

with $Jt=2\pi$, a singlet/triplet ancilla measurement has an archived ideal-model singlet probability $P_s(S_D)=1/(2S_D+1)^2$ for total data spin $S_D=0,1,2$, i.e. $1,1/9,1/25$. For $S_D=0$ the dynamics leave the encoded singlet manifold invariant. The archive reports a first-order single-bond gain derivative cancellation for ideal $S=0$ data inputs at this revival time, consistent with state infidelity $O(\delta^4)$ for that restricted model.

**Important hardware limitation:** this requires *four simultaneous equal-strength couplings*. Naive strict-serial Trotterization produced substantial false alarm and logical disturbance. Consequently this attractive spin-sector probe is **not** an established short positive-exchange serial gadget under the EO geometry used above, and its fourth-order scaling must not be transferred to the 92P/140P parity checks.

# 7. Limitations and concrete requirements for a fault-tolerance claim

The present findings should not be described as experimental quantum error correction, a full single-fault tolerance certificate, or evidence of a surface-code threshold. Necessary outstanding steps include:

1. **Fault completeness.** Audit all 140 physical pulse locations for all physical two-spin Pauli faults and relevant one-spin noise, and similarly audit the second and third parity checks, readouts, initializations and resets. Report detectors, logical transitions, gauge changes and all leakage sectors separately.
2. **Physical measurement.** Replace ideal encoded projections with actual singlet--triplet readout POVMs. The accepting $|0\rangle_L$ ancilla projection coincides with a physical singlet-pair projection, but other branches and leakage have ambiguous readout signatures.
3. **Leakage handling.** Add implementable leakage-reduction/reset-if-leaked procedures and include their pulse, dot, time and error budgets.
4. **Repeated QEC and decoding.** Construct a complete distance-three or larger layout, realistic stabilizer schedule and spacetime detector graph, then benchmark an explicit decoder under persistent per-bond noise across rounds.
5. **Fair resources and frames.** Count physical couplers, shuttling, control electronics, logical-frame conversion, idle durations, parallel crosstalk and the success/rejection cost in addition to pulse count.
6. **Independent audit and literature novelty.** Re-run the archive verifiers on a clean system; check exact branch conventions and provenance; conduct a dedicated literature/priority review before any claim of novelty or journal submission.

# 8. Conclusion

Native, strictly positive-exchange, gauge-aware four-EO parity measurements with 92-pulse $Z^{\otimes4}$ and rotated-$\widetilde X^{\otimes4}$ checks are supported by the supplied numerical archives. A 140-pulse flagged rotated-$X$ construction adds a targeted hook-fault detector using one extra three-spin EO block, without physical single-spin rotations. In the restricted three-check simulation, one flagged first check suppresses accepted encoded logical transitions at all tested first-gadget exchange-angle fault locations and lowers conditioned logical error by about 44% under a persistent-gain noise model, at the cost of lower acceptance and 48 more exchange pulses. Establishing actual fault tolerance and QEC usefulness requires complete physical fault coverage, nonideal measurement/leakage protocols and decoded multi-round logical-error comparisons.

# References and provenance

- I. Heinz, M. Sharma and J. Kattemölle, *Exchange-only qubit stabilized by a single-spin qubit*, arXiv:2608.14214v1 (14 Aug 2026), <https://arxiv.org/abs/2608.14214>. This is **prior work with a different SOEO+LD hardware model**, not an experimental validation of our native EO construction.
- Internal numerical research archive, `EO_EXCHANGE_ONLY_QEC_ADVANCE_20261030.zip`: initial exchange-only SOEO spin-sector and EO logical basis-change derivations.
- Internal numerical research archive, `EO_QEC_NATIVE_92P_100P_53P_RESULTS_20261030.zip`: 15-spin parity sequences and measurement-branch verification.
- Internal numerical research archive, `EO_ROTATED_CHECK_92P_GAUGE_ROBUST_20261030.zip`: rotated-frame parity and gauge-aware static-gain study.
- Internal numerical research archive, `EO_QEC_140P_FLAG_NATIVE_RESULTS_20261031.zip`: 18-spin flagged geometry, faults, and 240-draw one-check correlated-noise analysis.
- Internal numerical research archive, `EO_QEC_FLAGGED_LOGICAL_AUDIT_20261031.zip`: two-/three-check history, physical pulse tangent tests, 105 Pauli-fault probes and 50-draw paired-gain study.

The internal archives are project data, **not independently published references**. The selected CSV files and JSON evidence in this companion package preserve traceability; the full source archives should be retained for independent reproduction.