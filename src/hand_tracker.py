import cv2
import mediapipe as mp
import numpy as np

class HandTracker:
    def __init__(self, model):
        self.model = model
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def track_hands(self, frame):
        # Convert BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame to detect hands
        results = self.hands.process(rgb_frame)
        
        detected_gestures = []
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )
                
                # Draw bounding box around the hand
                self.draw_hand_frame(frame, hand_landmarks)
                
                # Detect gestures
                gestures = self.detect_gestures(hand_landmarks)
                detected_gestures.extend(gestures)
                
                # Display gestures on frame
                self.display_gestures(frame, gestures, hand_landmarks)
        
        return frame, detected_gestures

    def draw_hand_frame(self, frame, landmarks):
        # Get frame dimensions
        h, w, _ = frame.shape
        
        # Calculate bounding box coordinates
        x_coords = [landmark.x * w for landmark in landmarks.landmark]
        y_coords = [landmark.y * h for landmark in landmarks.landmark]
        
        x_min, x_max = int(min(x_coords)), int(max(x_coords))
        y_min, y_max = int(min(y_coords)), int(max(y_coords))
        
        # Add padding to the bounding box
        padding = 20
        x_min = max(0, x_min - padding)
        y_min = max(0, y_min - padding)
        x_max = min(w, x_max + padding)
        y_max = min(h, y_max + padding)
        
        # Draw rectangle frame around the hand
        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
        
        # Optional: Add label
        cv2.putText(frame, "Hand", (x_min, y_min - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    def draw_hand_landmarks(self, frame, landmarks):
        # Draw hand landmarks on the frame
        self.mp_drawing.draw_landmarks(frame, landmarks, self.mp_hands.HAND_CONNECTIONS)

    def detect_gestures(self, landmarks):
        """Detect specific hand gestures based on landmarks"""
        gestures = []
        
        # Get landmark positions
        landmarks_array = np.array([[lm.x, lm.y] for lm in landmarks.landmark])
        
        # Detect thumbs up
        if self.is_thumbs_up(landmarks_array):
            gestures.append("Thumbs Up")
        
        # Detect peace sign
        if self.is_peace_sign(landmarks_array):
            gestures.append("Peace Sign")
        
        # Detect fist
        if self.is_fist(landmarks_array):
            gestures.append("Fist")
        
        # Detect open palm
        if self.is_open_palm(landmarks_array):
            gestures.append("Open Palm")
        
        # Detect pointing
        if self.is_pointing(landmarks_array):
            gestures.append("Pointing")
        
        return gestures

    def is_thumbs_up(self, landmarks):
        """Check if thumb is up and other fingers are down"""
        # Thumb tip vs thumb IP
        thumb_up = landmarks[4][1] < landmarks[3][1]
        
        # Other fingers down (tip below PIP joint)
        fingers_down = all([
            landmarks[8][1] > landmarks[6][1],   # Index finger
            landmarks[12][1] > landmarks[10][1], # Middle finger
            landmarks[16][1] > landmarks[14][1], # Ring finger
            landmarks[20][1] > landmarks[18][1]  # Pinky
        ])
        
        return thumb_up and fingers_down

    def is_peace_sign(self, landmarks):
        """Check for peace sign (index and middle finger up)"""
        # Index and middle fingers up
        index_up = landmarks[8][1] < landmarks[6][1]
        middle_up = landmarks[12][1] < landmarks[10][1]
        
        # Ring and pinky down
        ring_down = landmarks[16][1] > landmarks[14][1]
        pinky_down = landmarks[20][1] > landmarks[18][1]
        
        return index_up and middle_up and ring_down and pinky_down

    def is_fist(self, landmarks):
        """Check if all fingers are closed (fist)"""
        # All fingertips below their PIP joints
        return all([
            landmarks[8][1] > landmarks[6][1],   # Index finger
            landmarks[12][1] > landmarks[10][1], # Middle finger
            landmarks[16][1] > landmarks[14][1], # Ring finger
            landmarks[20][1] > landmarks[18][1], # Pinky
            landmarks[4][0] < landmarks[3][0] if landmarks[4][0] < landmarks[0][0] else landmarks[4][0] > landmarks[3][0]  # Thumb
        ])

    def is_open_palm(self, landmarks):
        """Check if all fingers are extended (open palm)"""
        # All fingertips above their PIP joints
        return all([
            landmarks[8][1] < landmarks[6][1],   # Index finger
            landmarks[12][1] < landmarks[10][1], # Middle finger
            landmarks[16][1] < landmarks[14][1], # Ring finger
            landmarks[20][1] < landmarks[18][1], # Pinky
            landmarks[4][1] < landmarks[3][1]    # Thumb
        ])

    def is_pointing(self, landmarks):
        """Check if only index finger is extended"""
        # Index finger up
        index_up = landmarks[8][1] < landmarks[6][1]
        
        # Other fingers down
        fingers_down = all([
            landmarks[12][1] > landmarks[10][1], # Middle finger
            landmarks[16][1] > landmarks[14][1], # Ring finger
            landmarks[20][1] > landmarks[18][1], # Pinky
        ])
        
        return index_up and fingers_down

    def display_gestures(self, frame, gestures, landmarks):
        """Display detected gestures on the frame"""
        if gestures:
            h, w, _ = frame.shape
            
            # Get hand center for text positioning
            x_coords = [landmark.x * w for landmark in landmarks.landmark]
            y_coords = [landmark.y * h for landmark in landmarks.landmark]
            center_x = int(sum(x_coords) / len(x_coords))
            center_y = int(sum(y_coords) / len(y_coords))
            
            # Display each gesture
            for i, gesture in enumerate(gestures):
                cv2.putText(frame, gesture, (center_x - 50, center_y - 30 + i * 25), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)