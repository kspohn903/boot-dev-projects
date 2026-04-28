import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from logger import log_state, log_event # Added log_event
from shot import Shot
import os
import sys

def main(fps=60, bg_color_string="black"):
    pygame.init()
    
    # Use the constants for the display mode
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    dt = 0

    #print("Starting Asteroids...")
    #print(f"Screen width: {SCREEN_WIDTH}")
    #print(f"Screen height: {SCREEN_HEIGHT}")
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group() # New group for collision tracking later
    shots = pygame.sprite.Group()

    # Set up static containers
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = (updatable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Player.containers = (updatable, drawable)

    asteroid_field = AsteroidField()

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        # Step 1. Update track: Call update on the group itself
        updatable.update(dt)

        # Collision Check Track
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                print("Game over!")
                sys.exit()

            # Line Item #1: Destruction and Logging
            for shot in shots:
                if asteroid.collides_with(shot):
                    asteroid.split()
                    shot.kill()
                    log_event("asteroid_shot") # Crucial for the CLI test

        # Step 2: Update game state (Logging happens here for now)
        log_state()

        # Step 3: Draw the game to the screen
        
        # bg_color_rgb_tuple = (0,0,0)
        screen.fill(bg_color_string) # paint the background
        
        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip() # Show the finished frame to the user
        dt = clock.tick(fps) / NUM_MS_PER_S

if __name__ == "__main__":
    main()
