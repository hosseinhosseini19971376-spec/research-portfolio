# Advanced Robotics — FANUC S-420i

Source-code extraction and MATLAB project based on the 16-page Persian report "پروژه درس رباتیک پیشرفته" from Amirkabir University of Technology.

Robot: FANUC S-420i, six degrees of freedom.
Instructor: Dr. Iman Sharifi.
Students named in the report: Seyedhossein Seyedhosseini and Hadi Jafar Khani.
Date in source: Ordibehesht 1401.

## MATLAB files

| File | Purpose |
| --- | --- |
| matlab/fanuc_s420i_dh.m | DH values transcribed from the report |
| matlab/dh_transform.m | Standard DH homogeneous transform |
| matlab/01_forward_kinematics.m | Symbolic forward kinematics and end-effector pose |
| matlab/02_peter_corke_robot_model.m | Peter Corke SerialLink model |
| matlab/03_singularity_scan.m | Joint-grid scan using the Jacobian determinant |
| matlab/04_jacobian_comparison.m | Geometric and differential Jacobian comparison |
| matlab/05_lagrange_dynamics.m | Lagrangian M, C and gravity terms |
| matlab/06_newton_euler_dynamics.m | Recursive Newton-Euler dynamics |
| matlab/07_peter_corke_rne_template.m | Peter Corke RNE call and prerequisites |

## Source preservation

source-extracted/code_blocks_from_report.txt contains the code blocks extracted from the DOCX. EXTRACTION_NOTES.md documents missing material, ambiguities and normalization choices. The complete downloadable ZIP archive contains the original DOCX and all eight embedded figures.

## Requirements

- MATLAB.
- Symbolic Math Toolbox for symbolic kinematics, Jacobian and dynamics.
- Peter Corke Robotics Toolbox for Link, SerialLink, jacob0, jacobe, fkine, plot and rne.

Add the matlab folder to the MATLAB path. Suggested order: forward kinematics, Peter Corke model, singularity scan, Jacobian comparison, Lagrangian dynamics, Newton-Euler dynamics, then the RNE template after entering real dynamic parameters.

## Verification

The scripts have been organized from the source report but have not been executed in MATLAB in this environment. Numeric dynamics require complete link masses, COM locations and inertia data, which are not supplied in the report.
