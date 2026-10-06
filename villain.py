from pygame.sprite import Sprite


class Villain(Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.move_down = True
        self.hp = 1
        self.max_hp = 1
        self.speed = 2.5
        self.projectile = 'fire'
        self.cooldown = 900
        self.last_shot_ms = 0
        self.name = 'Mage'
        self.configure(self.settings.wave_for(0))
        self.reset_position()

    def configure(self, wave):
        self.name = wave['name']
        self.image = self.game.assets.villains[wave['sprite']]
        self.rect = self.image.get_rect()
        self.max_hp = wave['hp']
        self.hp = wave['hp']
        self.speed = wave['speed']
        self.projectile = wave['projectile']
        self.cooldown = wave['cooldown']
        self.last_shot_ms = 0
        self.move_down = True
        self.y = float(self.rect.y)

    def reset_position(self):
        screen_rect = self.screen.get_rect()
        self.rect.midright = (screen_rect.right - 28, screen_rect.centery + 20)
        self.y = float(self.rect.y)

    def move_villain(self):
        if self.move_down:
            self.y += self.speed
        else:
            self.y -= self.speed
        self.rect.y = int(self.y)
        self.move_flag()

    def move_flag(self):
        top = self.settings.play_area_top
        bottom = self.screen.get_rect().bottom - 8
        if self.rect.bottom >= bottom:
            self.move_down = False
            self.rect.bottom = bottom
            self.y = float(self.rect.y)
        elif self.rect.top <= top:
            self.move_down = True
            self.rect.top = top
            self.y = float(self.rect.y)

    def can_shoot(self, now_ms, hero_centery):
        aligned = abs(self.rect.centery - hero_centery) <= self.settings.alignment_slop
        return aligned and (now_ms - self.last_shot_ms) >= self.cooldown

    def mark_shot(self, now_ms):
        self.last_shot_ms = now_ms

    def take_damage(self, amount=1):
        self.hp = max(0, self.hp - amount)
        return self.hp <= 0

    def blit(self):
        if self.hp > 0:
            self.screen.blit(self.image, self.rect)

    def collide_rect(self):
        return self.rect.inflate(-36, -40)
