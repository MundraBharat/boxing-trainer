import numpy as np
import time

class PunchDetector:
    def __init__(self, speed_threshold=40, margin_factor=2.0):
        self.prev_right = None
        self.prev_left = None
        self.prev_time = time.time()
        
        self.speed_threshold = speed_threshold
        #hit zone ke bahr se andr aane ki condition
        self.margin_factor = margin_factor # radius * factor = outer zone

    def distance(self, p1, p2):
        return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    def detect_hit(self, right, left, target, radius):
        now = time.time()
        dt = now - self.prev_time
        if dt == 0:
            dt = 0.001

        hit = False
        outer_radius = radius * self.margin_factor 

        def check_punch(prev, curr):
            if prev is None or curr is None:
                return False
            
            #speed
            speed = self.distance(prev,curr) / dt
            if speed < self.speed_threshold:
                return False
            
            #distances
            prev_dist = self.distance(prev, target)
            curr_dist = self.distance(curr, target)

            if curr_dist > prev_dist:
                return False

            #condition
            # 1. phle outer zone k bahr tha
            # 2. ab inner radius k andr aa gya
            # 3. movement target k trf h
            if prev_dist > outer_radius and curr_dist < radius:
                return True
            
            return False

        #right hand
        if right and check_punch(self.prev_right, right):
            hit = True

        #left hand
        if left and check_punch(self.prev_left, left):
            hit = True

        self.prev_right = right
        self.prev_left = left
        self.prev_time = now

        return hit