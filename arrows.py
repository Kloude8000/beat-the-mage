import pygame
from pygame.sprite import Sprite


class Arrows(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        upgraded = game.stats.hero_upgraded
        self.image = game.assets.sword if upgraded else game.assets.arrow
        self.speed = self.settings.sword_speed if upgraded else self.settings.arrow_speed
        self.rect = self.image.get_rect()
        self.rect.midleft = game.hero.rect.midright
        self.x = float(self.rect.x)

    def update(self, dt=16):
        self.x += self.speed
        self.rect.x = int(self.x)
        if self.rect.left >= self.screen.get_rect().right:
            self.kill()

    def collide_rect(self):
        return self.rect.inflate(-12, -16)
