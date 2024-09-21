import numpy as np
import sys
from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))


class Particle:
    def __init__(self, pos, acceleration, velocity, mass, is_blocked):
        self.pos = pos
        self.acceleration = acceleration
        self.velocity = velocity
        self.mass = mass
        self.is_blocked = is_blocked
        self.radius = 20

    def update(self):
        if not self.is_blocked:
            for par in particles:
                if self != par:
                    # print(np.linalg.norm(np.subtract(self.pos, par.pos)))
                    if np.linalg.norm(np.subtract(self.pos, par.pos)) < self.radius:
                        # print('coll', self.pos[0] - par.pos[0])
                        print((self.pos - par.pos)/1000000 - self.acceleration)
                        # self.acceleration = ((self.pos - par.pos)/1000000000) - self.acceleration
                        self.pos = self.pos - par.pos + self.pos
                        # print(self.pos)

            if self.pos[1]+10 > height:
                self.acceleration[1] = 0#(self.pos[1] - height) / 2
                self.pos[1] = height-10

            self.acceleration = self.acceleration * 0.98
            self.velocity = self.acceleration

            self.pos = self.velocity + self.pos

    def draw(self):
        idx = next((i for i, x in enumerate(particles) if x == self), None)
        pygame.draw.circle(screen, colors[idx], self.pos, self.radius)
        # pygame.draw.circle(screen, 'white', self.pos, self.radius)


colors = ['white', 'red', 'purple', 'blue', 'green', 'yellow']


class Spring:
    def __init__(self, k, rest_length, a, b):
        self.k = k
        self.rest_length = rest_length
        self.a = a
        self.b = b

    def update(self):
        force = np.subtract(self.a.pos, self.b.pos)
        x = np.linalg.norm(force) - self.rest_length

        force = force / np.linalg.norm(force)

        force = force * (self.k * x)

        self.a.acceleration = self.a.acceleration - (force-gravity)*self.a.mass
        self.b.acceleration = self.b.acceleration + (force+gravity)*self.b.mass

    def draw(self):
        pygame.draw.line(screen, 'red', self.a.pos, self.b.pos)


gravity = np.array([0, 0.18])
# gravity = np.array([0, 0])

particles = []
particles.append(Particle(np.array([200, 50]), np.array([0, 0]), np.array([0, 0]), 1, False))
particles.append(Particle(np.array([250, 50]), np.array([0, 0]), np.array([0, 0]), 1, False))
particles.append(Particle(np.array([200, 100]), np.array([0, 0]), np.array([0, 0]), 1, False))
particles.append(Particle(np.array([250, 100]), np.array([0, 0]), np.array([0, 0]), 1, False))
particles.append(Particle(np.array([300, 50]), np.array([0, 0]), np.array([0, 0]), 1, False))
particles.append(Particle(np.array([300, 100]), np.array([0, 0]), np.array([0, 0]), 1, False))

springs = []
springs.append(Spring(0.2, 70, particles[0], particles[3]))
springs.append(Spring(0.2, 70, particles[1], particles[2]))
springs.append(Spring(0.2, 50, particles[0], particles[1]))
springs.append(Spring(0.2, 50, particles[1], particles[3]))
springs.append(Spring(0.2, 50, particles[3], particles[2]))
springs.append(Spring(0.2, 50, particles[2], particles[0]))

springs.append(Spring(0.2, 60, particles[4], particles[5]))
springs.append(Spring(0.2, 60, particles[3], particles[4]))
springs.append(Spring(0.2, 60, particles[1], particles[5]))
springs.append(Spring(0.2, 60, particles[1], particles[4]))
springs.append(Spring(0.2, 60, particles[3], particles[5]))

# particles = []
# num = 20
# for i in range(num):
#     particles.append(Particle(np.array([200 + i * 30, i * 10]), np.array([0, 0]), np.array([0, 0]), 1, False))
#
# springs = []
# for i in range(num - 1):
#     springs.append(Spring(0.2, 10, particles[i], particles[i + 1]))
#
# particles[0].is_blocked = True
key = False
# Game loop.
while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_w:
                key = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                key = False

    if key:
        for par in particles:
            par.acceleration[1] -= 5*gravity[1]

    # Update.
    for spring in springs:
        spring.update()
        spring.draw()

    if pygame.mouse.get_pressed()[0]:
        particles[-1].pos = list(pygame.mouse.get_pos())

    for par in particles:
        par.update()
        par.draw()

    # par1.update()
    # par2.update()
    #
    # par1.draw()
    # par2.draw()
    #
    # spr1.update()
    # print(par1.pos, par2.pos)
    # Draw.

    pygame.display.flip()
    fpsClock.tick(fps)
