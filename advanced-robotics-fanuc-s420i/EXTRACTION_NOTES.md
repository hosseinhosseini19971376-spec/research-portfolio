# Extraction notes — FANUC S-420i

## Report content

The 16-page source identifies a six-axis FANUC S-420i robot and includes a manufacturer specification image, joint-frame diagram, DH table, forward kinematics, a Peter Corke robot model, a Jacobian derivation by two methods, Lagrangian dynamics, recursive Newton-Euler dynamics, and workspace/robot-scene figures.

## DH values transcribed from the report

| Joint | a | alpha | d | theta |
|---:|---:|---:|---:|---|
| 1 | 0 | -90 deg | 1.0 | q1 |
| 2 | 0.95 | 0 deg | 0 | q2 - 90 deg |
| 3 | 0.24 | 90 deg | 0 | q3 |
| 4 | 0 | -90 deg | 1.3 | q4 |
| 5 | 0 | 90 deg | 0 | q5 |
| 6 | 0 | 0 deg | 0.2 | q6 |

The source does not explicitly state the length unit.

## Source limitations and ambiguities

1. The report shows a 3D workspace point-cloud figure, but the code under the workspace section is a joint-grid loop that evaluates det(jacob0(...)) and stores singular configurations. It is a singularity scan, not the point-cloud generation algorithm. The complete workspace-generation code is absent.
2. The report says a simulation video was attached separately. No video or executable Simulink/Simscape model is embedded in the supplied DOCX.
3. Numeric link masses, COM vectors/distances and complete inertia tensors are not supplied. The dynamics sections retain symbolic m1...m6, i1...i6 / I1...I6 and L1...L6.
4. The Peter Corke section comments describe links 2 and 3 as prismatic, but the shown Link([theta d a alpha]) constructors do not explicitly request prismatic joints. The source definitions are preserved; joint types must be checked against the robot manual.
5. The source assigns Th_1...Th_6 but calls fkine using teta1...teta6. The organized model uses q_home to avoid the undefined-variable mismatch.
6. The source singularity loop uses singular{i} and i=i+1 without showing initialization. The organized script initializes these and uses a determinant tolerance rather than exact equality to zero.
7. The source compares a matrix directly in an if expression for the Jacobian check. The organized script uses isequal on the simplified matrix difference.
8. The source reuses g for the gravity scalar and later the gravity vector. The organized scripts use g0 and Gvec.
9. The Newton-Euler recursion shown uses point-mass forces and COM distances; it does not include a complete rotational inertia-tensor contribution.
10. Peter Corke Robotics Toolbox method syntax may differ by release.

## Normalization

The source-extracted text file preserves the extracted source code blocks. The matlab scripts centralize shared DH data and resolve only clear variable/syntax issues. No missing workspace algorithm, physical parameters, or video/model file has been invented. MATLAB execution has not been verified in this environment.
