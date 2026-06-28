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
        
    def show_feedback(self, frame, x, y):
        if time.time() - self.feedback_time < 1:
            cv2.putText(frame, self.feedback, (x-40, y-60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,255), 3)
            
    def set_feedback(self, text):
        self.feedback = text
        self.feedback_time = time.time()