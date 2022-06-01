import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """整体类来管理游戏资源和行为."""

    def __init__(self):
        """始化游戏，并创建游戏资源."""
        pygame.init()
        self.settings = Settings()

        # 设置游戏屏幕大小
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        # 设置游戏名称
        pygame.display.set_caption("Alien Invasion")

        # 创建一个实例来存储游戏统计信息
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # 创建游戏开始按钮
        self.play_button = Button(self, "Play")

    def run_game(self):
        """开始游戏的主循环."""
        while True:
            self._check_events()

            # 判断游戏行为
            if self.stats.game_active:
                # 判断更新飞船
                self.ship.update()
                # 判断更新子弹
                self._update_bullets()
                # 判断更新外星人
                self._update_aliens()

            # 判断刷新屏幕
            self._update_screen()

    def _check_events(self):
        """响应按键和鼠标事件."""
        for event in pygame.event.get():
            # 判断退出游戏事件
            if event.type == pygame.QUIT:
                # 响应退出游戏事件
                sys.exit()
            # 判断键盘按下事件
            elif event.type == pygame.KEYDOWN:
                # 响应键盘按下事件
                self._check_keydown_events(event)
            # 判断键盘释放事件
            elif event.type == pygame.KEYUP:
                # 响应键盘释放事件
                self._check_keyup_events(event)
            # 判断鼠标按下事件
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 响应鼠标行为
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """当玩家点击Play时开始一个新游戏."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # 重置游戏统计信息
            self.stats.reset_stats()
            self.stats.game_active = True

            # 删除所有剩余的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            
            # 创建一个新的外星人群体和飞船
            self._create_fleet()
            self.ship.center_ship()

            # 隐藏鼠标光标
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """响应按键."""
        # 判断键盘按下右方向键
        if event.key == pygame.K_RIGHT:
            # 响应飞船向右移动
            self.ship.moving_right = True
        # 判断键盘按下左方向键
        elif event.key == pygame.K_LEFT:
            # 响应飞船向左移动
            self.ship.moving_left = True
        # 判断键盘按下q键
        elif event.key == pygame.K_q:
            # 响应退出游戏
            sys.exit()
        # 判断键盘按下空格键
        elif event.key == pygame.K_SPACE:
            # 响应开火
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """响应键盘."""
        # 判断键盘按下右方向键
        if event.key == pygame.K_RIGHT:
            # 响应飞船向右移动
            self.ship.moving_right = False
        # 判断键盘按下左方向键
        elif event.key == pygame.K_LEFT:
            # 响应飞船向左移动
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创建一个新子弹，并将其添加到子弹组."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹位置，清除旧子弹."""
        # 更新子弹的位置
        self.bullets.update()

        # 删除已经消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                 self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """对子弹与外星人碰撞做出反应."""
        # 移除碰撞过的任何子弹和外星人
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

        if not self.aliens:
            # 摧毁现有的子弹，创建新的外星人群体.
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self):
        """
        检查外星人群体是否在边缘，然后更新外星人群体中所有外星人的位置.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # 判断确定外星飞船碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 确定撞击屏幕底部的外星人.
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """判断是否有外星人到达屏幕底部."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 当做飞船被外星人碰撞.
                self._ship_hit()
                break

    def _ship_hit(self):
        """对被外星人击中的飞船做出反应."""
        if self.stats.ships_left > 0:
            # 减少飞船储备数量.
            self.stats.ships_left -= 1
            
            # 清除所有剩余的外星人和子弹.
            self.aliens.empty()
            self.bullets.empty()
            
            # 创建一个新的外星人群体和飞船.
            self._create_fleet()
            self.ship.center_ship()
            
            # 停顿0.5秒.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """创建外星人舰队."""
        # 创建一个外星人，并在一行中找到外星人的位置.
        # 每个外星人之间的距离等于一个外星人的宽度.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        
        # 确定屏幕上适合的外星人的行数.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                                (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        
        # 创建完整的外星人舰队.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """创建一个外星人，并把它放在行中."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """如果有外星人到达了边缘，整体要返回."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
            
    def _change_fleet_direction(self):
        """整个舰队改变方向."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # 如果游戏处于非开始状态，跳出开始按钮.
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # 创建一个游戏实例，并运行游戏.
    ai = AlienInvasion()
    ai.run_game()
