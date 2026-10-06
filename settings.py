class Settings:
    def __init__(self):
        self.screen_width = 1280
        self.screen_height = 720
        self.FPS = 60
        self.caption = 'Hit the Mage'
        self.play_area_top = 108

        self.hero_speed = 5.2
        self.arrow_speed = 13
        self.sword_speed = 15
        self.fireball_speed = 9
        self.ice_speed = 8
        self.arrow_limit = 3
        self.hero_lives = 3
        self.invuln_ms = 1100
        self.wave_clear_ms = 1600
        self.alignment_slop = 52
        self.hero_upgrade_wave = 3

        self.hit_points = 10
        self.combo_bonus = 5
        self.wave_clear_points = 30
        self.miss_penalty = 5

        self.panel_color = (16, 28, 48, 170)
        self.text_color = (255, 252, 240)
        self.accent_color = (255, 214, 70)
        self.danger_color = (220, 70, 60)
        self.hp_color = (70, 200, 90)
        self.hp_empty = (40, 40, 50)

        self.waves = [
            {
                'name': 'Fire Mage',
                'sprite': 'mage',
                'hp': 3,
                'speed': 2.6,
                'projectile': 'fire',
                'cooldown': 920,
            },
            {
                'name': 'Ice Witch',
                'sprite': 'ice_witch',
                'hp': 4,
                'speed': 3.0,
                'projectile': 'ice',
                'cooldown': 800,
            },
            {
                'name': 'Vampire',
                'sprite': 'vampire',
                'hp': 4,
                'speed': 3.4,
                'projectile': 'fire',
                'cooldown': 700,
            },
            {
                'name': 'Demon',
                'sprite': 'demon',
                'hp': 5,
                'speed': 3.1,
                'projectile': 'fire',
                'cooldown': 620,
            },
            {
                'name': 'Dark Lord',
                'sprite': 'darklord',
                'hp': 7,
                'speed': 2.4,
                'projectile': 'ice',
                'cooldown': 540,
            },
        ]

    def wave_for(self, index):
        base = self.waves[index % len(self.waves)]
        loops = index // len(self.waves)
        return {
            'name': base['name'] if loops == 0 else f"{base['name']} +{loops}",
            'sprite': base['sprite'],
            'hp': base['hp'] + loops * 2,
            'speed': min(base['speed'] + loops * 0.35, 6.5),
            'projectile': base['projectile'],
            'cooldown': max(320, int(base['cooldown'] * (0.88 ** loops))),
        }
