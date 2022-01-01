class Player():
    """Klasa opisująca gracza
    
    Atrybuty:
        _name (str): nazwa gracza
        _checker (Checker): obiekt reprezentujący monetę

    Gettery:
        name: pobieranie nazwy gracza
        checker: pobieranie monety, której używa gracz
    """
    
    def __init__(self, name, checker):
        self._name = name
        self._checker = checker

    @property
    def name(self):
        return self._name

    @property
    def checker(self):
        return self._checker
    
