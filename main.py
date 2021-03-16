import pygame as pg
import options
from const import *
from player import *


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((options.WIDTH, options.HEIGHT))
        pg.display.set_caption(options.TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    def load_data(self):
        self.spritesheet = Spritesheet(os.path.join(options.SPRITES, "char-2.svg"))

    def new(self):
        self.load_data()
        self.sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.sprites.add(self.player)
        self.platform_obj = [Platform(int(options.WIDTH * .5), int(options.HEIGHT * .9), options.WIDTH, 20),
                             Platform(int(options.WIDTH * .5), int(options.HEIGHT * .5), options.WIDTH * .3, 20),
                             Platform(int(options.WIDTH * .5), int(options.HEIGHT * .1), options.WIDTH, 20)]
        for p in self.platform_obj:
            self.sprites.add(p)
            self.platforms.add(p)
        g.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(options.FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.sprites.update()
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            if hits[0].rect.bottom < self.player.pos.y:  # platform on top
                self.player.pos.y = hits[0].rect.bottom + self.player.rect.height
                self.player.vel.y = 0
                if self.player.gravity_down:
                    self.player.gravity_down = False
            elif hits[0].rect.top < self.player.pos.y:  # platform on bottom
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
                if not self.player.gravity_down:
                    self.player.gravity_down = True

        if self.player.rect.left > options.WIDTH * .80:
            self.player.pos.x -= abs(self.player.vel.x)
            self.platform_obj[1].rect.x -= abs(self.player.vel.x)
        elif self.player.rect.left < options.WIDTH * .20:
            self.player.pos.x += abs(self.player.vel.x)
            self.platform_obj[1].rect.x += abs(self.player.vel.x)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def draw(self):
        self.screen.fill(Colors.FILL)
        self.sprites.draw(self.screen)
        pg.display.flip()

    def show_start_screen(self):
        pass

    def show_gameover_screen(self):
        pass


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_gameover_screen()

pg.quit()
