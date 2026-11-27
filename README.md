# Seyedhossein Seyedhosseini

## Research Portfolio · Robotics, Control Systems & Rehabilitation Engineering

This portfolio presents selected academic and engineering work in robotics, control theory, networked multi-agent systems, embedded implementation, and data-driven modeling.

Projects are documented with their objectives, mathematical foundations, system architecture, implementation details, and reproducibility limits. Only results and artifacts supported by the available source files are claimed.

## Selected projects

### 1. Design and Implementation of a Two-Degree-of-Freedom Ball-and-Plate Balancing Robot

![Physical ball-and-plate prototype](assets/prototype.jpg)

An undergraduate end-to-end engineering project involving mechanical construction, Euler–Lagrange modeling, resistive-touch position feedback, two-axis Arduino PID control, and MATLAB/Simulink-based modeling and parameter-estimation workflows.

**Technologies:** Arduino Mega 2560 · C/C++ · MATLAB · Simulink · PID Control

- [Read the project case study](ball-plate.md)
- [View the Arduino PID firmware](firmware/ball_plate_pid_controller.ino)
- [Read firmware setup and verification notes](firmware/README.md)

### 2. Resilient Consensus of Multi-Agent Systems Under DoS Attacks

A MATLAB/Simulink simulation study based on an IEEE paper on observer-based distributed consensus under denial-of-service communication attacks. The project package contains three model variants (nominal, DoS-dependent observer topology, and an extended observer-model variant), together with technical and reproducibility documentation.

**Technologies:** MATLAB · Simulink · State-Space Modeling · Distributed Observers · Graph Laplacians · Kronecker Products · DoS-Resilient Control

- [Read the project case study and model limitations](projects/resilient-consensus-dos/README.md)
- [Review the Simulink model guide](projects/resilient-consensus-dos/docs/MODEL_GUIDE.md)
- [Review implementation equations and caveats](projects/resilient-consensus-dos/docs/IMPLEMENTATION_NOTES.md)

**Artifact note:** the three original SLX binaries are identified and integrity-hashed in the project folder but are not yet committed to GitHub. The DoS-enabled models also require the original tuvar attack-signal workspace data, which was not included in the supplied archive. No unverified simulation plots or performance results are claimed.

## Research interests

- Rehabilitation robotics and human–robot interaction
- Feedback, robust, adaptive, and model predictive control
- Reinforcement learning for robotic systems
- Multi-agent and networked control systems
- Resilient and secure control under cyberattacks
- Real-time embedded control and hardware-in-the-loop experimentation
- System identification and data-driven modeling

## About the author

**Seyedhossein Seyedhosseini**  
M.Sc. in Electrical Engineering (Control), Amirkabir University of Technology

This portfolio is maintained as a research-oriented record of selected academic work and engineering implementations.
