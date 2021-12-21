import random
from checker import Checker
from player import Player

class GameRules:
    """Klasa bazowa reguł gry"""
    def __init__(self, n_rows, n_cols, player1, player2):
        self._n_rows = n_rows
        self._n_cols = n_cols
        self._player1 = player1
        self._player2 = player2
        self._whose_turn = None
        self._winner = None
        self._board = [[None for i in range(self._n_cols)] for j in range(self._n_rows)]

    def _whoStart(self):
        raise NotImplementedError()

    def dropCoin(self):
        raise NotImplementedError()

    def changePlayer(self):
        raise NotImplementedError()

    def whoWin(self):
        raise NotImplementedError()


class NormalRules(GameRules):
    """Brak limitu czasowego na ruch. Wygrywa osoba, która ułoży 4 monety w rzędzie."""
    def __init__(self, n_rows, n_cols, player1, player2):
        super().__init__(n_rows, n_cols, player1, player2)
        self._whose_turn = self._whoStart()
        self._n_moves = 0

    @property
    def whose_turn(self):
        return self._whose_turn

    def _whoStart(self):
        return random.choice([self._player1, self._player2])

    def dropCoin(self, col):
        free_row = -1
        for i, spot in enumerate(reversed(self._board)):
            if spot[col] is None:
                free_row = self._n_rows - i - 1
                break
        else:
            return (-1, -1, -1)  # Tutaj będzie wywoływany wyjątek ColumnIsFullException ALBO zablokuję możliwość kilkania przycisku dla pełnej kolumny
        
        self._board[free_row][col] = self._whose_turn.checker
        self._n_moves += 1
        return (self._whose_turn.checker, free_row, col)  # zwraca tuple (jaka_moneta, jaki_wiersz, jaka_kolumna)

    def changePlayer(self):
        self._whose_turn = self._player1 if self._whose_turn == self._player2 else self._player2
        return self._whose_turn

    def checkWin(self):
        winning_combo = [self._whose_turn.checker for _ in range(4)]
        # wygrana poziomo
        for row in self._board:
            for i in range(self._n_cols-3):
                if row[i:i+4] == winning_combo:
                    self._winner = self._whose_turn
                    return True
        
        # wygrana pionowo
        rows_prep = zip(*self._board)
        transposed_board = [list(row) for row in rows_prep]
        for row in transposed_board:
            for i in range(self._n_rows-3):
                if row[i:i+4] == winning_combo:
                    self._winner = self._whose_turn
                    return True
        
        # wygrana na ukos
        for j in range(4):
            for i in range(3):
                if [self._board[x+i][x+j] for x in range(4)] == winning_combo:
                    self._winner = self._whose_turn
                    return True
        for j in range(6, 2, -1):
            for i in range(3):
                if [self._board[x+i][j-x] for x in range(4)] == winning_combo:
                    self._winner = self._whose_turn
                    return True

        return False

    def whoWin(self):
        return self._winner

class TimeRules(GameRules):
    """Na graczy zostaje nałożony limit czasowy na ruch. Jeżeli dany gracz nie wykona ruchu w ciągu usttalonego czasu
    to program sam wykonuje ruch za gracza."""
    def __init__(self, n_rows, n_cols, player1, player2, time_limit):
        super().__init__(n_rows, n_cols, player1, player2)
        self._whose_turn = self.whoStart()
        self.is_time_limit = True
        self._time_limit = time_limit

    def whoStart(self):
        return random.choice([self._player1, self._player2])

    def dropCoin(self, player):
        pass

    def changePlayer(self):
        self._whose_turn = self._player1 if self._whose_turn == self._player2 else self._player2
        return self._whose_turn

    def whoWin(self):
        pass
