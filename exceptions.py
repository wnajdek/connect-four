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