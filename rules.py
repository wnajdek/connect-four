import random

class GameRules:
    """Klasa bazowa reguł gry"""
    def __init__(self, n_rows, n_cols, player1, player2):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self._player1 = player1
        self._player2 = player2
        self._whose_turn = None

    def whoStart(self):
        raise NotImplementedError()

    def whoseTurn(self):
        raise NotImplementedError()

    def whoWin(self):
        raise NotImplementedError()


class NormalRules(GameRules):
    """Brak limitu czasowego na ruch. Wygrywa osoba, która ułoży 4 monety w rzędzie."""
    def __init__(self, n_rows, n_cols, player1, player2):
        super().__init__(n_rows, n_cols, player1, player2)
        self._whose_turn = self.whoStart()
    
    def whoStart(self):
        return random.choice([self._player1, self._player2])

    def whoseTurn(self):
        tmp_whose_turn = self._whose_turn
        self._whose_turn = self._player1 if self._whose_turn == self._player2 else self._player2
        return tmp_whose_turn

    def whoWin(self):
        pass

class TimeRules(GameRules):
    """Na graczy zostaje nałożony limit czasowy na ruch. Jeżeli dany gracz nie wykona ruchu w ciągu usttalonego czasu
    to program sam wykonuje ruch za gracza."""
    def __init__(self, n_rows, n_cols, player1, player2, time_limit):
        super().__init__(n_rows, n_cols, player1, player2)
        self._whose_turn = self.whoStart()
        self.is_time_limit = True
        self._time_limit = time_limit
    
    def whoStart(self, player1, player2):
        return random.choice([player1, player2])

    def whoseTurn(self):
        tmp_whose_turn = self._whose_turn
        self._whose_turn = self._player1 if self._whose_turn == self._player2 else self._player2
        return tmp_whose_turn

    def whoWin(self):
        pass
