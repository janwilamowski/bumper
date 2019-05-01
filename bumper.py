#!/usr/bin/env python3

from __future__ import division

import math
import random
import sys
import time

import pygame
from pygame.locals import *

from ball import Ball
from constants import ball_colors, WIDTH, HEIGHT, BLACK, GREEN, WHITE
from player import Player


random.seed()
pygame.init()
pygame.display.set_caption('BUMP \'EM ALL')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.key.set_repeat(10, 10)
clock = pygame.time.Clock()

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
        # t0 = time.time()
        player.bump(ball, True)
        # t1 = time.time()
        ball.update()
        # t2 = time.time()
        ball.draw()
        # t3 = time.time()
        for other in balls[i+1:]:
            ball.bump(other)
        # t4 = time.time()
        # bumptime += t1-t0 + t4-t3
        # updatetime += t2-t1
        # drawtime += t3-t2
        # sumtime = bumptime + updatetime + drawtime
    # print('{:.3f} {:.3f} {:.3f} = {:.3f} ({:.3f} fps)'.format(bumptime*1000, updatetime*1000, drawtime*1000, sumtime*1000, clock.get_fps()))

    if show_fps:
        fps = clock.get_fps()
        fps_text = small_font.render('{:.3f}'.format(fps), 1, BLACK)
        screen.blit(fps_text, fps_text_pos)

    pygame.display.flip()

pygame.quit()
