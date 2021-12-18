class Player():
    """Klasa opisująca gracza"""
    def __init__(self, name):
        self._name = name
        # self._my_turn = None

    @property
    def name(self):
        return self._name

    # @property
    # def my_turn(self):
    #     return self._my_turn
    
