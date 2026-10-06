from pygame.sprite import Sprite


class AvailableHeros(Sprite):
    def __init__(self, game, index=0):
        super().__init__()
        self.image = game.assets.icon_hero
        self.rect = self.image.get_rect()
        self.rect.topleft = (24 + index * (self.rect.width + 8), 78)
