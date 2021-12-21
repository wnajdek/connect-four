class Player():
    """Klasa opisująca gracza"""
    def __init__(self, name, checker):
        self._name = name
        self._checker = checker

    @property
    def name(self):
        return self._name

    @property
    def checker(self):
        return self._checker
    
