from pygame.sprite import Sprite


class Fireball(Sprite):
    def __init__(self, game, kind='fire'):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.kind = kind
        if kind == 'ice':
            self.image = game.assets.ice
            self.speed = self.settings.ice_speed
        else:
            self.image = game.assets.fireball
            self.speed = self.settings.fireball_speed
        self.rect = self.image.get_rect()
        self.rect.midright = game.villain.rect.midleft
        self.x = float(self.rect.x)

    def update(self, dt=16):
        self.x -= self.speed
        self.rect.x = int(self.x)
        if self.rect.right <= 0:
            self.kill()

    def collide_rect(self):
        return self.rect.inflate(-18, -18)
