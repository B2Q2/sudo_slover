from .size import *
from special_type.positon import *
from .signs import *
from typing import List, Tuple


class Packing():
    def __init__(self, size: Size, values: List[int]) -> None:
        assert isinstance(size, Size), "Err.. Valid size type!"
        assert isinstance(values, list) or isinstance(values, str), "Err.. Valid values type!"

        self.size:Size = size
        self.shape: List[Position] = sum([ [ Position(row, column) for row in range(self.size.width)] for column in range(self.size.hight)], [])

        if len(values) == 1:
            values = [ values[0] for _ in range(self.size.data_storage())]
        else:
            assert all( isinstance(v, int) or isinstance(v, str) for v in values ), "Err.. Valid  type of list data!"
            assert len(values) >= self.size.data_storage(), "Err.. Insufficient amount of data! "
        self.values = values

        # for column in range(self.size.hight):
        #     for row in range(self.size.width):
                # index = row + column * self.size.width
                # data = values[ index  ]
                # sign = str( data )
                # self.shape[column][row] = sign

    # def __str__(self) -> str:
    #     return str(self.shape)

    @staticmethod
    def cube(lenght: int, values: List[int]) -> None:
        size = Size(lenght, lenght)
        return Packing(size, values)
    
    @staticmethod
    def line_horizontal(lenght: int, values: List[int]) -> None:
        size = Size(lenght, 1)
        return Packing(size, values)
    
    @staticmethod
    def line_vertical(lenght: int, values: List[int]) -> None:
        size = Size(1, lenght)
        return Packing(size, values)
    
    @staticmethod
    def field( value: int) -> None:
        size = Size(1, 1)
        values = [value]
        return Packing(size, values)
    