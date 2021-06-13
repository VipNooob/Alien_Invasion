import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """Class to manage the ship"""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings


        # load the image of the ship and get a rectangle
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # save real part of the coordinate of the ship center
        self.x = float(self.rect.x)

        # moving flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        # update attribute 'x' not 'rect.x'
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    def blitme(self):
        """draw the ship in the current position"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """place ship in the center of a down edge"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
