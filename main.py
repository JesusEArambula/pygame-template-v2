import pygame as pg
import random
from settings import *
from sprites import *


class Game:
    def __init__(self):
        # Initialize game window and other things
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        # Start new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)

        for platform in PLATFORM_LIST:
            p = Platform(*platform)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        # Defines game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Update game
        self.all_sprites.update()
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
        # If player reaches top 1/4 of screen
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += abs(self.player.vel.y)
            for platform in self.platforms:
                platform.rect.y += abs(self.player.vel.y)
                if platform.rect.top >= HEIGHT:
                    platform.kill()

        # Spawn new platforms
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            p = Platform(random.randrange(0, WIDTH - width), random.randrange(-75, -30), width, 20)
            self.platforms.add(p)
            self.all_sprites.add(p)

    def events(self):
        # Event handler
        for event in pg.event.get():
            # Close window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def draw(self):
        # Draw function
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # Flip display after drawing
        pg.display.flip()

    def show_start_screen(self):
        # Start screen
        pass

    def show_go_screen(self):
        # Game over screen
        pass


g = Game()
g.show_start_screen()

# Game Loop
while g.running:
    g.new()
    g.run()
    g.show_go_screen()

pg.quit()