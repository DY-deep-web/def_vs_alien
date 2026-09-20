class Settings:
    """存储游戏中所有设置的类（无尽模式）"""

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (10, 10, 30)

        self.ship_limit = 3

        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 255, 255)
        self.bullets_allowed = 100

        self.speedup_scale = 1.05
        self.score_scale = 1.3

        self.level_up_interval = 10000

        self.alien_types = [
            {
                'image': 'images/laoxiang.bmp',
                'weight': 50,
                'speed_mult': 0.8,
                'points': 50,
                'size': 90,
                'name': '小兵',
            },
            {
                'image': 'images/yl.jpg',
                'weight': 30,
                'speed_mult': 1.0,
                'points': 100,
                'size': 100,
                'name': '精英',
            },
            {
                'image': 'images/laoxiang_2.jpg',
                'weight': 15,
                'speed_mult': 1.3,
                'points': 200,
                'size': 110,
                'name': '王牌',
            },
            {
                'image': 'images/laoxiang_3.jpg',
                'weight': 5,
                'speed_mult': 1.6,
                'points': 400,
                'size': 130,
                'name': '首领',
            },
        ]

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 5.0
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        self.fleet_direction = 1

        self.alien_points = 50

        self.spawn_interval = 3000
        self.max_aliens_per_spawn = 1

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.spawn_interval = max(800, self.spawn_interval * 0.96)
        self.max_aliens_per_spawn = min(5, self.max_aliens_per_spawn + 1)
        self.alien_points = int(self.alien_points * self.score_scale)