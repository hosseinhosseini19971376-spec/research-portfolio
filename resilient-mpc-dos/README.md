# Resilient Model Predictive Control for Cyber-Physical Systems under DoS Attacks

A MATLAB/Simulink research project on resilient predictive control for cyber-physical systems (CPSs) exposed to Denial-of-Service (DoS) communication interruptions. The report compares LQR, state-space MPC, and Laguerre MPC, and describes an observer-based output predictor to compensate for unavailable measurement packets.

> **Source archive:** The original simulation bundle is committed at [source/original-simulation-bundle.zip](source/original-simulation-bundle.zip). It contains the supplied Simulink models, MATLAB scripts, and simulation-result PDFs. The eight-page report's extracted text is included at [report/report-extracted.txt](report/report-extracted.txt).

## Research objectives

- Model measurement-channel DoS interruptions using attack-duration and attack-frequency assumptions.
- Compare LQR, state-space MPC, and Laguerre MPC for single-agent and multi-agent CPS examples.
- Use observer-based state/output prediction to maintain feedback when measurements are unavailable.
- Examine leaderless consensus and leader–follower coordination under interrupted communication.

## Case studies in the supplied report

### UPS systems
Single and multi-unit UPS examples compare state trajectories, error norms, and control effort. The supplied result PDFs include normal operation, attacked operation, and a comparison of LQR, state-space MPC, and Laguerre MPC.

### Unstable microgrid
The report studies an unstable linear microgrid and a distributed multi-agent extension, focusing on stability, voltage regulation, and consensus when sensor/observer communication is interrupted.

### Six single-link manipulators
A leader–follower multi-agent case study considers six single-link manipulators driven by DC motors. The report specifies a 0.01 s network transmission period and gives the observer/controller coupling and design parameters.

## Algorithms and architecture

- **LQR:** linear-quadratic feedback control.
- **State-space MPC:** receding-horizon optimization based on predicted system outputs.
- **Laguerre MPC:** MPC parameterized using Laguerre functions.
- **Observer-based resilient prediction:** estimates/predicts unavailable measurement information during DoS intervals so control can continue using reconstructed data.

## Original package inventory

The original simulation archive contains:
- 11 Simulink models (.slx): 5 UPS, 3 microgrid, and 3 manipulator models.
- 3 MATLAB scripts (.m): one associated with each case-study group.
- 5 simulation-result PDFs: two UPS, one microgrid, and two manipulator plots.

See [ASSET_INVENTORY.md](ASSET_INVENTORY.md) for exact filenames and inspection notes.

## MATLAB / Simulink compatibility and reproducibility

The model metadata identifies MATLAB/Simulink **R2018b** as the saved release.

The submitted bundle is not a verified one-click reproduction package:
- Ten of the eleven inspected Simulink models contain From Workspace blocks referencing simulink_input and/or tuvar.
- No standalone .mat input-data file or separate data-generation script defining these workspace inputs is included.
- The active portions of the UPS and microgrid initialization scripts use logged simulation variables such as DOS and recorded state/error/control signals for plotting; much of their parameter setup is commented out.
- The manipulator initialization script defines system matrices and controller-related parameters, but does not define the From Workspace input signals. It also begins with clear, so required workspace inputs must be prepared after running it.

The supplied result plots are retained as reported simulation evidence. An independent end-to-end rerun has not been verified from the submitted files alone.

## Reference cited in the report

Longjie Zhang, Yong Chen, and Meng Li, “Resilient predictive control for cyber–physical systems under denial-of-service attacks,” *IEEE Transactions on Circuits and Systems II: Express Briefs*, vol. 69, no. 1, pp. 144–148, 2021.

The report's complete bibliography is preserved in the text extraction.
