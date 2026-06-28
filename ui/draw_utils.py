import cv2
import time

class Drawer:
    def __init__(self):
        self.feedback = ""
        self.feedback_time = 0

    def draw_target(self, frame, x, y, radius):
        cv2.circle(frame, (x,y), radius, (0,255,0), -1)

    def draw_score(self, frame, score):
        cv2.putText(frame, f"Score: {score}", (20,50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,255,255), 3)
        
    def show_feedback_center(self, frame):
        if time.time() - self.feedback_time < 1:
            h, w, _ = frame.shape
            cv2.putText(frame, self.feedback, (w//2 - 100, h//2),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,255), 5)
            
    def set_feedback(self, text):
        self.feedback = text
        self.feedback_time = time.time()