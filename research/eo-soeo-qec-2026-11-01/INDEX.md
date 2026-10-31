# Exchange-only / SOEO spin-qubit research (working draft)

**Status: numerical/theoretical research archive; not peer reviewed or an experimental demonstration.**

This directory consolidates results on robust single-qubit EO/SOEO gates, SOEO spin-sector detection, and limitations of encoded EO entangling gates.

- [Read the research paper (Markdown)](PAPER.md)
- [Read the research paper (PDF)](PAPER.pdf)
- [Reproduction guide](README.md) / [中文说明](README_CN.md)
- [Physical verification code](code/)
- [Exchange pulse sequences](sequences/)
- [Reproduction evidence](evidence/)
- [Complete source archive](EO_SOEO_QEC_RESEARCH_PAPER_AND_CODE_20261101.zip)

## Selected verified results

- First-order quasi-static per-bond gain compensated positive-exchange 11P H and 13P S/Z, on EO and SOEO encoded spaces, with gauge/leakage checks (numerical).
- Four-coupling spin-sector revival in a **simultaneous-J** star geometry, which protects an identity operation and realizes probabilistic singlet-versus-nonsinglet detection (analytical/numerical, not a serial gate).
- A 43P to 41P physical-unitary-preserving rewrite of a locally rotated controlled phase; reduced the selected gain-response coefficient but **does not** cancel inter-block bond gains.
- Restricted single-cross-bond obstructions; no proof of general entangler impossibility.

No all-bond first-order-robust CZ, hardware threshold, or complete multi-round QEC code is claimed. See the paper for full definitions and limitations.
