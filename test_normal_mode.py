import unittest
from logic.exceptions import ColumnIsFullException
from logic.rules_impl.normal_rules import NormalRules
from logic.objects.checker import Checker
from logic.objects.player import Player


class TestConnectFour(unittest.TestCase):

    def setUp(self):
        self.player1 = Player("Gracz 1", Checker.RED)
        self.player2 = Player("Gracz 2", Checker.YELLOW)
        self.normal = NormalRules(6, 7, self.player1, self.player2)

    def test_one(self):
        """Test sprawdza czy po wykonaniu dwóch ruchów przez każdego z graczy spowoduje,
        że monety spadają na dół pola gry lub zatrzymują się na już wrzuconym żetonie."""

        checker = self.normal.whose_turn.checker
        for _ in range(4):
            self.normal.drop_checker(0)
        
        board2 = [[None for i in range(7)] for j in range(6)]
        board2[5][0] = checker
        board2[4][0] = Checker.YELLOW if checker != Checker.YELLOW else Checker.RED
        board2[3][0] = checker
        board2[2][0] = Checker.YELLOW if checker != Checker.YELLOW else Checker.RED
        self.assertListEqual(self.normal.board, board2)
            
    def test_two(self):
        """Test sprawdzający czy ułożenie pionowej linii przez pierwszego gracza zwróci informację o wygranej."""
        
        who_start = self.player1
        self.normal._whose_turn = who_start
        for _ in range(3):
            checker, row, col, win, draw = self.normal.drop_checker(1)
            self.normal.drop_checker(2)
        self.assertEqual(win, False)  # tu jeszcze nie powinno być wygranej gracza 1
        checker, row, col, win, draw = self.normal.drop_checker(1)  # dodaje monete i zwraca informacje o niej oraz czy jest wygrana/remis
        self.assertEqual(checker, self.player1.checker)  # czy wrzucona moneta należy do pierwszego gracza
        self.assertEqual(win, True)  # czy gracz wygrał
        self.assertEqual(who_start.checker, self.normal.who_win().checker)  # czy wygrał gracz 1

    def test_three(self):
        """Test sprawdzający czy ułożenie poziomej linii przez drugiego gracza zwróci informację o wygranej."""
        
        who_start = self.player2
        self.normal._whose_turn = who_start
        for i in range(3):
            self.normal.drop_checker(i)
            checker, row, col, win, draw = self.normal.drop_checker(i)
        self.assertEqual(win, False)  # tu nie powinno być wygranej gracza 2
        checker, row, col, win, draw = self.normal.drop_checker(3)  # dodaje monete i zwraca informacje o niej oraz czy jest wygrana/remis
        self.assertEqual(checker, self.player2.checker)  # czy wrzucona moneta należy do drugiego gracza
        self.assertEqual(win, True)  # czy gracz wygrał
        self.assertEqual(who_start.checker, self.normal.who_win().checker)  # czy wygrał gracz 2

    def test_four(self):
        """Test sprawdzający czy ułożenie poziomej lini przez jednego z graczy zwróci informację o wygranej."""

        # 'X' oznacza gracza rozpoczynającego (może to być gracz 1 lub gracz 2), 'O' oznacza gracza, który nie rozpoczynał
        who_start = self.normal.whose_turn
        # układam:
        #   0 1 2 3 4 5 6
        # 0
        # 1
        # 2       X
        # 3   O X O
        # 4   X X X
        # 5 X O O O

        self.normal.drop_checker(0) # X (5, 0)
        self.normal.drop_checker(1) # O (5, 1)
        self.normal.drop_checker(1) # X (4, 1)
        self.normal.drop_checker(3) # O (5, 3)
        self.normal.drop_checker(3) # X (4, 3)
        self.normal.drop_checker(3) # O (3, 3)
        self.normal.drop_checker(3) # X (2, 3)
        self.normal.drop_checker(2) # O (5, 2)
        self.normal.drop_checker(2) # X (4, 2)
        checker, row, col, win, draw = self.normal.drop_checker(1) # O (3, 1)
        self.assertNotEqual(checker, who_start.checker)  # teraz wrzucona moneta nie jest gracza zaczynającego
        self.assertEqual(self.normal.who_win(), None)  # nikt jeszcze nie wygrał
        checker, row, col, win, draw = self.normal.drop_checker(2) # X (3, 2)
        self.assertEqual(checker, who_start.checker)  # teraz wrzucana moneta jest gracza, który zaczynał
        self.assertEqual(win, True)  # jest informacja, że ktoś wygrał
        self.assertEqual(who_start.checker, self.normal.who_win().checker)  # wygrał gracz, który zaczynał 
        
        
    def test_five(self):
        """Test sprawdzający czy po zapełnieniu planszy i braku zwycięzcy będzie informacja o remisie."""

        # 'X' oznacza gracza rozpoczynającego (może to być gracz 1 lub gracz 2), 'O' oznacza gracza, który nie rozpoczynał
        # układam:
        #   0 1 2 3 4 5 6
        # 0 O X O X O X O
        # 1 O X O X O X X
        # 2 O X O X O X O
        # 3 X O X O X O X
        # 4 X O X O X O O
        # 5 X O X O X O X
        for _ in range(3):
            self.normal.drop_checker(0)
            self.normal.drop_checker(1)
            self.normal.drop_checker(2)
            self.normal.drop_checker(3)
            self.normal.drop_checker(4)
            self.normal.drop_checker(5)
        self.normal.drop_checker(6)
        for _ in range(3):
            self.normal.drop_checker(0)
            self.normal.drop_checker(1)
            self.normal.drop_checker(2)
            self.normal.drop_checker(3)
            self.normal.drop_checker(4)
            self.normal.drop_checker(5)
        for _ in range(4):
            checker, row, col, win, draw = self.normal.drop_checker(6)
        self.assertEqual(draw, False)  # nie ma jeszcze remisu
        self.assertEqual(win, False)  # nie ma zwycięzcy
        checker, row, col, win, draw = self.normal.drop_checker(6) # wrzucanie ostatniej monety (plansza po wrzuceniu jest pełna)
        self.assertEqual(draw, True)  # jest remis
        self.assertEqual(win, False)  # nie ma zwycięzcy

    def test_six(self):
        """Test prawdzający czy po ułożeniu linii dłuższej niż przez jednego z graczy da informację o wygranej"""

        # 'X' oznacza gracza rozpoczynającego (może to być gracz 1 lub gracz 2), 'O' oznacza gracza, który nie rozpoczynał
        # układam:
        #   0 1 2 3 4 5 6
        # 0 
        # 1 
        # 2 
        # 3
        # 4 O O O   O O O
        # 5 X X X   X X X   <- w następnym ruchu gracz, który zaczynał wrzuca monetę do pustej kolumny
        
        who_start = self.normal.whose_turn
        for i in range(3):
            self.normal.drop_checker(i) # X
            self.normal.drop_checker(i) # O
        for i in range(6, 3, -1):
            self.normal.drop_checker(i) # X
            self.normal.drop_checker(i) # O
        
        self.assertEqual(self.normal.who_win(), None)  # jeszcze nikt nie wygrał
        checker, row, col, win, draw = self.normal.drop_checker(3)
        self.assertEqual(self.normal.who_win().checker, who_start.checker) # gracz zaczynający wygrał

    def test_seven(self):
        for _ in range(6):
            self.normal.drop_checker(5)  # zapełniam kolumnę o indeksie 5 (szósta kolumna on lewej)
        self.assertRaises(ColumnIsFullException, self.normal.drop_checker, 5)  # próba wrzucenia monety do pełnej kolumny, oczekiwany wyjątek
if __name__ == "__main__":
    unittest.main()
        
