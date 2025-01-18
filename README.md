# OpenCV_Project.github.io
Air Canvas using OpenCV and MediaPipe
This project implements an "Air Canvas" that allows users to draw in the air using their hands, captured via a webcam. It leverages OpenCV for image processing and MediaPipe for hand detection and gesture recognition.

Features
Draw on a virtual canvas by moving your index finger in the air.
Change drawing color between Red, Green, Blue, and Yellow using the keyboard.
Erase parts of the drawing using a hand gesture (peace sign).
Save the canvas as an image file.

Requirements
Python 3.x
OpenCV (cv2)
MediaPipe (mediapipe)
NumPy (numpy)
You can install the required dependencies using pip:

pip install opencv-python mediapipe numpy

How It Works
Hand Tracking: The application uses MediaPipe to detect and track the user's hand and fingers through the webcam.
Drawing: The user can draw on a virtual canvas by raising their index finger. The previous position of the finger is used to draw a line connecting to the current position.
Eraser Mode: By showing a "peace" sign (index and middle fingers up, others down), the eraser mode is activated, allowing the user to erase parts of the drawing.
Change Colors: The user can switch the drawing color using the following keys:
Press r for Red.
Press g for Green.
Press b for Blue.
Press y for Yellow.

Save the Drawing: Press s to save the canvas as an image (air_canvas_output.png).
Controls
r : Change pen color to Red.
g : Change pen color to Green.
b : Change pen color to Blue.
y : Change pen color to Yellow.
s : Save the current canvas as an image (air_canvas_output.png).
ESC : Exit the application.
