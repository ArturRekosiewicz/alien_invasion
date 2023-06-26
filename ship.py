import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """klasa przeznaczona do zarządzania statkiem kosmicznym."""

    def __init__(self, ai_game):
        """inicalizacja statku kosmicznego i jego polozenie poczatkowe."""
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # wczytywanie obrazu statku kosmicznego i pobranie jego prostokata.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # kazdy nowy statek kosmiczny pojawia sie na dole ekranu.
        self.rect.midbottom = self.screen_rect.midbottom

        # polozenie poziome statku jest przechowywane w postaci liczby zmniennoprzecinkowiej.
        self.x = float(self.rect.x)

        # opcje wskazujace na poruszanie sie statku.
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """ uaktualnienie polozenia statku na podstawie opcji wskazujacej
            na jego ruch"""
        # uaktualnienie wartosci wspolrzednej X statku, a nie jego prostokata.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # uaktyalnienie obiektu rect na podstawie wartosci self.x.
        self.rect.x = self.x

    def blitme(self):
        """wyswietlanie statku kosmicznego w jego aktualnym polozeniu."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """umieszczenie statku na srodku przy dolnej krawedzi ekranu."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
