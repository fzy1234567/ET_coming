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