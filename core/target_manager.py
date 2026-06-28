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
        self.x = random.randint(150, width-150)
        self.y = random.randint(int(height * 0.4), int(height * 0.7))
        self.color = random_color() #new random color everytime
        self.last_spawn = time.time()

    def auto_respawn(self, width, height):
        if time.time() - self.last_spawn > self.spawn_interval:
            self.spawn(width, height)