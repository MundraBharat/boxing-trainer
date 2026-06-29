import numpy as np
import time
from collections import deque

class PunchDetector:
    def __init__(self, speed_threshold=35, travel_threshold=35, buffer_size=5):
        self.prev_time = time.time()

        #frame buffer( for last 5 wrist position)
        self.right_buffer = deque(maxlen=buffer_size)
        self.left_buffer = deque(maxlen=buffer_size)
        
        self.speed_threshold = speed_threshold
        self.travel_threshold = travel_threshold

    def distance(self, p1, p2):
        return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    def detect_hit(self, right, left, target, radius):
        now = time.time()
        dt = now - self.prev_time
        if dt == 0:
            dt = 0.001

        hit = False

        #add to buffers
        if right:
            self.right_buffer.append(right)
        if left:
            self.left_buffer.append(left)

        def check_punch(buffer):
            if len(buffer) < 3:
                return False
            
            p1, p2, p3 = buffer[-3], buffer[-2], buffer[-1]
            
            #speed check
            speed = self.distance(p2,p3) / dt
            if speed < self.speed_threshold:
                return False
            
            #direction check
            prev_dist = self.distance(p2, target)
            curr_dist = self.distance(p3, target)

            if curr_dist > prev_dist:
                return False

            # travel check
            travel = prev_dist - curr_dist
            if travel < self.travel_threshold:
                return False
            
            #hit check
            if curr_dist < radius:
                return True
            
            return False

        #right hand
        if right and check_punch(self.right_buffer):
            hit = True

        #left hand
        if left and check_punch(self.left_buffer):
            hit = True

        self.prev_time = now
        return hit