import mediapipe as mp
import cv2

class PoseDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()

    def get_wrist_positions(self, frame):
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.pose.process(rgb)

        if not result.pose_landmarks:
            return None, None
        
        lm = result.pose_landmarks.landmark

        rw = lm[self.mp_pose.PoseLandmark.RIGHT_WRIST]
        lw = lm[self.mp_pose.PoseLandmark.LEFT_WRIST]

        right = (int(rw.x * w), int(rw.y * h))
        left = (int(lw.x * w), int(lw.y * h))

        return right, left