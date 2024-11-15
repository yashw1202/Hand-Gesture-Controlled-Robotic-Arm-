import cv2
import mediapipe as mp
import serial
import time

# Configure serial port
serial_port = "COM15"  # Replace with your Arduino's COM port
baud_rate = 115200
arduino = serial.Serial(serial_port, baud_rate, timeout=1)
time.sleep(2)  # Allow time for the serial connection to initialize

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Servo angle limits
BASE_MIN, BASE_MAX = 0, 180
ARM_MIN, ARM_MAX = 30, 150
ELBOW_MIN, ELBOW_MAX = 30, 150
GRIPPER_OPEN, GRIPPER_CLOSE = 180, 90

# Sensitivity factors (amplify movements)
BASE_SENSITIVITY = 3  # Amplify small base movements
ELBOW_SENSITIVITY = 4  # Amplify small elbow movements

# Clamping function to keep angles within 0-180 range
def clamp(value, min_val, max_val):
    return max(min_val, min(max_val, int(value)))

# Gesture mapping
def map_gesture_to_servo(hand_landmarks):
    wrist = hand_landmarks[mp_hands.HandLandmark.WRIST]
    index_tip = hand_landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    thumb_tip = hand_landmarks[mp_hands.HandLandmark.THUMB_TIP]

    # Base rotation: Amplify small wrist x-movements
    base_angle = clamp(BASE_MIN + (wrist.x * BASE_SENSITIVITY * (BASE_MAX - BASE_MIN)), BASE_MIN, BASE_MAX)

    # Arm lift: Map wrist y-coordinate to arm movement
    arm_angle = clamp(ARM_MIN + (1 - wrist.y) * (ARM_MAX - ARM_MIN), ARM_MIN, ARM_MAX)

    # Elbow: Use wrist’s y-position for movement
    elbow_angle = clamp(ELBOW_MIN + (1 - wrist.y) * ELBOW_SENSITIVITY * (ELBOW_MAX - ELBOW_MIN), ELBOW_MIN, ELBOW_MAX)

    # Gripper: Thumb to index finger distance
    thumb_index_distance = ((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)**0.5
    gripper_angle = GRIPPER_CLOSE if thumb_index_distance < 0.1 else GRIPPER_OPEN

    return [base_angle, arm_angle, elbow_angle, gripper_angle]

# Start capturing video
cap = cv2.VideoCapture(0)

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Flip and process the frame
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                servo_angles = map_gesture_to_servo(hand_landmarks.landmark)
                print(f"Servo Angles: {servo_angles}")

                # Send servo angles to Arduino as bytes
                arduino.write(bytearray(servo_angles))

        # Display the frame
        cv2.imshow('Hand Gesture Control', frame)

        # Exit on pressing 'q'
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    arduino.close()
