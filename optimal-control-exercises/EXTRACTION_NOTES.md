# Extraction notes

## Source
- Uploaded source: 99123183_99123161docx.docx
- Document title: **تمرینهای کنترل بهینه** (Optimal Control Exercises)
- Authors shown on the title page: Seyedhossein Seyedhosseini and Homa Golestaninejad
- Length: 57 pages

## Extracted MATLAB / Simulink code
| File | Source content |
| --- | --- |
| matlab/01_teleoperation_dynamic_programming.m | Teleoperation master/slave model, delay-coupled matrices, finite-horizon dynamic-programming recursion, state/input simulation, and cost |
| matlab/02_hjb_riccati_lqr.m | HJB/Riccati LQR implementation |
| simulink/euler_constrained_fcn.m | MATLAB Function block for the constrained Euler/Pontryagin state-costate dynamics |
| matlab/03_hamiltonian_lqr.m | Hamiltonian LQR with unconstrained inputs |
| matlab/04_hamiltonian_lqt_tracking.m | LQT reference-tracking implementation |
| matlab/05_pontryagin_lqr_input_constraints.m | Pontryagin-based LQR with bounded control inputs |

## Extraction and normalization decisions
1. The source's first dynamic-programming section uses the overall A and B matrices but does not show their assembly in the same code block. Their assembly from A11, A12, A21, A22, B11, B12, B21, and B22 is made explicit in 01_teleoperation_dynamic_programming.m; the same assembly is explicitly shown later in the source.
2. In the Pontryagin script, the source contains two statements written as else(condition). MATLAB syntax requires a plain else; these two lines are normalized to else. The original conditions are already covered by the preceding if/elseif branches.
3. Other recursion formulas, parameter values, initial conditions, reference signals, and cost expressions are retained from the source. Their mathematical correctness and runtime behavior have not been independently certified.
4. The section titled **اویلر بدون محدودیت** and the final **تحلیل با روشهای عددی** heading do not contain a complete standalone code block in the uploaded DOCX; no missing implementation was invented.
5. The DOCX contains a screenshot of a Simulink block diagram and the MATLAB Function source code, but no .slx model file. The complete companion ZIP archive preserves the source images and converted figure previews; the GitHub commit focuses on the native MATLAB/Simulink source files and documentation.
6. MATLAB/Simulink is not available in this execution environment, so these files have been extracted and statically organized but not run in MATLAB.

## Figures and embedded media
The complete companion ZIP archive includes assets/source-images/ with all original embedded media (including EMF originals), and assets/converted-figures/ with PNG previews of the result plots, Simulink diagram screenshot, and handwritten derivation page.
