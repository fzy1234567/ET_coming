import sys

import pygame

from settings import Settings

class AlienInvasion:
    """整体类来管理游戏资源和行为."""

    def __init__(self):
        """始化游戏，并创建游戏资源."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")


    def run_game(self):
        """开始游戏的主循环."""
        while True:
            # 监视键盘和鼠标响应.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # 在每次循环中重新绘制屏幕.
            self.screen.fill(self.settings.bg_color)

            # 使最近绘制的屏幕可见.
            pygame.display.flip()

if __name__ == '__main__':
    # 创建一个游戏实例，并运行游戏.
    ai = AlienInvasion()
    ai.run_game()
