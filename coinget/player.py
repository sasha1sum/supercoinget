"""
player.py

"""
import math
from random import choice

import pygame
from pygame.locals import *
from pygame import Surface
from pygame.sprite import Sprite

from graphics import Animation, SpriteSheet
from core.resource import load_image

DIAG = 1 / math.sqrt(2)

class PlayerAnimation(Animation):
    _rows = {( 0, 1): 0,
             (-1, 0): 1,
             ( 1, 0): 2,
             ( 0,-1): 3,
             (-1, 1): 4,
             (-1,-1): 5,
             ( 1, 1): 6,
             ( 1,-1): 7 }

    def __init__(self, player, image, duration):
        self.player = player
        self.row = self._rows[(0, 1)]
    
        spritesheet = SpriteSheet(image, (3, 8))
        frames = [ (duration, 0),
                   (duration, 1),
                   (duration, 2),
                   (duration, 1) ]

        Animation.__init__(self, spritesheet, frames)

    def update(self, dt):
        vx, vy = self.player.vx, self.player.vy

        # calculate the direction facing
        try:
            vx /= abs(vx)
        except:
            vx = 0

        try:
            vy /= abs(vy)
        except:
            vy = 0

        # figure out spritesheet row
        if vx == 0 and vy == 0:
            self.time = 0
            self.col = 1
        else:
            self.time += dt
            self.col = self.get_frame_data(self.time)
            self.row = self._rows[(vx, vy)]


class Player(Sprite):
    speed = 300

    def __init__(self, level):
        Sprite.__init__(self)
        self.vx = 0
        self.vy = 0
        self.level = level
        self.target = None
        self.cheating = False

        ply_img = load_image("mario")
        self.anim = PlayerAnimation(self, ply_img, 80)
        self.image = self.anim.get_current_frame()
        self.rect = self.image.get_rect()


    def update(self, dt):
        self.anim.update(dt)
        self.image = self.anim.get_current_frame()

        self.vx, self.vy = 0, 0

        # ai controls
        if self.cheating:
            if self.target is None or not self.target.alive():
                coins = [ coin for coin in self.level.coins.sprites() if coin.height == 0 ]
                if len(coins) > 0:
                    self.target = choice(coins) 

            if self.target:
                dx = self.target.orig_rect.centerx - self.rect.centerx
                dy = self.target.orig_rect.centery - self.rect.centery

                self.vx = math.copysign(self.speed, dx) if abs(dx) > 5 else 0
                self.vy = math.copysign(self.speed, dy) if abs(dy) > 5 else 0

        # keyboard controls
        else:
            keys = pygame.key.get_pressed()
            if keys[K_UP]:
                self.vy = -self.speed
            if keys[K_DOWN]:
                self.vy =  self.speed
            if keys[K_LEFT]:
                self.vx = -self.speed
            if keys[K_RIGHT]:
                self.vx =  self.speed

        if self.vx and self.vy:
            self.vx *= DIAG
            self.vy *= DIAG

        dt = dt / 1000.0
        self.rect.x += self.vx * dt
        self.rect.y += self.vy * dt
