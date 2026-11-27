# Resilient consensus under communication interruptions

How does loss of communication between selected agents affect their ability to follow a shared trajectory? These MATLAB/Simulink models represent a network of six agents with four states per agent.

| Model | Scenario |
| --- | --- |
| [withoutDOS.slx](models/withoutDOS.slx) | Baseline with a fixed communication graph |
| [withDOS.slx](models/withDOS.slx) | Selected links change with a simulated denial-of-service signal |
| [RESILIENT.slx](models/RESILIENT.slx) | Resilient design under simulated interruptions |

## Inspecting the models

Open the baseline model in Simulink and inspect its MATLAB Function blocks and state trajectories. Then compare the communication graph and observer equations in the two interruption scenarios. The models use the R2018b file format. The interruption models contain From Workspace blocks. The archive includes only the three model files, and simulation results have not been independently reproduced for this portfolio.
