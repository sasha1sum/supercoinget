"""
level.py

"""

import os

import pygame
from pygame import Rect, Surface
from pygame.sprite import GroupSingle, spritecollide

from core.resource import load_image, play_song
from player import Player
from coin import CoinGroup

class Level(object):
    def __init__(self, size):
        self.bounds = Rect((0,0), size)

    def restart(self):
        self.player = Player(self)
        self.player.rect.center = self.bounds.center

        self.coins = CoinGroup(self.bounds)

    def update(self, dt):
        self.player.update(dt)
        self.coins.update(dt)

        # lock player in bounds
        self.player.rect.clamp_ip(self.bounds)

        # collide player with coins
        for coin in spritecollide(self.player, self.coins, False):
            coin.collect(self.player)
