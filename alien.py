import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Class representing a single alien"""
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # loading an alien image and assign attribute 'rect'
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        # each new alien appears in the top left corner of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # retain accurate position of the alien
        self.x = float(self.rect.x)

    def update(self):
        """Move the alien to the right."""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """return True if an alien is near the edge of the screen """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
