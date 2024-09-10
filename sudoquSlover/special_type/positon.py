#/position
from typing import Tuple, Callable

class Position():
    def __init__(self, x:int, y:int) -> None:
        assert Position.Check_is_positive_number(x), "Err.. Must by positive number!"
        assert Position.Check_is_positive_number(y), "Err.. Must by positive number!"
        self.x:int = x
        self.y:int = y
        
        self.creator_key: Callable[ [], Tuple[int, int] ] = lambda: (self.x, self.y)
        self.key = self.creator_key()

    def scale(self, scale_x, scale_y) -> None:
        assert Position.Check_is_scale(scale_x), "Err.. Scale must be positive value!"
        assert Position.Check_is_scale(scale_y), "Err.. Scale must be positive value!"
        self.x = int(self.x * scale_x)
        self.y = int(self.y * scale_y)

    def add(self, position:"Position") -> None:
        self.x = self.x + position.x
        self.y = self.y + position.y
        self.key = self.creator_key()
    
    def __add__(self, position:"Position")->"Position":
        x = self.x + position.x
        y = self.y + position.y
        return Position(x,y)


    def __str__(self) -> str:
        return str(self.key)

    @staticmethod
    def Key(x, y) -> Tuple[int, int]:
        assert Position.Check_is_positive_number(x), "Err.. Must by positive number!"
        assert Position.Check_is_positive_number(y), "Err.. Must by positive number!"
        return (x, y)

    @staticmethod
    def Check_is_positive_number(value:int) -> bool:
        return  isinstance(value, int) and (value >= 0)
    
    @staticmethod
    def Check_is_scale(value:int|float) -> bool:
        return (isinstance(value, int) or isinstance(value, float)) and (value > 0)
    
    @staticmethod
    def Check_is_position(value: any) -> bool:
        if isinstance(value, tuple):
            if len(value) == 2:
                if all( Position.Check_is_positive_number(check_object) for check_object in value):
                    return True
        return False

if __name__ == "__main__":
    p1 = Position(1,3)
    p2 = Position(3,4)
    p1.add(p2)