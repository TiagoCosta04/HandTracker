import cv2

class CameraHandler:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None

    def start_camera(self):
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            raise Exception("Could not open video device")

    def get_frame(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if not ret:
                raise Exception("Could not read frame from camera")
            return frame
        else:
            raise Exception("Camera not started. Call start_camera() first.")

    def release_camera(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None