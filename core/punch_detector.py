import numpy as np
import time
from collections import deque

class PunchDetector:
    def __init__(self, speed_threshold=1000, accel_threshold=500, travel_threshold=35, buffer_size=5):
        self.prev_time = time.time()

        #frame buffer( for last 5 wrist position)
        self.buffer = {
            "right" : deque(maxlen=buffer_size),
            "left" : deque(maxlen=buffer_size)
        }
        
        self.speed_threshold = speed_threshold
        self.accel_threshold = accel_threshold
        self.travel_threshold = travel_threshold

    def distance(self, p1, p2):
        return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    def detect_hit(self, right, left, target, radius):
        now = time.time()
        dt = 1/30
        #dt = now - self.prev_time
        #if dt == 0:
        #    dt = 0.001

        hit = False
        impact_radius = radius * 1.1 #expand impact zone

        def check_punch(hand, curr):
            buffer = self.buffer[hand]

            if curr:
                buffer.append(curr)

            if len(buffer) < 4:
                return False
            
            p1, p2, p3, p4 = buffer[-4], buffer[-3], buffer[-2], buffer[-1]
            print("distance: ", p1,p2,p3,p4)

            #velocity peak
            v1 = self.distance(p1, p2) / dt
            v2 = self.distance(p2, p3) / dt
            v3 = self.distance(p3, p4) / dt
            print("velocity:", v1,v2,v3)

            peak_speed = max(v1, v2, v3)
            if peak_speed < self.speed_threshold:
                return False
            
            #acceleration
            accel1 = v2 - v1
            accel2 = v3 - v2
            peak_accel = max(accel1, accel2)

            if peak_accel < self.accel_threshold:
                return False
            
            #forward momentum
            d1 = self.distance(p1, target)
            d2 = self.distance(p2, target)
            d3 = self.distance(p3, target)
            d4 = self.distance(p4, target)

            forward = (d1 - d2) + (d2 - d3) + (d3 - d4)
            if forward < self.travel_threshold:
                return False
            
            #impact zone
            if d4 < impact_radius:
                return True
            
            return False
            
        #right hand
        if right and check_punch("right", right):
            hit = True

        #left hand
        if left and check_punch("left", left):
            hit = True

        self.prev_time = now
        return hit