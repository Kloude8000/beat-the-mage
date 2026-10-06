import pygame
from pygame.sprite import Sprite


class Hero(Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.stats = game.stats
        self.moving_up = False
        self.moving_down = False
        self.invuln_ms = 0
        self._set_image()
        self.reset_position()

    def _set_image(self):
        center = getattr(self, 'rect', pygame.Rect(0, 0, 0, 0)).center
        if self.stats.hero_upgraded:
            self.image = self.game.assets.hero_sword
        else:
            self.image = self.game.assets.hero_archer
        self.rect = self.image.get_rect()
        if center != (0, 0):
            self.rect.center = center
        self.y = float(self.rect.y)

    def refresh_image(self):
        self._set_image()

    def reset_position(self):
        self._set_image()
        self.rect.midleft = (
            36,
            self.screen.get_rect().centery + 20,
        )
        self.y = float(self.rect.y)
        self.moving_up = False
        self.moving_down = False
        self.invuln_ms = 0

    def move_hero(self):
        top = self.settings.play_area_top
        bottom = self.screen.get_rect().bottom - 8
        if self.moving_up and self.rect.top > top:
            self.y -= self.settings.hero_speed
        if self.moving_down and self.rect.bottom < bottom:
            self.y += self.settings.hero_speed
        self.rect.y = int(self.y)
        if self.rect.top < top:
            self.rect.top = top
            self.y = float(self.rect.y)
        if self.rect.bottom > bottom:
            self.rect.bottom = bottom
            self.y = float(self.rect.y)

    def take_hit(self, duration=None):
        self.invuln_ms = duration if duration is not None else self.settings.invuln_ms

    def update_timers(self, dt):
        if self.invuln_ms > 0:
            self.invuln_ms = max(0, self.invuln_ms - dt)

    def is_visible(self):
        if self.invuln_ms <= 0:
            return True
        return (pygame.time.get_ticks() // 90) % 2 == 0

    def blit(self):
        if self.is_visible():
            self.screen.blit(self.image, self.rect)

    def collide_rect(self):
        return self.rect.inflate(-40, -50)
