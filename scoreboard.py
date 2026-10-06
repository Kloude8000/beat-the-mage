import pygame


def draw_panel(surface, rect, color, radius=12):
    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(panel, color, panel.get_rect(), border_radius=radius)
    surface.blit(panel, rect.topleft)


class Scoreboard:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.stats = game.stats
        self.title_font = pygame.font.SysFont('georgia,timesnewroman,serif', 64, bold=True)
        self.big_font = pygame.font.SysFont('segoeui,arial,sans', 40, bold=True)
        self.mid_font = pygame.font.SysFont('segoeui,arial,sans', 28, bold=True)
        self.small_font = pygame.font.SysFont('segoeui,arial,sans', 20)
        self.tiny_font = pygame.font.SysFont('segoeui,arial,sans', 16)
        self.prep()

    def prep(self):
        self.screen_rect = self.screen.get_rect()
        self._prep_scores()
        self._prep_icons()

    def _prep_scores(self):
        self.hero_score_image = self.big_font.render(
            str(self.stats.hero_score), True, self.settings.text_color
        )
        self.hero_score_rect = self.hero_score_image.get_rect()
        self.hero_score_rect.topleft = (24, 14)

        self.vs_image = self.mid_font.render('VS', True, self.settings.accent_color)
        self.vs_rect = self.vs_image.get_rect(midtop=(self.screen_rect.centerx, 8))

        wave = self.game.villain.name
        self.wave_image = self.tiny_font.render(
            f'Wave {self.stats.wave_index + 1}  {wave}', True, self.settings.text_color
        )
        self.wave_rect = self.wave_image.get_rect(midtop=(self.screen_rect.centerx, 40))

        self.villain_score_image = self.big_font.render(
            str(self.stats.villain_score), True, self.settings.text_color
        )
        self.villain_score_rect = self.villain_score_image.get_rect()
        self.villain_score_rect.topright = (self.screen_rect.right - 24, 12)

        self.high_image = self.tiny_font.render(
            f'Best {self.stats.high_score}', True, self.settings.accent_color
        )
        self.high_rect = self.high_image.get_rect()
        self.high_rect.midleft = (self.hero_score_rect.right + 14, self.hero_score_rect.centery)

    def _prep_icons(self):
        self.life_icons = []
        icon = self.game.assets.icon_hero
        for index in range(self.stats.lives):
            rect = icon.get_rect()
            rect.topleft = (24 + index * (rect.width + 8), 58)
            self.life_icons.append(rect)

        remaining = self.settings.arrow_limit - len(self.game.arrows)
        self.ammo_icons = []
        ammo = self.game.assets.icon_arrow
        start_x = 24 + max(self.stats.lives, 1) * (icon.get_width() + 8) + 10
        for index in range(max(0, remaining)):
            rect = ammo.get_rect()
            rect.topleft = (start_x + index * (rect.width + 6), 64)
            self.ammo_icons.append(rect)

    def show_score(self):
        bar = pygame.Rect(12, 8, self.screen_rect.width - 24, 90)
        draw_panel(self.screen, bar, self.settings.panel_color)
        self.screen.blit(self.hero_score_image, self.hero_score_rect)
        self.screen.blit(self.vs_image, self.vs_rect)
        self.screen.blit(self.wave_image, self.wave_rect)
        self.screen.blit(self.villain_score_image, self.villain_score_rect)
        self.screen.blit(self.high_image, self.high_rect)

        for rect in self.life_icons:
            self.screen.blit(self.game.assets.icon_hero, rect)
        for rect in self.ammo_icons:
            self.screen.blit(self.game.assets.icon_arrow, rect)

        self._draw_villain_hp()

    def _draw_villain_hp(self):
        villain = self.game.villain
        width = 180
        height = 14
        rect = pygame.Rect(0, 0, width, height)
        rect.topright = (self.screen_rect.right - 24, 58)
        pygame.draw.rect(self.screen, self.settings.hp_empty, rect, border_radius=6)
        ratio = 0 if villain.max_hp == 0 else villain.hp / villain.max_hp
        fill = rect.copy()
        fill.width = max(0, int(width * ratio))
        if fill.width:
            pygame.draw.rect(self.screen, self.settings.hp_color, fill, border_radius=6)
        pygame.draw.rect(self.screen, self.settings.text_color, rect, 1, border_radius=6)
        label = self.tiny_font.render(f'HP {villain.hp}/{villain.max_hp}', True, self.settings.text_color)
        self.screen.blit(label, (rect.left, rect.bottom + 2))

    def _dim(self, alpha=150):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((8, 12, 24, alpha))
        self.screen.blit(overlay, (0, 0))

    def _center_text(self, font, text, color, y):
        image = font.render(text, True, color)
        rect = image.get_rect(center=(self.screen_rect.centerx, y))
        self.screen.blit(image, rect)
        return rect

    def show_menu(self):
        self._dim(110)
        self._center_text(self.title_font, 'HIT THE MAGE', self.settings.accent_color, 160)
        self._center_text(self.mid_font, 'Dodge the spells. Drain every mage. Survive the roster.', self.settings.text_color, 230)
        lines = [
            'Move           Up / Down   or   W / S',
            'Shoot          Space   (shots can block spells)',
            'Pause          P            Fullscreen  F',
            'Start / retry  Enter        Quit  Esc or Q',
        ]
        for index, line in enumerate(lines):
            self._center_text(self.small_font, line, self.settings.text_color, 320 + index * 32)
        self._center_text(self.mid_font, 'Press Enter to fight', self.settings.accent_color, 500)

    def show_pause(self):
        self._dim()
        self._center_text(self.big_font, 'PAUSED', self.settings.accent_color, 280)
        self._center_text(self.small_font, 'P or Enter to resume    Esc to quit', self.settings.text_color, 340)

    def show_game_over(self):
        self._dim()
        self._center_text(self.big_font, 'GAME OVER', self.settings.danger_color, 250)
        self._center_text(
            self.mid_font,
            f'Score {self.stats.hero_score}    Best {self.stats.high_score}',
            self.settings.text_color,
            320,
        )
        self._center_text(self.small_font, 'Enter to fight again    Esc to quit', self.settings.accent_color, 390)

    def show_wave_clear(self):
        self._dim(90)
        self._center_text(self.big_font, 'MAGE DOWN', self.settings.accent_color, 280)
        next_index = self.stats.wave_index + 1
        next_wave = self.settings.wave_for(next_index)
        self._center_text(
            self.mid_font,
            f'Incoming: {next_wave["name"]}',
            self.settings.text_color,
            350,
        )
