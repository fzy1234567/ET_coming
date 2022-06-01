import pygame
 
class Ship:
    """管理飞船的一个类."""
 
    def __init__(self, ai_game):
        """初始化该船并设置其初始位置."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # 加载船只图像并获得它的图像.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # 每艘新船都从屏幕中心底部开始.
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """在当前位置绘制该船."""
        self.screen.blit(self.image, self.rect)
