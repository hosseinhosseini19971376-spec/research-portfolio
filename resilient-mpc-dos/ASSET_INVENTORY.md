# Original simulation asset inventory

The original uploaded archive contains 23 ZIP entries (including directory entries) and the following project assets.

## Simulink models — 11

### UPS systems (5)
- LQR.slx
- laguerre.slx
- state-space.slx
- with-attack.slx
- without-attack.slx

### Microgrid / distributed cooperative control (3)
- Resilient MPC.slx
- With-Attack.slx
- without-attack.slx

### Manipulators (3)
- Resilient-MPC.slx
- With-Attack.slx
- Without-Attack.slx

## MATLAB scripts — 3
- UPS: initialization.m
- Microgrid: Initialization.m
- Manipulators: Initialization.m

## Simulation-result PDFs — 5
- UPS: ups1.pdf, ups2.pdf
- Microgrid: Figure.pdf
- Manipulators: x.pdf, xo.pdf

## Report
- mpc_project_Report.pdf — 8 pages.

## Inspection findings

- Simulink model metadata identifies MATLAB/Simulink R2018b as the saved version.
- Ten models contain From Workspace references to simulink_input and/or tuvar; the archive contains no separate .mat input dataset.
- The UPS and microgrid scripts have parameter-initialization sections commented out; their active sections read DOS and logged output signals for plotting.
- The manipulator script actively defines model matrices and controller parameters, but does not define the From Workspace inputs.
