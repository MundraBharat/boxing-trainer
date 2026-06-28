import numpy as np
import time

class PunchDetector:
    def __init__(self, speed_threshold=25):
        self.prev_right = None
        self.prev_left = None
        self.prev_time = time.time()
        self.speed_threshold = speed_threshold

    def distance(self, p1, p2):
        return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    def get_speed(self, prev, current, dt):
        if prev is None:
            return 0
        return self.distance(prev, current)/ dt
    
    def detect_hit(self, right, left, target, radius):
        now = time.time()
        dt = now - self.prev_time

        hit = False

        if right:
            speed_r = self.get_speed(self.prev_right, right, dt)
            if speed_r > self.speed_threshold and self.distance(right, target) < radius:
                hit = True

        if left:
            speed_l = self.get_speed(self.prev_left, left, dt)
            if speed_l > self.speed_threshold and self.distance(left, target) < radius:
                hit = True

        self.prev_right = right
        self.prev_left = left
        self.prev_time = now

        return hit