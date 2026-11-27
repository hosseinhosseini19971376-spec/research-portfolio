# Ball-and-Plate Arduino Firmware

This folder contains the thesis-based Arduino sketch for the two-degree-of-freedom ball-and-plate balancing robot.

## Hardware mapping

| Function | Arduino Mega 2560 pin |
|---|---|
| X-axis servo signal | D5 |
| Y-axis servo signal | D6 |
| Status output | D9 |
| Touchscreen YP | A0 |
| Touchscreen XM | A1 |
| Touchscreen YM | D3 |
| Touchscreen XP | D4 |

The sketch uses two MG946 servo motors and a four-wire resistive touchscreen. Confirm the actual wiring and touchscreen pin orientation against the physical assembly before powering the system.

## Required Arduino libraries

- PID_v1 (Brett Beauregard's Arduino PID Library)
- Adafruit TouchScreen
- Servo (Arduino Servo library)

## Controller configuration

- Board: Arduino Mega 2560
- Serial baud rate: 115200
- PID sample time: 50 ms
- X-axis gains: Kp=0.10, Ki=0.01, Kd=0.06
- Y-axis gains: Kp=0.30, Ki=0.08, Kd=0.13
- Neutral servo command: 95 degrees
- Servo output limits: 20–160 degrees
- Setpoints: X=175 mm, Y=144 mm

The numerical values are transcribed from the undergraduate thesis and its firmware. They are not independently tuned or validated in this repository.

## Build and safety status

The sketch has **not** been compiled against a confirmed set of library versions and has **not** been tested on the original prototype. Before running it:

1. Verify all signal and power connections.
2. Verify servo direction and touchscreen coordinate orientation.
3. Support the platform and remove the ball while checking servo travel.
4. Confirm that the mechanism cannot strike its mechanical limits.
5. Use an appropriate external servo supply with a common ground to the controller, as required by the actual hardware design.

The initial regulation loop accumulates in-band detections without resetting the counter on every out-of-band sample. The monitoring loop also does not independently validate touchscreen contact before using a reading. These behaviors are preserved from the thesis-based transcription and should be reviewed before using the sketch as a production controller.

The sketch explicitly configures D9 as an output for the status signal. The source material writes to this pin but does not show the corresponding pin-mode configuration.
