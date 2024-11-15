#include <Servo.h>

Servo servo[4];
int default_angle[4] = {75, 90, 90, 60};

void setup() {
    Serial.begin(115200);
    servo[0].attach(11); // Base servo
    servo[1].attach(3);  // Arm servo
    servo[2].attach(5);  // Elbow servo
    servo[3].attach(9);  // Grappler servo

    // Set servos to default positions
    for (int i = 0; i < 4; i++) {
        servo[i].write(default_angle[i]);
    }
}

byte angles[4];

void loop() {
    if (Serial.available()) {
        Serial.readBytes(angles, 4); // Read 4 bytes for servo angles
        for (int i = 0; i < 4; i++) {
            servo[i].write(angles[i]);
        }
    }
}

