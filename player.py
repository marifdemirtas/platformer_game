import os

import pygame as pg

import options
from const import *

vec = pg.math.Vector2

FRICTION = 0.5


class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert_alpha()

    def get_image(self, x, y, w, h):
        #image = pg.Surface((w * 23, h * 23), pg.SRCALPHA).convert_alpha()
        #image.blit(self.spritesheet, (0, 0), (x*25, y*25, w*25, h*25))
        rect = pg.Rect((x*25, y*25), (w*25, h*25))
        image = self.spritesheet.subsurface(rect)
        image = pg.transform.scale(image, (int(image.get_width()*.5), int(image.get_height()*.5)))
        return image


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        super(Player, self).__init__()
        self.game = game


        self.walking = False
        self.jumping = False
        self.curr_frame = 0
        self.last_update = 0
        self.facing_right = False
        self.status = 0

        self.load_images()

        self.image = self.idle_d

        self.rect = self.image.get_rect()
        self.rect.center = (options.WIDTH / 2, options.HEIGHT / 2)
        self.pos = vec(options.WIDTH / 2, options.HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jump_count = 3

        self.gravity_down = True


    def load_images(self):
        self.idle_d = self.game.spritesheet.get_image(18, 18, 9, 9)
        self.idle_u = self.game.spritesheet.get_image(27, 18, 9, 9)

        self.from_walk_r_d = self.game.spritesheet.get_image(27, 0, 9, 9)
        self.from_walk_r_u = self.game.spritesheet.get_image(0, 27, 9, 9)

        self.from_walk_l_d = self.game.spritesheet.get_image(27, 9, 9, 9)
        self.from_walk_l_u = self.game.spritesheet.get_image(0, 36, 9, 9)

        self.jump_pose = self.game.spritesheet.get_image(0, 18, 9, 9)
        self.fall_pose = self.game.spritesheet.get_image(9, 18, 9, 9)

        self.walk_r_d = [self.game.spritesheet.get_image(*img)
                         for img in ((9, 0, 9, 9),
                                     (0, 0, 9, 9),
                                     (18, 0, 9, 9),
                                     (0, 0, 9, 9))]

        self.walk_l_d = [self.game.spritesheet.get_image(*img)
                         for img in ((9, 9, 9, 9),
                                     (0, 9, 9, 9),
                                     (18, 9, 9, 9),
                                     (0, 9, 9, 9))]
        self.walk_r_u = [self.game.spritesheet.get_image(*img)
                         for img in ((9, 27, 9, 9),
                                     (27, 27, 9, 9),
                                     (18, 27, 9, 9),
                                     (27, 27, 9, 9))]

        self.walk_l_u = [pg.transform.flip(pos, True, False)
                         for pos in self.walk_r_u]

    def animate(self):
        now = pg.time.get_ticks()
        self.idle = self.idle_d if self.gravity_down else self.idle_u
        self.from_walk_r = self.from_walk_r_d if self.gravity_down else self.from_walk_r_u
        self.from_walk_l = self.from_walk_l_d if self.gravity_down else self.from_walk_l_u

        if self.vel.y == 0 and not self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.curr_frame = (self.curr_frame + 1) % 2
                bottom = self.rect.bottom
                if self.status == 1:
                    self.image = self.from_walk_r
                elif self.status == 2:
                    self.image = self.from_walk_l
                else:
                    self.image = self.idle
                self.status = 0

        elif self.walking:
            if now - self.last_update > 100:
                self.last_update = now
                self.curr_frame = (self.curr_frame + 1) % 4
                bottom = self.rect.bottom
                if self.facing_right:
                    self.status = 1
                    if self.gravity_down:
                        self.image = self.walk_r_d[self.curr_frame]
                    else:
                        self.image = self.walk_r_u[self.curr_frame]
                else:
                    self.status = 2
                    if self.gravity_down:
                        self.image = self.walk_l_d[self.curr_frame]
                    else:
                        self.image = self.walk_l_u[self.curr_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        elif self.vel.y > 0:
            if now - self.last_update > 200:
                self.last_update = now
                self.curr_frame = (self.curr_frame + 1) % 2
                bottom = self.rect.bottom
                if self.acc.y < 0:
                    self.image = self.jump_pose
                else:
                    self.image = self.fall_pose
                self.status = 0

        elif self.gravity_down:
            if now - self.last_update > 100:
                self.last_update = now
                self.curr_frame = (self.curr_frame + 1) % 4
                bottom = self.rect.bottom
                self.image = self.walk_r_d[self.curr_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1

        if hits:
            self.jump_count = 3
        self.jump_count -= 1
        if self.jump_count > 0:
            if self.gravity_down:
                self.vel.y = -20
            else:
                self.vel.y = +20

    def update(self):
        self.animate()
        self.acc = vec(0, options.Player.GRAV if self.gravity_down else -options.Player.GRAV)
        self.walking = False

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.walking = True
            self.facing_right = False
            self.acc.x = -options.Player.ACC
        if keys[pg.K_RIGHT]:
            self.walking = True
            self.facing_right = True
            self.acc.x = options.Player.ACC
        if keys[pg.K_DOWN]:
            self.acc.y = options.Player.ACC
        if keys[pg.K_UP]:
            self.acc.y = -options.Player.ACC

        self.acc.x += self.vel.x * options.Player.FR
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos


class GreenMob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super(GreenMob, self).__init__()
        self.game = game

        self.idle = [self.game.ss2.get_image(0, 0, 9, 9),
                     self.game.ss2.get_image(9, 0, 9, 9),
                     self.game.ss2.get_image(0, 0, 9, 9),
                     self.game.ss2.get_image(18, 0, 9, 9)]

        self.image = pg.Surface(self.idle[0].get_rect().size)
        self.rect = self.image.get_rect()
        self.rect.midbottom = x, y

        self.curr_frame = 0
        self.last_update = 0

    def animate(self):
        now = pg.time.get_ticks()

        if now - self.last_update > 350:
            self.last_update = now
            self.curr_frame = (self.curr_frame + 1) % 4
            self.image = self.idle[self.curr_frame]


class BlueMob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super(BlueMob, self).__init__()
        self.game = game

        self.idle = [self.game.ss2.get_image(9, 9, 9, 9),
                     self.game.ss2.get_image(0, 9, 9, 9),
                     self.game.ss2.get_image(9, 9, 9, 9),
                     self.game.ss2.get_image(18, 9, 9, 9)]

        self.image = pg.Surface(self.idle[0].get_rect().size)
        self.rect = self.image.get_rect()
        self.rect.midtop = x, y

        self.curr_frame = 0
        self.last_update = 0

    def animate(self):
        now = pg.time.get_ticks()

        if now - self.last_update > 100:
            self.last_update = now
            self.curr_frame = (self.curr_frame + 1) % 4
            self.image = self.idle[self.curr_frame]


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super(Platform, self).__init__()
        self.image = pg.Surface((w, h))
        self.image.fill(Colors.GREEN)
        self.rect = self.image.get_rect()
        self.rect.midbottom = x, y
