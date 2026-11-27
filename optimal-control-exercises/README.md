# Optimal Control Exercises

A source-code extraction and research-portfolio entry based on the 57-page document **تمرینهای کنترل بهینه** (*Optimal Control Exercises*) by Seyedhossein Seyedhosseini and Homa Golestaninejad.

The material studies a delayed bilateral teleoperation master–slave system and applies several optimal-control formulations. The source discusses communication **delay** and uncertainty, and motivates a cost with terminal accuracy, tracking, and control-effort terms (including a telesurgery example).

## MATLAB implementations

| File | Method |
| --- | --- |
| [01_teleoperation_dynamic_programming.m](matlab/01_teleoperation_dynamic_programming.m) | Delayed teleoperation model and finite-horizon dynamic programming |
| [02_hjb_riccati_lqr.m](matlab/02_hjb_riccati_lqr.m) | HJB / Riccati LQR implementation |
| [03_hamiltonian_lqr.m](matlab/03_hamiltonian_lqr.m) | Hamiltonian LQR with unconstrained inputs |
| [04_hamiltonian_lqt_tracking.m](matlab/04_hamiltonian_lqt_tracking.m) | Linear-quadratic tracking of a sinusoidal reference |
| [05_pontryagin_lqr_input_constraints.m](matlab/05_pontryagin_lqr_input_constraints.m) | Pontryagin formulation with bounded control inputs |

## Simulink function

- [euler_constrained_fcn.m](simulink/euler_constrained_fcn.m) — MATLAB Function block source for the state, costate, and accumulated input-energy derivatives.

## Model and methods

The teleoperation setup contains coupled **Master** and **Slave** robot dynamics. The source identifies communication **Delay** as a central limitation, with uncertainty also mentioned. Its cost discussion separates terminal-position accuracy, tracking performance, and operator/control effort.

The extracted code covers:
- finite-horizon dynamic programming;
- HJB/Riccati recursion;
- Hamiltonian LQR;
- LQT reference tracking;
- Pontryagin-based bounded-input control;
- state/costate dynamics implemented as a Simulink MATLAB Function.

## How to use

1. Open the .m files in MATLAB.
2. Run the standalone scripts after reviewing EXTRACTION_NOTES.md.
3. To use simulink/euler_constrained_fcn.m, copy the function body into a Simulink **MATLAB Function** block or adapt the block interface to the model.
4. Review the source-preserved recursion indexing and assumptions before relying on numerical outputs.

## Important limitations

- The uploaded DOCX includes a Simulink diagram screenshot and a MATLAB Function code listing, but it does **not** include an executable .slx model.
- The source's unconstrained Euler section and final numerical-methods section do not provide complete standalone code in the uploaded document.
- The Pontryagin script has two MATLAB else(condition) syntax issues in the source; these are normalized to plain else in the extracted file and documented in EXTRACTION_NOTES.md.
- The scripts have been extracted and organized but have not been executed in MATLAB/Simulink in this environment.
