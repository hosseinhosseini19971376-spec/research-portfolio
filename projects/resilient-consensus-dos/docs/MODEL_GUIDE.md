# Model Guide

This guide describes the three original Simulink files as supplied. It is based on inspection of the SLX package contents and embedded MATLAB Function scripts; it does not replace execution-based validation.

## 1. withoutDOS.slx — nominal reference model

- Six-node network with one reference/leader and five followers in the model structure.
- Four-state linear agent model.
- Fixed graph coupling in the plant/controller and observer functions.
- Distributed observer with output-injection term.
- No tuvar From Workspace input was found.
- Stored stop time: 30 s.
- Solver configuration: variable-step automatic.

## 2. withDOS.slx — DoS-affected observer model

The observer function receives a DOS input and constructs a Laplacian whose entries depend on that signal. The active plant/controller MATLAB Function uses a fixed Laplacian and does not use a DOS argument.

- Six-node network.
- Observer parameters: \(c=2\), \(\theta=5\).
- Stored stop time: 5 s.
- Solver configuration: variable-step automatic.
- Contains a From Workspace block configured to read tuvar.

## 3. RESILIENT.slx — extended observer-model variant

The observer function receives DOS and defines matrices R, LO, L, and LC. Its active derivative expression uses the stacked system matrix, the DoS-dependent Laplacian, and the observer error-injection term. It does not apply a state-reset operation using R.

The plant/controller MATLAB Function receives a DOS input but uses a fixed Laplacian in its active derivative expression.

- Six-node network.
- Observer parameters: \(c=2\), \(\theta=5\).
- Stored stop time: 10 s.
- Solver configuration: variable-step automatic.
- Contains a From Workspace block configured to read tuvar.

## Common embedded model parameters

\[
A=\begin{bmatrix}
0&1&0&0\\
-48.6&-1.26&48.6&0\\
0&0&0&10\\
1.95&0&-1.95&0
\end{bmatrix},\quad
B=\begin{bmatrix}0\\21.6\\0\\0\end{bmatrix}
\]

\[
C=\begin{bmatrix}1&0&1&-1\\0&1&0&0\end{bmatrix}
\]

The embedded gain matrices are:

\[
K=\begin{bmatrix}79.1094&5.2218&-29.6598&163.9093\end{bmatrix}
\]

\[
H=\begin{bmatrix}
3.0849&0.6931\\
2.4258&34.9384\\
7.0235&3.5334\\
0.54&1.8007
\end{bmatrix}
\]

The stacked network terms use \(A_0=I_6\otimes A\), \(Z_1=L\otimes(BK)\), and \(Z_2=L\otimes(HC)\).

## Consensus-error output

The embedded consensus-error function is:

\[
e=0.2\left\|\sum_{i=1}^{5}(x_i-X_o)\right\|
\]

This expression should not be described as the average of individual leader-following error norms. The separate observer-estimation error function uses \(\|X-\hat X\|\), while another function outputs the vector difference \(X-\hat X\).

## Implementation differences to retain in any interpretation

- The DoS-dependent Laplacian is used in the observer function of withDOS.slx and RESILIENT.slx.
- The active plant/controller function in both DoS-enabled files uses a fixed nominal Laplacian.
- RESILIENT.slx defines R, LO, and LC, but the active observer derivative does not apply a reset operation using R.
- The stored simulation stop times differ between the model variants.
- Both DoS-enabled variants require the original tuvar workspace signal.

These details mean the supplied files should be presented as a simulation study of selected observer-based DoS-resilient consensus structures, not as a verified reproduction of every scenario and mechanism in the paper.
