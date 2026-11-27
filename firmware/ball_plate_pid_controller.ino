/*
 * Design and Implementation of a Two-Degree-of-Freedom Ball-and-Plate Robot
 * Author: Seyedhossein Seyedhosseini
 *
 * Source: undergraduate thesis, Arduino implementation, pp. 48-54.
 *
 * Transcription notes:
 * - The control structure and numerical parameters follow the thesis.
 * - Pin 9 is explicitly configured as OUTPUT because the source writes HIGH
 *   to that pin as a status indicator but does not configure its mode.
 * - Unused variables and duplicate initialization statements were removed.
 * - The firmware has not been compiled against the original libraries or
 *   tested on the original physical prototype in this environment.
 *
 * Required libraries:
 * - PID_v1 (Brett Beauregard Arduino PID Library)
 * - Adafruit TouchScreen
 * - Servo (Arduino library)
 */

#include <stdint.h>
#include <PID_v1.h>
#include <TouchScreen.h>
#include <Servo.h>

// Four-wire resistive touchscreen connections.
#define YP A0
#define XM A1
#define YM 3
#define XP 4

// Hardware pins.
const uint8_t SERVO_X_PIN = 5;
const uint8_t SERVO_Y_PIN = 6;
const uint8_t STATUS_PIN  = 9;

// Touchscreen resistance measured between the two same-name pins.
TouchScreen touchScreen(XP, YP, XM, YM, 300);

Servo servoX;
Servo servoY;

// Touchscreen raw-to-millimetre conversion factors from the thesis firmware.
const double X_RAW_TO_MM = 322.0 / 868.0;
const double Y_RAW_TO_MM = 247.0 / 885.0;

// Desired ball position in millimetres.
double setpointX = 175.0;
double setpointY = 144.0;

// Measured ball position and servo commands.
double inputX = 175.0;
double inputY = 144.0;
double outputX = 95.0;
double outputY = 95.0;

// PID gains reported in the thesis.
const double KP_X = 0.10;
const double KI_X = 0.01;
const double KD_X = 0.06;

const double KP_Y = 0.30;
const double KI_Y = 0.08;
const double KD_Y = 0.13;

// Controller and servo configuration.
const unsigned long PID_SAMPLE_TIME_MS = 50;
const int SERVO_NEUTRAL_DEG = 95;
const int SERVO_MIN_DEG = 20;
const int SERVO_MAX_DEG = 160;

// Ball-position acceptance band and stability threshold.
const double POSITION_TOLERANCE_MM = 20.0;
const unsigned long STABLE_COUNT_LIMIT = 125;

// The source firmware uses loop-count thresholds for no-touch handling.
unsigned int noTouchCount = 0;
unsigned long stableCount = 0;

PID pidX(&inputX, &outputX, &setpointX, KP_X, KI_X, KD_X, DIRECT);
PID pidY(&inputY, &outputY, &setpointY, KP_Y, KI_Y, KD_Y, DIRECT);

/*
 * This contact-detection condition is retained from the thesis:
 * X must be nonzero and Y must be outside the 740-751 raw-count band.
 */
bool isBallDetected(const TSPoint &point)
{
    return (point.x != 0) && ((point.y < 740) || (point.y > 751));
}

bool isInsideTargetBand()
{
    return (inputX > setpointX - POSITION_TOLERANCE_MM &&
            inputX < setpointX + POSITION_TOLERANCE_MM &&
            inputY > setpointY - POSITION_TOLERANCE_MM &&
            inputY < setpointY + POSITION_TOLERANCE_MM);
}

bool isOutsideTargetBand()
{
    return (inputX < setpointX - POSITION_TOLERANCE_MM ||
            inputX > setpointX + POSITION_TOLERANCE_MM ||
            inputY < setpointY - POSITION_TOLERANCE_MM ||
            inputY > setpointY + POSITION_TOLERANCE_MM);
}

void attachServos()
{
    if (!servoX.attached()) {
        servoX.attach(SERVO_X_PIN);
    }
    if (!servoY.attached()) {
        servoY.attach(SERVO_Y_PIN);
    }
}

void detachServos()
{
    if (servoX.attached()) {
        servoX.detach();
    }
    if (servoY.attached()) {
        servoY.detach();
    }
}

void commandNeutralPosition()
{
    outputX = SERVO_NEUTRAL_DEG;
    outputY = SERVO_NEUTRAL_DEG;
    servoX.write(SERVO_NEUTRAL_DEG);
    servoY.write(SERVO_NEUTRAL_DEG);
}

void setup()
{
    pinMode(STATUS_PIN, OUTPUT);
    digitalWrite(STATUS_PIN, LOW);

    attachServos();
    commandNeutralPosition();

    Serial.begin(115200);

    // The thesis uses the plate centre as the initial position and setpoint.
    inputX = setpointX;
    inputY = setpointY;

    pidX.SetMode(AUTOMATIC);
    pidY.SetMode(AUTOMATIC);

    pidX.SetOutputLimits(SERVO_MIN_DEG, SERVO_MAX_DEG);
    pidY.SetOutputLimits(SERVO_MIN_DEG, SERVO_MAX_DEG);

    pidX.SetSampleTime(PID_SAMPLE_TIME_MS);
    pidY.SetSampleTime(PID_SAMPLE_TIME_MS);

    delay(100);
}

void loop()
{
    // Regulation stage: operate until the stability counter reaches its limit.
    while (stableCount < STABLE_COUNT_LIMIT) {
        TSPoint contactPoint = touchScreen.getPoint();

        if (isBallDetected(contactPoint)) {
            noTouchCount = 0;
            attachServos();

            // A second touchscreen read is retained as in the thesis source.
            TSPoint measuredPoint = touchScreen.getPoint();

            inputX = measuredPoint.x * X_RAW_TO_MM;
            inputY = measuredPoint.y * Y_RAW_TO_MM;

            if (isInsideTargetBand()) {
                stableCount++;
                digitalWrite(STATUS_PIN, HIGH);
            }

            pidX.Compute();
            pidY.Compute();

            servoX.write((int)outputX);
            servoY.write((int)outputY);
        }
        else {
            noTouchCount++;

            if (noTouchCount == 75) {
                // The extra increment is retained from the thesis implementation.
                noTouchCount++;
                commandNeutralPosition();
            }

            if (noTouchCount == 150) {
                detachServos();
            }

            // Telemetry format retained from the thesis implementation.
            Serial.print(setpointX);
            Serial.print(",");
            Serial.print(setpointY);
            Serial.print(",");
            Serial.print(inputX);
            Serial.print(",");
            Serial.print(inputY);
            Serial.println(noTouchCount);
        }
    }

    detachServos();

    // Monitoring stage: re-enable regulation if the ball leaves the target band.
    while (stableCount == STABLE_COUNT_LIMIT) {
        TSPoint measuredPoint = touchScreen.getPoint();

        inputX = measuredPoint.x * X_RAW_TO_MM;
        inputY = measuredPoint.y * Y_RAW_TO_MM;

        if (isOutsideTargetBand()) {
            attachServos();
            stableCount = 0;
        }
    }
}
