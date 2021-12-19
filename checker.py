class Checker:
    def __init__(self, color):
        self._color = color
    
    @property
    def color(self):
        return self._color