import pygame as pg
import options
import random
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
        self.ss2 = Spritesheet(os.path.join(options.SPRITES, "other_char_sheet.svg"))
        tiles = (self.ss2.get_image(45, 0, 9, 9),
                 self.ss2.get_image(45, 9, 9, 9),
                 self.ss2.get_image(54, 0, 9, 9),
                 self.ss2.get_image(54, 9, 9, 9),
                 self.ss2.get_image(63, 0, 9, 9),
                 self.ss2.get_image(63, 9, 9, 9))
        dark = pg.Surface(tiles[-1].get_rect().size).convert_alpha()
        dark.fill((50, 50, 50, 150))
        for tile in tiles:
            tile.blit(dark, (0, 0))
        self.background = pg.Surface((options.WIDTH * 100, options.HEIGHT))
        self.background.fill(Colors.BLUE)
        k = (int(options.WIDTH * 100 / 112) + 1) * (int(options.HEIGHT / 112) + 1)
        tile_choices = random.choices(tiles, weights=[10, 10, 5, 10, 2, 2], k=k)
        tile_count = 0
        for x in range(0, int(options.WIDTH * 100), 112):
            for y in range(0, int(options.HEIGHT), 112):
                self.background.blit(tile_choices[tile_count], (x, y))
                tile_count += 1

    def new(self):
        self.load_data()
        self.back_x = -int(self.background.get_rect().width / 2)
        self.sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.to_slip = pg.sprite.Group()
        self.to_anim = pg.sprite.Group()
        self.player = Player(self)
        self.platform_obj = [Platform(int(options.WIDTH * .5), int(options.HEIGHT), options.WIDTH, options.HEIGHT - int(options.HEIGHT * .9)),
                             Platform(int(options.WIDTH * .5), int(options.HEIGHT * .5) + 10, options.WIDTH * .3, 20),
                             Platform(int(options.WIDTH * .5), int(options.HEIGHT * .1), options.WIDTH, options.HEIGHT - int(options.HEIGHT * .9))]
        _mob1 = GreenMob(self, int(options.WIDTH *.8), int(options.HEIGHT) - options.HEIGHT + int(options.HEIGHT * .9))

        _mob2 = BlueMob(self, int(options.WIDTH *.35), options.HEIGHT - int(options.HEIGHT * .9))

        self.sprites.add(_mob1)
        self.sprites.add(_mob2)

        self.to_anim.add(_mob1)
        self.to_anim.add(_mob2)

        self.to_slip.add(self.platform_obj[1])
        self.to_slip.add(_mob1)
        self.to_slip.add(_mob2)

        self.sprites.add(self.player)

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
        for sprite in self.to_anim:
            sprite.animate()
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
            for sprite in self.to_slip:
                sprite.rect.x -= abs(self.player.vel.x)
            self.back_x -= abs(self.player.vel.x)
        elif self.player.rect.left < options.WIDTH * .20:
            self.player.pos.x += abs(self.player.vel.x)
            for sprite in self.to_slip:
                sprite.rect.x += abs(self.player.vel.x)
            self.back_x += abs(self.player.vel.x)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def draw(self):
        img = self.ss2.get_image(45, 0, 18, 9)
        self.screen.fill(Colors.FILL)
        self.screen.blit(self.background, (self.back_x, 0))
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
