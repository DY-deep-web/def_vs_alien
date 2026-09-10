import pygame

class Ship:
    """管理飞船的类"""
    def __init__(self,ai_game):
        """初始化飞船并设置其初始位置"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        

        #加载飞船图像
        self.image = pygame.image.load(r'D:\祥祥大战外星人\images\LaoDi.bmp').convert()

        #获取图片左上角像素颜色（通常是背景色）
        bg_color = self.image.get_at((0, 0))
        self.image.set_colorkey(bg_color)

        #获取原始尺寸，按比例缩放到宽度100px
        original_width = self.image.get_width()
        original_height = self.image.get_height()
        target_width = 100
        target_height = int(original_height * target_width / original_width)
        self.image = pygame.transform.scale(self.image, (target_width, target_height))

        self.rect = self.image.get_rect()
        
        #将每艘新飞船放在屏幕底部中央
        self.rect.midbottom = self.screen_rect.midbottom

        #在飞船的属性中存储小数x和y值
        self.x = float(self.rect.x)

        #移动标志
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image,self.rect)

    def update(self):
        """根据移动标志调整飞船的位置"""
        #更新飞船而不是rect对象的x值
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        #根据小数x值更新rect对象
        self.rect.x = self.x 
