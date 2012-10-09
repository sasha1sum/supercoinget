import pygame

from core.app import Application
from mainmenu import MainMenu

def main():
    # initialize pygame
    pygame.init()
    pygame.display.set_mode((1024, 768))
    pygame.display.set_caption("Super Coin Get v1.0")
    pygame.display.toggle_fullscreen()

    # create game
    app = Application(MainMenu)
    try:
        app.run()
    except KeyboardInterrupt:
        app.quit()
    finally:
        pygame.display.quit()
        pygame.quit()
