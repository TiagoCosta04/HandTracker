import cv2
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from hand_tracker import HandTracker
from camera_handler import CameraHandler

def main():
    # Initialize the camera
    camera = CameraHandler()
    camera.start_camera()

    # Create an instance of the hand tracker
    hand_tracker = HandTracker(model=None)  # MediaPipe doesn't need external model

    while True:
        # Get a frame from the camera
        frame = camera.get_frame()
        if frame is None:
            break

        # Track hands in the frame and get processed frame
        processed_frame = hand_tracker.track_hands(frame)

        # Display the frame with hand landmarks and bounding boxes
        cv2.imshow("Hand Tracking", processed_frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close windows
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()