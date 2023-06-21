class GameStats:
    """monitorowanie danych statystycznych w grze "inwazja obcych."""

    def __init__(self, ai_game):
        """inicjalizacja danych statystycznych"""
        self.settings = ai_game.settings
        self.reset_stats()

        # uruchomienie gry "inwazja obych" w stanie nieaktywnym.
        self.game_active = False

    def reset_stats(self):
        """Inicjalizacja danych statysycznych,ktore moga zmienaic sie
            w trakcie gry"""
        self.ships_left = self.settings.ship_limit
