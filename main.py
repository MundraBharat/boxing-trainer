import cv2
import random

from core.camera import Camera
from core.pose_detector import PoseDetector
from core.target_manager import TargetManager
from core.punch_detector import PunchDetector
from ui.draw_utils import Drawer

def main():
    cam = Camera()
    pose = PoseDetector()
    target = TargetManager()
    punch = PunchDetector()
    drawer = Drawer()

    score = 0

    while True:
        frame = cam.get_frame()
        if frame is None:
            continue

        h, w, _ = frame.shape

        #auto respawn target
        target.auto_respawn(w, h)

        #Draw target
        drawer.draw_target(frame, target.x, target.y, target.radius, target.color)

        #Get wrist postions
        right, left = pose.get_wrist_positions(frame)

        #Draw wrist points if detected
        if right:
            cv2.circle(frame, right, 10, (0,255,0), -1)
        if left:
            cv2.circle(frame, left, 10, (0,0,255), -1)

        #Detect Punch
        if punch.detect_hit(right, left, (target.x, target.y), target.radius):
            score += 1
            drawer.set_feedback(random.choice(["Great!", "Nice!", "Super!", "Wow!"]))
            target.spawn(w,h)

        #Draw score + feedback
        drawer.draw_score(frame, score)
        drawer.show_feedback_center(frame)

        cv2.imshow("Boxing Trainer", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q'): #ESC or q
            break

    cam.release()

if __name__ == "__main__":
    main()