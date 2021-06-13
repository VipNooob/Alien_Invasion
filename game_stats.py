class GameStats():
    """Track game statistics"""
    def __init__(self, ai_game):
        """Initialize statistics"""
        self.settings = ai_game.settings
        self.reset_stats()
        # game stats in inactive state
        self.game_active = False
        # record should not be reseted
        with open("the_highest_score.txt") as file:
            self.high_score = int(file.readline())


    def reset_stats(self):
        """initialize game statistics that is changing during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0

        self.level = 1


