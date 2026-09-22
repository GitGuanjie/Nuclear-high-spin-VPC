# Mathematica -> Python migration notes

## Direct translations

- Mathematica `SpinMatrices[s]` -> `vpc.core.spin_matrices(I)`.
- Mathematica `StateθφInitial[θ,φ]` -> `vpc.core.css_state(I, theta, phi)` using the same rotation convention.
- Mathematica `Hmuti[φ1,...]` -> `vpc.core.h_vpc(I, phases)`.
- `MatrixExp[-I H t] . state` -> `vpc.core.unitary_state` or the exact fast `vpc_state_fast` implementation.
- KU squeezing -> `xi_ku` with the normalization used in the present calculations `2 Var_min/I`.
- Wineland squeezing -> `xi_wineland` with `2 I Var_min/|<I>|^2`.
- Mathematica master-equation calculations -> explicit Lindblad superoperator in `evolve_lindblad`.
- Mathematica fidelity calculation -> `fidelity`.

## Exact optimization acceleration

For the open transition chain, the phase-controlled VPC Hamiltonian satisfies

`H_VPC(phases) = D Ix D^dagger`

for a diagonal phase matrix D. Therefore the Python optimizer evaluates

`D exp(-i Ix t) D^dagger |psi0>`

instead of calling a fresh matrix exponential at every objective evaluation. This is an exact algebraic identity, not an approximation. `scripts/validate_core.py` verifies it against direct `expm(-i H_VPC t)` for all three spins with errors around 1e-16.

## TACT benchmark and related updates

- The TACT comparison includes the polar `CSS_z=|I,I>` initial state as the primary benchmark.
- Fig. 2 includes TACT dynamics from both `CSS_z` and the equatorial `CSS_y` state for comparison.
- Fig. 6 uses `CSS_z` for the TACT noise curves, with all noisy channels active from `t=0`.
- Fig. 7 includes both `CSS_y` and `CSS_z` TACT curves under `Iz^2` noise.
- Fig. 12 includes both TACT initial states, and VPC can be optimized directly for the Wineland cost.
- The resulting comparison exhibits a speed-depth/noise-channel tradeoff rather than a universal advantage of either protocol.

## Generated evidence

Everything in `results/` was created by the Python scripts. The key numerical validation is in `validation_summary.json` and `key_results_python.csv`.
