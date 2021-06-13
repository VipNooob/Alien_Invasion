import pygame.font

class Button():
    def __init__(self, ai_game, msg):
        """initialize the button's attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # set the dimensions and properties of the button
        self.button_block = pygame.image.load("images/button.png")
        self.text_color = (125, 125, 125)
        self.font = pygame.font.SysFont(None, 120)

        # build an rect and align it in the screen center
        self.rect = self.button_block.get_rect()
        self.rect.center = self.screen_rect.center

        # message of button creates only once
        self.prep_msg(msg)


    def prep_msg(self, msg):
        """transfer msg into a rectangle and align a text in screen center"""
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #  Draw blank button and then draw message
        self.screen.blit(self.button_block, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)