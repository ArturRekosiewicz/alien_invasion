class Settings:
    """klasa przeznaczona do przechowywania wszystkich ustawień."""

    def __init__(self):
        """Inicjalizacja ustawień gry."""
        # ustawienia ekranu.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_speed = 1.5
        self.ship_limit = 3
        # ustawienia dotyczace pocisku.
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        #ustawienie dotyczace obcego.
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        #wartosc fleet_director wynoszaca 1 oznacza prawo, natomiast -1 lewo.
        self.fleet_direction = 1
