from pygame.sprite import Sprite


class AvailableVillains(Sprite):
    def __init__(self, game, index=0):
        super().__init__()
        self.image = game.assets.icon_mage
        self.rect = self.image.get_rect()
        self.rect.topright = (
            game.screen.get_rect().right - 24 - index * (self.rect.width + 8),
            78,
        )
