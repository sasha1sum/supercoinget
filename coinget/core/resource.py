import os
from os.path import abspath, dirname

import pygame

# this will not work with py2exe or PyApp, but works for everything else

import __main__
ROOT_DIR = dirname(abspath(__main__.__file__))
DATA_DIR = ROOT_DIR

SFX_DIR = os.path.join(DATA_DIR, "sounds")
MUSIC_DIR = os.path.join(DATA_DIR, "sounds", "music")
IMG_DIR = os.path.join(DATA_DIR, "images")

class ResourceManager(object):
    def __init__(self):
        self._root = dirname(abspath(__main__.__file))


def play_song(song, times=-1, volume=1.0):
    path = os.path.join(MUSIC_DIR, song + ".ogg")
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(times)


_images = {}
def load_image(name):
    if name not in _images:
        path = os.path.join(IMG_DIR, name + ".bmp")
        _images[name] = pygame.image.load(path)

    return _images[name].convert()

_sfx = {}
def load_sfx(name):
    if name not in _sfx:
        path = os.path.join(SFX_DIR, name + ".ogg")
        _sfx[name] = pygame.mixer.Sound(path)

    return _sfx[name]
