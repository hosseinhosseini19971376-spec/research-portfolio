# Design and Implementation of a Two-Degree-of-Freedom Ball-and-Plate Balancing Robot

**Undergraduate thesis project · B.Sc. Electrical Engineering (Control)**  
**Hamedan University of Technology · September 2019**

**Author:** Seyedhossein Seyedhosseini

---

## Project at a glance

A physical two-axis ball-and-plate system was designed, assembled, modeled, and controlled. The objective was to regulate a ball's position on a tilting platform using closed-loop X–Y feedback. The project combines nonlinear dynamics, mechanical design, resistive-touch sensing, servo actuation, embedded PID control, and MATLAB/Simulink-based model-based design and parameter estimation.

| Area | Implementation documented in the thesis |
|---|---|
| Embedded controller | Arduino Mega 2560 |
| Position sensing | Four-wire resistive touchscreen |
| Actuation | Two MG946 servo motors |
| Mechanical arrangement | Tilting plate, spherical joint, two servo supports and metal linkages |
| Feedback controller | Two independent PID loops, one per axis |
| Modeling | Euler–Lagrange formulation and local linearization |
| Engineering software | Arduino IDE, MATLAB R2018b, Simulink |
| Model calibration | MATLAB/Simulink Parameter Estimation using recorded input/output data |

## 1. Engineering objective

The ball-and-plate plant is nonlinear and open-loop unstable. Two servo motors tilt the platform along perpendicular axes; a resistive touchscreen measures the ball's location and supplies feedback to the controller.

The control objective is to keep the ball near a specified coordinate on the plate, or move it toward a desired position, while preventing it from leaving the sensing surface.

## 2. Mathematical modeling

The thesis derives the equations of motion using the Euler–Lagrange method. The model considers the kinetic and potential energy of the ball and plate and relates the ball coordinates to the two plate inclination angles.

The derivation uses the following idealizing assumptions stated in the thesis:

- Negligible friction between the ball and plate.
- A homogeneous, symmetric ball.
- No slipping between the ball and plate.
- Servo angle is treated as the controllable input to the corresponding plate inclination.

The nonlinear equations are then linearized around the horizontal operating point (zero plate angles and small angular velocities). The thesis obtains an axis-wise transfer-function representation from servo angle to ball position, with the perpendicular axis treated analogously under the system symmetry assumption.

**Modeling note:** the linearized axis model is a local approximation around the nominal operating point; it should not be interpreted as a globally valid representation of the full nonlinear coupled plant.

## 3. Mechanical design and hardware integration

The physical assembly documented in the thesis includes:

- A wooden upper plate sized to support and protect the touchscreen.
- A spherical joint connecting the tilting platform to the lower structure.
- Two servo mounting supports arranged to actuate the X and Y directions.
- Metal servo arms/linkages with joints that permit the required relative movement.
- The resistive touchscreen mounted on the moving platform.
- Battery supply, breadboard, wiring, and the Arduino controller.

The thesis describes the mechanical layout, selected components, touchscreen pin identification and electrical testing, and the assembled system.

## 4. Position sensing and coordinate handling

A four-wire resistive touchscreen is used as the position-feedback sensor. The Arduino reads the analog values associated with the X and Y directions. The implementation converts raw touchscreen readings into millimetre-scale coordinates using the conversion factors recorded in the firmware.

The firmware defines a home/centre reading for the touchscreen and uses the measured coordinates as the two PID process variables.

## 5. Embedded two-axis PID controller

The Arduino Mega 2560 executes two PID controllers, one for each axis. The firmware documented in the thesis includes:

- Touchscreen, PID, and Servo library integration.
- Separate X- and Y-axis process variables, setpoints, and controller outputs.
- Servo initialization and a neutral platform command.
- Automatic PID operation and bounded servo output commands.
- A nominal controller sample time of **50 ms**.
- Serial transmission of setpoints, measured coordinates, and sensor-contact status.
- Logic for detecting when the ball is not detected by the touchscreen, returning the servos to a neutral command, and detaching servo outputs after a prolonged no-contact interval.
- A stability counter that monitors whether the ball remains within a tolerance band around the target.

### PID parameters documented in the firmware

| Axis | (K_p) | (K_i) | (K_d) |
|---|---:|---:|---:|
| X | 0.10 | 0.01 | 0.06 |
| Y | 0.30 | 0.08 | 0.13 |

The firmware sets the servo command limits to 20–160 degrees and uses 95 degrees as the nominal neutral command. The thesis describes the implemented controller as maintaining the ball on the plate to a satisfactory qualitative level. No numerical tracking metrics are claimed here beyond those reported in the source.

## 6. MATLAB/Simulink integration and model-based design

A second part of the project investigates a model-based workflow using MATLAB R2018b and Simulink. The thesis documents:

1. Installing and configuring MATLAB support packages for Arduino.
2. Connecting MATLAB/Simulink with the Arduino hardware.
3. Using Simulink blocks to command servo angles.
4. Generating C++ code from a Simulink model for execution on Arduino.
5. Acquiring servo input values, measured ball-position outputs, and timestamps from the physical setup.
6. Importing the recorded data into MATLAB.
7. Configuring a transfer-function model and selecting its parameters in the Parameter Estimation environment.
8. Comparing the simulated model output with measured experimental output and estimating model parameters.

This workflow connects the theoretical model to measurements obtained from the implemented physical system.

## 7. Reported outcome

The thesis reports the construction and implementation of the two-degree-of-freedom ball-and-plate setup, successful operation of the Arduino-based PID control to a satisfactory qualitative level, and use of recorded experimental data in a MATLAB/Simulink parameter-estimation workflow.

The thesis does not present validated numerical values for tracking RMSE, settling time, overshoot, or disturbance-rejection indices in the material summarized here. These metrics are therefore not invented or inferred.

## 8. Engineering capabilities demonstrated

- End-to-end electromechanical system development.
- Mechanical prototyping and actuator-linkage integration.
- Nonlinear dynamic modeling using the Euler–Lagrange formulation.
- Local linearization and transfer-function modeling.
- Resistive touchscreen sensing and coordinate calibration.
- Two-axis PID feedback design and embedded implementation.
- Arduino Mega 2560 programming and servo control.
- MATLAB/Simulink hardware integration and code generation.
- Experimental data acquisition and model parameter estimation.

## Source

Seyedhossein Seyedhosseini, *Control Design for a 2 DOF Ball and Plate System*, B.Sc. thesis in Electrical Engineering (Control), Hamedan University of Technology, September 2019.
