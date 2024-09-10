from types import NoneType
from typing import Dict, Tuple, cast
from itertools import product

"""
Structure

Sudogu - board
Section
Field

"""

class Field:
    my_instance:list["Field"] = []

    POSIBILITES:list[int] = [
            1, 2, 3, 
            4, 5, 6, 
            7, 8, 9,
        ]

    def __init__(self, sector:"Sector", sudo_position:Tuple[int, int] = (0,0) ) -> None:
        assert len(sudo_position) == 2 and isinstance(sudo_position, tuple), "Valid sudo-position!"
        
        self.sector:Sector = sector
        self.sudo_position:Tuple[int] = sudo_position
        self.value:int = 0
        self.posibilites:list[int] = Field.POSIBILITES

        Field.my_instance.append(self)

    def set_value(self, new_val):
        if self.posibilites.count(new_val):
            self.value = new_val
            self.posibilites:list = [new_val]

    def get_map_of_posibility(self) -> str:
        mpp: str = ""

        for k in range(1,10):
            if self.posibilites.count(k) == 1:
                mpp = mpp + str(k) + ' '
            else:
                mpp = mpp + '. '
            if (k)%3 == 0:
                mpp = mpp + '\n'

        return mpp
    
    def get_map_of_posibility_ASLIST(self) -> list[str]:
        mppal: list[str] = []

        for k in range(1,10):
            if self.posibilites.count(k) == 1:
                mppal.append( str(k) )
            else:
                mppal.append('.')

        return mppal

class Sector:
    USE_SUDO_POSITION: list[Tuple[int, int]] = []

    MAIN_SQUARE:list[tuple] = [
            (0, 0), (0, 1), (0, 2),
            (1, 0), (1, 1), (1, 2),
            (2, 0), (2, 1), (2, 2),
        ]
    
    def __init__(self, position:tuple[2] = (0,0), shape:list[tuple] = None ) -> None:
        
        # set shape
        if isinstance(shape, NoneType):
            shape = Sector.MAIN_SQUARE
        else: # check shape format stuction
            assert isinstance(shape, list), f"Valid shape type <{type(shape)}> must be <list>!"
            lsh = len(shape)
            assert lsh  == 9, f"Valid shape pattern lenght! {lsh}"
            for tpp in shape:
                assert isinstance(tpp, tuple) == True, f"Valid shape pattern position type <{type(tpp)}> must by <tuple>!"
                ltp = len(tpp)
                assert ltp == 2, f"Valid shape pattern position lenght {ltp} must by 2!"
                assert 0 <= tpp[0] <= 8, f"Valid pattern x-position value! overflow! {tpp[0]}"
                assert 0 <= tpp[1] <= 8, f"Valid pattern y-position value! overflow! {tpp[1]}"

        self.shape: list[tuple] = Sector.generate_shape( shape , position  )
        
        self.position = position
        self.fields: list[Field] = [Field(self, sudo_position) for sudo_position in self.shape]
        

    def generate_shape( pattern_shape:list[tuple], position:tuple[2] ):
        section_shape:list[tuple] = []
        for i in range(9):
            tpp = ( pattern_shape[i][0] + position[0], pattern_shape[i][1] + position[1], )
            assert Sector.USE_SUDO_POSITION.count(tpp) == 0, f"Valid sudo-position, duplication! {tpp} {position}"
            Sector.USE_SUDO_POSITION.append(tpp)
            section_shape.append(tpp)
        else:
            return section_shape

class Board:
    SUDO_POSITION: list[Tuple[int, int]] = list( product( [j for j in range(9)] , repeat=2)) 
    SUDO_FIELD_MAP: Dict[Tuple[int, int], int] = {key: None for key in SUDO_POSITION}

    # C0 Controls and Basic Latin
    CHAR_NEXT: str = "\u000A"
    CHAR_SPACE: str = '\u0020' 
    # box drawings
    CHAR_HEAVY_HORIZONTAL: str = '\u2501'
    CHAR_HEAVY_VERTICAL: str = '\u2503'
    CHAR_HEAVY_VERTICAL_AND_HORIZONTAL:str =  '\u254B'
    CHAR_LIGHT_HORIZONTAL:str = '\u2500'
    CHAR_LIGHT_VERTICAL:str = '\u2502'

    MIDDLE_LINE:str = CHAR_HEAVY_VERTICAL + CHAR_SPACE
    BOTTOM_LINE:str = CHAR_NEXT + (CHAR_HEAVY_HORIZONTAL*6) + CHAR_HEAVY_VERTICAL_AND_HORIZONTAL \
                                + (CHAR_HEAVY_HORIZONTAL*7) + CHAR_HEAVY_VERTICAL_AND_HORIZONTAL + (CHAR_HEAVY_HORIZONTAL*6)
    
    BASE_TEST_SETPIEC:list[int] = [
        5, 0, 0,    0, 8, 0,   9, 0, 0, 
        0, 7, 8,    0, 9, 0,   1, 0, 3, 
        3, 0, 0,    7, 4, 0,   0, 5, 0, 
        
        4, 0, 0,    0, 2, 0,   3, 0, 5, 
        0, 5, 0,    0, 0, 0,   0, 0, 0, 
        0, 0, 6,    0, 1, 8,   7, 2, 4, 

        0, 4, 0,    3, 0, 1,   5, 0, 2, 
        0, 6, 0,    0, 0, 2,   0, 9, 0, 
        2, 0, 0,    0, 6, 0,   8, 0, 0, 
    ]

    SUDO_SETPIECE_MAP: Dict[Tuple[int, int], int] = dict()

    def __init__(self, setpiece:list[int] = None) -> None:

        if isinstance(setpiece, NoneType):
            setpiece = Board.BASE_TEST_SETPIEC
        assert isinstance(setpiece, list), "Valid setpiece!"
        assert all( isinstance(sudo_number, int) for sudo_number in setpiece ), "Valid type of setpiece value!"
        assert len(setpiece) == 81, "Setpiece has valid lenght! {0}".format( len(setpiece) )

        self.Sectors:list[Sector] = [
            Sector( (0, 0) ),
            Sector( (3, 0) ),
            Sector( (6, 0) ),
            Sector( (0, 3) ),
            Sector( (3, 3) ),
            Sector( (6, 3) ),
            Sector( (0, 6) ),
            Sector( (3, 6) ),
            Sector( (6, 6) ),
        ]

        # creat conection between sudo_position and sudo_setpiece
        for (sudo_position, sudo_setpiece) in zip (Board.SUDO_POSITION, setpiece):
            Board.SUDO_SETPIECE_MAP[sudo_position] =  sudo_setpiece

        # use conection to set vales of fields
        for field in Field.my_instance:
            field.set_value( Board.SUDO_SETPIECE_MAP[field.sudo_position] )

    def display(self):
        def fprintf(special_char):
            print( special_char, end="")

        sudo_map_transfer = Board.SUDO_FIELD_MAP.copy()
        
        for field in Field.my_instance:
            sudo_map_transfer[field.sudo_position] = field.value

        for key, sudo_val in sudo_map_transfer.items():
            fprintf( sudo_val )
            fprintf( Board.CHAR_SPACE ) 
            if (key[1] == 2 or key[1] == 5):
                fprintf( Board.MIDDLE_LINE )
            if key[1] == 8:
                if (key[0] == 2 or key[0] == 5 ):
                    fprintf( Board.BOTTOM_LINE )
                fprintf( Board.CHAR_NEXT )
    
    def display_posibility(self):
        def fprintf(special_char, FLAG_side:bool = False, char_side:str = ' ' ):
            if FLAG_side:
                special_char = f"{char_side}{special_char}{char_side}"
            print( special_char, end="")

        size = 35 # 9*4+2

        grid = [ [-1 for _ in range(size)] for _ in range(size)]

        for field in Field.my_instance:
            mov = 4
            mappl = field.get_map_of_posibility_ASLIST()
            for iy in range(3):
                for ix in range(3):
                    grid[ field.sudo_position[0]*mov + ix ][ field.sudo_position[1]*mov + iy ] = mappl[iy*3 + ix]


        for y in range(size):
            for x in range(size):
                if (x+1)%12 == 0 or (y+1)%12 == 0:
                    grid[x][y] = 0

        for y in range(size):
            for x in range(size):
                if grid[x][y] == 0:
                    if (y == 0 or y == size-1):
                        grid[x][y] = Board.CHAR_HEAVY_VERTICAL
                    elif (x == 0 or x == size-1):
                        grid[x][y] = Board.CHAR_HEAVY_HORIZONTAL
                    else:
                        if grid[x][y+1] == 0 and grid[x+1][y] == 0 :
                            grid[x][y] = Board.CHAR_HEAVY_VERTICAL_AND_HORIZONTAL
                        elif grid[x][y+1] == 0:
                            grid[x][y] = Board.CHAR_HEAVY_VERTICAL
                        elif grid[x+1][y] == 0 :
                            grid[x][y] = Board.CHAR_HEAVY_HORIZONTAL
                if grid[x][y] == -1:
                    if (y == 0 or y == size-1):
                        grid[x][y] = Board.CHAR_LIGHT_VERTICAL
                    elif (x == 0 or x == size-1):
                        grid[x][y] = Board.CHAR_LIGHT_HORIZONTAL
                    else:
                        if set([ grid[x][y-1], grid[x][y+1] ]) & set([ -1, Board.CHAR_LIGHT_VERTICAL ]) and set([ grid[x-1][y], grid[x+1][y] ]) & set([ -1, Board.CHAR_LIGHT_HORIZONTAL ]):
                            grid[x][y] = '+'
                        elif set([ grid[x][y-1], grid[x][y+1] ]) & set([ -1, Board.CHAR_LIGHT_VERTICAL ]):
                            grid[x][y] = Board.CHAR_LIGHT_VERTICAL
                        elif set([ grid[x-1][y], grid[x+1][y] ]) & set([ -1, Board.CHAR_LIGHT_HORIZONTAL ]):
                            grid[x][y] = Board.CHAR_LIGHT_HORIZONTAL
                        

        for y in range(size):
            for x in range(size): 
                if grid[x][y] == Board.CHAR_HEAVY_HORIZONTAL or grid[x][y] == Board.CHAR_HEAVY_VERTICAL_AND_HORIZONTAL:
                    fprintf( grid[x][y], True, Board.CHAR_HEAVY_HORIZONTAL)
                elif grid[x][y] == Board.CHAR_LIGHT_HORIZONTAL:
                    fprintf( grid[x][y], True, Board.CHAR_LIGHT_HORIZONTAL)
                else:
                    fprintf( grid[x][y], True )
            fprintf( Board.CHAR_NEXT )

'''
    ff = Field( )
    ff.set_value(1)
    msg = ff.get_map_of_posibility()
    print(msg)

'''

if __name__ == "__main__":
    b = Board()
    b.display_posibility()