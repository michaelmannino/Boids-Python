import pygame as pg
import sys

from boid import Boid

# Define constants
MAX_VELOCITY = 3
MAX_ACCELERATION = 5
VIEW_DISTANCE = 50
BOID_COLOR = (255, 243, 177)
BG_COLOR = (50, 50, 100)

# Initialize pygame
pg.init()

# Set size of and create screen
size = width, height = 800, 600
screen = pg.display.set_mode(size)

# Create flock
numberOfBoids = 30
flock = []
for i in range(numberOfBoids):
    flock.append(Boid(height, width, MAX_VELOCITY, MAX_ACCELERATION))

# Define initial conditions for boids to follow
runCohesion = False
runAlignment = False
runSeparation = False

# Run simulation
while True:
    # Set game to update 600x/second
    pg.time.Clock().tick(600)

    # Iterate through events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_1:
                runCohesion = not runCohesion
            if event.key == pg.K_2:
                runAlignment = not runAlignment
            if event.key == pg.K_3:
                runSeparation = not runSeparation

    screen.fill(BG_COLOR)

    # Iterate through each boid
    for boid in flock:
        # Fill array will all boids within view distance
        closeBoids = []
        for otherBoid in flock:
            if boid == otherBoid:
                continue
            if boid.distance(otherBoid) < VIEW_DISTANCE:
                closeBoids.append(otherBoid)

        # Check positions to ensure boids stay on the screen
        # Boids that leave the screen will reappear on the opposite side
        if boid.position.x < 0:
            boid.position.x = width
        if boid.position.x > width:
            boid.position.x = 0
        if boid.position.y < 0:
            boid.position.y = height
        if boid.position.y > height:
            boid.position.y = 0

        # Run cohesion, alignment, and separation algorithms
        if runCohesion:
            boid.cohesion(closeBoids)
        if runAlignment:
            boid.alignment(closeBoids)
        if runSeparation:
            boid.separation(closeBoids)

        # Update boids position
        boid.updatePosition()

    # Draw boids to screen
    for boid in flock:
        boidPosition = round(boid.position.x), round(boid.position.y)
        pg.draw.circle(screen, BOID_COLOR, boidPosition, 1)

    # Update screen
    pg.display.flip()
