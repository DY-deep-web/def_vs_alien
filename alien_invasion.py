import sys
import random
import time
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from sound_manager import SoundManager


class AlienInvasion:

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(200, 50)

        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('祥祥大战鲜鲜 - 无尽模式')

        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.sb = Scoreboard(self)
        self.sound = SoundManager(self)

        self.spawn_timer = 0
        self.level_timer = 0
        self.play_button = Button(self, '开始游戏')

    def run_game(self):
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._spawn_aliens_timed()
                self._check_level_up()

            self._update_screen()
            self.clock.tick(120)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()

    def _start_game(self):
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_high_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        self.aliens.empty()
        self.bullets.empty()

        self.spawn_timer = pygame.time.get_ticks()
        self.level_timer = pygame.time.get_ticks()

        self.ship.center_ship()
        pygame.mouse.set_visible(False)
        self.sound.play('start')
        self.sound.play_music('bgm.mp3')

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            if self.stats.game_active:
                self._fire_bullet()
        elif event.key == pygame.K_RETURN or event.key == pygame.K_e:
            if not self.stats.game_active:
                self._start_game()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _pick_alien_type(self):
        """按权重随机选一种外星人类型"""
        types = self.settings.alien_types
        total = sum(t['weight'] for t in types)
        r = random.randint(1, total)
        cumulative = 0
        for t in types:
            cumulative += t['weight']
            if r <= cumulative:
                return t
        return types[0]

    def _spawn_aliens_timed(self):
        """定时刷出外星人（核心无尽逻辑）"""
        now = pygame.time.get_ticks()
        if now - self.spawn_timer > self.settings.spawn_interval:
            num_to_spawn = random.randint(1, self.settings.max_aliens_per_spawn)
            for _ in range(num_to_spawn):
                type_info = self._pick_alien_type()
                self.aliens.add(Alien(self, type_info))
            self.spawn_timer = now

    def _check_level_up(self):
        """每10秒自动升级"""
        now = pygame.time.get_ticks()
        if now - self.level_timer >= self.settings.level_up_interval:
            self.level_timer = now
            self.stats.level += 1
            self.settings.increase_speed()
            self.sb.prep_level()
            self.sound.play('levelup', volume=0.8)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            self.bullets.add(Bullet(self))
            self.sound.play('shoot', volume=0.6)

    def _update_bullets(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                for alien in aliens:
                    self.stats.score += alien.points
                self.sound.play('explode', volume=0.7)
            self.sb.prep_score()
            self.sb.check_high_score()

    def _update_aliens(self):
        self.aliens.update()

        for alien in self.aliens.sprites():
            alien.check_edges()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            return

        screen_rect = self.screen.get_rect()
        for alien in self.aliens.copy():
            if alien.rect.top > screen_rect.bottom:
                self.aliens.remove(alien)
                self._ship_hit()
                if not self.stats.game_active:
                    return

    def _ship_hit(self):
        if self.stats.ships_left > 1:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.sound.play('hit', volume=0.9)

            for alien in self.aliens.copy():
                if alien.rect.top > self.screen.get_rect().bottom:
                    self.aliens.remove(alien)

            self.spawn_timer = pygame.time.get_ticks()
            self.ship.center_ship()
            time.sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            self.sound.play('gameover', volume=1.0)
            self.sound.stop_music()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()