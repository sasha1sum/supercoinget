"""
game.py

"""

import pygame
from pygame import Rect, Surface
from pygame.locals import *
from pygame.sprite import spritecollide, GroupSingle

from core.app import Application
from core.resource import load_sfx
from graphics import TextBlock

class PauseMenu(Application.State):
    keys = {
        "quit": [ K_q ],
        "resume": [ K_ESCAPE, K_SPACE ],
        "restart": [ K_r ]
    }

    def setup(self):
        self.sfx = load_sfx("pause")

    def resume(self):
        self.game = self.app.state

        screen = pygame.display.get_surface()
        frame = screen.convert_alpha()
        frame.fill((0,0,0,128))
        screen.blit(frame, (0,0))

        # render instructions
        font = pygame.font.Font(None, 40)
        tb = TextBlock(font, padding=10, justify=TextBlock.CENTER)

        inst = []
        for term in sorted(self.keys):
            word = term.capitalize()
            keys = " or ".join( "<%s>" % pygame.key.name(k).upper() for k in self.keys[term] )
            text = "Press %s to %s" % (keys, word)
            inst.append(text)

        block = tb.render(inst, True, (255,255,255))
        rect = block.get_rect()
        rect.center = screen.get_rect().center
        screen.blit(block, rect)

        # play menu sound
        self.sfx.play()

    def pause(self):
        # stop just in case the stop is still playing
        self.sfx.stop()

    def handle_event(self, event):
        if event.type == KEYDOWN and event.key in self.keys["quit"]:
            from mainmenu import MainMenu
            self.app.set_state(MainMenu)
        elif event.type == KEYDOWN and event.key in self.keys["restart"]:
            self.app.set_state(self.game.__class__)
        elif event.type == KEYDOWN and event.key in self.keys["resume"]:
            self.app.set_state(self.game)


