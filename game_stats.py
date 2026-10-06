class GameStats:
    def __init__(self, game):
        self.settings = game.settings
        self.high_score = 0
        self.reset()

    def reset(self):
        self.hero_score = 0
        self.villain_score = 0
        self.lives = self.settings.hero_lives
        self.wave_index = 0
        self.game_active = True

    @property
    def hero_upgraded(self):
        return self.wave_index + 1 >= self.settings.hero_upgrade_wave

    def add_hero_score(self, amount):
        self.hero_score = max(0, self.hero_score + amount)
        self.high_score = max(self.high_score, self.hero_score)
        return self.hero_score

    def add_villain_score(self, amount):
        self.villain_score += amount
        return self.villain_score
