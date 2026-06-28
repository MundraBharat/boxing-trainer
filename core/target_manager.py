import random
import time

def random_color():
    return (
        random.randint(150,255),
        random.randint(150,255),
        random.randint(150,255)
    )

class TargetManager:
    def __init__(self, spawn_interval=3, radius=50):
        self.spawn_interval = spawn_interval
        self.radius = radius
        self.last_spawn = time.time()

        #initial target
        self.x = 300
        self.y = 300
        self.color = random_color()

    def spawn(self, width, height):
        center_x = width // 2

        #horizontal zone: only center area
        min_x = center_x - 150
        max_x = center_x + 150

        #vertical zone: chest to head height
        min_y = int(height * 0.35)
        max_y = int(height * 0.55)

        self.x = random.randint(min_x, max_x)
        self.y = random.randint(min_y, max_y)
        self.color = random_color() #new random color everytime
        self.last_spawn = time.time()

    def auto_respawn(self, width, height):
        if time.time() - self.last_spawn > self.spawn_interval:
            self.spawn(width, height)