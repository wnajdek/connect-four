import unittest
from logic.exceptions import ColumnIsFullException, CheckerCannotBeRemovedException
from logic.rules_impl.pop_out import PopOut
from logic.objects.checker import Checker
from logic.objects.player import Player

class TestPopOut(unittest.TestCase):

    def setUp(self):
        self.player1 = Player("Gracz 1", Checker.RED)
        self.player2 = Player("Gracz 2", Checker.YELLOW)
        self.logic = PopOut(6, 7, self.player1, self.player2)

    def test_one(self):
        """Test sprawdza czy po wykonaniu dwóch ruchów przez każdego z graczy spowoduje,
        że monety spadają na dół pola gry lub zatrzymują się na już wrzuconym żetonie."""
        # 'X' oznacza gracza rozpoczynającego (może to być gracz 1 lub gracz 2), 'O' oznacza gracza, który nie rozpoczynał
        # układam:
        #   0 1 2 3 4 5 6
        # 0
        # 1
        # 2 O      
        # 3 X   
        # 4 O  
        # 5 X 
        checker = self.logic.whose_turn.checker
        for _ in range(4):
            self.logic.drop_checker(0)
        
        board2 = [[None for i in range(7)] for j in range(6)]
        board2[5][0] = checker
        board2[4][0] = Checker.YELLOW if checker != Checker.YELLOW else Checker.RED
        board2[3][0] = checker
        board2[2][0] = Checker.YELLOW if checker != Checker.YELLOW else Checker.RED
        self.assertListEqual(self.logic.board, board2)
            
    def test_two(self):
        """Test sprawdzający czy ułożenie pionowej linii przez pierwszego gracza zwróci informację o wygranej."""
        # 'X' oznacza gracza rozpoczynającego (może to być gracz 1 lub gracz 2), 'O' oznacza gracza, który nie rozpoczynał
        # układam:
        #   0 1 2 3 4 5 6
        # 0
        # 1
        # 2   X     
        # 3   X O
        # 4   X O 
        # 5   X O
        who_start = self.player1
        self.logic._whose_turn = who_start
        for _ in range(3):
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
        # układam:
        #   0 1 2 3 4 5 6
        # 0
        # 1
        # 2        
        # 3    
        # 4 O O O  
        # 5 X X X X
        who_start = self.player2
        self.logic._whose_turn = who_start
        for i in range(3):
            self.logic.drop_checker(i)
            checker, row, col, win, draw = self.logic.drop_checker(i)
        self.assertEqual(win, False)  # tu nie powinno być wygranej gracza 2
        checker, row, col, win, draw = self.logic.drop_checker(3)  # dodaje monete i zwraca informacje o niej oraz czy jest wygrana/remis
        self.assertEqual(checker, self.player2.checker)  # czy wrzucona moneta należy do drugiego gracza
        self.assertEqual(win, True)  # czy gracz wygrał
        self.assertEqual(who_start.checker, self.logic.who_win().checker)  # czy wygrał gracz 2

    def test_four(self):
        """Test sprawdzający czy ułożenie linii po skosie przez jednego z graczy zwróci informację o wygranej."""

        # 'X' oznacza gracza rozpoczynającego (może to być gracz 1 lub gracz 2), 'O' oznacza gracza, który nie rozpoczynał
        # układam:
        #   0 1 2 3 4 5 6
        # 0
        # 1
        # 2       X
        # 3   O X O
        # 4   X X X
        # 5 X O O O
        who_start = self.logic.whose_turn
        self.logic.drop_checker(0) # X (5, 0)
        self.logic.drop_checker(1) # O (5, 1)
        self.logic.drop_checker(1) # X (4, 1)
        self.logic.drop_checker(3) # O (5, 3)
        self.logic.drop_checker(3) # X (4, 3)
        self.logic.drop_checker(3) # O (3, 3)
        self.logic.drop_checker(3) # X (2, 3)
        self.logic.drop_checker(2) # O (5, 2)
        self.logic.drop_checker(2) # X (4, 2)
        checker, row, col, win, draw = self.logic.drop_checker(1) # O (3, 1)
        self.assertNotEqual(checker, who_start.checker)  # teraz wrzucona moneta nie jest gracza zaczynającego
        self.assertEqual(self.logic.who_win(), None)  # nikt jeszcze nie wygrał
        checker, row, col, win, draw = self.logic.drop_checker(2) # X (3, 2)
        self.assertEqual(checker, who_start.checker)  # teraz wrzucana moneta jest gracza, który zaczynał
        self.assertEqual(win, True)  # jest informacja, że ktoś wygrał
        self.assertEqual(who_start.checker, self.logic.who_win().checker)  # wygrał gracz, który zaczynał 
        
        
    def test_five(self):
        """Test sprawdzający czy po zapełnieniu planszy pojawi się informacja o remisie.
        W tym trybie nie ma remisu, ponieważ gracze mogą wyciągać swoje monety z dolnego rzędu.
        Remis zawsze będzie False."""

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
            self.logic.drop_checker(0)
            self.logic.drop_checker(1)
            self.logic.drop_checker(2)
            self.logic.drop_checker(3)
            self.logic.drop_checker(4)
            self.logic.drop_checker(5)
        self.logic.drop_checker(6)
        for _ in range(3):
            self.logic.drop_checker(0)
            self.logic.drop_checker(1)
            self.logic.drop_checker(2)
            self.logic.drop_checker(3)
            self.logic.drop_checker(4)
            self.logic.drop_checker(5)
        for _ in range(4):
            checker, row, col, win, draw = self.logic.drop_checker(6)
        self.assertEqual(draw, False)  # nie ma jeszcze remisu
        self.assertEqual(win, False)  # nie ma zwycięzcy
        checker, row, col, win, draw = self.logic.drop_checker(6) # wrzucanie ostatniej monety (plansza po wrzuceniu jest pełna)
        self.assertEqual(draw, False)  # nie ma remisu
        self.assertEqual(win, False)  # nie ma zwycięzcy

    def test_six(self):
        """Test sprawdzający czy po ułożeniu linii dłuższej niż 4 przez jednego z graczy da informację o wygranej"""

        # 'X' oznacza gracza rozpoczynającego (może to być gracz 1 lub gracz 2), 'O' oznacza gracza, który nie rozpoczynał
        # układam:
        #   0 1 2 3 4 5 6
        # 0 
        # 1 
        # 2 
        # 3
        # 4 O O O   O O O
        # 5 X X X   X X X   <- w następnym ruchu gracz, który zaczynał wrzuca monetę do pustej kolumny
        
        who_start = self.logic.whose_turn
        for i in range(3):
            self.logic.drop_checker(i) # X
            self.logic.drop_checker(i) # O
        for i in range(6, 3, -1):
            self.logic.drop_checker(i) # X
            self.logic.drop_checker(i) # O
        
        self.assertEqual(self.logic.who_win(), None)  # jeszcze nikt nie wygrał
        self.logic.drop_checker(3)
        self.assertEqual(self.logic.who_win().checker, who_start.checker) # gracz zaczynający wygrał

    def test_seven(self):
        """Test sprawdzający czy wrzucenie monety do zapełnionej kolumny zwróci wyjątek."""
        # 'X' oznacza gracza rozpoczynającego (może to być gracz 1 lub gracz 2), 'O' oznacza gracza, który nie rozpoczynał
        # układam: (jest to stan przed próbą wrzucenia monety do pełnej kolumny)
        #   0 1 2 3 4 5 6
        # 0           O
        # 1           X
        # 2           O
        # 3           X
        # 4           O  
        # 5           X
        for _ in range(6):
            self.logic.drop_checker(5)  # zapełniam kolumnę o indeksie 5 (szósta kolumna on lewej)
        self.assertRaises(ColumnIsFullException, self.logic.drop_checker, 5)  # próba wrzucenia monety do pełnej kolumny, oczekiwany wyjątek

    def test_remove(self):
        """Test sprawdzający możliwośc usuwania monet.
        Jeżeli moneta nie należy do danego gracza to wyrzucony zostaje wyjątek.
        Jeżeli w danej kolumnie nie ma żadnej monety to rownież wywołany zostanie wyjątek."""
        # 'X' oznacza gracza rozpoczynającego (może to być gracz 1 lub gracz 2), 'O' oznacza gracza, który nie rozpoczynał
        # układam:
        #   0 1 2 3 4 5 6
        # 0           
        # 1          
        # 2           
        # 3   X       
        # 4   O       
        # 5   X       
        # następują teraz nieudane próby usunięcia monety i w końcu dodanie monety przez gracza
        #   0 1 2 3 4 5 6
        # 0           
        # 1          
        # 2   O       
        # 3   X       
        # 4   O       
        # 5   X
        # teraz gracz oznaczony jako X wyciąga monetę
        # stan po wyjęciu:
        #   0 1 2 3 4 5 6
        # 0           
        # 1          
        # 2          
        # 3   O       
        # 4   X       
        # 5   O
        # wrzucam monetę, aby sprawdzić w tej kolumnie dalej można dodawać poprawnie monety:
        #   0 1 2 3 4 5 6
        # 0           
        # 1          
        # 2   O      
        # 3   O       
        # 4   X       
        # 5   O
        who_start = self.player1
        self.logic._whose_turn = who_start
        self.logic.drop_checker(1) 
        self.logic.drop_checker(1)
        self.logic.drop_checker(1)
        self.assertRaises(CheckerCannotBeRemovedException, self.logic.remove_checker, 1)  # moneta, którą gracz chce wyjąć nie należy do tego gracza
        self.assertRaises(CheckerCannotBeRemovedException, self.logic.remove_checker, 2)  # w tej kolumnie nie ma żadnej monety
        self.logic.drop_checker(3)
        self.logic.remove_checker(1)  # poprawne wyjęcie monety
        self.assertEqual(self.logic.board[5][1], Checker.YELLOW)  # na pozycji (5, 1) powinna być żółta moneta
        self.assertEqual(self.logic.board[4][1], Checker.RED)  # na pozycji (4, 1) powinna być czerwona moneta
        self.assertEqual(self.logic.board[3][1], None)  # na pozycji (3, 1) nie powinno być żadnej monety
        self.logic.drop_checker(1)
        self.assertEqual(self.logic.board[3][1], Checker.YELLOW)  # na pozycji (3, 1) powinna być teraz żółta moneta, sprawdzam czy w miejsce usuniętych monet można wstawiać monety

    
if __name__ == "__main__":
    unittest.main()
        
