"""
game.py

"""

import pygame
from pygame.locals import *
from pygame.sprite import spritecollide, GroupSingle

from core.app import Application
from core.resource import load_image, play_song
from coin import CoinAnimation
from game import Game
from graphics import Animation, TiledImage
from score import Score

class MenuBackground(TiledImage):
    bg_color = 255, 200, 0
    image = Animation.frameproperty("anim")
    speed = -20

    def __init__(self):
        self.anim = CoinAnimation(500)
        self.rect = self.image.get_rect()
        self.rect.width *= 2
        self.rect.height *= 2
        self.offset = 0

    def update(self, dt):
        self.anim.update(dt)

        self.offset += self.speed * (dt / 1000.0)
        self.rect.x = self.rect.y = self.offset

    def draw(self, surf, rect=None):
        if rect is None:
            rect = surf.get_rect()

        surf.fill(self.bg_color)

        # draw the image twice, once offset
        orig_rect = self.rect
        TiledImage.draw(self, surf, rect)
        self.rect = self.rect.move(self.rect.width / 2, self.rect.height / 2)
        TiledImage.draw(self, surf, rect)
        self.rect = orig_rect



class MainMenu(Application.State):
    fg_color = 255,255,255
    bg_color = 0,0,0
    flash_rate = 500

    def setup(self):
        if not hasattr(self.app, "scores"):
            self.app.scores = Score()

        self.title = load_image("logo")

        font = pygame.font.Font(None, 60)
        font.set_italic(True)
        self.inst = font.render("Press <SPACE> to Start", True, self.fg_color, self.bg_color)

        font.set_italic(False)
        self.score = font.render("Hiscore: %05d" % self.app.scores.hiscore, True, self.fg_color, self.bg_color)

        self.anim = CoinAnimation(duration=100000)
        self.background = MenuBackground()

        play_song("title")

    def resume(self):
        self.clock = pygame.time.Clock()
        self.time = 0

    def handle_event(self, event):
        if event.type == KEYDOWN and (event.key == K_q or event.key == K_ESCAPE):
            self.app.quit()
        elif event.type == KEYDOWN and event.key == K_SPACE:
            self.app.set_state(Game)

    def update(self):
        dt = self.clock.tick(30)

        self.time += dt
        self.time %= 2 * self.flash_rate
        self.draw_inst = self.time < self.flash_rate

        self.background.update(dt)


    def draw(self, screen):
        bounds = screen.get_rect()

        screen.fill(self.bg_color)

        self.background.draw(screen)
        
        rect = self.title.get_rect()
        rect.center = bounds.centerx, bounds.centery - bounds.height / 4
        screen.blit(self.title, rect)

        rect = self.score.get_rect()
        rect.midbottom = bounds.midbottom
        screen.blit(self.score, rect)

        if self.draw_inst:
            rect = self.inst.get_rect()
            rect.center = bounds.centerx, bounds.centery + bounds.height / 4
            screen.blit(self.inst, rect)

