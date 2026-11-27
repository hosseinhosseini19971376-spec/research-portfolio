# MATLAB Function Blocks Extracted from the Original Models

This document records the MATLAB Function block scripts embedded in the three supplied SLX files. The code below is transcribed from the `simulink/stateflow.xml` entries inside each model archive. It is included to make the implementation inspectable in GitHub without requiring Simulink just to review the equations.

No code in the original SLX files has been changed by this extraction. These listings are source documentation, not a replacement for the executable models.

## Shared agent model

All variants use the same four-state agent matrices, feedback gain, and six-node nominal Laplacian where applicable:

\[
A=\begin{bmatrix}
0&1&0&0\\
-48.6&-1.26&48.6&0\\
0&0&0&10\\
1.95&0&-1.95&0
\end{bmatrix},\quad
B=\begin{bmatrix}0\\21.6\\0\\0\end{bmatrix},\quad
C=\begin{bmatrix}1&0&1&-1\\0&1&0&0\end{bmatrix}
\]

\[
K=\begin{bmatrix}79.1094&5.2218&-29.6598&163.9093\end{bmatrix}
\]

## withoutDOS.slx

### Observer state derivative — observer/MATLAB Function1

```matlab
function Xhat_dot = X(Xhat,ehat)
A=[0 1 0 0;-48.6 -1.26 48.6 0;0 0 0 10; 1.95 0 -1.95 0];
B=[0;21.6;0;0];
C=[1 0 1 -1;0 1 0 0];
c=2;
teta=5;
H=[3.0849 0.6931;2.4258 34.9384;7.0235 3.5334;.54 1.8007];
N=6;
L=[0 0 0 0 0 0;-1 2 0 0 0 -1;-1 -1 2 0 0 0;0 -1 0 1 0 0;0 0 -1 0 1 0;0 0 -1 -1 -1 3];
K=[79.1094 5.2218 -29.6598 163.9093];
A0=kron(eye(N),A);
z1=kron(L,B*K);
z2=kron(L,H*C);
Xhat_dot= (A0-c*z1)*Xhat+teta*(z2*ehat);
```

### Plant state derivative — system/MATLAB Function

```matlab
function X_dot = X(X,Xhat)
A=[0 1 0 0;-48.6 -1.26 48.6 0;0 0 0 10; 1.95 0 -1.95 0];
B=[0;21.6;0;0];
C=[1 0 1 -1;0 1 0 0];
c=2;
N=6;
L=[0 0 0 0 0 0;-1 2 0 0 0 -1;-1 -1 2 0 0 0;0 -1 0 1 0 0;0 0 -1 0 1 0;0 0 -1 -1 -1 3];
K=[79.1094 5.2218 -29.6598 163.9093];
A0=kron(eye(N),A);
z1=kron(L,B*K);
X_dot= A0*X-c*(z1*Xhat);
```

### Consensus error — e/MATLAB Function

```matlab
function e = fcn(x1,x2,x3,x4,x5,Xo)
e =0.2* norm(x1-Xo+x2-Xo+x3-Xo+x4-Xo+x5-Xo);
```

### Observer error norm — ehat/MATLAB Function

```matlab
function ehat = fcn(X,Xhat)
ehat = norm(X-Xhat);
```

### Observer error vector — observer/MATLAB Function

```matlab
function ehat = fcn(X,Xhat)
ehat =( X-Xhat);
```

## withDOS.slx

### DoS-dependent observer state derivative — observer/MATLAB Function1

```matlab
function Xhat_dot = X(Xhat,ehat,DOS)
A=[0 1 0 0;-48.6 -1.26 48.6 0;0 0 0 10; 1.95 0 -1.95 0];
B=[0;21.6;0;0];
C=[1 0 1 -1;0 1 0 0];
c=2;
teta=5;
H=[3.0849 0.6931;2.4258 34.9384;7.0235 3.5334;.54 1.8007];
N=6;
L=[0 0 0 0 0 0;-1 2 0 0 0 -1;-1 -1 2 0 0 0;0 -1 0 1 0 0;0 0 -1 0 1 0;0 0 -1 -1 -1 3];
%L=[0 0 0 0 0 0;-1 1 0 0 0 0;0 -1 1 0 0 0;0 0 0 0 0 0;0 0 -1 0 1 0;0 0 0 -1 -1 2];
L=[0 0 0 0 0 0;-1 2-DOS 0 0 0 -1+DOS;-1+DOS -1 2-DOS 0 0 0;0 -1+DOS 0 1-DOS 0 0;0 0 -1 0 1 0;0 0 -1+DOS -1 -1 3-DOS];
K=[79.1094 5.2218 -29.6598 163.9093];
A0=kron(eye(N),A);
z1=kron(L,B*K);
z2=kron(L,H*C);
Xhat_dot= (A0-c*z1)*Xhat+teta*(z2*ehat);
```

### Plant state derivative — system/MATLAB Function

The plant function is identical in its active expression to the nominal model and does not receive a DOS input:

```matlab
function X_dot = X(X,Xhat)
A=[0 1 0 0;-48.6 -1.26 48.6 0;0 0 0 10; 1.95 0 -1.95 0];
B=[0;21.6;0;0];
C=[1 0 1 -1;0 1 0 0];
c=2;
N=6;
L=[0 0 0 0 0 0;-1 2 0 0 0 -1;-1 -1 2 0 0 0;0 -1 0 1 0 0;0 0 -1 0 1 0;0 0 -1 -1 -1 3];
K=[79.1094 5.2218 -29.6598 163.9093];
A0=kron(eye(N),A);
z1=kron(L,B*K);
X_dot= A0*X-c*(z1*Xhat);
```

### Error functions

The consensus-error, observer-error-norm, and observer-error-vector functions are the same as those listed for withoutDOS.slx.

## RESILIENT.slx

### DoS-dependent observer state derivative — observer/MATLAB Function1

```matlab
function Xhat_dot = X(Xhat,ehat,DOS)
A=[0 1 0 0;-48.6 -1.26 48.6 0;0 0 0 10; 1.95 0 -1.95 0];
B=[0;21.6;0;0];
C=[1 0 1 -1;0 1 0 0];
c=2;
teta=5;
H=[3.0849 0.6931;2.4258 34.9384;7.0235 3.5334;.54 1.8007];
R=[-0.9886 0.0381;0 -1; -1.0405 .0402;-1.0291 0.0783]
N=6;
LO=[0 0 0 0 0 0;-1 1 0 0 0 0;0 -1 1 0 0 0;0 0 0 0 0 0;0 0 -1 0 1 0;0 0 0 -1 -1 2];
L=[0 0 0 0 0 0;-1 2-DOS 0 0 0 -1+DOS;-1+DOS -1 2-DOS 0 0 0;0 -1+DOS 0 1-DOS 0 0;0 0 -1 0 1 0;0 0 -1+DOS -1 -1 3-DOS];
LC=[0 0 0 0 0 0;0 0 0 0 0 0;-1 -1 2 0 0 0;0 -1 0 1 0 0;0 0 0 0 0 0;0 0 -1 -1 -1 3];
K=[79.1094 5.2218 -29.6598 163.9093];
A0=kron(eye(N),A);
z1=kron(L,B*K);
z2=kron(L,H*C);
Xhat_dot= (A0-c*z1)*Xhat+teta*(z2*ehat);
```

### Plant state derivative — system/MATLAB Function

```matlab
function X_dot = X(X,Xhat,DOS)
A=[0 1 0 0;-48.6 -1.26 48.6 0;0 0 0 10; 1.95 0 -1.95 0];
B=[0;21.6;0;0];
C=[1 0 1 -1;0 1 0 0];
c=2;
N=6;
L=[0 0 0 0 0 0;-1 2 0 0 0 -1;-1 -1 2 0 0 0;0 -1 0 1 0 0;0 0 -1 0 1 0;0 0 -1 -1 -1 3];
%Lo=[0 0 0 0 0 0;-1 1 0 0 0 0;0 -1 1 0 0 0;0 0 0 0 0 0;0 0 -1 0 1 0;0 0 0 -1 -1 2];
LC=[0 0 0 0 0 0;0 0 0 0 0 0;-1 -1 2 0 0 0;0 -1 0 1 0 0;0 0 0 0 0 0;0 0 -1 -1 -1 3];
%L=[0 0 0 0 0 0;-1+DOS 2-2*DOS 0 0 0 -1+DOS;-1 -1 2 0 0 0;0 -1 0 1 0 0;0 0 -1+DOS 0 1-DOS 0;0 0 -1 -1 -1 3];
K=[79.1094 5.2218 -29.6598 163.9093];
A0=kron(eye(N),A);
z1=kron(L,B*K);
X_dot= A0*X-c*(z1*Xhat);
```

### Error functions

The consensus-error, observer-error-norm, and observer-error-vector functions are the same as those listed for withoutDOS.slx.

## Interpretation notes

1. The DoS-dependent Laplacian is used in the observer function of withDOS.slx and RESILIENT.slx.
2. The active plant/controller function uses the fixed nominal Laplacian in all three model variants. In RESILIENT.slx the function signature includes DOS, but DOS is not used in the active derivative expression.
3. In RESILIENT.slx, R, LO, and LC are defined in the observer function, but R is not used in the active derivative expression to reset or reconstruct the observer state.
4. The consensus-error function computes the norm of the sum of the five follower-to-reference differences, multiplied by 0.2. It does not compute the average of five individual norms.
5. The DoS-enabled models require the original workspace variable tuvar. That signal was not present in the supplied source archive.
