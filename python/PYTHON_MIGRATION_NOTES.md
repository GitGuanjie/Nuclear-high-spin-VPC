# Mathematica -> Python migration notes

## Direct translations

- Mathematica `SpinMatrices[s]` -> `vpc.core.spin_matrices(I)`.
- Mathematica `StateθφInitial[θ,φ]` -> `vpc.core.css_state(I, theta, phi)` using the same rotation convention.
- Mathematica `Hmuti[φ1,...]` -> `vpc.core.h_vpc(I, phases)`.
- `MatrixExp[-I H t] . state` -> `vpc.core.unitary_state` or the exact fast `vpc_state_fast` implementation.
- KU squeezing -> `xi_ku` with the revised manuscript normalization `2 Var_min/I`.
- Wineland squeezing -> `xi_wineland` with `2 I Var_min/|<I>|^2`.
- Mathematica master-equation calculations -> explicit Lindblad superoperator in `evolve_lindblad`.
- Mathematica fidelity calculation -> `fidelity`.

## Exact optimization acceleration

For the open transition chain, the phase-controlled VPC Hamiltonian satisfies

`H_VPC(phases) = D Ix D^dagger`

for a diagonal phase matrix D. Therefore the Python optimizer evaluates

`D exp(-i Ix t) D^dagger |psi0>`

instead of calling a fresh matrix exponential at every objective evaluation. This is an exact algebraic identity, not an approximation. `scripts/validate_core.py` verifies it against direct `expm(-i H_VPC t)` for all three spins with errors around 1e-16.

## Reviewer 2 changes

- TACT comparison is recomputed with the polar `CSS_z=|I,I>` initial state.
- Fig. 2: corrected TACT(CSS_z) is included together with the old CSS_y curve for transparency.
- Fig. 6: TACT noise curves use CSS_z and all noisy channels start at t=0.
- Fig. 7: both CSS_y and corrected CSS_z TACT curves are available under Iz^2 noise.
- Fig. 12: both TACT initial states are available and VPC can be reoptimized directly for the Wineland cost.
- Conclusions should be stated as a speed–depth/noise-channel tradeoff, not as universal VPC superiority.

## Generated evidence

Everything in `results/` was created by the Python scripts. The key numerical validation is in `validation_summary.json` and `key_results_python.csv`.
