#!/usr/bin/env python3

from __future__ import division

import math
import random
import sys
import time

import numpy as np
import pygame
from numpy.linalg import norm
from pygame.locals import *

random.seed()
pygame.init()
pygame.display.set_caption('BUMP \'EM ALL')
WIDTH, HEIGHT = SCREEN_SIZE = (640, 480)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.key.set_repeat(10, 10)
clock = pygame.time.Clock()

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


class Player(Ball):
    def __init__(self, size, pos, color, screen, dir=0, speed=0):
        super().__init__(size, pos, color, screen, dir, speed)
        self.step = 3

    def fix_pos(self):
        self.pos = np.maximum(0, np.minimum(self.pos, SCREEN_SIZE))

    def up(self):
        self.pos -= (0, self.step)
        self.fix_pos()

    def down(self):
        self.pos += (0, self.step)
        self.fix_pos()

    def right(self):
        self.pos += (self.step, 0)
        self.fix_pos()

    def left(self):
        self.pos -= (self.step, 0)
        self.fix_pos()

    def move(self, pos):
        self.pos = np.array(pos)

    def __repr__(self):
        return 'Player' + super().__repr__()


BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
ball_colors = (BLUE, RED, YELLOW, CYAN, MAGENTA, BLACK)

player = Player(5, (WIDTH//2, HEIGHT//2), GREEN, screen)

num_balls = 33
balls = []
for _ in range(num_balls):
    size = random.randint(5, 10)
    pos = (random.randint(10, 630), random.randint(10, 470))
    color = random.choice(ball_colors)
    dir = random.random() * 2 * math.pi
    speed = random.random() * 2 + 0.1
    ball = Ball(size, pos, color, screen, dir, speed)
    balls.append(ball)

font_file = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
small_font = pygame.font.Font(font_file, 16)
fps_text_pos = pygame.Rect(WIDTH-50, 2, WIDTH, 30)

running = show_fps = True
while running:
    clock.tick(50)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            break

    pressed = pygame.key.get_pressed()
    if pressed[K_ESCAPE]:
        break
    if pressed[K_UP]:
        player.up()
    elif pressed[K_DOWN]:
        player.down()
    if pressed[K_RIGHT]:
        player.right()
    elif pressed[K_LEFT]:
        player.left()
    if pressed[K_f]:
        show_fps = not show_fps

    if any(pygame.mouse.get_rel()):
        player.move(pygame.mouse.get_pos())

    # check win condition
    if all(ball.color == GREEN for ball in balls):
        print('YOU WON')
        break

    screen.fill(WHITE)
    player.draw()
    bumptime = updatetime = drawtime = 0
    for i, ball in enumerate(balls):
        t0 = time.time()
        player.bump(ball, True)
        t1 = time.time()
        ball.update()
        t2 = time.time()
        ball.draw()
        t3 = time.time()
        for other in balls[i+1:]:
            ball.bump(other)
        t4 = time.time()
        bumptime += t1-t0 + t4-t3
        updatetime += t2-t1
        drawtime += t3-t2
        sumtime = bumptime + updatetime + drawtime
    # print('{:.3f} {:.3f} {:.3f} = {:.3f} ({:.3f} fps)'.format(bumptime*1000, updatetime*1000, drawtime*1000, sumtime*1000, clock.get_fps()))

    if show_fps:
        fps = clock.get_fps()
        fps_text = small_font.render('{:.3f}'.format(fps), 1, BLACK)
        screen.blit(fps_text, fps_text_pos)

    pygame.display.flip()

pygame.quit()
