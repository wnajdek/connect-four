import unittest
from logic.exceptions import ColumnIsFullException
from logic.rules_impl.five_in_a_row import FiveInARow
from logic.objects.checker import Checker
from logic.objects.player import Player


class TestFiveInARow(unittest.TestCase):

    def setUp(self):
        self.player1 = Player("Gracz 1", Checker.RED)
        self.player2 = Player("Gracz 2", Checker.YELLOW)
        self.logic = FiveInARow(self.player1, self.player2)  # wymiary planszy: 6 wierszy x 9 kolumn

    def test_one(self):
        """Test sprawdza czy po wykonaniu dwóch ruchów przez każdego z graczy spowoduje,
        że monety spadają na dół pola gry lub zatrzymują się na już wrzuconym żetonie."""

        # 'X' oznacza gracza rozpoczynającego (może to być gracz 1 lub gracz 2), 'O' oznacza gracza, który nie rozpoczynał
        # c - moneta czerwona, ż - moneta żółta
        # układam:
        #   0 1 2 3 4 5 6 7 8
        # 0 ż               c
        # 1 c               ż
        # 2 ż   O           c
        # 3 c   X           ż
        # 4 ż   O           c
        # 5 c   X           ż
        checker = self.logic.whose_turn.checker
        for _ in range(4):
            self.logic.drop_checker(2)
        
        board2 = [[None for i in range(9)] for j in range(6)]
        for i in range(6):
            if i % 2:
                board2[i][0] = Checker.RED
                board2[i][9-1] = Checker.YELLOW
            else:
                board2[i][0] = Checker.YELLOW
                board2[i][9-1] = Checker.RED
        board2[5][2] = checker
        board2[4][2] = Checker.YELLOW if checker != Checker.YELLOW else Checker.RED
        board2[3][2] = checker
        board2[2][2] = Checker.YELLOW if checker != Checker.YELLOW else Checker.RED
        self.assertListEqual(self.logic.board, board2)  # czy plansze sa takie same
            
    def test_two(self):
        """Test sprawdzający czy ułożenie pionowej linii przez pierwszego gracza zwróci informację o wygranej."""
        
        # 'X' oznacza gracza rozpoczynającego (może to być gracz 1 lub gracz 2), 'O' oznacza gracza, który nie rozpoczynał
        # c - moneta czerwona, ż - moneta żółta
        # układam:
        #   0 1 2 3 4 5 6 7 8
        # 0 ż               c
        # 1 c X             ż
        # 2 ż X O           c
        # 3 c X O           ż
        # 4 ż X O           c
        # 5 c X O           ż
        who_start = self.player1
        self.logic._whose_turn = who_start
        for _ in range(4):
            checker, row, col, win, draw = self.logic.drop_checker(1)
            self.logic.drop_checker(2)
        self.assertEqual(win, False)  # tu jeszcze nie powinno być wygranej gracza 1
        checker, row, col, win, draw = self.logic.drop_checker(1)  # dodaje monete i zwraca informacje o niej oraz czy jest wygrana/remis
        self.assertEqual(checker, self.player1.checker)  # czy wrzucona moneta należy do pierwszego gracza
        self.assertEqual(win, True)  # czy gracz wygrał
        self.assertEqual(who_start.checker, self.logic.who_win().checker)  # czy wygrał gracz 1

    def test_three(self):
        """Test sprawdzający czy ułożenie poziomej linii przez drugiego gracza zwróci informację o wygranej."""
        
        # 'X' oznacza gracza rozpoczynającego (może to być gracz 1 lub gracz 2), 'O' oznacza gracza, który nie rozpoczynał
        # c - moneta czerwona, ż - moneta żółta
        # układam:
        #   0 1 2 3 4 5 6 7 8
        # 0 ż               c
        # 1 c               ż
        # 2 ż               c
        # 3 c               ż
        # 4 ż   O O O O     c
        # 5 c   X X X X X   ż
        who_start = self.player2
        self.logic._whose_turn = who_start
        for i in range(2, 6):
            self.logic.drop_checker(i)
            checker, row, col, win, draw = self.logic.drop_checker(i)
        self.assertEqual(win, False)  # tu nie powinno być wygranej gracza 2
        checker, row, col, win, draw = self.logic.drop_checker(6)  # dodaje monete i zwraca informacje o niej oraz czy jest wygrana/remis
        self.assertEqual(checker, self.player2.checker)  # czy wrzucona moneta należy do drugiego gracza
        self.assertEqual(win, True)  # czy gracz wygrał
        self.assertEqual(who_start.checker, self.logic.who_win().checker)  # czy wygrał gracz 2

    def test_four(self):
        """Test sprawdzający czy ułożenie poziomej lini przez jednego z graczy zwróci informację o wygranej."""

        # 'X' oznacza gracza rozpoczynającego (może to być gracz 1 lub gracz 2), 'O' oznacza gracza, który nie rozpoczynał
        # c - moneta czerwona, ż - moneta żółta
        # układam:
        #   0 1 2 3 4 5 6 7 8
        # 0 ż               c
        # 1 c         X     ż
        # 2 ż     O X X     c
        # 3 c   O X O O     ż
        # 4 ż   X X X X     c
        # 5 c X O O O O     ż
        who_start = self.logic.whose_turn
        self.logic.drop_checker(1) # X (5, 1)
        self.logic.drop_checker(2) # O (5, 2)
        self.logic.drop_checker(2) # X (4, 2)
        self.logic.drop_checker(4) # O (5, 4)
        self.logic.drop_checker(4) # X (4, 4)
        self.logic.drop_checker(4) # O (3, 4)
        self.logic.drop_checker(4) # X (2, 4)
        self.logic.drop_checker(3) # O (5, 3)
        self.logic.drop_checker(3) # X (4, 3)
        self.logic.drop_checker(5) # O (5, 5)
        self.logic.drop_checker(3) # X (3, 3)
        self.logic.drop_checker(5) # O (4, 5)
        self.logic.drop_checker(5) # X (3, 5)
        checker, row, col, win, draw = self.logic.drop_checker(5) # O (2, 5)
        self.assertNotEqual(checker, who_start.checker)  # teraz wrzucona moneta nie jest gracza zaczynającego
        self.assertEqual(self.logic.who_win(), None)  # nikt jeszcze nie wygrał
        checker, row, col, win, draw = self.logic.drop_checker(5) # X (1, 5)
        self.assertEqual(checker, who_start.checker)  # teraz wrzucana moneta jest gracza, który zaczynał
        self.assertEqual(win, True)  # jest informacja, że ktoś wygrał
        self.assertEqual(who_start.checker, self.logic.who_win().checker)  # wygrał gracz, który zaczynał 
        
        
    def test_five(self):
        """Test sprawdzający czy po zapełnieniu planszy i braku zwycięzcy będzie informacja o remisie."""

        # 'X' oznacza gracza rozpoczynającego (może to być gracz 1 lub gracz 2), 'O' oznacza gracza, który nie rozpoczynał
        # c - moneta czerwona, ż - moneta żółta
        # układam:
        #   0 1 2 3 4 5 6 7 8
        # 0 ż O X O X O X O c
        # 1 c O X O X O X X ż
        # 2 ż O X O X O X O c
        # 3 c X O X O X O X ż
        # 4 ż X O X O X O O c
        # 5 c X O X O X O X ż
        for _ in range(3):
            self.logic.drop_checker(1)
            self.logic.drop_checker(2)
            self.logic.drop_checker(3)
            self.logic.drop_checker(4)
            self.logic.drop_checker(5)
            self.logic.drop_checker(6)
        self.logic.drop_checker(7)
        for _ in range(3):
            self.logic.drop_checker(1)
            self.logic.drop_checker(2)
            self.logic.drop_checker(3)
            self.logic.drop_checker(4)
            self.logic.drop_checker(5)
            self.logic.drop_checker(6)
        for _ in range(4):
            checker, row, col, win, draw = self.logic.drop_checker(7)
        self.assertEqual(draw, False)  # nie ma jeszcze remisu
        self.assertEqual(win, False)  # nie ma zwycięzcy
        checker, row, col, win, draw = self.logic.drop_checker(7) # wrzucanie ostatniej monety (plansza po wrzuceniu jest pełna)
        self.assertEqual(draw, True)  # jest remis
        self.assertEqual(win, False)  # nie ma zwycięzcy

    def test_six(self):
        """Test prawdzający czy po ułożeniu linii dłuższej niż 5 przez pierwszego gracza (monety czerwone) da informację o wygranej"""

        # c - moneta czerwona, ż - moneta żółta
        # układam:
        #   0 1 2 3 4 5 6 7 8
        # 0 ż               c
        # 1 c               ż
        # 2 ż               c
        # 3 c               ż
        # 4 ż ż ż ż   ż ż ż c
        # 5 c c c c   c c c ż  <- w następnym ruchu gracz 1 wrzuca monetę do kolumny o indeksie 4
        
        who_start = self.player1
        self.logic._whose_turn = who_start
        for i in range(1, 4):
            self.logic.drop_checker(i) # X
            self.logic.drop_checker(i) # O
        for i in range(7, 4, -1):
            self.logic.drop_checker(i) # X
            self.logic.drop_checker(i) # O
        
        self.assertEqual(self.logic.who_win(), None)  # jeszcze nikt nie wygrał
        checker, row, col, win, draw = self.logic.drop_checker(4)  # wrzucana jest moneta gracza 1 do kolumny o indeksie 4
        self.assertEqual(self.logic.who_win().checker, who_start.checker) # gracz zaczynający wygrał

    def test_seven(self):
        """Test sprawdzający czy wrzucenie monety do zapełnionej kolumny zwróci wyjątek."""
        
        for _ in range(6):
            self.logic.drop_checker(5)  # zapełniam kolumnę o indeksie 5 (szósta kolumna on lewej)
        self.assertRaises(ColumnIsFullException, self.logic.drop_checker, 5)  # próba wrzucenia monety do pełnej kolumny, oczekiwany wyjątek
        self.assertRaises(ColumnIsFullException, self.logic.drop_checker, 8)  # próba wrzucenia monety do pełnej kolumny, która była wypełniana automatycznie na poczatku gry
                                                                              # w wersji graficznej nie przycisków nad kolumnami wypełnionymi automatycznie

if __name__ == "__main__":
    unittest.main()
        
