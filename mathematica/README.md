# Nuclear High-Spin VPC

This repository contains Wolfram Mathematica notebooks for numerical studies of VPC control sequences in high-spin nuclear systems. The current notebooks focus on spin `I = 3/2`, `I = 5/2`, and `I = 7/2`.

The notebooks construct spin operators, build phase-dependent control Hamiltonians, search VPC phase sequences that improve spin squeezing, and compare the resulting states with squeezed-state, cat-state, OAT, TACT, and Wineland-type benchmarks. The repository is intended as a research notebook collection rather than a packaged software library.

## Requirements

- Wolfram Mathematica 14.0 or newer is recommended. The notebooks were created with Mathematica 14.0.
- The visible code mainly uses built-in Mathematica functions such as `MatrixExp`, `MatrixPower`, `DensityPlot`, `ContourPlot`, `ListPlot`, and matrix operations.
- Some searches use random initial phases through `RandomReal`. To reproduce a numerical search exactly, set a seed with `SeedRandom[...]` before the search cells, or keep the saved output cells already stored in the notebooks.
- Re-running the full search notebooks may take time, especially for the `I = 5/2` and `I = 7/2` cases.

## File Naming

- `3half2`, `5half2`, and `7half2` denote spin `I = 3/2`, `I = 5/2`, and `I = 7/2`.
- In the density-plot filenames, `3haf2`, `5haf2`, and `7haf2` refer to the same spin values.
- `0p5`, `0p408`, and `0p314` denote fixed total evolution times `0.5`, `0.408`, and `0.314`.

## Notebook Guide

| Notebook | Main purpose |
| --- | --- |
| `VPC Sequence search 3half2.nb` | Searches VPC phase sequences for spin `I = 3/2`. It constructs the spin matrices, defines the phase-dependent Hamiltonian, evolves spin-coherent initial states, scans random phase choices, and records the best squeezing values and durations. |
| `VPC Sequence search 5half2.nb` | Same workflow as the `3/2` search notebook, adapted to spin `I = 5/2` with five phase parameters. |
| `VPC Sequence search 7half2.nb` | Same workflow as the `3/2` and `5/2` search notebooks, adapted to spin `I = 7/2` with seven phase parameters. |
| `density plot profile 3haf2 0p5.nb` | Visualizes the squeezing landscape for the `I = 3/2` case at fixed total evolution time `t = 0.5`. It uses density/profile plots to show how the squeezing result changes with phase parameters. |
| `density plot profile 5haf2 0p408.nb` | Visualizes the corresponding parameter landscape for `I = 5/2` at fixed total evolution time `t = 0.408`. |
| `density plot profile 7haf2 0p314.nb` | Visualizes the corresponding parameter landscape for `I = 7/2` at fixed total evolution time `t = 0.314`. |
| `3half2SolutionCompare.nb` | Compares alternative candidate solutions for the spin `I = 3/2` case, including VPC-style evolution and reference twisting evolutions such as `Iz.Iz`. |
| `no decoherence and linear plot.nb` | Collects comparison plots for optimal results without decoherence, additional noisy/decoherence-related comparisons, linear-scale plots, initial-point analysis, and spin-coherent-state evolution. |
| `TACT and Wineland plot.nb` | Compares VPC results with OAT/TACT-style reference protocols and Wineland-type squeezing curves for `I = 3/2`, `I = 5/2`, and `I = 7/2`. It also contains master-equation/decay backup sections. |
| `Squeeze and Cat state compare Fidelity.nb` | Computes fidelities between generated states and target squeezed/cat states. It includes sections for `I = 3/2`, `I = 5/2`, `I = 7/2`, and combined comparison plots. |

## Numerical Workflow

The notebooks follow the same general structure:

1. Construct spin matrices `Ix`, `Iy`, and `Iz` for a chosen spin value `I`.
2. Define a phase-dependent VPC Hamiltonian, usually written in the notebooks as `Hmuti[...]`.
3. Build the unitary evolution operator with `MatrixExp[-I H t]`.
4. Prepare a spin-coherent initial state parameterized by angles `theta` and `phi`.
5. Evolve the state and compute observables along the mean-spin direction and transverse directions.
6. Evaluate squeezing-related quantities, including Wineland-type squeezing in the comparison notebooks.
7. Search over phase parameters and total durations, storing values such as `SqueezeTable`, `SqueezeTableduration`, and `MinSqueeze`.
8. Compare the optimized VPC results with reference states or protocols such as squeezed states, cat states, OAT, and TACT.

## Suggested Running Order

For reproducing the main calculations, a useful order is:

1. Run one of the `VPC Sequence search ... .nb` notebooks for the desired spin value.
2. Use the matching `density plot profile ... .nb` notebook to inspect the parameter landscape near the selected total evolution time.
3. Use `3half2SolutionCompare.nb` for detailed checks of the `I = 3/2` case.
4. Use `no decoherence and linear plot.nb` to compare optimal curves without decoherence and with noise-related variants.
5. Use `TACT and Wineland plot.nb` to compare VPC squeezing curves with OAT/TACT and Wineland-type benchmarks.
6. Use `Squeeze and Cat state compare Fidelity.nb` to evaluate fidelities with target squeezed and cat states.

When re-running notebooks from scratch, it is best to start from a clean Mathematica kernel and evaluate cells from top to bottom. The notebooks already contain stored output cells, so opening them may show previous results even before re-evaluation.

## Important Variables and Functions

Common functions and variables used across the notebooks include:

- `SpinMatrices[s]`: constructs the spin matrices for spin `s`.
- `Hmuti[...]`: phase-dependent Hamiltonian used for VPC sequence evolution.
- `UHmuti[...]`: unitary evolution generated by the VPC Hamiltonian.
- `StateThetaPhiInitial[...]`: spin-coherent initial state as a function of angular parameters.
- `StateEvo[...]`: evolved state after applying the VPC sequence.
- `SqueezeTable`: table of squeezing values collected during parameter scans.
- `SqueezeTableduration`: best squeezing values as a function of duration or scan index.
- `MinSqueeze`: extracted minimum squeezing values from the search.
- `Fidelity[rho, sigma]`: density-matrix fidelity used in the squeezed/cat-state comparison notebook.

The exact Mathematica names may display Greek symbols in the notebook interface, for example `theta`, `phi`, and related phase parameters.

## Notes

- These are exploratory research notebooks. Many definitions are repeated across files so that each notebook can be opened and run independently.
- GitHub may not render large Mathematica notebooks smoothly. For the best experience, open the `.nb` files directly in Wolfram Mathematica.
- Some export cells may write figures to local paths. Update those paths before re-running exports on a different computer.
- Because some searches use random initial phase guesses, newly generated numerical results can differ slightly unless a fixed random seed is used.

