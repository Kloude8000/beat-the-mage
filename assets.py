import pygame
from pathlib import Path


def scale_to_height(surface, height):
    width, current_height = surface.get_size()
    if current_height == height:
        return surface
    new_width = max(1, round(width * (height / current_height)))
    return pygame.transform.smoothscale(surface, (new_width, height))


def scale_to_width(surface, width):
    current_width, height = surface.get_size()
    if current_width == width:
        return surface
    new_height = max(1, round(height * (width / current_width)))
    return pygame.transform.smoothscale(surface, (width, new_height))


def trim_surface(surface):
    bounds = surface.get_bounding_rect()
    if bounds.width == 0 or bounds.height == 0:
        return surface
    return surface.subsurface(bounds).copy()


class Assets:
    """Load, trim, and cache every image the game needs."""

    def __init__(self, root=None):
        self.root = Path(root) if root else Path(__file__).resolve().parent
        self.hero_archer = self.load('images/Actor1_5.png', height=190)
        self.hero_sword = self.load('characters/Swordsman.png', height=190)
        self.icon_hero = self.load('images/Actor1_5a.png', height=38)
        self.icon_arrow = self.load('images/arrow3.png', height=28)
        self.icon_mage = self.load('images/Mage2.png', height=36)

        self.arrow = self.load('images/arrow2.png', width=58)
        sword = self.load('images/sword.png')
        sword = pygame.transform.rotate(sword, -90)
        self.sword = scale_to_width(trim_surface(sword), 52)

        self.fireball = self.load('images/fireball.png', width=82)
        self.ice = self.load('images/ice3.png', width=74)

        self.villains = {
            'mage': self.load('characters/Mage.png', height=200),
            'ice_witch': self.load('characters/Actor2_6.png', height=200),
            'vampire': pygame.transform.flip(
                self.load('characters/Vampire.png', height=200), True, False
            ),
            'demon': pygame.transform.flip(
                self.load('characters/Demon.png', height=220), True, False
            ),
            'darklord': self.load('characters/Darklord.png', height=230),
        }

        self.anim_hit = self.slice_sheet('animations/Hit1.png', size=96)
        self.anim_hit_fire = self.slice_sheet('animations/HitFire.png', size=110)
        self.anim_hit_ice = self.slice_sheet('animations/HitIce.png', size=110)
        self.anim_flash = self.slice_sheet('animations/Flash.png', size=120)

        self.sky_source = self.load('images/BlueSky.png', trim=False)

    def path(self, relative):
        return self.root / relative.replace('\\', '/')

    def load(self, relative, height=None, width=None, trim=True):
        image = pygame.image.load(str(self.path(relative))).convert_alpha()
        if trim:
            image = trim_surface(image)
        if height:
            image = scale_to_height(image, height)
        elif width:
            image = scale_to_width(image, width)
        return image

    def slice_sheet(self, relative, cell=192, size=None):
        sheet = pygame.image.load(str(self.path(relative))).convert_alpha()
        frames = []
        columns = sheet.get_width() // cell
        rows = sheet.get_height() // cell
        for row in range(rows):
            for column in range(columns):
                frame_rect = pygame.Rect(column * cell, row * cell, cell, cell)
                frame = sheet.subsurface(frame_rect).copy()
                if frame.get_bounding_rect().width == 0:
                    continue
                if size:
                    frame = scale_to_height(frame, size)
                frames.append(frame)
        return frames

    def make_background(self, size):
        width, height = size
        source_width, source_height = self.sky_source.get_size()
        scale = max(width / source_width, height / source_height)
        scaled = pygame.transform.smoothscale(
            self.sky_source,
            (max(1, round(source_width * scale)), max(1, round(source_height * scale))),
        )
        background = pygame.Surface(size).convert()
        background.blit(
            scaled,
            ((width - scaled.get_width()) // 2, (height - scaled.get_height()) // 2),
        )
        return background
