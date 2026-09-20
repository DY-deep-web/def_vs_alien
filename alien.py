import random
import pygame
from pygame.sprite import Sprite


class Alien(Sprite):

    """表示单个外星人的类（支持多种类型）"""

    def __init__(self, ai_game, type_info):
        """初始化外星人
        type_info: 来自 settings.alien_types 的字典
        """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        base_path = r'D:\祥祥大战外星人'
        image_path = base_path + '\\' + type_info['image']
        self.image = pygame.image.load(image_path).convert()

        bg_color = self.image.get_at((0, 0))
        self.image.set_colorkey(bg_color)

        original_width = self.image.get_width()
        original_height = self.image.get_height()
        target_width = type_info['size']
        target_height = int(original_height * target_width / original_width)
        self.image = pygame.transform.scale(
            self.image, (target_width, target_height))

        self.rect = self.image.get_rect()

        max_x = self.settings.screen_width - self.rect.width
        self.rect.x = random.randint(0, max_x)
        self.rect.y = -self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        speed_mult = type_info['speed_mult']
        base = self.settings.alien_speed
        self.horizontal_speed = base * speed_mult * random.uniform(0.3, 1.2)
        self.vertical_speed = base * speed_mult * random.uniform(0.5, 1.5)
        self.direction = random.choice([-1, 1])

        self.points = type_info['points']
        self.alien_name = type_info['name']

    def update(self):
        """独立移动：左右漂移 + 持续下落"""
        self.x += self.horizontal_speed * self.direction
        self.y += self.vertical_speed
        self.rect.x = self.x
        self.rect.y = self.y

    def check_edges(self):
        """碰左右边就自己反向"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            self.direction = -1
            return True
        elif self.rect.left <= 0:
            self.direction = 1
            return True
        return False