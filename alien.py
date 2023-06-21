import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """klasa przedstawiajaca pojedynczego obcego we floce."""

    def __init__(self, ai_game):
        """inicjanizacja obcego i zdefiniowanie jego polozenia poczatkowego."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # wczytywanie obrazu obcego i zdefiniowanie jego atrybutu rect.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # umieszczenie nowego obcego w poblizu lewego gornego rogu.

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # przechowywanie dokladnego poziomego polozenia obcego.
        self.x = float(self.rect.x)

    def check_edge(self):
        """zwraca wartosc true, jesli obcy jest przy krawedzi"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """przesuniecie obcego w prawo lub lewo."""
        self.x += (self.settings.alien_speed *
                   self.settings.fleet_direction)
        self.rect.x = self.x
