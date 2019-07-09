#! usr/bin/env python3

import pygame as pg
import random as rn
from settings import *
from sprites import *

class Game:
    def __init__(self):
        # initialize pygame and set up a window
        pg.init()
        pg.mixer.init()

        self.screen     = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        
        self.clock      = pg.time.Clock()
        
        self.running    = True

    def new(self):
        # initiates new game
        self.all_sprites    = pg.sprite.Group()
        self.platforms      = pg.sprite.Group()
        self.mobs           = pg.sprite.Group()

        self.player         = Player(self)
        self.initPLats      = []
        for plat in INIT_PLAT:
            p = Platform(self, *plat)
            self.initPLats.append(p)
            try:
                p.mob.kill()
            except:
                pass

        for i in range(4):
            Platform(self, rn.randrange(WIDTH + 10, WIDTH * 3 // 2), rn.randrange(80, HEIGHT - 80), rn.randrange(100, 200))

        self.run()

    def run(self):
        # main Game loop
        self.playing    = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            
    def update(self):
        # update the game
        self.all_sprites.update()

        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            for hit in hits:
                # if abs(self.player.vel.y) <= 5:
                if self.player.pos.y > hit.rect.centery:
                    if abs(self.player.rect.right - hit.rect.left) <= 10:
                        self.player.rect.right = hit.rect.left
                        self.player.pos = vec(self.player.rect.midbottom[0], self.player.rect.midbottom[1] - 1)
                        self.player.vel.x = 0
                    elif abs(self.player.rect.left - hit.rect.right) <= 10:
                        self.player.rect.left = hit.rect.right
                        self.player.pos = vec(self.player.rect.midbottom[0], self.player.rect.midbottom[1] - 1)
                        self.player.vel.x = 0

            if self.player.vel.y > 0 and self.player.pos.y < hits[0].rect.bottom:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
            elif self.player.vel.y < 0:
                self.player.pos.y = hits[0].rect.bottom + self.player.rect.height
                self.player.vel.y = 0

        for plat in self.platforms:
            if plat.rect.right < -10:
                plat.kill()
                try:
                    plat.mob.kill()
                except:
                    pass
                Platform(self, rn.randrange(WIDTH + 10, WIDTH * 2), rn.randrange(80, HEIGHT - 80), rn.randrange(100, 200))

        if self.player.pos.x >= WIDTH * 0.75:
            self.player.pos.x += -abs(self.player.vel.x)
            for plat in self.platforms:
                plat.rect.x += -abs(self.player.vel.x)
            for i_plat in self.initPLats:
                i_plat.rect.x = 0
            for mob in self.mobs:
                mob.pos.x += -abs(self.player.vel.x)

    def events(self):
        # detects events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.player.jump()

    def draw(self):
        # draws on the screen
        self.screen.fill(BLACK)

        self.all_sprites.draw(self.screen)

        pg.display.flip()

    def show_GO_screen(self):
        pass

    def show_splash_screen(self):
        pass

g = Game()
g.show_splash_screen()
while g.running:
    g.new()
    g.show_GO_screen()

pg.quit()

