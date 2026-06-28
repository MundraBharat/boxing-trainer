import cv2
import time

class Drawer:
    def __init__(self):
        self.feedback = ""
        self.feedback_time = 0

    def draw_target(self, frame, x, y, radius, color):
        # glow effect
        cv2.circle(frame, (x,y), radius + 10, (255,255,255), 2)
        #inner circle
        cv2.circle(frame, (x,y), radius, color, -1)

    def draw_score(self, frame, score):
        cv2.putText(frame, f"Score: {score}", (20,70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.8, (255,255,0), 4)
        
    def draw_timer(self, frame, seconds_left):
        cv2.putText(frame, f"Time: {seconds_left}s", (20,130),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0,255,255), 3)
        
    def show_feedback_center(self, frame):
        if time.time() - self.feedback_time < 1:
            h, w, _ = frame.shape
            cv2.putText(frame, self.feedback, (w//2 - 160, h//2),
                        cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0,255,255), 6)
            
    def set_feedback(self, text):
        self.feedback = text
        self.feedback_time = time.time()