import mediapipe as mp
import cv2

class PoseDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        #previous stable wrist positions
        self.prev_right = None
        self.prev_left = None

    #reject sudden jumps (mediapipe jitter fix)
    def reject_jump(self, prev, curr, max_jump=300):
        if prev is None:
            return curr
        if abs(prev[0] - curr[0]) > max_jump or abs(prev[1] - curr[1]) > max_jump:
            return prev #ignore this frame
        return curr
        
    #smooth wrist movement(low pass filter)
    def smooth(self, prev, curr, factor=0.15):
        if prev is None:
            return curr
        x = int(prev[0] * factor + curr[0] * (1 - factor))
        y = int(prev[1] * factor + curr[1] * (1 - factor))
        return (x,y)

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

        #reject sudden jump
        right = self.reject_jump(self.prev_right, right)
        left = self.reject_jump(self.prev_left, left)

        #smooth movement
        right = self.smooth(self.prev_right, right)
        left = self.smooth(self.prev_left, left)

        #save stable positions
        self.prev_right = right
        self.prev_left = left

        return right, left