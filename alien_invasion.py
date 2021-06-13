import sys

import pygame

from settings import Settings

from ship import Ship

from bullet import Bullet

from alien import Alien

from time import sleep

from game_stats import GameStats

from button import Button

from scoreboard import ScoreBoard

class AlienInvasion:
    """Class for control game resources and behavior"""

    def __init__(self):
        """initialize a game and create game resources"""
        pygame.init()


        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Alien Invasion')

        # objects to store stats and output them
        self.stats = GameStats(self)
        self.sb = ScoreBoard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        # create a play button
        self.play = Button(self, "PLAY")

    def run_game(self):
        """Run a main game"""
        while True:

            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Watch for keyboard and mouse events"""
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                with open("the_highest_score.txt", 'w') as file:
                    file.write(str(self.stats.high_score))
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """start the game if the play button is pressed"""
        button_clicked = self.play.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # reset game settings
            self.settings.initialize_dynamic_settings()

            self.running_game()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()



    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            # move the ship to the right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_p:
            if not self.stats.game_active:
                self.running_game()
        elif event.key == pygame.K_1 and not self.stats.game_active:
            self.settings.alien_speed = 1.5
            print("Была выбрана средняя сложность игры!")
        elif event.key == pygame.K_2 and not self.stats.game_active:
            self.settings.speedup_scale = 2.5
            print("Была выбрана высокая сложность игры!")
        elif event.key == pygame.K_3 and not self.stats.game_active:
            self.settings.speedup_scale = 6
            print("Была выбрана запредельная сложность игры!")



    def running_game(self):
        """restart the game"""
        self.stats.reset_stats()
        self.stats.game_active = True

        # clear alien's and bullet's lists
        self.aliens.empty()
        self.bullets.empty()

        # create new fleet and locate the ship in the center of the screen
        self._create_fleet()
        self.ship.center_ship()

        # hide the mouse cursor
        pygame.mouse.set_visible(False)

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        if self.stats.game_active:
            # Redraw the screen during each pass through the loop.
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            # Make the most recently drawn screen visible
            self.aliens.draw(self.screen)
            self.sb.show_score()
            pygame.display.flip()

        else:
            self.screen.fill(self.settings.bg_color)
            self.play.draw_button()
            pygame.display.flip()

    def _fire_bullet(self):
        """Create a new bullet and add it in the GROUP bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        # update positions of bullets
        self.bullets.update()

        # delete bullets intersect the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))
        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        """collision processing of bullets and aliens """
        # delete bullets and aliens if they collide
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()


        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        """Create an invasion fleet"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        avaliable_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = avaliable_space_x // (2 * alien_width)

        """Determine the number of rows of aliens that fit on the screen"""
        ship_height = self.ship.rect.height
        avaliable_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = avaliable_space_y // (2 * alien_height)
        # create invasion fleet
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """create an alien and place it in the row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Set down all fleet and change the fleet direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        """update positions of all aliens"""
        self._check_fleet_edges()
        self.aliens.update()

        # check collision "alien-ship"
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # check, if aliens have reached the bottom of screen
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            # dicrease ship_left
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # clear lists of aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # create new fleet and place the ship in the center
            self._create_fleet()
            self.ship.center_ship()

            # game pause
            sleep(1)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # same like _ship_hit
                self._ship_hit()
                break


if __name__ == "__main__":
    # create a game instance and run game
    ai = AlienInvasion()
    ai.run_game()
