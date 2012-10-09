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
    CHEAT = [ K_UP, K_UP, K_DOWN, K_DOWN, K_LEFT, K_RIGHT, K_LEFT, K_RIGHT, K_b, K_a ]

    def setup(self):
        scr_size = self.app.screen.get_size()

        self.level = Level(scr_size)
        self.level.restart()

        self.cheat_idx = 0

        self.background = TiledImage(load_image("grass"))

        # makes things look a bit nicer for some reason
        w = self.background.rect.width
        self.background.rect.move_ip(-w/2, -w/2)

        self.l_shadow = ShadowLayer(scr_size)
        self.l_sprite = Layer(scr_size)

        self.sprites = Group()

        self.app.scores.reset()

        self.font = pygame.font.Font(None, 60) 

        self.cheating = False

        play_song("maintheme", volume=0.7)


    def resume(self):
        self.clock = pygame.time.Clock()
        pygame.mixer.music.unpause()

    def pause(self):
        pygame.mixer.music.pause()

    def handle_event(self, event):
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            self.level.player.cheating = False
            self.app.set_state(PauseMenu)

        elif event.type == KEYDOWN and event.key == self.CHEAT[self.cheat_idx]:
            self.cheat_idx += 1
        elif event.type == KEYDOWN:
            self.cheat_idx = 0

        if self.cheat_idx == len(self.CHEAT):
            self.cheat_idx = 0
            self.level.player.cheating = not self.level.player.cheating

    def update(self):
        dt = self.clock.tick(self.fps)
        self.level.update(dt)

        if self.level.player.cheating:
            self.cheating = True
            
        elif not self.level.player.cheating and len(self.level.coins) == 1:
            self.cheating = False
           
        if not self.cheating: 
            self.app.scores.update( len(self.level.coins) )
        else:
            self.app.scores.update(-1)


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

        # draw score

        score = self.font.render("Coins: %d" % self.app.scores.score, True, (255,255,255))
        rect = score.get_rect()
        rect.bottomleft = screen.get_rect().bottomleft
        screen.blit(score, rect)
        
        hiscore = self.font.render("Hiscore: %d" % self.app.scores.hiscore, True, (255,255,255))
        rect = hiscore.get_rect()
        rect.bottomright = screen.get_rect().bottomright
        screen.blit(hiscore, rect)

