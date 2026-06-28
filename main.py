import cv2
import random
import time
import traceback

from core.camera import Camera
from core.pose_detector import PoseDetector
from core.target_manager import TargetManager
from core.punch_detector import PunchDetector
from ui.draw_utils import Drawer

GAME_DURATION = 60 # seconds per session

def run_game():
    cam = Camera()
    pose = PoseDetector()
    target = TargetManager()
    punch = PunchDetector()
    drawer = Drawer()

    score = 0
    start_time = time.time()

    #full screen window
    cv2.namedWindow("Boxing Trainer",cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Boxing Trainer",
                          cv2.WND_PROP_FULLSCREEN,
                          cv2.WINDOW_FULLSCREEN)
    
    try:
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
                cv2.circle(frame, right, 12, (255,0,0), -1)
            if left:
                cv2.circle(frame, left, 12, (0,0,255), -1)

            #Detect Punch
            if punch.detect_hit(right, left, (target.x, target.y), target.radius):
                score += 1
                drawer.set_feedback(random.choice(["Great!", "Nice!", "Super!", "Wow!", ""]))
                target.spawn(w,h)

            #Timer
            elapsed = time.time() - start_time
            seconds_left = max(0, int(GAME_DURATION - elapsed))

            #Draw score + feedback + timer
            drawer.draw_score(frame, score)
            drawer.show_feedback_center(frame)
            drawer.draw_timer(frame, seconds_left)

            cv2.imshow("Boxing Trainer", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 27 or key == ord('q'): #ESC or q
                break

            #auto-restart when time over
            if seconds_left <= 0:
                #pause to show score
                time.sleep(7)
                score = 0
                start_time = time.time()
                # clear feedback
                drawer.set_feedback("")
    
    except Exception as e:
        print("Error in game loop:")
        traceback.print_exc()
        time.sleep(5)

    finally:
        cam.release()

def main():
    while True:
        run_game()
        #if you want full exit after one session, break here
        #break

if __name__ == "__main__":
    main()