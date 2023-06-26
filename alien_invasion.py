import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from alien import Alien
from bullet import Bullet


class AlienInvasion:
    """ogólna klasa przeznaczona do zarządzania zasobami i sposobem działania gry."""

    def __init__(self):
        """Inicjalizacja gry i utworzenie jej zasobów."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Inwazja obcych")

        # utworzenie egzemplarza przechowujacego dane statysttyczne gry.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # utworzenie przycisku gra.
        self.play_button = Button(self, "Gra")

        # zdefiniowanie koloru tła.

    def run_game(self):
        """Rozpoczęcie pętli głównej gry."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """reakcja na zdarzenia generowane przez klawiature i mysz."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """rozpoczecie nowej gry po klikieciu przycisku Gra przez uzytkownika."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # reset ustawien gry
            self.settings.initialize_dynamic_settings()

            #wyzerowanie danych statystycznych gry.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()


            #usuniecie zawartosci list aliens i bullets.
            self.aliens.empty()
            self.bullets.empty()

            #utworzenie nowej floty i wysrodkowanie statku.
            self._create_fleet()
            self.ship.center_ship()

            #ukrycie kursowa myszy
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """reakcja na nacisniecie klawisza."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """reakcja na zwolnienie klawisza"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """utworzenie nowego pocisku i dodatnie go do grupy pociskow."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """uaktualnienie polozenia pociskow i usuniecie tych niewidocznych
        na ekranie"""
        self.bullets.update()

        # usuniecie pociskow, ktore znajduja sie poza ekranem.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """reakcja na kolizje miedzy pociskiem i obcym"""
        # usuniecie wszystkich pociskow i obcych, miedzy ktorymi doszlo do kolizji.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # pozbycie sie istniejacych pociskow i utworzenie nowej floty.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #inkrementacja numeru poziomu.
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """sprawdzenie,czy flota obcych znajduje sie przy krawedzi
            a nastepnie uaktualnienie polozenia wszystkich obcych we flocie"""
        self._check_fleet_edges()
        self.aliens.update()

        # wykrywanie kolizji miedzy obcym i statkiem.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # wyszukiwanie obcych docierajacych do dolnej krawedzi ekranu.
        self._check_aliens_bottom()

    def _create_fleet(self):
        """utworzenie pelnej floty obcego"""
        # utworzenie obcego i ustalenie liczby obcych, ktorzy zmieszcza sie w rzedzie.
        # odleglosc miedzy poszczegolnymi obcymi jest rowna szerokosci obcego.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # ustalenie ile rzedow obcych zmiesci sie na ekranie.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # utworzenie pierszego rzedu obcych.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """utworzenie obcego i umieszzczenie go w rzedzie"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edge():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        """sprawdzenie, czy ktorykolwiek obcy dotarl do dolnej krawedzi
            ekranu."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # tak samo jak w przypadku zderzenia statku z obcym.
                self._ship_hit()
                break

    def _ship_hit(self):
        """reakcja na uderzenie  obcego w statek."""
        if self.stats.ships_left > 0:
            # zmniejszenei wartosci przechowywanej w ships_left.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # usuniecie zawartosci list aliens i bullets.
            self.aliens.empty()
            self.bullets.empty()

            # utworzenie nowej floty i wysrodkowanie statku.
            self._create_fleet()
            self.ship.center_ship()

            # pauza.
            sleep(0.5)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        """ uaktualnienie obrazow na ekranie i przejscie do nowego ekranu."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # wyswietlanie inforamacji o punktacji.
        self.sb.show_score()

        # wyswietlenie przycisku tylko wtedy, gey gra nie jest aktywna.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # wyświetlenie ostatnio zmodyfikowanego ekranu
        pygame.display.flip()


if __name__ == '__main__':
    # Utworzenie egzemplarza gry i jej uruchomienie.
    ai = AlienInvasion()
    ai.run_game()
