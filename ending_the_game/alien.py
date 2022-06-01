import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """代表舰队中的一个外星人的类."""

    def __init__(self, ai_game):
        """初始化外星人并设置其初始位置."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # 加载外星人图像并设置它的rect属性.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # 从屏幕左上角开始的每一个新的外星人.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的准确水平位置.
        self.x = float(self.rect.x)

    def check_edges(self):
        """如果外星人在屏幕边缘则返回True."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """向右或向左移动外星人."""
        self.x += (self.settings.alien_speed *
                   self.settings.fleet_direction)
        self.rect.x = self.x
