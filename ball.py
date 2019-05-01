import math
import pygame
import numpy as np
from numpy.linalg import norm

from constants import GREEN, WIDTH, HEIGHT


class Ball(object):
    def __init__(self, size, pos, color, screen, dir=0, speed=0):
        self.size = size
        self.color = color
        self.pos = np.array(pos)
        self.screen = screen
        vx = speed * math.cos(dir)
        vy = speed * math.sin(dir)
        self.v = np.array([vx, vy])
        # print(self.pos, speed, self.v)

    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.pos.astype(int), self.size)

    def bump(self, other, is_player=False):
        m1 = self.size
        m2 = other.size
        dpos = self.pos - other.pos
        d = sum(dpos*dpos)
        m1m2 = m1 + m2
        if d > m1m2*m1m2: return
        # print('bump:', self, other, d)
        v1, v2 = self.v, other.v
        x1, x2 = self.pos, other.pos
        self.v  = v1 - 2*m2/(m1 + m2) * np.dot(v1-v2, x1-x2) / np.square(norm(x1-x2)) * (x1-x2)
        other.v = v2 - 2*m1/(m1 + m2) * np.dot(v2-v1, x2-x1) / np.square(norm(x2-x1)) * (x2-x1)
        if is_player:
            other.color = GREEN
        elif self.color == GREEN:
            self.color = other.color
        elif other.color == GREEN:
            other.color = self.color
        else:
            # bigger one wins
            if self.size > other.size:
                other.color = self.color
            elif self.size < other.size:
                self.color = other.color

    def update(self):
        if not self.v.any(): return

        new_pos = self.pos + self.v
        new_x, new_y = new_pos

        if not (self.size < new_x < WIDTH - self.size):
            self.v *= (-1, 1)
        if not (self.size < new_y < HEIGHT - self.size):
            self.v *= (1, -1)

        self.pos = new_pos

    def __repr__(self):
        return 'Ball (size={}, color={}, pos={})'.format(self.size, self.color, self.pos)
