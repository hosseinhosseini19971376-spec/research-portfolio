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


## 3.1. Mechanical prototype documentation

The thesis includes photographs of the physical assembly and the resistive touchscreen test. The mechanical design uses a central spherical joint and two servo-driven linkages arranged to tilt the plate about the two controlled axes. The touchscreen is mounted on the moving plate and provides the ball-position feedback.

## 5.1. Firmware source

The Arduino sketch transcribed from the thesis is available here:

- [Arduino PID controller firmware](firmware/ball_plate_pid_controller.ino)

The sketch uses the PID_v1, Adafruit TouchScreen, and Servo libraries. The code transcription preserves the constants and control flow shown in the thesis (including the axis setpoints, conversion factors, sample time, output limits, and no-touch handling). It has not yet been independently compiled or validated on the original hardware. The library versions and exact board wiring should be confirmed before attempting to reproduce the experiment.

### Key implementation parameters

| Parameter | Value in thesis firmware |
|---|---:|
| Arduino board | Mega 2560 |
| X servo pin | 5 |
| Y servo pin | 6 |
| Touchscreen pins | YP=A0, XM=A1, YM=3, XP=4 |
| Serial baud rate | 115200 |
| PID sample time | 50 ms |
| X setpoint | 175 (converted touchscreen coordinate) |
| Y setpoint | 144 (converted touchscreen coordinate) |
| Servo neutral command | 95° |
| Servo command limits | 20°–160° |
| Stability tolerance | ±20 coordinate units on each axis |
| Stability counter threshold | 125 consecutive in-band samples |

The sketch includes variables for touchscreen centre coordinates (homeX, homeY) and a stability/status output on digital pin 9, as shown in the report. The source does not show a corresponding pinMode(9, OUTPUT) configuration; this has not been silently added to the transcription.

## 6.1. Parameter-estimation workflow documented in the thesis

The model-based-design chapter describes an experimental identification workflow:

1. Command the two servo motors through the Arduino-based setup.
2. Record the servo input values, measured ball-position outputs, and timestamps.
3. Export the recorded data to Excel and import it into MATLAB as matrices.
4. Build the corresponding Simulink signal and transfer-function model.
5. Select the model parameters in the Parameter Estimation environment.
6. Associate the measured experimental output and time vector with the model output.
7. Run parameter estimation to fit the model response to the experimental data.

The report contains Simulink screenshots illustrating this procedure. The original .slx model and the raw Excel/measurement dataset are not embedded as editable source files in the report, so they cannot be reconstructed exactly from screenshots alone.

## Reproducibility status

- **Firmware:** transcribed into this repository from the report; compilation and hardware verification remain outstanding.
- **Mechanical assembly:** documented by photographs and construction notes in the report.
- **Mathematical model:** derivation and assumptions are documented in the thesis; equations should be checked against the typeset source before numerical reuse.
- **Simulink model:** workflow and screenshots are documented, but the original editable .slx file is not available in the report.
- **Experimental data:** the report describes recorded input/output data and an Excel workflow, but the underlying raw data file is not embedded as a separate dataset.


## 3.1. Prototype photographs and hardware references

The report and subsequently supplied images document the physical prototype, its wooden base and moving plate, the central spherical joint, the servo-driven linkages, the resistive touchscreen, and the Arduino-based electronics. The photographs are intended to be used as the primary visual evidence of the built system. Product/catalogue illustrations are treated as component references, not as photographs of the prototype.

Hardware specifications stated in the thesis:
- **Controller:** Arduino Mega 2560 (ATmega2560).
- **Actuators:** two MG946 metal-gear servo motors.
- **Servo supply:** 6 V supplied from batteries; the report describes two battery holders and eight 1.5 V cells.
- **Position sensor:** four-wire resistive touchscreen.
- **Mechanical support:** central spherical joint and two servo/linkage assemblies.
- **Controller feedback:** ball position measured along X and Y using the touchscreen.

The thesis describes the MG946 servo as operating from 4.8–6.6 V, with 180-degree travel and a stated maximum torque of 13 kg·cm at 6.6 V (10.5 kg·cm at 4.8 V). These are manufacturer/report specifications, not measured torque values from the experiment.

## 5.2. Firmware source and implementation notes

The cleaned, thesis-based two-axis Arduino sketch is available at [firmware/ball_plate_pid_controller.ino](firmware/ball_plate_pid_controller.ino).

The sketch retains the reported control architecture and numerical values while making the source easier to read:
- PID_v1, Adafruit TouchScreen, and Servo libraries.
- Touchscreen pins YP=A0, XM=A1, YM=3, XP=4.
- Servo signal pins 5 and 6.
- Serial baud rate 115200.
- X and Y setpoints 175 mm and 144 mm as labelled in the thesis.
- X gains: Kp=0.10, Ki=0.01, Kd=0.06.
- Y gains: Kp=0.30, Ki=0.08, Kd=0.13.
- PID sample time: 50 ms.
- Servo output limits: 20–160 degrees; nominal neutral command: 95 degrees.
- Ball-position tolerance band: ±20 converted coordinate units.
- Stability counter threshold: 125 in-band detections.
- No-touch handling: neutral servo command after the source counter reaches 75, and servo detach at 150.

**Important:** the original report code writes HIGH to digital pin 9 without explicitly configuring it as an output. The cleaned sketch configures pin 9 as OUTPUT to make that status-indicator operation explicit. This is a small implementation clarification, not a claim that the original source contained that line. The firmware has not been compiled with the exact library versions or tested on the original prototype in this environment.

## 6.2. Supplied Simulink models: scope and limitations

Three Simulink files were supplied and inspected at the SLX package/XML level:

- `untitled4.slx.original`: a minimal servo-command example with a Constant block, Slider Gain, and Arduino Standard Servo Write. The servo block is configured for digital pin 9; the slider gain is 0 with a 0–180 range.
- `untitled4.slx`: a similar servo-command example, with a Scope and Slider Gain value 95.4, again connected to an Arduino Standard Servo Write block on pin 9.
- `untitledrfrf.slx`: a serial-receive/monitoring model with Serial Configuration and Serial Receive blocks configured for COM4 at 9600 baud, conversion/display blocks, and a Real-Time Pacer. It appears to be a serial monitoring/helper model, not a complete two-axis plant or controller model.

These files are supporting implementation examples. They should not be described as a complete Simulink model of the two-axis ball-and-plate dynamics. The report's Parameter Estimation procedure is documented separately; a fully connected, editable plant model and its fitted parameter values are not evidenced by these three supplied files alone.

## 7.1. Experimental data supplied for this portfolio

The following spreadsheets were supplied:
- `x.xlsx`: 3,486 raw touchscreen X-channel samples.
- `y.xlsx`: 3,486 raw touchscreen Y-channel samples (stored in the second worksheet column).
- `time.xlsx`: 3,486 time values, spanning 0.101–10.001 s.
- `sevo1.xlsx` and `sevo2.xlsx`: 21 servo command values per channel, without timestamps.

The time vector is strictly increasing. Its median sampling interval is approximately 0.003 s (about 3 ms); the observed intervals vary between 1 and 5 ms. This is the sampling interval of the supplied recorded data and should not be confused with the 50 ms PID sample time configured in the Arduino firmware.

Using the exact scale factors in the thesis firmware (322/868 for X and 247/885 for Y), the raw touchscreen values can be converted to nominal millimetre coordinates. The X channel contains 115 zero readings; these are treated as invalid/no-contact samples for visualization, while the original raw values should be retained in the source dataset. The report's contact test also includes a Y raw-count exclusion band from 740 to 751; the supplied Y samples do not fall in that band.

The 21 servo command samples in each servo spreadsheet have no corresponding time column. They are therefore plotted against sample index only and are not aligned to the 3,486-point position/time record. They may represent a separate input sequence used in the Parameter Estimation workflow, as described in the thesis, but the available files do not establish a one-to-one time alignment.

### Data interpretation

The recorded X–Y trajectory is a measured sensor trace, not by itself proof of closed-loop setpoint regulation. The current files do not include a synchronized servo-input time series for the 3,486 position samples, a separate disturbance marker, or a validated set of tracking-error performance metrics. Accordingly, no RMSE, settling time, overshoot, or disturbance-rejection score is claimed.

## Reproducibility and artifact status

| Artifact | Status |
|---|---|
| Thesis-based two-axis Arduino sketch | Cleaned and documented; not hardware-verified here |
| Ball-position X/Y/time spreadsheets | Inspected; coordinate scaling documented |
| Servo input spreadsheets | Inspected; 21 samples per servo, no timestamps |
| Simulink servo example files | Inspected; supporting examples only |
| Simulink serial monitor file | Inspected; helper/monitoring model |
| Full two-axis Simulink plant/controller | Not established by supplied SLX files |
| Synchronized raw actuator and position dataset | Not available in supplied spreadsheets |

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
