import numpy as np
import pygame as pg
import random as rand


class Boid:
    # Define starting position and velocity
    def __init__(self, height, width, maxVelocity, maxAcceleration):
        self.position = pg.Vector2(rand.randint(0, width), rand.randint(0, height))
        self.velocity = pg.Vector2(rand.uniform(-maxVelocity, maxVelocity), rand.uniform(-maxVelocity, maxVelocity))
        self.acceleration = pg.Vector2(0, 0)
        self.maxVelocity = maxVelocity
        self.maxAcceleration = maxAcceleration

    # Return the distance to another boid
    def distance(self, boid):
        return np.linalg.norm(boid.position - self.position)

    # Update the boid's position and velocity based of velocity and acceleration
    # If a boid's speed is too fast, limit it
    def updatePosition(self):
        self.position += self.velocity
        self.velocity += self.acceleration

        if np.linalg.norm(self.velocity) > self.maxVelocity:
            self.velocity = self.velocity / np.linalg.norm(self.velocity) * self.maxVelocity

        self.acceleration = pg.Vector2(0, 0)

    # Compute a center of mass for boids in a range
    # Adjust boid's acceleration to direct towards that center of mass
    def cohesion(self, closeBoids):
        if len(closeBoids) < 1:
            return

        centerOfMass = pg.Vector2(0, 0)
        for boid in closeBoids:
            # Include all other boids, not self
            if boid == self:
                continue
            centerOfMass += boid.position

        centerOfMass /= len(closeBoids)

        dirToCOM = centerOfMass - self.position
        dirToCOM /= np.linalg.norm(dirToCOM)
        dirToCOM *= 0.25

        if np.linalg.norm(dirToCOM) > self.maxAcceleration:
            dirToCOM = dirToCOM / np.linalg.norm(dirToCOM) * self.maxAcceleration

        self.acceleration += dirToCOM

    # Compute an average velocity for boids in a range
    # Adjust boid's acceleration to direct towards that average velocity
    def alignment(self, closeBoids):
        if len(closeBoids) < 1:
            return

        avgVelocity = pg.Vector2(0, 0)
        for boid in closeBoids:
            # Include all other boids, not self
            if boid == self:
                continue
            avgVelocity += boid.velocity

        avgVelocity /= len(closeBoids)
        avgVelocity /= np.linalg.norm(avgVelocity)

        if np.linalg.norm(avgVelocity) > self.maxAcceleration:
            avgVelocity = avgVelocity / np.linalg.norm(avgVelocity) * self.maxAcceleration

        self.acceleration += avgVelocity

    def separation(self, closeBoids):
        if len(closeBoids) < 1:
            return

        sepDirection = pg.Vector2(0, 0)
        for boid in closeBoids:
            # Include all other boids, not self
            if boid == self:
                continue
            difference = self.position - boid.position
            difference /= self.distance(boid) * .8
            sepDirection += difference

        sepDirection /= len(closeBoids)
        sepDirection /= np.linalg.norm(sepDirection)
        sepDirection *= 0.25

        if np.linalg.norm(sepDirection) > self.maxAcceleration:
            sepDirection = sepDirection / np.linalg.norm(sepDirection) * self.maxAcceleration

        self.acceleration += sepDirection

    # Redefine str function to print the boid's current position
    def __str__(self):
        return "Boid Position: (" + str(self.xPosition) + ", " + str(self.yPosition) + ")"
