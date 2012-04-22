"""
game.py

"""

import pygame
from pygame.locals import *
from pygame.sprite import spritecollide, Group

from core.app import Application
from core.resource import load_image, play_song
from graphics import Layer, ShadowLayer, TiledImage
from level import Level
from pausemenu import PauseMenu
from util import sortby_y_h

class Game(Application.State):
    fps = 60

    def setup(self):
        scr_size = self.app.screen.get_size()

        self.level = Level(scr_size)
        self.level.restart()

        self.background = TiledImage(load_image("grass"))

        # makes things look a bit nicer for some reason
        w = self.background.rect.width
        self.background.rect.move_ip(-w/2, -w/2)

        self.l_shadow = ShadowLayer(scr_size)
        self.l_sprite = Layer(scr_size)

        self.sprites = Group()

        if not hasattr(self.app, "hiscore"):
            self.app.hiscore = 0

        play_song("maintheme", volume=0.7)


    def resume(self):
        self.clock = pygame.time.Clock()
        pygame.mixer.music.unpause()

    def pause(self):
        pygame.mixer.music.pause()

    def handle_event(self, event):
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            self.app.set_state(PauseMenu)

    def update(self):
        dt = self.clock.tick(self.fps)
        self.level.update(dt)

        # handle scores
        self.score = len(self.level.coins)
        if self.score > self.app.hiscore:
            self.app.hiscore = self.score

    def draw(self, screen):
        self.l_shadow.clear()
        self.l_sprite.clear()

        # switch to layers
        screen.fill((80,80,80))
        self.background.draw(screen)
    
        # create a list of sprites we need to draw
        self.sprites.empty()
        self.sprites.add(self.level.player)
        for coin in self.level.coins:
            if coin.visible:
                self.sprites.add(coin)

        # sort the sprites by their height
        sprites = sorted(self.sprites, sortby_y_h)
        self.l_shadow.draw_sprites(sprites)
        self.l_sprite.draw_sprites(sprites)

        self.l_shadow.draw(screen)
        self.l_sprite.draw(screen)
