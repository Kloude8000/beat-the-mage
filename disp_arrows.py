from pygame.sprite import Sprite


class AvailableArrows(Sprite):
    def __init__(self, game, index=0):
        super().__init__()
        self.image = game.assets.icon_arrow
        self.rect = self.image.get_rect()
        self.rect.topleft = (180 + index * (self.rect.width + 6), 86)
