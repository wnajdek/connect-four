import unittest
from  logic.normal_rules import *

class TestConnectFour(unittest.TestCase):

    def setUp(self):
        self.player1 = Player("Gracz 1", Checker.RED)
        self.player2 = Player("Gracz 2", Checker.YELLOW)
        self.normal = NormalRules(6, 7, self.player1, self.player2)

    def test_one(self):
        """Test sprawdza czy po wykonaniu dwóch ruchów przez każdego z graczy spowoduje,
        że monety spadają na dół pola gry lub zatrzymują się na już wrzuconym żetonie."""
        self.normal.