import sys

import pygame

from settings import Settings
from ship import Ship

class AlienInvasion:
    """整体类来管理游戏资源和行为."""

    def __init__(self):
        """始化游戏，并创建游戏资源."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)


    def run_game(self):
        """开始游戏的主循环."""
        while True:
            self._check_events()
            self._update_screen()

    def _check_events(self):
        """响应按键和鼠标事件."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        pygame.display.flip()


if __name__ == '__main__':
    # 创建一个游戏实例，并运行游戏.
    ai = AlienInvasion()
    ai.run_game()
