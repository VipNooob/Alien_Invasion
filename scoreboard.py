import pygame.font
from pygame.sprite import Group

from ship import Ship

class ScoreBoard():
    """class for output game information"""
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # font settings for score output
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # preparing original image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()

        self.prep_ships()



    def prep_score(self):
        """convert original score to surface"""
        rounded_score = round(self.stats.score, -1)
        score_str = 'Score: {:,}'.format(rounded_score)

        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # output score in the right upper part of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20


    def prep_high_score(self):
        """convert record score to surface"""
        high_score = round(self.stats.high_score, -1)
        high_score_str ="Record: {:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # the record will be alligned regarding the center of the upper side
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top




    def check_high_score(self):
        """check whether a new record appears"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()




    def prep_level(self):
        """convert level in the surface"""
        level_str = str(self.stats.level)
        level_str = f"Level: {level_str}"
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        # output level under score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10


    def prep_ships(self):
        """Say the number of the ships (lives)"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)





    def show_score(self):
        """output score on the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)




