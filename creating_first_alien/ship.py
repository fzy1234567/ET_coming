import pygame


class Ship:
    """管理飞船的一个类."""

    def __init__(self, ai_game):
        """初始化该船并设置其初始位置."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # 加载船只图像并获得它的图像.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # 每艘新船都从屏幕中心底部开始.
        self.rect.midbottom = self.screen_rect.midbottom

        # 存储飞船水平位置的十进制值.
        self.x = float(self.rect.x)

        # 运动方向的标志
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据运动标志更新船的位置."""
        # 更新船只的x值，而不是图像.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # 从self.x更新rect对象.
        self.rect.x = self.x

    def blitme(self):
        """在当前位置绘制船."""
        self.screen.blit(self.image, self.rect)