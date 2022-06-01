class GameStats:
    """追踪外星人入侵的统计数据."""
    
    def __init__(self, ai_game):
        """初始化数据."""
        self.settings = ai_game.settings
        self.reset_stats()

        #以非开始状态开始游戏.
        self.game_active = False
        
    def reset_stats(self):
        """初始化游戏中可以改变的统计数据."""
        self.ships_left = self.settings.ship_limit