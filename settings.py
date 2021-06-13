class Settings():
    """Class stored all game settings"""

    def __init__(self):
        """Initialize game settings"""
        # screen configuration
        self.screen_width = 1600
        self.screen_height = 1000
        self.bg_color = (255, 255, 255)
        self.ship_speed = 4
        # bullet configuration

        self.bullet_width = 4
        self.bullet_height = 15
        self.bullet_color = (255, 128, 0)
        self.bullets_allowed = 3
        # alien configuration

        self.fleet_drop_speed = 20

        # ship settings
        self.ship_limit = 2

        # game acceleration pace
        self.speedup_scale = 1.1

        # increasing score pace
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """initialize changeable game settings"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 3.0

        # fleet direction = 1 - denote right movement; -1 - left
        self.fleet_direction = 1

        self.alien_points = 50


    def increase_speed(self):
        """increase game speed"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)
