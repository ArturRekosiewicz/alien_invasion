import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """klasa przeznaczona do zarzadzania pociskami wystrzeliwanymi przez statek."""

    def __init__(self, ai_game):
        """utworzenie obiektu pocisku w aktualnym polozeniu statku."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # utworzenie prostokata pocisku w punkcie(0, 0) a nastepnie
        # zdefiniwanie dla niego odpowidniegniego polozenia.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # polozenie pocisku jest zdefiniowane za pomoca wartosci zmiennoprzenikowej.
        self.y = float(self.rect.y)

    def update(self):
        """poruszanie pociskiem po ekranie"""
        # uaktualnienie polozenia pocisku.
        self.y -= self.settings.bullet_speed
        # uaktualneinei polozenia prostokata pocisku.
        self.rect.y = self.y

    def draw_bullet(self):
        """wyswietalnei pocisku na ekranie."""
        pygame.draw.rect(self.screen, self.color, self.rect)
