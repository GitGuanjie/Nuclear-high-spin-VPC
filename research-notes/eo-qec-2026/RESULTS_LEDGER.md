# Evidence ledger for R138–R154

Every result below is computational. "Negative" means a bounded search or specified construction family, not a universal no-go theorem.

| Round | Key result or constraint |
|---|---|
| R138 | Exact simultaneous reparameterization of CZ; modest noise gains, no bridge gain cancellation. |
| R139 | Short 24/26/28-control CZ Pareto candidates; accurate positive simultaneous controls. |
| R140 | Four-spin exact spectral revival; direct identity insertion worsens static noise. |
| R141 | Positive-exchange reflector frame, but four-spin-only core cannot supply the full specified two-EO CZ. |
| R142 | Additional five-spin endpoint directions; 26-control bridge/IID points, not new overall static optimum. |
| **R143** | **30C/19D exact CZ: Hpb 32.011918, H34 8.945056, Hiid 43.539274.** No J34 cancellation. |
| R144 | Isolated H34 7.860740 at 32C, but Hpb 49.780782: unfavorable noise trade-off. |
| R145 | J56 participation opens new directions; positive-cone local obstruction near previous seed and worse mirror frame. |
| **R146** | **Six-layer 12-control dual-axis gain-flat 3-spin logical SWAP**, fourth-order static-noise scaling for isolated triple, not encoded two-EO protection. |
| R147 | Six-spin projector cone permits idealized harmful-error cancellation, but requires costly nonphysical weighting. |
| R148 | Up to four complete SWAP identity-loop additions do not improve the certified static baseline. |
| R149 | Nonzero nested commutator involving J34, J45, J56; 35-control six-spin CZ is exact but noisier. |
| R150 | Two-bond commutator Q direction more promising than one nested three-bond direction in idealized budgets. |
| R151 | Positive exchange can produce signed Q *components* but not pure Q static-error derivatives; loop insertion worse. |
| R152 | New 32-control simultaneous exact branch, total static harm around 53; finite area constraints matter. |
| **R153** | Verified full nine-spin 50C ZZ / 62C XX Kraus instruments. J56 is an important syndrome-error bond. |
| **R154** | **48C ZZ / 60C XX**, including measurement-boundary pruning and alternate ancilla preparation. Star-graph 15-spin 92C ZZZZ / 116C XXXX reference calculations. |

## Scientific interpretation

- Preserve the distinction between physical 8D three-spin, encoded 64D two-EO, nine-spin 512D instrument and 15-spin 32768D state-vector calculations.
- Distinguish per-bond shot-static gain, independent per-control jitter and hypothetical simultaneous context errors.
- A correct weight-four measurement must preserve coherence inside each stabilizer parity sector; classically multiplying two separate two-body measurement outcomes is not equivalent.
- Correct gate endpoints are necessary, not sufficient: leakage, syndrome error, time and repeated-cycle behavior must all be included before fault-tolerance claims.
