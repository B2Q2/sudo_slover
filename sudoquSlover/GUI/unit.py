#/GUI
from typing import List, Dict, Tuple
from .size import Size
from special_type.positon import Position
from .signs import SIGNS
from .packing import Packing

class CONSOLE_UNIT():
    """
        Before initializacjon SET_SIZE(w,h) must by specified
    """

    EMPTY:str = SIGNS.DOT
    NEXT_LINE:str = SIGNS.ENTER

    CRUSH_SIGN: Tuple[str] = ( SIGNS.SPACE, '0', 0 )

    BASE_SIZE:Size = None
    @staticmethod
    def SET_SIZE(width:int, hight:int) -> Size:
        CONSOLE_UNIT.BASE_SIZE = Size(width, hight)

    @staticmethod
    def CREATOR_gp(SIZE:Size) -> List[ Position ]:
        MAP_OF_POSITION:list = []

        for y in range(SIZE.hight):
            for x in range(SIZE.width):
                MAP_OF_POSITION.append( Position(x,y) )

        return MAP_OF_POSITION

    @staticmethod
    def CREATOR_GRID( MAP_OF_POSITION: List[Position], MAP_OF_SIGNS: List[str] = None) -> Dict[Position, str]:
        assert isinstance( MAP_OF_POSITION, list), "Err.. Valid data format!"
        assert all( [isinstance(position, Position) for position in MAP_OF_POSITION] ), "Err.. Valid map of position!" 

        def wrapper(ITERATION_OBJECT):
            return {key: value for key, value in ITERATION_OBJECT }
    
        if isinstance(MAP_OF_SIGNS, list):
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
            MAP_OF_SIGNS = [ CONSOLE_UNIT.EMPTY for _ in range(len(MAP_OF_POSITION)) ]
            iter_obj = zip( MAP_OF_POSITION, MAP_OF_SIGNS )
            return wrapper(iter_obj)
    
    @staticmethod
    def CREATOR_BUFFER( SIZE:Size ) -> List[List[str]]:
        return [ [ CONSOLE_UNIT.EMPTY for row in range(SIZE.width)] for column in range(SIZE.hight)]
    
    def __init__(self) -> None:
        assert isinstance(CONSOLE_UNIT.BASE_SIZE, Size), "Err.. Not define SIZE"
        self.size = CONSOLE_UNIT.BASE_SIZE

        gp: List[Position] = CONSOLE_UNIT.CREATOR_gp( self.size )
        self.GRID: Dict[Position, str] = CONSOLE_UNIT.CREATOR_GRID( gp, None )
        self.BUFFER: List[List] = CONSOLE_UNIT.CREATOR_BUFFER( self.size )
    
    def ADD_PACKING_TO_GRID(self, packing:Packing, position:Position) -> None:
        shape_position: List[Tuple[int,int]] = []
        shape_values: List[str] = packing.values

        for shp_pos in packing.shape:
            calc_pos = shp_pos + position 
            shape_position.append(calc_pos.key)    

        pack_data_transfer: Dict[Tuple[int,int], str] = dict(zip(shape_position, shape_values))

        for gp in list(self.GRID.keys()):
            try:
                current_sign = self.GRID.get(gp)
                graphic_sign = pack_data_transfer.get( gp.key, current_sign)
                self.GRID[gp] = graphic_sign
            except KeyError:
                pass

    def UPDATE_BUFFER(self) -> None:
        for position, graphic_sign in self.GRID.items():
            row = position.x
            column = position.y
            self.BUFFER[column][row] = graphic_sign
    
    def UPDATE_SCREEN(self) -> None:
        max_row = self.size.width
        max_column = self.size.hight
        print(self.NEXT_LINE, end='')
        for c in range( max_column ):
            for r in range( max_row ):
                graphic_sign = self.BUFFER[c][r]
                
                # zero filter
                if  graphic_sign in self.CRUSH_SIGN: 
                    graphic_sign = self.CRUSH_SIGN[0]

                print(graphic_sign, end='')
            print(self.NEXT_LINE, end='')  

    def RESIZE_GRID(self, width:int, height:int):
        self.SET_SIZE(width, height)
        self.GRID.clear()
        self.BUFFER.clear()
        self.__init__()
