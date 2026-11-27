/*
 * Two-DOF Ball-and-Plate Balancing Robot
 * Arduino firmware transcribed from the undergraduate thesis report
 * Author: Seyedhossein Seyedhosseini
 *
 * Source pages: 48-55 of the thesis PDF.
 * This is a faithful transcription for documentation; it has not been
 * independently compiled or re-tested on the original hardware.
 */

#include <PID_v1.h>
#include <stdint.h>
#include "TouchScreen.h"
#include <Servo.h>

#define YP A0 // 0
#define XM A1 // 1
#define YM 3  // 3
#define XP 4  // 4

TouchScreen ts = TouchScreen(XP, YP, XM, YM, 300);

unsigned int noTouchCount = 0;
double k = 0;

double Setpoint, Input, Output;     // X axis
double Setpoint1, Input1, Output1;  // Y axis

Servo servo1; // X axis
Servo servo2; // Y axis

uint16_t homeX = 472;
uint16_t homeY = 517;

float convertX = 322.0 / 868.0;
float convertY = 247.0 / 885.0;

int Ts = 50;
unsigned long Stable = 0;

float Kp = 0.1;
float Ki = 0.01;
float Kd = 0.06;

float Kp1 = 0.3;
float Ki1 = 0.08;
float Kd1 = 0.13;

long cas = 0;

PID myPID(&Input, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);
PID myPID1(&Input1, &Output1, &Setpoint1, Kp1, Ki1, Kd1, DIRECT);

void setup()
{
    servo1.attach(5);
    servo2.attach(6);

    Output = 95;
    Output1 = 95;

    servo1.write(Output);
    servo2.write(Output1);

    Serial.begin(115200);

    TSPoint p = ts.getPoint();

    Input = 175;
    Input1 = 144;

    Setpoint = 175;
    Setpoint1 = 144;

    // Set the plate to its nominal level position.
    servo1.attach(5);
    servo2.attach(6);

    Output = 95;
    Output1 = 95;

    servo1.write(Output);
    servo2.write(Output1);

    myPID.SetMode(AUTOMATIC);
    myPID.SetOutputLimits(20, 160);

    myPID1.SetMode(AUTOMATIC);
    myPID1.SetOutputLimits(20, 160);

    myPID1.SetSampleTime(Ts);
    myPID.SetSampleTime(Ts);

    delay(100);
}

void loop()
{
    while (Stable < 125) // Regulation loop
    {
        TSPoint p = ts.getPoint(); // Measure pressure on the plate.

        if ((p.x != 0 && (p.y < 740 || p.y > 751))) // Ball is on plate
        {
            noTouchCount = 0;

            servo1.attach(5);
            servo2.attach(6);

            TSPoint p = ts.getPoint();

            Input = (p.x * convertX);
            Input1 = (p.y * convertY);

            if ((Input > Setpoint - 20 && Input < Setpoint + 20 &&
                 Input1 > Setpoint1 - 20 && Input1 < Setpoint1 + 20))
            {
                Stable = Stable + 1;
                digitalWrite(9, HIGH);
            }
            else
            {
            }

            myPID.Compute();
            myPID1.Compute();

            servo1.write(Output);
            servo2.write(Output1);
        }
        else // Ball is not detected on the plate
        {
            noTouchCount++;

            if (noTouchCount == 75)
            {
                noTouchCount++;

                Output = 95;
                Output1 = 95;

                servo1.write(Output);
                servo2.write(Output1);
            }

            if (noTouchCount == 150)
            {
                servo1.detach();
                servo2.detach();
            }

            Serial.println(Setpoint);
            Serial.print(",");
            Serial.print(Setpoint1);
            Serial.print(",");
            Serial.print(Input);
            Serial.print(",");
            Serial.print(Input1);
            Serial.println(noTouchCount);
        }
    }

    servo1.detach();
    servo2.detach();

    while (Stable == 125) // If the ball is stable, keep monitoring its position.
    {
        TSPoint p = ts.getPoint();

        Input = (p.x * convertX);
        Input1 = (p.y * convertY);

        if (Input < Setpoint - 20 || Input > Setpoint + 20 ||
            Input1 > Setpoint1 + 20 || Input1 < Setpoint1 - 20)
        {
            servo1.attach(5);
            servo2.attach(6);

            Stable = 0; // Change STABLE state.
        }
    }
}
