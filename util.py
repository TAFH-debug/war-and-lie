class DoubleNumber[T]:
    """
    Class to represent pair of numbers.
    """
    
    x: T
    y: T
    
    def __init__(self, a: T, b: T):
        self.x = a
        self.y = b
    
    @staticmethod
    def from_tuple(tpl: tuple[T, T]) -> "DoubleNumber":
        return DoubleNumber(tpl[0], tpl[1])
    
    def as_tuple(self) -> tuple[T]:
        return self.x, self.y
    
    def __add__(self, other: "DoubleNumber[T]") -> "DoubleNumber[T]":
        return DoubleNumber(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: "DoubleNumber[T]") -> "DoubleNumber[T]":
        return DoubleNumber(self.x - other.x, self.y - other.y)
    