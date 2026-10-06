import pygame
from pygame.sprite import Sprite


class HitEffect(Sprite):
    def __init__(self, frames, center, fps=16):
        super().__init__()
        self.frames = frames
        self.index = 0
        self.image = frames[0]
        self.rect = self.image.get_rect(center=center)
        self.frame_ms = 1000 / fps
        self.elapsed = 0

    def update(self, dt=16):
        self.elapsed += dt
        while self.elapsed >= self.frame_ms:
            self.elapsed -= self.frame_ms
            self.index += 1
            if self.index >= len(self.frames):
                self.kill()
                return
            center = self.rect.center
            self.image = self.frames[self.index]
            self.rect = self.image.get_rect(center=center)
