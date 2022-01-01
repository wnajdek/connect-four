from logic.base import *
from logic.exceptions import *
from logic.rules_impl.rules_txt import *
import random


class PopOut(GameRules):
    """Klasa pochodna klasy GameRules. Tryb PopOut.
    
    Klasa reprezentuje zmodyfikowane zasady gry.
    Rozmiar planszy może być dowolny. Gra kończy się po ułożeniu przez jednego gracza 4 monety w rzędzie.
    W tym trybie nia ma możliwości remisu, ponieważ gracze poza dodawaniem monet do planszy mogą je również wyjmować.

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
        change_player(): daj prawo ruchu drugiemu graczowi
        check_win(): sprawdź wygraną
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
        
        Zwraca:
            Obiekt klasy PopOut.
        """

        super().__init__(n_rows, n_cols, player1, player2)
        self._whose_turn = self._who_start()
        self._n_moves = 0
        self._rules_txt_header = POP_OUT_HEADER
        self._rules_txt_info = POP_OUT_INFO

    @property
    def n_rows(self):
        """Pobierz liczbę wierszy. Zwraca wartość typu int."""
        return self._n_rows

    @property
    def n_cols(self):
        """Pobierz liczbę kolumn. Zwraca wartość typu int."""
        return self._n_cols

    @property
    def whose_turn(self):
        """Pobierz gracza, którego jest teraz tura. Zwraca obiekt Player."""
        return self._whose_turn
    
    @property
    def board(self):
        """Pobierz planszę. Zwraca dwuwymiarową listę."""
        return self._board

    @property
    def rules_txt_header(self):
        """Pobierz nazwę trybu. Zwraca wartośc typu str."""
        return self._rules_txt_header
    
    @property
    def rules_txt_info(self):
        """Pobierz opis reguł. Zwraca wartośc typu str."""
        return self._rules_txt_info

    def _who_start(self):
        """Wylosuj kto zaczyna.
        
        Metoda decyduje kto rozpoczyna grę.

        Zwraca:
            Player: gracz który zaczyna.
        """
        return random.choice([self._player1, self._player2])

    def drop_checker(self, col):
        """Dodaj monetę do planszy.
        
        Metoda sprawdza czy wrzucenie monety do danej kolumny jest możliwe. 
        Jeżeli kolumna jest pełna to wystąpi wyjątek ColumnIsFullException z odpowiednim komunikatem.
        Jeżeli kolumna nie jest pełna to moneta dodawana jest do planszy.

        Parametry:
            col (int): numer kolumny do której gracz chce wrzucić monetę
        
        Zwrace:
            tuple: (jaka_moneta (Checker), jaki_wiersz (int), jaka_kolumna (int), wygrana (bool), remis (bool))
        """

        free_row = -1
        for i, spot in enumerate(reversed(self._board)):
            if spot[col] is None:
                free_row = self._n_rows - i - 1
                break
        else:
            raise ColumnIsFullException("Kolumna jest pełna. Wybierz inną kolumnę.")
        
        self._board[free_row][col] = self._whose_turn.checker
        self._n_moves += 1

        tmp_checker = self._whose_turn.checker

        if self.check_win():
            return (tmp_checker, free_row, col, True, False)
        else:
            self.change_player()
            return (tmp_checker, free_row, col, False, False)  # zwraca tuple (jaka_moneta, jaki_wiersz, jaka_kolumna, wygrana, remis)

    def remove_checker(self, col):
        """Usuń monetę z planszy.
        
        Metoda sprawdza czy gracz, który ma teraz prawo ruchu, może usunąć monetę w danej kolumnie.
        Jeżeli może to moneta na samym dole danej kolumny jest usuwana, a pozostałe monety są przesuwane o 1 w dół.
        Jeżeli gracz nie może usunąć monety to wystąpi wyjątek CheckerCannotBeRemovedException z odpowiednim komunikatem.

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
        

    def change_player(self):
        """Zmień na drugiego gracza.
        
        Metoda powoduje, że prawo ruchu przechodzi na drugiego gracza.

        Zwraca:
            Player: gracz, który dostał prawo wykonania ruchu.
        """
        self._whose_turn = self._player1 if self._whose_turn == self._player2 else self._player2
        return self._whose_turn

    def check_win(self):
        """Sprawdź wygraną.
        
        Metoda sprawdza czy gracz, który wykonał teraz ruch, wygrał grę poprzez ułożenie 
        4 monet jednego koloru w rzędzie. Najpierw sprawdzana jest możliwość wygranej w poziomie, następnie w pionie,
        a na końcu wygranej po skosie.

        Zwraca:
            bool: Zwraca True jeżeli gracz ułożył 4 monet w rzędzie lub w przeciwnym przypadku False.
        """

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
        for j in range(self._n_cols-3):
            for i in range(self._n_rows-3):
                if [self._board[x+i][x+j] for x in range(4)] == winning_combo:
                    self._winner = self._whose_turn
                    return True
        for j in range(self._n_cols-1, 2, -1):
            for i in range(self._n_rows-3):
                if [self._board[x+i][j-x] for x in range(4)] == winning_combo:
                    self._winner = self._whose_turn
                    return True

        return False

    def who_win(self):
        """Kto wygrał.
        
        Zwraca:
            Player: Zwraca gracza, który wygrał.
        """
        return self._winner