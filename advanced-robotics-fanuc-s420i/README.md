# Advanced Robotics — FANUC S-420i

A MATLAB-based study of the **FANUC S-420i six-degree-of-freedom industrial robot**, prepared from the original 16-page Persian course report *پروژه درس رباتیک پیشرفته* (Amirkabir University of Technology, Ordibehesht 1401).

The repository keeps two complementary layers: the organized MATLAB implementation already in `matlab/`, and the **original student-submitted MATLAB scripts** preserved in `matlab/original/`. The report's visual material is represented below and indexed in `figures/FIGURE_INDEX.md`.

## Report figures

The overview below is assembled from the eight images embedded in the original report: the robot specification sheet, coordinate-frame drawing, DH parameter table, MATLAB/toolbox screenshots, and workspace/robot visualizations.

![Overview of figures extracted from the original FANUC S-420i report](figures/report-figures-overview.jpg)

See [the figure index](figures/FIGURE_INDEX.md) for the description of each source image. The full-resolution originals are preserved in the companion project archive.

## Project scope

The report and scripts cover:

- FANUC S-420i robot geometry and Denavit–Hartenberg parameters.
- Homogeneous transformation matrices and symbolic forward kinematics.
- End-effector position and orientation representations.
- Inverse-kinematics derivation.
- Geometric and analytical Jacobians.
- Singularity analysis and joint-space sampling.
- Workspace visualization and robot plotting.
- Lagrangian formulation of the dynamic model.
- Recursive Newton–Euler formulation.

## MATLAB source files

### Organized implementation

The following files are organized for readability and staged use:

| File | Purpose |
| --- | --- |
| `matlab/fanuc_s420i_dh.m` | DH parameters transcribed from the report |
| `matlab/dh_transform.m` | Homogeneous DH transformation |
| `matlab/01_forward_kinematics.m` | Symbolic forward kinematics and end-effector pose |
| `matlab/02_peter_corke_robot_model.m` | Peter Corke `SerialLink` robot model |
| `matlab/03_singularity_scan.m` | Joint-grid scan using the Jacobian determinant |
| `matlab/04_jacobian_comparison.m` | Geometric and differential Jacobian comparison |
| `matlab/05_lagrange_dynamics.m` | Lagrangian mass, Coriolis and gravity terms |
| `matlab/06_newton_euler_dynamics.m` | Recursive Newton–Euler dynamics |
| `matlab/07_peter_corke_rne_template.m` | Peter Corke RNE template and prerequisites |

### Original submitted files

These nine files were added as supplied, without silently repairing or rewriting their source:

| Original file | Main subject |
| --- | --- |
| `matlab/original/path_sim_6DOF.m` | Peter Corke model, motion plotting, forward kinematics, Jacobians and singularity scan |
| `matlab/original/Rot_rep.m` | Fixed XYZ angles, ZYZ Euler angles, angle-axis and quaternion representations |
| `matlab/original/Sinularities.m` | Geometric Jacobian and determinant-based singularity condition |
| `matlab/original/workspace.m` | Symbolic workspace sampling and plotting |
| `matlab/original/end_position.m` | Symbolic end-effector position |
| `matlab/original/forward.m` | Graphical robot motion and inverse-kinematics demo |
| `matlab/original/Inverse.m` | Symbolic inverse-kinematics derivation |
| `matlab/original/mycode.m` | Jacobian formulations and Lagrangian dynamics |
| `matlab/original/oyler.m` | Recursive Newton–Euler dynamics |

## Requirements and dependencies

- MATLAB.
- Symbolic Math Toolbox for symbolic transformations, Jacobians and dynamics.
- Peter Corke Robotics Toolbox for `Link`, `SerialLink`, `fkine`, `jacob0`, `jacobe` and robot plotting.
- The separate `ncgr_*` / `cgr_*` helper functions referenced by the original `forward.m` graphical demo.

Add the relevant MATLAB folders to the MATLAB path. The organized scripts are intended as the clearer starting point; the original scripts are retained for traceability to the submitted work.

## Source notes and verification

- The original scripts have been preserved, not represented as fully validated or production-ready code.
- The original `forward.m` identifies its graphical example as SCARA and calls external `ncgr_*` / `cgr_*` functions that are not included in the submitted files.
- The original workspace script references `Tee`, which is not defined in that file as supplied.
- The initial joint vector in `path_sim_6DOF.m` is `[-pi/4,ldots,-pi/4]`, while the listed joint limits begin at zero; this mismatch is documented in [EXTRACTION_NOTES.md](EXTRACTION_NOTES.md).
- The report does not provide complete numerical link masses, centres of mass and inertia tensors. Therefore the dynamics scripts remain symbolic and require those physical parameters for numerical validation.
- MATLAB execution and numerical validation have not been performed in this environment.

## Repository layout

```text
advanced-robotics-fanuc-s420i/
├── README.md
├── EXTRACTION_NOTES.md
├── extraction_inventory.json
├── figures/
│   ├── report-figures-overview.jpg
│   └── FIGURE_INDEX.md
├── matlab/
│   ├── ... organized MATLAB scripts
│   └── original/
│       ├── ... nine original submitted .m files
└── source-extracted/
    └── ... code blocks extracted from the report
```
