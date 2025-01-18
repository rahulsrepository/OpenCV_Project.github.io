import cv2
import numpy as np
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Initialize the canvas and the drawing color
canvas = np.zeros((480, 640, 3), dtype=np.uint8)  # Black canvas for drawing
drawing_color = (0, 255, 0)  # Default to green
eraser_color = (0, 0, 0)     # Black for erasing (matches the canvas color)
brush_thickness = 10
eraser_thickness = 50
previous_x, previous_y = 0, 0  # Store previous coordinates of index finger

# Open the webcam feed
cap = cv2.VideoCapture(0)

# Function to check if the hand is in eraser gesture (peace sign)
def is_eraser_gesture(hand_landmarks):
    # Index and middle fingers up, ring and pinky down
    return (hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y and  # Index finger up
            hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y and  # Middle finger up
            hand_landmarks.landmark[16].y > hand_landmarks.landmark[14].y and  # Ring finger down
            hand_landmarks.landmark[20].y > hand_landmarks.landmark[18].y)  # Pinky finger down

drawing_enabled = True  # Flag to control whether drawing is enabled or not
eraser_mode = False     # Flag to control eraser mode

while True:
    # Capture frame from the webcam
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)  # Flip the image horizontally (like a mirror)

    # Convert the image to RGB as MediaPipe processes RGB images
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Detect hands and their landmarks
    result = hands.process(img_rgb)

    # Get the landmark positions if hands are detected
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Get the coordinates of the index finger (landmark 8)
            x, y = int(hand_landmarks.landmark[8].x * img.shape[1]), int(hand_landmarks.landmark[8].y * img.shape[0])

            # Draw hand landmarks on the webcam feed (optional)
            mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Check for eraser gesture (peace sign)
            if is_eraser_gesture(hand_landmarks):
                eraser_mode = True  # Activate eraser mode
                print("Eraser Mode Activated")
            else:
                eraser_mode = False  # Deactivate eraser mode

            # Drawing logic (if drawing is enabled and the index finger is up)
            if not eraser_mode and hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y:
                if previous_x == 0 and previous_y == 0:
                    previous_x, previous_y = x, y

                # Draw on the canvas (line from previous position to current position)
                cv2.line(canvas, (previous_x, previous_y), (x, y), drawing_color, brush_thickness)

                # Update the previous coordinates
                previous_x, previous_y = x, y
            elif eraser_mode and hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y:
                if previous_x == 0 and previous_y == 0:
                    previous_x, previous_y = x, y

                # Erase on the canvas (line from previous position to current position with black color)
                cv2.line(canvas, (previous_x, previous_y), (x, y), eraser_color, eraser_thickness)

                # Update the previous coordinates
                previous_x, previous_y = x, y
            else:
                # Reset the previous coordinates when the index finger is not raised
                previous_x, previous_y = 0, 0

    # Blend the canvas with the original webcam feed
    img = cv2.addWeighted(img, 0.6, canvas, 0.4, 0)  # Adjusted transparency for smoother blend

    # Show the resulting frame
    cv2.imshow("Air Canvas", img)

    # Keypress to change pen color
    key = cv2.waitKey(1)
    if key & 0xFF == ord('r'):
        drawing_color = (0, 0, 255)  # Red
        print("Pen color changed to Red")
    elif key & 0xFF == ord('g'):
        drawing_color = (0, 255, 0)  # Green
        print("Pen color changed to Green")
    elif key & 0xFF == ord('b'):
        drawing_color = (255, 0, 0)  # Blue
        print("Pen color changed to Blue")
    elif key & 0xFF == ord('y'):
        drawing_color = (0, 255, 255)  # Yellow
        print("Pen color changed to Yellow")

    # Save the canvas to a file when the 's' key is pressed
    if key & 0xFF == ord('s'):
        cv2.imwrite("air_canvas_output.png", canvas)
        print("Canvas saved as 'air_canvas_output.png'")

    # Press 'ESC' to exit the loop
    if key == 27:
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
