from logic.rules_impl.normal_rules import NormalRules
from logic.exceptions import *
from logic.rules_impl.rules_txt import *
import random


class PopOut(NormalRules):
    """Klasa pochodna klasy NormalRules. Tryb PopOut.
    
    Klasa reprezentuje zmodyfikowane zasady gry.
    Rozmiar planszy może być dowolny. Gra kończy się po ułożeniu przez jednego gracza 4 monety w rzędzie.
    W tym trybie nia ma możliwości remisu, ponieważ gracze poza dodawaniem monet do planszy mogą je również wyjmować (z dolnego wiersza).

    Atrybuty:
        _n_rows (int): liczba wierszy planszy
        _n_cols (int): liczba kolumn planszy
        _player1 (Player): gracz pierwszy
        _player2 (Player): gracz drugi
        _whose_turn (Player): przechowuje informację kogo tura
        _winner (Player): przechowuje informację kto wygrał
        _board (list): plansza przechowywana w formie dwuwymiarowej listy
        _n_moves (int): liczba wykonanych ruchów przez obu graczy
        _rules_txt_header (str): nazwa trybu
        _rules_txt_info (str): tekstowy opis reguł dla tego trybu
    
    Gettery:
        n_rows: zwraca liczbę wierszy planszy
        n_cols: zwraca liczbę kolumn na planszy
        whose_turn: zwraca gracza, którego teraz jest tura
        board: zwraca planszę w formie listy dwuwymiarowej
        rules_txt_header: zwraca nazwę trybu
        rules_txt_info: zwraca tekstowy opis reguł dla tego trybu

    Metody:
        _who_start(): kto rozpoczyna grę
        drop_checker(col): umieść monetę na planszy
        remove_checker(col): usuń monetę z planszy
        change_player(): daj prawo ruchu drugiemu graczowi
        check_win(): sprawdź wygraną
        check_draw(): sprawdź remis
        who_win(): zwróć informację kto wygrał 
    """
    
    def __init__(self, n_rows, n_cols, player1, player2):
        """Inicjalizacja obiektu klasy PopOut

        Wywoływany jest konstruktor klasy bazowej oraz tworzone są dodatkowe pola.

        Parametry:
            n_rows (int): liczba wierszy planszy
            n_cols (int): liczba kolumn planszy
            player1 (Player): gracz pierwszy
            player2 (Player): gracz drugi
        """

        super().__init__(n_rows, n_cols, player1, player2)
        self._whose_turn = self._who_start()
        self._n_moves = 0
        self._rules_txt_header = POP_OUT_HEADER  # z pliku rules_txt.py
        self._rules_txt_info = POP_OUT_INFO  # z pliku rules_txt.py

    def remove_checker(self, col):
        """Usuń monetę z planszy.
        
        Metoda sprawdza czy gracz, który ma teraz prawo ruchu, może usunąć monetę w danej kolumnie.
        Jeżeli może to moneta na samym dole danej kolumny jest usuwana, a pozostałe monety są przesuwane o 1 w dół.
        Jeżeli gracz nie może usunąć monety to wystąpi wyjątek CheckerCannotBeRemovedException z odpowiednim komunikatem.
        Na końcu następuje sprawdzenie czy któryś z graczy wygrał.

        Parametry:
            col (int): numer kolumny z której usuwana jest moneta.

        Zwraca:
            bool: czy po usunięciu któryś z graczy wygrał
        """

        if self._board[-1][col] == None:
            raise CheckerCannotBeRemovedException("Nie ma w tej kolumnie żadnej monety do wyjęcia.")
        elif self._board[-1][col] != self._whose_turn.checker:
            raise CheckerCannotBeRemovedException("Moneta, którą próbujesz wyjąć nie jest twoja.")
        
        # przesuwanie kolumny monet o 1 w dół
        for i in range(self._n_rows-1, 0, -1):
            self._board[i][col] = self._board[i-1][col]
        
        self._board[0][col] = None

        if self.check_win():
            self._winner = self._whose_turn
            return True
        
        self.change_player()

        if self.check_win():
            self._winner = self._whose_turn
            return True

    def check_draw(self):
        """Sprawdź czy remis
        
        W wypadku tego trybu remis nigdy nie nastąpi.

        Zwraca:
            bool: w tym wypadku zawsze zwraca False.
        """
        return False
