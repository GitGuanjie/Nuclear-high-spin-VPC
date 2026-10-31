---
title: "Exchange-Only and Singlet-Only Spin Qubits: Gain-Robust Local Gates, Spin-Sector Detection, and Constraints on Encoded Entanglers"
subtitle: "A reproducible technical research report — numerical working draft, not peer reviewed"
date: "1 November 2026"
lang: en
---

# Abstract

We consolidate a sequence of theoretical and numerical studies of exchange-only (EO) three-spin qubits, four-spin singlet-only exchange-only (SOEO) qubits, and interactions between encoded blocks. The shared control model uses nonnegative isotropic Heisenberg exchange with independent quasi-static fractional gain errors assigned to each physical bond. Within a *strictly serial* control class we report numerical composite-pulse realizations of encoded Hadamard, phase, and Pauli-$Z$ gates whose first-order error generators on every **active** bond are scalar on the encoded space, with vanishing first-order leakage. The duration-optimized Hadamard uses 11 pulses and total normalized exchange area $8.308609\pi$; the selected $S$ and $Z$ constructions use 13 pulses each. Full physical-spin calculations check the EO logical and gauge sectors and the SOEO singlet subspace. Separately, a six-spin collective-exchange and singlet-probe model implements probabilistic detection of departure from the SOEO $S_D=0$ sector and exhibits first-order cancellation of four independent, static coupling-gain errors at a special revival time. This star construction, however, requires four simultaneous couplings and implements a protected identity, **not** an entangling gate. For two EO blocks we certify an ideal-unitary-preserving 43-to-41-pulse rewrite of a locally rotated controlled phase, with a $16.4\%$ reduction of a specified small-gain response coefficient, while the interblock response remains nonzero. We prove restricted obstructions to single-cross-bond exchange-only entanglers and explain why robust local dressing does not cure a noisy entangling core. This is a research audit, not a claim of hardware performance, fault-tolerant QEC, global gate optimality, or all-bond-robust CZ synthesis.

**Keywords:** exchange-only qubits; singlet-only encoding; silicon quantum dots; Heisenberg exchange; correlated gain errors; composite pulses; leakage; fault-tolerant syndrome extraction.

# 1. Scope, status, and relation to prior work

Three-spin EO encodes a qubit in the multiplicity space of total spin $S=1/2$, with an accompanying $m=\pm1/2$ gauge degree of freedom. Four-spin SOEO encodes one qubit in the two-dimensional total-spin-zero sector. The recent hybrid EO–Loss–DiVincenzo proposal of Heinz, Sharma and Kattemölle [1] uses *single-spin addressable* ancillas and flagged low-level $XXXX/ZZZZ$ checks. Such ancilla gates are **not native** to a strictly exchange-only controller. We distinguish its physical-spin checks from higher-level checks $X_L^{(A)}X_L^{(B)}X_L^{(C)}X_L^{(D)}$ across four separately encoded EO qubits.

The independent numerical constructions below come from four archived research packages supplied with this report. Earlier dynamically corrected EO gates were developed by Hickman *et al.* [2], and corrected exchange-coupled two-qubit gates were treated by Setiawan *et al.* [3]. Singlet-only always-on gapless (SAGE) qubits [4] employ a different protected Hamiltonian and are not covered by no-go arguments derived here for isolated fixed EO/SOEO blocks. Novelty relative to the full composite-pulse and dynamically corrected gate literature has **not** been established.

Throughout, labels mean: **ANALYTICAL** (derivation under explicitly stated assumptions), **NUMERICAL** (reproducible matrix verification at finite precision), **MODEL-ONLY** (estimated rates under specified synthetic noise), and **OPEN** (unrealized or unverified target). We do not equate a Monte Carlo model with experimental gate fidelity.

# 2. Spin encoding, pulse convention, and robustness criterion

For spin-$1/2$ particles, let $P^{(s)}_{ij}=(I-\mathrm{SWAP}_{ij})/2$. A positive exchange pulse of area $a$ is

$$
X_{ij}(a)=\exp\!\bigl(i\pi a P_{ij}^{(s)}\bigr), \qquad a>0.
$$

We distinguish ideal pulse periodicity $X_{ij}(a+2)=X_{ij}(a)$ from *noisy* periodicity: with fractional gain miscalibration the two physical implementations have different derivatives. In the strict model at most one physical bond is active per time step. Additional simultaneous-coupling schemes are always labeled separately.

For the full physical Hilbert-space propagator $U(\boldsymbol\delta)$, with a gain $\delta_b$ shared by all pulses acting on bond $b$, let $E$ be the isometric embedding of all code columns (including both EO gauge sectors) and $P=EE^\dagger$. A physically meaningful first-order condition for target encoded gate $U_T$ is

$$
U(0)E=e^{i\phi}E U_T,
\qquad
G_b E=c_b E,\quad
G_b=-iU(0)^\dagger \partial_{\delta_b} U\big|_0.
$$

Here $G_b$ is Hermitian, $c_b$ is real, and the second condition includes both **non-scalar logical/gauge errors** and **leakage**. The equivalent decomposition is $E^\dagger G_bE=c_bI$ and $(I-EE^\dagger)G_bE=0$. For chronological pulses, up to the sign convention of the pulse phase,

$$
G_b=\pi\sum_{k:b_k=b}a_k V_{k-1}^\dagger P_b^{(s)}V_{k-1},
$$

where $V_{k-1}$ is the ideal prefix before pulse $k$. This definition does **not** permit a favorable average over gauge states to hide harmful gauge dependence.

The main noise proxy is $a_k^{\rm actual}=a_k(1+\delta_{b_k}+\eta_k)$, with $\delta_b\sim N(0,\sigma_{\rm pb}^2)$ independent across bonds but fixed throughout a word, and $\eta_k\sim N(0,\sigma_{\rm iid}^2)$ independent for every pulse. Unless stated, idle, shuttling, readout, reset, crosstalk, and context errors are omitted.

# 3. Spin-sector revival: a protected *identity* and probabilistic detector

Consider four SOEO data spins with total $\mathbf S_D=\sum_{i=1}^4\mathbf S_i$ and an ancilla singlet $|S_{ab}\rangle$. Spin $b$ is a spectator during a star pulse in which **four** bonds to spin $a$ are activated simultaneously:

$$
H_\star=J\sum_{i=1}^4\mathbf S_i\cdot\mathbf S_a
=J\mathbf S_D\cdot\mathbf S_a.
$$

For every encoded $S_D=0$ state, $H_\star P_0=0$ and thus $U_\star(t)P_0=P_0$ for any $t$: this is a dark subspace, not a useful logical rotation. For data total-spin sector $S=0,1,2$, the ancilla-singlet return Kraus amplitude is

$$
A_S(t)=\frac{(S+1)e^{-iJSt/2}+Se^{iJ(S+1)t/2}}{2S+1}.
$$

At the revival time $JT=2\pi$,

$$
K_s=P_0-\tfrac13 P_1+\tfrac15P_2,\qquad
E_t=I-K_s^\dagger K_s=\tfrac89 P_1+\tfrac{24}{25}P_2.
$$

Thus an ideal single-spin Pauli error from a valid four-spin singlet is flagged with probability $8/9$ per check. After $n$ independent ideal repeats using new singlet pairs, the miss probability for a persistent $S_D=1$ error is $9^{-n}$. This is **not** a one-shot projective $P_0$ measurement, nor a proof of finite-round distance-three QEC.

For independent **static** gain biases $J_i=J(1+\delta_i)$, the perturbation $V=J\sum_i\delta_i\mathbf S_i\cdot\mathbf S_a$ connects an initial $S_D=0,F=1/2,E=0$ state at first order only to the $S_D=1,F=1/2,E=-J$ sector. The Dyson term contains

$$
\partial_{\delta_i} U(T)P_0\propto
\int_0^{2\pi/J}e^{iJt}\,dt=0.
$$

Hence every individual star-bond first derivative vanishes on the encoded input, and the single-operation state infidelity begins at $O(\|\boldsymbol\delta\|^4)$. **This cancellation applies to the dark identity and only to the stated time-independent isotropic-gain model.** An $O(\delta^2)$ effective *logical* Hamiltonian remains for unequal gains: letting $\mathbf D=\sum_i\delta_i\mathbf S_i$,

$$
H_{\rm eff}^{(2)}=\frac J4P_0\mathbf D^2P_0.
$$

The associated coherent logical rotation can accumulate over cycles. The research notes previously reported a model-level accepted-state infidelity near $5\times10^{-7}$ per star probe at $\sigma_{\rm pb}=0.015$ but near $5\times10^{-3}$ after 100 cycles with persistent gain biases. These quantities are **not** decoded logical QEC failure rates. The star also violates the strict one-bond-at-a-time hardware contract; naive serial Trotterization does not preserve its finite-pulse guarantees.

# 4. Nontrivial encoded gate mechanisms: what survives and what fails

A smaller two-bond simultaneous star $H_{2J}=J(\mathbf S_1+\mathbf S_2)\cdot\mathbf S_a$ has an exact revival at $T=4\pi/(3J)$:

$$
U_{2J}(T)=P_{12}^{(s)}+e^{-2\pi i/3}P_{12}^{(t)}.
$$

Because pair singlet/triplet distinguishes the customary encoded $|0_L\rangle,|1_L\rangle$ in EO and SOEO, this acts as a nontrivial encoded $R_{Z_L}(-2\pi/3)$. It uses two simultaneous bonds and does **not** cancel both independent gain errors. A three-segment $2J$ echo with two interleaved physical SWAPs suppresses the *differential* first-order error under the ideal-SWAP assumption, but the common gain and SWAP bond errors remain. A direct one-bond phase pulse outperformed these mechanisms in the source model at $\sigma_{\rm pb}=1.5\%$.

Perturbative SOEO–SOEO and EO–SOEO two-block couplers were also derived from gap-protected virtual transitions, with $J_{ZZ}\propto g_1g_2/\Delta$. They are not exact native CZ gates; their useful phase is itself first-order sensitive to fractional $g_1$, $g_2$, and $\Delta$ variations, and the tested parameters led to long operation times. EO-to-SOEO conversion through a total-spin-zero projection was found as a heralded isometry of ideal success probability $1/2$ given a known EO gauge and one polarized added spin, not a deterministic coding conversion. These constructions are retained as *candidate mechanisms*, not recommended gate frontiers.

# 5. Strictly serial gain-robust local Clifford primitives

Composite words alternate two noncommuting physical bonds. The 11-pulse Hadamard was optimized for lower total positive exchange area relative to an earlier 9-pulse candidate. Full precision chronological angles are included in `sequences/`. For EO, the two bonds are $J_{12},J_{23}$; for SOEO, the numerically verified mapping is $J_{12},J_{13}$. The two encoded logical axes have the same $2\times2$ representation, so a shared set of pulse angles implements the same logical target; the full-spin calculations verify gauge independence and absence of nominal leakage.

| Target | Word | Pulse count | Total area $\sum a_k$ | EO target residual | SOEO target residual |
|:--|:--|--:|--:|--:|--:|
| $H_L$ | H11 | 11 | 8.308609 | $7.10\times10^{-14}$ | $5.03\times10^{-14}$ |
| $S_L=\mathrm{diag}(1,i)$ | S13 | 13 | 8.858912 | $1.20\times10^{-14}$ | $8.49\times10^{-15}$ |
| $Z_L=\mathrm{diag}(1,-1)$ | Z13 | 13 | 7.838015 | $9.24\times10^{-14}$ | $6.53\times10^{-14}$ |

All active-bond first-order non-scalar tangent norms for the listed EO words are below $3\times10^{-13}$ in the supplied double-precision verifier, with nominal leakage near $10^{-15}$ or below. The supplementary archive also contains an 11-pulse S candidate with *larger* area ($10.324126\pi$). The values constitute **numerically exact**, not symbolic transcendental, pulse solutions; no globally minimal length or duration has been proven.

The prescribed synthetic noise model with $\sigma_{\rm pb}=0.015$ and $\sigma_{\rm iid}=0.0006$ gave the following averages (the fidelity definition follows the source package's encoded/gauge treatment):

| Local gate | Native short word, $1-F$ | Selected robust word, $1-F$ | Approx. ratio |
|:--|--:|--:|--:|
| $H_L$: 3P vs 11P | $9.37\times10^{-4}$ | $1.36\times10^{-5}$ | $69\times$ |
| $S_L$: 1P vs 13P | $9.95\times10^{-4}$ | $1.02\times10^{-5}$ | $97\times$ |
| $Z_L$: 1P vs 13P | $4.43\times10^{-4}$ | $9.05\times10^{-6}$ | $49\times$ |

These ratios are *not* hardware advantages. The 11P H has $8.31\pi$ total area versus approximately $2\pi$ for the 3P reference and eight additional switch events. A modeled area-dependent penalty exceeding roughly $1.46\times10^{-4}$ per additional normalized area unit could reverse the benefit under the original source assumptions; this crossover is illustrative, not measured. In syndrome extraction a conjugated two-data $XX$ instrument would cost $47+4\times3=59$ pulses with basic H, but $47+4\times11=91$ pulses with robust H, *conditional* on the unavailable archived 47P physical source word. The full 59P/91P instruments were **not** independently revalidated.

# 6. Six-spin encoded entangler: exact 43P to 41P rewrite

For two EO blocks $A=(1,2,3)$ and $B=(4,5,6)$ in a linear chain, an archived 43-pulse source word was found despite its misleading `CZ25` filename. The encoded target in its explicit basis is a **locally rotated** controlled reflection

$$
U_{\rm rotCZ}=I_4-2|vv\rangle\langle vv|,\qquad
|v\rangle=(\sqrt3|0_L\rangle+|1_L\rangle)/2,
$$

with identity action on both gauge qubits. It is locally equivalent to a literal computational-basis CZ; the provided CSV is **not** the latter without a local-frame conversion. Two exact physical rewrite identities merge disjoint-bond-adjacent pulses, and one merger replaces a nominal pulse of area $2.5$ by $0.5$ using $X_b(a+2)=X_b(a)$. The resulting **41P** word is identical to the 43P word on all 64 physical states to Frobenius norm $1.68\times10^{-15}$, with encoded leakage $1.75\times10^{-15}$. The change of angle branch reduces the derivative with respect to the associated physical bond, although it leaves the ideal gate unchanged.

We define a same-convention, normalized squared tangent measure

$$
h_b=\frac{\|E^\dagger G_bE-c_bI\|_F^2+\|(I-EE^\dagger)G_bE\|_F^2}{16},\qquad
c_b=\frac{\operatorname{Tr}(E^\dagger G_bE)}{16}.
$$

| Bond | 43P $h_b$ | 41P $h_b$ |
|:--|--:|--:|
| $J_{12}$ | 63.5527 | 39.1871 |
| $J_{23}$ | 24.1692 | 24.1692 |
| $J_{34}$, interblock | 33.3549 | 33.3549 |
| $J_{45}$ | 18.3557 | 18.3557 |
| $J_{56}$ | 9.4908 | 9.4908 |
| **Total** | **148.9232** | **124.5576** |

The total coefficient decreases by $16.4\%$, but **no active bond** meets the full zero-tangent condition. In particular the cross-bond response is unchanged. A paired 850-trial model comparison at $\sigma_{\rm pb}=0.015$ and $\sigma_{\rm iid}=0.0006$ yielded phase-optimized encoded operator distances $D_{43}=0.03380$ and $D_{41}=0.02817$; this $D$ is **not** Haar-average gate infidelity. The 41P result is neither a shortest CZ nor a fully robust entangler; existing 25P/27P gate baselines in the wider project were not recertified in this archive.

# 7. Necessary constraints on fully robust encoded entanglers

**Single-use-bond theorem (ANALYTICAL).** If a physical bond occurs only once in a word and its independent gain derivative must be a scalar phase with no first-order leakage on the transported input code, its conjugated singlet projector must restrict to eigenvalue $0$ or $1$ on that transported code. Therefore that pulse acts as an overall scalar on the code and is removable from the *ideal encoded action*. If every cross-block bond occurs at most once and each satisfies exact individual-bond robustness, the remaining internal exchange operations cannot generate entanglement. Thus a nontrivial all-bond-first-order-robust entangler needs at least one repeated nontrivial cross bond, or additional hardware resources/changed code assumptions. This is **not** a global CZ no-go theorem.

**Single-cross-pulse obstruction (ANALYTICAL + NUMERICAL).** For $U=L_{\rm post}X_{ij}(a)L_{\rm pre}$, with $L_{\rm pre/post}$ restricted to inside fixed EO/SOEO blocks, the leakage norm is

$$
\|QUP\|_F=2|\sin(\pi a/2)|\,\|QP_{ij}^{(s)}P\|_F.
$$

The rightmost factor is independent of which physical spin in a block is used:

| Block pair | Physical spins | Encoded rank | $\|QP_{ij}^{(s)}P\|_F$ |
|:--|--:|--:|:--|
| EO–EO | 6 | 16 | $\sqrt{56/27}\approx1.44016$ |
| EO–SOEO | 7 | 8 | $\sqrt{3/2}\approx1.22474$ |
| SOEO–SOEO | 8 | 4 | $\sqrt{3/4}\approx0.86603$ |

A single nontrivial isolated cross-block pulse consequently leaks from the fixed code. For the pairs involving a singlet SOEO block, the projected cross-block singlet operator is only $P P_{ij}^{(s)}P=P/4$. This does **not** contradict gate constructions with always-on intra-block Hamiltonians, encoding changes, measurement-assisted control, or more than one cross pulse.

**Local-dressing theorem.** If $U=L_{\rm post}EL_{\rm pre}$ and a gain parameter acts only in the noisy entangling core $E$, the harmful derivative is merely unitarily conjugated by $L_{\rm pre}$. Consequently putting individually robust H/S gates around an unchanged CZ **cannot** cancel its interblock gain tangent. The core itself, or the physical resources, must change.

# 8. Implications for QEC and priorities

The source hybrid SOEO paper measures physical-spin $XXXX/ZZZZ$ within a *single* four-spin encoding using addressable LD ancillas. Our strict EO objective instead concerns encoded logical parity instruments and the actual physical measurement branches; the unitary equality $H_L Z_L H_L=X_L$ is insufficient to certify the entire noisy instrument. Any candidate must be tested on the full encoded logical$\times$gauge space, the correct ancilla preparation/readout channel, leakage sectors and single-fault hook propagation, and persistent bond gains over multiple rounds. Conditional postselection fidelity, a one-shot parity readout probability, and a decoded logical error per real-time cycle are different metrics.

The order of priority is: (i) obtain and recertify the original **shortest geometry-matched** six-spin CZ source CSVs; (ii) synthesize a short core with repeated cross-bond interfaces, optimizing all full-space tangent matrices rather than one scalar; (iii) compare the same core in a physical QEC instrument under static gain, IID pulse jitter, idle, readout/reset, and leakage-aware decoding; (iv) evaluate whether robust local frames improve total syndrome cost after pulse duration and switching overhead. Until those tasks are complete, the project's strongest result is a set of **local robust primitives and an informative restricted entangler obstruction**, not a practical QEC threshold or fully gain-robust CZ.

# 9. Reproducibility and limitations

The main local and six-spin code verifiers were rerun on 1 November 2026 using NumPy, with single-threaded BLAS. For local gates, `code/verify_all_physical.py` tests both EO gauge sectors in the 8D physical space and the 16D SOEO singlet subspace, and `code/replay_benchmark.py` reruns a 3,000-trial stochastic benchmark. For the entangler, an independent physical SWAP/permutation implementation verifies the 41P/43P ideal equivalence, `code/cz43_audit.py` returns the full bond tangent decomposition, and `code/single_bridge_no_go.py` tests all nine EO–EO interface choices. The accompanying archives include original chronological CSVs and provenance. They may include additional exploratory scripts that retain working-session paths; such scripts require adaptation before external reproduction. No hardware was controlled, no experimental samples were obtained, and no multiperiod stabilizer decoding was run.

The calculations should not be submitted as a novelty-centered paper without (a) a systematic quantitative comparison against [2,3] and later dynamically corrected EO literature; (b) independent analytic or high-precision certification of composite words; (c) a fair physical noise/time budget; and (d) a new entangling-gate or end-to-end QEC gain. This report is a transparent technical research artifact.

# References

[1] I. Heinz, M. Sharma, and J. Kattemölle, *Exchange-only qubit stabilized by a single-spin qubit*, arXiv:2608.14214v1 (2026), <https://arxiv.org/abs/2608.14214>.

[2] G. T. Hickman, X. Wang, J. P. Kestner, and S. Das Sarma, *Dynamically corrected gates for an exchange-only qubit*, *Phys. Rev. B* **88**, 161303(R) (2013), <https://doi.org/10.1103/PhysRevB.88.161303>.

[3] F. Setiawan, H.-Y. Hui, J. P. Kestner, X. Wang, and S. Das Sarma, *Robust two-qubit gates for exchange-coupled qubits*, *Phys. Rev. B* **89**, 085314 (2014), <https://doi.org/10.1103/PhysRevB.89.085314>.

[4] N. L. Foulk, S. Hoffman, K. Laubscher, and S. Das Sarma, *Singlet-Only Always-on Gapless Exchange Qubits with Baseband Control*, *Phys. Rev. Lett.* **135**, 106202 (2025), <https://arxiv.org/abs/2501.18589>.
