# Tutaj będą umieszczane klasy wyjątków dziedziczące po klasie Exception

class ConnectFourException(Exception):
    """Klasa bazowa dla wszystkich wyjątków w grze 'Cztery w rzędzie'."""
    pass


class ColumnIsFullException(ConnectFourException):
    """Klasa wyjątku oznajmiająca, że do tej kolumny nie można już wrzucać monet."""
    pass


class DrawException(ConnectFourException):
    """Wyjątek wywoływany, gdy gra zakończy się remisem."""
    pass


class SetOfRulesNotDefinedException(ConnectFourException):
    """Wyjątek wywoływany, gdy podczas inicjalizacji obiektu ConnectFourWindow podamy nieprawidłowe parametry."""
    pass


class CheckerCannotBeRemovedException(ConnectFourException):
    """Wyjątek wywoływany, gdy moneta nie może zostać usunięta (tryb PopOut)."""
    pass