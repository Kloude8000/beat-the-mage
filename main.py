import sys
import pygame
from settings import Settings
from assets import Assets
from hero import Hero
from arrows import Arrows
from villain import Villain
from fireball import Fireball
from game_stats import GameStats
from scoreboard import Scoreboard
from effects import HitEffect


STATE_MENU = 'menu'
STATE_PLAY = 'play'
STATE_PAUSE = 'pause'
STATE_WAVE_CLEAR = 'wave_clear'
STATE_GAME_OVER = 'game_over'


def collide_rects(left, right):
    left_rect = left.collide_rect() if hasattr(left, 'collide_rect') else left.rect
    right_rect = right.collide_rect() if hasattr(right, 'collide_rect') else right.rect
    return left_rect.colliderect(right_rect)


class MainGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Hit the Mage')
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        self.fullscreen = False
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        self.assets = Assets()
        self.background = self.assets.make_background(self.screen.get_size())
        self.stats = GameStats(self)
        self.hero = Hero(self)
        self.villain = Villain(self)
        self.arrows = pygame.sprite.Group()
        self.fireballs = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()
        self.scoreboard = Scoreboard(self)
        self.state = STATE_MENU
        self.wave_clear_ms = 0
        self.hero.reset_position()
        self.villain.reset_position()
        self.scoreboard.prep()

    def run_game(self):
        while True:
            dt = self.clock.tick(self.settings.FPS)
            self._check_events()
            if self.state == STATE_PLAY:
                self._update_play(dt)
            elif self.state == STATE_WAVE_CLEAR:
                self._update_wave_clear(dt)
            self._screen_update()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._keyup_events(event)

    def _keydown_events(self, event):
        if event.key == pygame.K_q:
            sys.exit()
        if event.key == pygame.K_f:
            self._toggle_fullscreen()
            return
        if event.key == pygame.K_ESCAPE:
            if self.state == STATE_PLAY:
                self.state = STATE_PAUSE
            elif self.state == STATE_PAUSE:
                self.state = STATE_PLAY
            else:
                sys.exit()
            return

        if self.state == STATE_MENU:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._start_game()
            return
        if self.state == STATE_GAME_OVER:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._start_game()
            return
        if self.state == STATE_PAUSE:
            if event.key in (pygame.K_p, pygame.K_RETURN):
                self.state = STATE_PLAY
            return
        if self.state == STATE_WAVE_CLEAR:
            return

        if event.key == pygame.K_p:
            self.state = STATE_PAUSE
        elif event.key in (pygame.K_UP, pygame.K_w):
            self.hero.moving_up = True
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.hero.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_arrows()

    def _keyup_events(self, event):
        if event.key in (pygame.K_UP, pygame.K_w):
            self.hero.moving_up = False
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.hero.moving_down = False

    def _start_game(self):
        self.stats.reset()
        self.arrows.empty()
        self.fireballs.empty()
        self.effects.empty()
        self.villain.configure(self.settings.wave_for(0))
        self.hero.reset_position()
        self.villain.reset_position()
        self.state = STATE_PLAY
        self.scoreboard.prep()

    def _toggle_fullscreen(self):
        hero_ratio = self.hero.rect.centery / max(1, self.screen.get_height())
        villain_ratio = self.villain.rect.centery / max(1, self.screen.get_height())
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height)
            )
        self.hero.screen = self.screen
        self.villain.screen = self.screen
        self.scoreboard.screen = self.screen
        self.background = self.assets.make_background(self.screen.get_size())
        height = self.screen.get_height()
        self.hero.rect.centery = int(height * hero_ratio)
        self.hero.y = float(self.hero.rect.y)
        self.hero.rect.left = 36
        self.villain.rect.centery = int(height * villain_ratio)
        self.villain.y = float(self.villain.rect.y)
        self.villain.rect.right = self.screen.get_rect().right - 28
        self.scoreboard.prep()

    def _fire_arrows(self):
        if len(self.arrows) >= self.settings.arrow_limit:
            return
        self.arrows.add(Arrows(self))
        self.scoreboard.prep()

    def _fire_fireballs(self, now_ms):
        if self.villain.hp <= 0:
            return
        if self.villain.can_shoot(now_ms, self.hero.rect.centery):
            self.fireballs.add(Fireball(self, self.villain.projectile))
            self.villain.mark_shot(now_ms)

    def _spawn_effect(self, kind, center):
        frames = {
            'hit': self.assets.anim_hit,
            'fire': self.assets.anim_hit_fire,
            'ice': self.assets.anim_hit_ice,
            'flash': self.assets.anim_flash,
        }.get(kind, self.assets.anim_hit)
        if frames:
            self.effects.add(HitEffect(frames, center))

    def _update_play(self, dt):
        now_ms = pygame.time.get_ticks()
        self.hero.move_hero()
        self.hero.update_timers(dt)
        self.villain.move_villain()
        self._fire_fireballs(now_ms)
        ammo_before = len(self.arrows)
        self.arrows.update(dt)
        self.fireballs.update(dt)
        self.effects.update(dt)
        self._detect_collisions()
        if len(self.arrows) != ammo_before:
            self.scoreboard.prep()

    def _update_wave_clear(self, dt):
        self.effects.update(dt)
        self.wave_clear_ms -= dt
        if self.wave_clear_ms <= 0:
            self._begin_next_wave()

    def _detect_collisions(self):
        blocked = pygame.sprite.groupcollide(
            self.arrows, self.fireballs, True, True, collided=collide_rects
        )
        for arrow, balls in blocked.items():
            self._spawn_effect('hit', arrow.rect.center)
            self.stats.add_hero_score(self.settings.combo_bonus)
            if balls:
                self._spawn_effect(balls[0].kind, balls[0].rect.center)
        if blocked:
            self.scoreboard.prep()

        hits = pygame.sprite.spritecollide(
            self.villain, self.arrows, True, collided=collide_rects
        )
        for hit in hits:
            self._spawn_effect('hit', hit.rect.center)
            self.stats.add_hero_score(self.settings.hit_points + self.stats.wave_index * 2)
            if self.villain.take_damage():
                self._on_villain_down()
                return
        if hits:
            self.scoreboard.prep()

        if self.hero.invuln_ms > 0:
            return
        fire_hits = pygame.sprite.spritecollide(
            self.hero, self.fireballs, True, collided=collide_rects
        )
        if fire_hits:
            kind = fire_hits[0].kind
            self._spawn_effect(kind, self.hero.rect.center)
            self._on_hero_hit()

    def _on_hero_hit(self):
        self.stats.add_villain_score(15)
        self.stats.add_hero_score(-self.settings.miss_penalty)
        self.stats.lives -= 1
        self.fireballs.empty()
        self.hero.take_hit()
        self.scoreboard.prep()
        if self.stats.lives <= 0:
            self.state = STATE_GAME_OVER

    def _on_villain_down(self):
        self.stats.add_hero_score(
            self.settings.wave_clear_points + self.stats.wave_index * 10
        )
        self._spawn_effect('flash', self.villain.rect.center)
        self.arrows.empty()
        self.fireballs.empty()
        self.wave_clear_ms = self.settings.wave_clear_ms
        self.state = STATE_WAVE_CLEAR
        self.scoreboard.prep()

    def _begin_next_wave(self):
        self.stats.wave_index += 1
        self.villain.configure(self.settings.wave_for(self.stats.wave_index))
        self.hero.reset_position()
        self.hero.refresh_image()
        self.villain.reset_position()
        self.arrows.empty()
        self.fireballs.empty()
        self.state = STATE_PLAY
        self.scoreboard.prep()

    def _screen_update(self):
        self.screen.blit(self.background, (0, 0))
        if self.state != STATE_MENU:
            self.hero.blit()
            self.villain.blit()
            self.arrows.draw(self.screen)
            self.fireballs.draw(self.screen)
            self.effects.draw(self.screen)
            self.scoreboard.show_score()
        else:
            self.hero.blit()
            self.villain.blit()

        if self.state == STATE_MENU:
            self.scoreboard.show_menu()
        elif self.state == STATE_PAUSE:
            self.scoreboard.show_pause()
        elif self.state == STATE_GAME_OVER:
            self.scoreboard.show_game_over()
        elif self.state == STATE_WAVE_CLEAR:
            self.scoreboard.show_wave_clear()

        pygame.display.flip()


if __name__ == '__main__':
    MainGame().run_game()
