#/GUI
from types import NoneType
from typing import List, Dict, Tuple, Callable, Any
from itertools import product
from .typing_alias import *
from .signs import SIGNS

class GUI_sudo():

    EMPTY = SIGNS.DOT
    NEXT_LINE = SIGNS.ENTER

    BASE_SIZE: Size = (0, 9)

    CREATOR_COMBINATION_OF_DUBLE_PAIR_IN_RANGE: Callable[ [int, int], List[Position]] \
        = lambda RANGE_MINIMUM, RANGE_MAXIMUM: list(product([ _ for _ in range(RANGE_MINIMUM, RANGE_MAXIMUM)], repeat=2))
    
    BASE_TRANSFORMATION: Callable[ [int], int] = lambda pos_V: pos_V

    @staticmethod
    def CREATOR_DISPLAY_GRID( MAP_OF_POSITION: List[Position], MAP_OF_SIGNS: List[str] = None) -> Dict[Position, str]:
        assert isinstance( MAP_OF_POSITION, list), "Err.. Valid data format!"
        assert all( [Is_Position(pos) for pos in MAP_OF_POSITION] ), "Err.. Valid map of position!" 

        def wrapper(ITERATION_OBJECT):
            return {key: value for key, value in ITERATION_OBJECT }
    
        if isinstance(MAP_OF_SIGNS, List):
            if all([ isinstance(sig, str) for sig in MAP_OF_SIGNS ]):
                # zip can return error!
                iter_obj = zip( MAP_OF_POSITION, MAP_OF_SIGNS )
                return wrapper(iter_obj)
            else:
                MAP_OF_SIGNS = [ str(sig) for sig in MAP_OF_SIGNS ]
                 # zip can return error!
                iter_obj = zip( MAP_OF_POSITION, MAP_OF_SIGNS )
                return wrapper(iter_obj)
        else:
            MAP_OF_SIGNS = [ GUI_sudo.EMPTY for _ in range(len(MAP_OF_POSITION)) ]
            iter_obj = zip( MAP_OF_POSITION, MAP_OF_SIGNS )
            return wrapper(iter_obj)
        
    def __init__(self, size: Size = None) -> None:

        self.size =  GUI_sudo.set_size(size)
        position = GUI_sudo.CREATOR_COMBINATION_OF_DUBLE_PAIR_IN_RANGE(*self.size)
        self.DISPLAY_GIRD = GUI_sudo.CREATOR_DISPLAY_GRID( position, None )
        self.position_transformation = GUI_sudo.BASE_TRANSFORMATION

    def run(self):
        pass
    
    # last eye shot
    def scale_DISPLAY_GRID(self, scale:int = 1, direcion: int = 1) -> None:
        def scale_if_Size(scale_size: Size, scale) -> Size: 
            return ( scale_size[0]*scale, scale_size[1]*scale)
    
        def creat_scale_transformation(scale:int, direcion:int) -> callable:
            if direcion >= 1:
                scale_transformation: Callable[ [int], int] = lambda pos_V: pos_V * scale
            elif direcion <= -1:
                scale_transformation: Callable[ [int], int] = lambda pos_V: pos_V % scale
                scale:float = 1/scale
            else:
                scale_transformation: Callable[ [int], int] = GUI_sudo.BASE_TRANSFORMATION
            return scale_transformation, scale
        
        scale_position_transformation, scale = creat_scale_transformation(scale, direcion)

        scale_size = scale_if_Size(self.size, scale)        
        scale_position = GUI_sudo.CREATOR_COMBINATION_OF_DUBLE_PAIR_IN_RANGE(*scale_size)
        scale_DISPLAY_GRID = GUI_sudo.CREATOR_DISPLAY_GRID(scale_position)

        self.DISPLAY_GIRD = scale_DISPLAY_GRID
        self.position_transformation = scale_position_transformation

    def resize_DISPLAY_GRID(self, resize:Size)-> None:
        
        def creat_scale_transformation(resize)->callable:
            sx = resize[0]
            sy = resize[1]
            
            return 1


        self.size = Is_Size_Resize(self.size, resize)
        resize_position = GUI_sudo.CREATOR_COMBINATION_OF_DUBLE_PAIR_IN_RANGE(*self.size)
        self.DISPLAY_GIRD =   GUI_sudo.CREATOR_DISPLAY_GRID(resize_position)
        self.position_transformation = creat_scale_transformation(resize)


    def print_DISPLAY_GRID_on_screen(self):
        min_x, max_x = self.size
        min_y, max_y = self.size

        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                key: Size = (x, y)
                pix = self.DISPLAY_GIRD[key]
                print(pix, end='')
            print(self.NEXT_LINE, end='')  

    @staticmethod
    def set_size(new_size: Any) -> Size:
        if isinstance(new_size, int): new_size: Size = (0, new_size)   
        return new_size if Is_Size(new_size) else GUI_sudo.BASE_SIZE 