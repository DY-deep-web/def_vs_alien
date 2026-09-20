import pygame.font


class Scoreboard:
    """显示得分信息的类"""

    def __init__(self, ai_game):
        """初始化显示得分涉及的属性"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.text_color = (230, 230, 230)
        self.font = pygame.font.SysFont('simhei', 48)

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self._ship_icon = self._make_ship_icon()

    def _make_ship_icon(self):
        """创建一个缩小版飞船图标"""
        icon_w = 40
        icon_h = int(
            icon_w * self.ai_game.ship.image.get_height()
            / self.ai_game.ship.image.get_width())
        return pygame.transform.scale(
            self.ai_game.ship.image, (icon_w, icon_h))

    def prep_score(self):
        """将得分转换为一幅渲染的图像"""
        score_str = f'得分: {self.stats.score}'
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """将最高得分转换为一幅渲染的图像"""
        high_score_str = f'最高分: {self.stats.high_score}'
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, self.settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """将等级转换为一幅渲染的图像"""
        level_str = f'等级: {self.stats.level}'
        self.level_image = self.font.render(
            level_str, True, self.text_color, self.settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """飞船数变化时，无需做额外操作（图标通过 stats.ships_left 动态绘制）"""
        pass

    def show_score(self):
        """在屏幕上显示得分、等级和剩余飞船"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)

        icon_h = self._ship_icon.get_height()
        for i in range(self.stats.ships_left):
            self.screen.blit(self._ship_icon,
                             (10 + i * (self._ship_icon.get_width() + 5),
                              10))

    def check_high_score(self):
        """检查是否诞生了新的最高得分"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()