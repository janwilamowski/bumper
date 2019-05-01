import numpy as np
from ball import Ball
from constants import SCREEN_SIZE


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
