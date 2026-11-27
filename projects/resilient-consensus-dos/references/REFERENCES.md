# References

## Primary reference

Z. Zuo, X. Cao, Y. Wang, and W. Zhang, “Resilient Consensus of Multiagent Systems Against Denial-of-Service Attacks,” *IEEE Transactions on Systems, Man, and Cybernetics: Systems*, vol. 52, no. 4, pp. 2664–2675 (2022; first listed online in February 2021).

DOI: [10.1109/TSMC.2021.3051730](https://doi.org/10.1109/TSMC.2021.3051730)

The article studies consensus of multi-agent systems under DoS attacks that block information exchange. Its abstract describes constraints on attack frequency and duration, a distributed observer-based controller for reconstructing agent states, and a scenario in which both controller and observer communication networks are jammed.

This repository contains the supplied Simulink models and implementation documentation, not the publisher's PDF. The models implement selected parts of the paper's observer-based framework; see the project README, Model Guide, and extracted MATLAB Function scripts for implementation limits.

## Source and scope

The paper is the source for the theoretical problem formulation and stability claims. The repository's own SLX files are the source for statements about the implemented matrices, function blocks, stop times, and workspace dependencies. Those two evidence sources should not be conflated.
