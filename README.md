# **Project Overview**
This project enables a robotic arm with four servo motors to be controlled via real-time hand gestures using a laptop camera and MediaPipe's hand tracking library. The robotic arm mimics natural hand movements, offering precise and intuitive control.

---

## **Features**
- **Base Rotation**: The robotic arm's base rotates in response to the horizontal movement of your hand.
- **Arm Lift**: The arm's height adjusts based on the vertical position of your wrist.
- **Elbow Control**: The elbow servo moves proportionally to the wrist's vertical movement, amplified for greater sensitivity.
- **Gripper Operation**: The gripper opens or closes based on the distance between your thumb and index finger.

---

## **Technologies Used**
- **Python**: For processing hand gestures using OpenCV and MediaPipe.
- **MediaPipe Hands**: To detect and track hand landmarks in real time.
- **Arduino**: Interfaced with servo motors to control the robotic arm.
- **Serial Communication**: To send commands from the Python script to the Arduino.

---

## **Hardware Requirements**
- A 4-DOF robotic arm with servo motors connected to the following pins:
  - **Base**: Pin 11
  - **Arm**: Pin 3
  - **Elbow**: Pin 5
  - **Gripper**: Pin 9
- **Arduino board** (e.g., Arduino Uno)
- **Laptop** with a webcam

---

## **Software Requirements**
- Python 3.8+
- **Arduino IDE**
- Required Python Libraries:
  - `opencv-python`
  - `mediapipe`
  - `pyserial`

---

## **How It Works**
1. **Hand Gesture Detection**: The laptop's camera captures hand movements, which are processed using MediaPipe to extract key landmarks.
2. **Gesture Mapping**: Hand landmarks are mapped to specific angles for each servo motor.
3. **Servo Control**: The calculated angles are sent to the Arduino over a serial connection, which adjusts the servo motors accordingly.

---

## **Setup Instructions**
### **Hardware Setup**
- Connect the servos to the appropriate Arduino pins as specified above.
- Ensure the robotic arm is powered adequately.

### **Arduino Code**
- Flash the provided Arduino sketch to the board using the Arduino IDE.

### **Python Script**
- Install the required Python libraries:
  ```bash
  pip install opencv-python mediapipe pyserial
  ---

## **Run the Python Script**
Run the Python script to start gesture-based control.

---

## **Applications**
- Robotics education and prototyping.
- Remote robotic arm control for tasks requiring precision.
- Demonstrating hand-gesture-based interaction techniques.

---

## **Future Improvements**
- Adding more degrees of freedom for finer control.
- Improving gesture sensitivity and adding support for additional gestures.
- Integrating wireless communication for increased portability.
