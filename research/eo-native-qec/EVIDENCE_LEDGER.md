# Evidence ledger and limits

**Status:** selected findings from previous numerical research archives, reviewed for terminology and claim boundaries. This snapshot was not a fresh exhaustive rerun of those computations.

| Claim | Source | Evidence type | Critical limitation |
|---|---|---|---|
| 92P/44D native encoded ZZZZ | `EO_QEC_NATIVE_92P_100P_53P_RESULTS_20261030.zip` | Reported physical 15-spin simulation and parity branch check | Proposed layout; ideal encoded readout |
| 100P/45D fixed-frame logical XXXX | Same | Reported physical 15-spin simulation | Not fault tolerant; under the chosen static-gain model can be worse than 116P |
| 92P/44D rotated-X check | `EO_ROTATED_CHECK_92P_GAUGE_ROBUST_20261030.zip` | Full gauge nominal tests, static tangent comparison | Requires consistent global logical-Pauli frame |
| 140P/60D 18-spin flag | `EO_QEC_140P_FLAG_NATIVE_RESULTS_20261031.zip` | 96 selected physical input tests; encoded ancilla hook injections; 240-draw one-check MC | NOT exhaustive all data inputs, pulse fault types, or real POVMs |
| 32/92 unflagged vs 0/140 flagged first-check pulse locations causing accepted encoded logical transition | `EO_QEC_FLAGGED_LOGICAL_AUDIT_20261031.zip` | Full physical tangent scan at all first-check positions, two selected flagged initial codeword/gauge settings | Later two checks assumed ideal; not arbitrary noise or input certification |
| 105 sampled two-spin Pauli faults, no accepted encoded transition on one input | Same | 15 nontrivial 2-spin Pauli errors at seven pulse positions | Does not cover all 140 pulse locations; leakage persists |
| 276P vs 324P three-check conditional encoded logical error 0.06682% vs 0.03744% | Same | Paired 50-draw physical per-bond gain MC, persistent gain + IID jitter | One input/gauge, ideal readout/reset, no decoded QEC |
| Star-coupled SOEO spin-sector probe, ideal quartic single-bond scaling | `EO_EXCHANGE_ONLY_QEC_ADVANCE_20261030.zip` | Ideal simultaneous-coupling numerical and analytic restricted model | Requires four equal couplings simultaneously; not strict serial |

## Metric definitions that must not be conflated

- **Nominal ideal residual** tests correct measurement-unitary/instrument action without noise. It does not measure a device fidelity.
- **First-order tangent / coefficient** is a local small-parameter sensitivity. A zero accepted encoded-codeword transition does not imply zero leakage or universal fault tolerance.
- **Per-attempt logical failure** and **conditional-on-acceptance logical failure** differ, and both differ from distance-three decoded logical error.
- **Accept/reject fraction** is not throughput until physical readout, reset, discarded attempts, and wall-clock latency are included.
- **The $\widetilde X$ frame** is a rotated encoded Pauli operator, not the same fixed-frame physical operation as the original $X_L$.

## What should be published only after independent checks

Review source pulse CSV branch conventions, verify operator-level gauge identities and 18-spin no-fault action for all encoded input columns, run a complete all-component/Pauli-fault audit with physically grounded readout, and reproduce the 50 paired gain samples across multiple codewords and gauge patterns. A code-level distance-three detector model and real decoder are necessary before any claim about fault-tolerant QEC or threshold.