# Implementation Notes

## State-space model

The MATLAB Function blocks define a four-state agent:

\[
\dot x_i=Ax_i+Bu_i,\qquad y_i=Cx_i
\]

with the matrices \(A\), \(B\), and \(C\) listed in the [Model Guide](MODEL_GUIDE.md).

## Distributed controller and observer

The embedded scripts build stacked multi-agent terms using Kronecker products:

\[
A_0=I_6\otimes A
\]

\[
Z_1=L\otimes(BK),\qquad Z_2=L\otimes(HC)
\]

The active plant derivative has the form:

\[
\dot X=A_0X-cZ_1\hat X
\]

The observer derivative has the form:

\[
\dot{\hat X}=(A_0-cZ_1)\hat X+\theta Z_2\hat e
\]

where \(c=2\) and \(\theta=5\). In the DoS-enabled observer variants, the observer-side Laplacian \(L\) is modified as a function of the DOS input.

## DoS topology implementation

In withDOS.slx and RESILIENT.slx, the observer function replaces selected entries of the nominal graph Laplacian with expressions involving DOS. This changes the observer communication topology as the signal changes.

The active plant/controller function in these models retains the fixed nominal Laplacian. Consequently, the supplied implementation does not demonstrate simultaneous DoS disruption of both the controller and observer communication networks.

## Extended RESILIENT variant

The observer function defines additional matrices R, LO, and LC. However, the active observer derivative expression does not use R to reset or reconstruct the state. The plant/controller function also receives a DOS input that is not used in its active derivative expression.

For this reason, the model is documented as an extended variant whose full reset-based resilience mechanism remains unverified.

## Error signals

The consensus-error function is:

\[
e=0.2\left\|\sum_{i=1}^{5}(x_i-X_o)\right\|
\]

It is not the average of five separate norms. The observer error is represented by either the vector difference \(X-\hat X\) or its norm, depending on the MATLAB Function block.

## Validation boundary

These notes describe code extracted from the supplied Simulink files. They do not establish that the models run successfully, that the chosen attack signal matches the paper's constraints, or that the plotted outputs satisfy the paper's theoretical convergence claims. Those points require the original experiment inputs and an execution/validation pass in MATLAB/Simulink.
