import random
import pygame
from circleshape import CircleShape
from constants import *
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        log_event("asteroid_split")

        # Calculate the new trajectory
        random_angle = random.uniform(20, 50)

        # Vector math for the fragments
        v1 = self.velocity.rotate(random_angle)
        v2 = self.velocity.rotate(-random_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS
        
        # Create two smaller shards
        shard1 = Asteroid(self.position.x, self.position.y, new_radius)
        shard1.velocity = v1 * 1.2 # Give them a little speed boost
        
        shard2 = Asteroid(self.position.x, self.position.y, new_radius)
        shard2.velocity = v2 * 1.2
    
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt
