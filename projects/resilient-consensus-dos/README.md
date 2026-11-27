# Resilient Consensus of Multi-Agent Systems Under Denial-of-Service (DoS) Attacks

**Research simulation study · MATLAB / Simulink**  
**Author:** Seyedhossein Seyedhosseini  
**Reference paper:** Zuo, Cao, Wang, and Zhang, *Resilient Consensus of Multiagent Systems Against Denial-of-Service Attacks*, IEEE Transactions on Systems, Man, and Cybernetics: Systems.  
**DOI:** [10.1109/TSMC.2021.3051730](https://doi.org/10.1109/TSMC.2021.3051730)

---

## Project overview

This project studies observer-based consensus control in a networked multi-agent system under communication denial-of-service (DoS) attacks. It translates selected equations and network structures from the reference paper into MATLAB/Simulink models and compares nominal and attack-dependent communication configurations.

The supplied models represent a six-node leader–follower network, with one reference node and five followers. Each agent is represented by a four-state linear model. The implementation combines graph-Laplacian coupling, a distributed state observer, state-feedback control, and consensus/estimation-error signals.

**Scope statement:** this is a simulation study based on selected elements of the reference paper, not a verified reproduction of every theorem, attack scenario, or resilience mechanism in the publication. The implementation differences and missing experiment inputs are documented below.

## Model variants

| Model | Purpose | Verified structure from the supplied file |
|---|---|---|
| **withoutDOS.slx** | Nominal baseline | Fixed communication Laplacian; no external tuvar input |
| **withDOS.slx** | DoS-dependent observer case | Observer Laplacian depends on the DOS input; plant/controller coupling remains fixed |
| **RESILIENT.slx** | Extended observer-model variant | Defines additional R, LO, and LC matrices; the active observer derivative does not apply a reset operation using R |

The Simulink model files are intended to be stored in the adjacent **models/** directory. See [models/README.md](models/README.md) for the current artifact status and the exact filenames.

## Technical approach

The MATLAB Function blocks embed the following agent model:

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
C=\begin{bmatrix}
1&0&1&-1\\
0&1&0&0
\end{bmatrix}
\]

The six-agent stacked model uses Kronecker products:

\[
A_0=I_6\otimes A,\qquad
Z_1=L\otimes(BK),\qquad
Z_2=L\otimes(HC)
\]

where \(L\) is the communication-graph Laplacian, \(K\) is the feedback gain, and \(H\) is the observer gain. The observer implementation uses \(c=2\) and \(\theta=5\).

For the DoS-enabled observer variants, the observer-side Laplacian is parameterized by the scalar DOS signal. The exact embedded matrices and function expressions are preserved in the original SLX files and summarized in [Implementation Notes](docs/IMPLEMENTATION_NOTES.md).

## Work represented in this project

- Studying the reference paper's observer-based distributed-control formulation.
- Translating the agent dynamics and graph-coupling equations into Simulink MATLAB Function blocks.
- Constructing a six-node leader–follower network model.
- Implementing nominal and DoS-dependent observer-topology variants.
- Exposing consensus and state-estimation error signals for analysis.
- Comparing model structures and documenting implementation and reproducibility limitations.

## Reproducibility status

The original package contains three Simulink model files. However, the DoS-enabled variants include a **From Workspace** block that expects a variable named **tuvar**. The corresponding original attack-signal data or script was not included in the supplied archive. The correct attack schedule and time/value format must be restored from the original experiment files; no substitute signal is fabricated here.

The models' stored stop times are 30 s (withoutDOS), 5 s (withDOS), and 10 s (RESILIENT). All three use variable-step automatic solver configuration. The exact MATLAB release used to create the files has not been confirmed.

The models have been inspected at the SLX package/XML level, but they have **not** been executed in MATLAB/Simulink as part of this portfolio preparation. No new plots, numerical comparisons, or performance claims are presented.

## Model architecture

```mermaid
flowchart LR
  X[Agent states] --> O[Distributed observer]
  O --> E[State estimates]
  E --> C[Distributed feedback controller]
  C --> P[Multi-agent plant]
  P --> X
  D[DoS signal] --> L[Observer-side topology L(DOS)]
  L --> O
```

In the supplied attack-enabled models, the observer-side Laplacian depends on the DOS signal. The active plant/controller derivative retains the nominal fixed Laplacian; see the implementation notes before interpreting this as a simultaneous controller-and-observer attack experiment.

Read:
- [Extracted MATLAB Function block scripts](docs/MATLAB_FUNCTION_BLOCKS.md)
- [Model Guide](docs/MODEL_GUIDE.md)
- [Implementation Notes](docs/IMPLEMENTATION_NOTES.md)
- [Reproducibility Notes](docs/REPRODUCIBILITY.md)
- [Reference](references/REFERENCES.md)

## Important interpretation limits

The reference paper's abstract describes DoS constraints on attack frequency and duration, a distributed observer-based controller, and a scenario in which both controller and observer communication networks can be jammed. The supplied withDOS and RESILIENT models make the observer-side Laplacian DoS-dependent while the active plant/controller function retains a fixed Laplacian. Therefore, the supplied files do not establish a complete simulation of the simultaneous controller-and-observer attack scenario.

In RESILIENT.slx, matrices R, LO, and LC are defined in the observer function, but the active observer derivative does not apply a state-reset operation using R. It is therefore described as an extended model variant, not as a verified implementation of the paper's full reset-based state-reconstruction mechanism.

The consensus-error function calculates \(0.2\|\sum_{i=1}^{5}(x_i-X_o)\|\). This is not the same as the average of the five individual leader-following error norms.

## Software requirements

- MATLAB
- Simulink
- Stateflow support for MATLAB Function blocks

The original SLX models and the original tuvar input are required for full model execution. See [Reproducibility Notes](docs/REPRODUCIBILITY.md).

## Reference

Z. Zuo, X. Cao, Y. Wang, and W. Zhang, “Resilient Consensus of Multiagent Systems Against Denial-of-Service Attacks,” *IEEE Transactions on Systems, Man, and Cybernetics: Systems*, vol. 52, no. 4, pp. 2664–2675. DOI: [10.1109/TSMC.2021.3051730](https://doi.org/10.1109/TSMC.2021.3051730).
