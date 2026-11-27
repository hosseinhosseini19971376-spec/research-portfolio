# Seyedhossein Seyedhosseini

## Research Portfolio · Robotics, Control Systems & Rehabilitation Engineering

This portfolio documents academic and engineering work in control theory, robotics, rehabilitation systems, embedded implementation, and data-driven modeling. Projects include a ball-and-plate balancing robot and a six-agent consensus simulation study.

The featured project is documented with its engineering objective, system architecture, modeling approach, implementation details, experimental workflow, and reproducibility limitations. Only files that are available and reviewed are presented as repository artifacts.

## Featured projects

### Design and Implementation of a Two-Degree-of-Freedom Ball-and-Plate Balancing Robot

![Physical ball-and-plate prototype](assets/prototype.jpg)

An undergraduate end-to-end engineering project involving mechanical construction, Euler–Lagrange modeling, resistive-touch position feedback, two-axis Arduino PID control, and MATLAB/Simulink-based modeling and parameter-estimation workflows.

**Technologies:** Arduino Mega 2560 · C/C++ · MATLAB R2018b · Simulink · PID Control

- [Read the project case study](ball-plate.md)
- [View the Arduino PID firmware](firmware/ball_plate_pid_controller.ino)
- [Read firmware setup and verification notes](firmware/README.md)

### Resilient consensus under communication interruptions

Three Simulink models compare nominal communication, interrupted links, and a resilient control design.

[Explore the models and reproducibility notes](resilient-consensus/)

## Repository structure

- **README.md** — portfolio landing page.
- **ball-plate.md** — project case study, technical details, and reproducibility status.
- **firmware/ball_plate_pid_controller.ino** — thesis-based Arduino firmware transcription.
- **firmware/README.md** — firmware dependencies, pin mapping, and verification notes.
- **assets/prototype.jpg** — photograph of the physical prototype.
- **assets/mechanical-schematic.jpg** — single-axis mechanical principle diagram.

**Ball-and-plate data availability:** the raw measurement spreadsheets and supplied Simulink example files reviewed during project preparation are not currently included in this repository. The case study describes their scope and the limitations of the available data without presenting them as downloadable files.

## Research interests

- Rehabilitation robotics and human–robot interaction
- Feedback, robust, adaptive, and model predictive control
- Reinforcement learning for robotic systems
- Multi-agent and networked control systems
- Real-time embedded control and hardware-in-the-loop experimentation
- System identification and data-driven modeling

## About the author

**Seyedhossein Seyedhosseini**  
M.Sc. in Electrical Engineering (Control), Amirkabir University of Technology

This portfolio is maintained as a research-oriented record of selected academic work and engineering implementations.
