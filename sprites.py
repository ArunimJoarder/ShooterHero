import pygame as pg
import random as rn 
from settings import *

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.game   = game
        pg.sprite.Sprite.__init__(self, self.game.all_sprites)
        
        self.image  = pg.Surface((30,50))
        self.image.fill(YELLOW)

        self.rect   = self.image.get_rect()
        self.rect.midbottom = (WIDTH / 2, HEIGHT - 100)

        self.pos    = vec(WIDTH / 2, HEIGHT - 20)
        self.vel    = vec(0,0)
        self.acc    = vec(0,0)

    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = PLAYER_JUMP_VELOCITY
    
    def update(self):

        self.acc = vec(0,GRAVITY)

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACCELERATION
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACCELERATION

        self.acc.x  += self.vel.x * FRICTION
        self.vel    += self.acc
        self.pos    += self.vel + self.acc * 0.5

        if abs(self.vel.x) < 0.01:
            self.vel.x = 0

        self.rect.midbottom = self.pos

        if self.rect.left <= 0:
            self.rect.left = 0

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, length, width = 30):
        self.game   = game
        pg.sprite.Sprite.__init__(self, game.all_sprites, self.game.platforms)

        self.image  = pg.Surface((length,width))
        self.image.fill(GREEN)

        self.rect   = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        mobChance   = rn.randrange(100)
        if mobChance >= 50:
            self.mob    = Mob(self.game, self)

class Mob(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self.game   = game
        self.plat   = plat
        pg.sprite.Sprite.__init__(self, self.game.all_sprites, self.game.mobs)

        self.image  = pg.Surface((30,50))
        self.image.fill(RED)

        self.rect           = self.image.get_rect()
        self.rect.bottom    = self.plat.rect.top
        self.rect.centerx   = rn.randrange(self.plat.rect.left, self.plat.rect.right)

        self.pos    = vec(self.rect.centerx, self.rect.bottom)
        self.vel    = vec(0,0)
        self.acc    = vec(0,0)

        self.facing = rn.choice([-1,1])

    def update(self):
        if self.rect.left <= self.plat.rect.left + 10:
            self.facing = 1
        elif self.rect.right >= self.plat.rect.right - 10:
            self.facing = -1

        self.acc.x  = self.facing * MOB_ACCELERATION

        self.acc.x  += self.vel.x * FRICTION
        self.vel    += self.acc
        self.pos    += self.vel + self.acc * 0.5

        self.rect.midbottom = self.pos
