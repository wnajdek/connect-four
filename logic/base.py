import abc
from logic.objects.checker import Checker
from logic.objects.player import Player

class GameRules(metaclass=abc.ABCMeta):
    """Klasa bazowa reguł gry
    
    Metody w tej klasie są wirtualne.
    W klasach pochodnych wymagane jest zaimplementowanie wszystkich metod tej klasy (w tym getterów).

    Atrybuty:
        _n_rows (int): liczba wierszy planszy
        _n_cols (int): liczba kolumn planszy
        _player1 (Player): gracz pierwszy
        _player2 (Player): gracz drugi
        _whose_turn (Player): przechowuje informację kogo tura
        _winner (Player): przechowuje informację kto wygrał
        _board (list): plansza przechowywana w formie dwuwymiarowej listy
    
    Gettery (wymagają zaiplementowania w klasie pochodnej):
        n_rows: zwraca liczbę wierszy planszy
        n_cols: zwraca liczbę kolumn na planszy
        whose_turn: zwraca gracza, którego teraz jest tura
        board: zwraca planszę w formie listy dwuwymiarowej

    Metody wirtualne (wymagają zaimplementowania w klasie pochodnej):
        _who_start(): kto rozpoczyna grę
        drop_checker(col): umieść monetę na planszy
        change_player(): daj prawo ruchu drugiemu graczowi
        check_win(): sprawdź wygraną
        who_win(): zwróć informację kto wygrał 
    """

    def __init__(self, n_rows, n_cols, player1, player2):
        self._n_rows = n_rows
        self._n_cols = n_cols
        self._player1 = player1
        self._player2 = player2
        self._whose_turn = None
        self._winner = None
        self._board = [[None for i in range(self._n_cols)] for j in range(self._n_rows)]

    @property
    def n_rows(self):
        pass

    @property
    def n_cols(self):
        pass

    @property
    def whose_turn(self):
        pass
    
    @property
    def board(self):
        pass

    @abc.abstractmethod
    def _who_start(self):
        pass

    @abc.abstractmethod
    def drop_checker(self, col):
        pass

    @abc.abstractmethod
    def change_player(self):
        pass

    @abc.abstractmethod
    def check_win(self):
        pass

    @abc.abstractmethod
    def check_draw(self):
        pass

    @abc.abstractmethod
    def who_win(self):
        pass
