from random import randrange

from pygame import Surface
from pygame.sprite import Sprite, Group

from graphics import Animation, SpriteSheet
from core.resource import load_image, load_sfx


class CoinAnimation(Animation):
    frames = 8

    def __init__(self, duration=10):
        coin_img = load_image("coin")
        self.spritesheet = SpriteSheet(coin_img, (self.frames, 1))
        
        self.time = 0
        self.duration = duration

        self.row = 0
        self.col = 0

    def update(self, dt):
        self.time += dt
        if self.time > self.duration:
            self.time %= self.duration
            self.col += 1
            self.col %= self.frames



## Coin
class Coin(Sprite):
    life = 12000
    dying = 3000
    flash_rate = 150

    height = 2000
    vy = -1000
    gravity = 1000

    bounces = 3
    bounce_factor = 4   # how much to cut the vy each bounce
    
    anim_speedup = 3

    def __init__(self, loc):
        Sprite.__init__(self)

        self.anim = CoinAnimation()
        self.image = self.anim.get_current_frame()
        self.orig_rect = self.image.get_rect()
        self.orig_rect.topleft = loc

        self.sfx = load_sfx("coin")
        self.visible = True
        self.falling = True
        self.bounce = 0

        self.update(0)


    def update(self, dt):
        self.image = self.anim.get_current_frame()
        self.anim.update(dt)

        # slowly kill the coin
        self.life -= dt
        if self.life < 0:
            self.kill()

        # make player fall
        if self.falling:
            self.height += self.vy * (dt / 1000.0)
            self.vy -= self.gravity * (dt / 1000.0)

            if self.height < 0:
                self.height = 0
                self.vy = -self.vy / self.bounce_factor
                self.anim.duration *= self.anim_speedup
                self.bounce += 1

            self.rect = self.orig_rect.move(0, -self.height)

            if self.bounce >= self.bounces:
                self.falling = False
                self.anim.duration = 240
        
        # set visible variable to hide the coin with a flash
        if self.life < self.dying:
            self.visible = (self.life / self.flash_rate) % 2
        else:
            self.visible = True


    def collect(self, sprite):
        dh = sprite.rect.y - self.rect.y

        # collect if on the ground or player is "bellow" the coin
        if self.height == 0 or self.height < dh + sprite.rect.height:
            self.sfx.stop()
            self.sfx.play()

            # create 2 new coins in the spawner
            if hasattr(self, "spawner"):
                self.spawner.spawn()
                self.spawner.spawn()

            self.kill()



class CoinGroup(Group):

    def __init__(self, bounds):
        Group.__init__(self)

        self.bounds = bounds.copy()

        # adjust bounds to compensate for coin size
        coin_img = load_image("coin")
        spritesheet = SpriteSheet(coin_img, (8, 1))
        self.bounds.width -= spritesheet.width
        self.bounds.height -= spritesheet.height

    def spawn(self):
        x = randrange(self.bounds.x, self.bounds.x + self.bounds.width)
        y = randrange(self.bounds.y, self.bounds.y + self.bounds.height)

        coin = Coin((x,y))
        coin.spawner = self
        self.add(coin)

    def update(self, dt):
        Group.update(self, dt)

        if len(self) < 1:
            self.spawn()

    def draw(self, surf):
        # sort the sprites from back to front
        sprites = sorted(self.sprites(), lambda a,b: cmp(a.rect.y, b.rect.y))
        for coin in sprites:
            if coin.visible:
                surf.blit(coin.image, coin.rect)
    
