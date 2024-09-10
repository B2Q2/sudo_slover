# /sudo
from typing import List, Dict, Tuple
from itertools import product
from special_type.positon import Position
from GUI.signs import SIGNS
# class Position:
#     def __init__(self) -> None:
#         self.x:int = 0
#         self.y:int = 0
#         self.get:Tuple[int, int] = self.retrun_position()
    
#     def set_position(self, new_pos: Tuple[int, int]) -> None:
#         assert isinstance(new_pos, tuple), "Err.. New-pos have valid type!"
#         assert all( isinstance(check_objet, int) for check_objet in new_pos), "Err.. Valid New-pos Position value!"

#         self.x = new_pos[0]
#         self.y = new_pos[1]
    
#     def retrun_position(self) -> Tuple[int, int]:
#         return (self.x, self.y)

class Region():
    '''
        Class use to define Position of one sudo-region, the smallest squer in sudo-board
        Definion needs where region egsist.
        Further changes will be declarate value or possibility  of a such result
    '''
    EMPTY = SIGNS.DOT

    BASE_POSIBILITES = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def __init__(self, x, y) -> None:
        self.position:Position = Position(x, y)
        self.value:int = 0
        self.possibilites:List[int] = Region.BASE_POSIBILITES.copy()

        # parent adnotation
        self.sector:Sector = None
        self.line_vertical:Line_vertical = None
        self.line_horizontal:Line_horizontal = None

    def set_value(self, new_value:int) -> None:
        assert new_value == 0 or new_value in Region.BASE_POSIBILITES, "Err.. Incorrect value for Region!"
  
        self.value = new_value
        if self.value != 0:
            self.possibilites = [new_value]

    def remove_possibilites(self, rem_psb:int ) -> None:
        if rem_psb in self.possibilites and self.possibilites.__len__() != 1:
            self.possibilites.remove(rem_psb)
            
            if self.possibilites.__len__() == 1:
                self.set_value( self.possibilites[0] )
            elif self.possibilites.__len__() == 0:
                raise IndexError("Possibilited have not range!")
        
    
    def get_possibilites(self) ->  List[int|str]:
        ret_possib: List[int|str] = []
        for base_possib in Region.BASE_POSIBILITES:
            if base_possib in self.possibilites:
                ret_possib.append(base_possib)
            else:
                ret_possib.append(Region.EMPTY)
        return ret_possib

# -----------------------------------------------------------------------------

class Line_horizontal():
    def __init__(self, row, map_of_region: List[Region] ) -> None:
        self.row = row
        self.REGION_IN_LINE: list[Region] = []
        self.find_region(map_of_region)

    def find_region(self, map_of_region: List[Region] ):
        for region in map_of_region:
            if region.position.y == self.row:
                region.line_horizontal = self
                self.REGION_IN_LINE.append( region )
    
    def __str__(self) -> str:
        msg = ""
        for region in self.REGION_IN_LINE:
            msg = msg + " " + str(region.value)
        return msg

class Line_vertical():
    def __init__(self, column, map_of_region: List[Region] ) -> None:
        self.column = column
        self.REGION_IN_LINE: list[Region] = []
        self.find_region(map_of_region)

    def find_region(self, map_of_region: List[Region]):
        for region in map_of_region:
            if region.position.x == self.column:
                region.line_vertical = self
                self.REGION_IN_LINE.append( region )
    
    def __str__(self) -> str:
        msg = ""
        for region in self.REGION_IN_LINE:
            msg = msg + " " + str(region.value)
        return msg

class Sector():
    def __init__(self, sector_x:int, sector_y:int, map_of_region: List[Region] ) -> None:
        self.sector_x:int = sector_x
        self.sector_y:int = sector_y
        self.REGION_IN_SECTOR: list[Region] = []
        self.find_region(map_of_region)

    def find_region(self, map_of_region: List[Region]):
        for region in map_of_region:
            sx = self.sector_x*3 
            sy = self.sector_y*3 
            if (sx <= region.position.x <= sx + 2) and (sy <= region.position.y <= sy + 2):
                region.sector = self
                self.REGION_IN_SECTOR.append( region )

    def __str__(self) -> str:
        msg = ""
        for region in self.REGION_IN_SECTOR:
            msg = msg + " " + str(region.value)
        return msg
            
# -----------------------------------------------------------------------------

class Board():
    '''
        The object stores the game map as a dictionary,
        where keys are positions stored as Tuple[int, int]

    '''
    REGION_AMMOUNT: int = 81

    ALL_POSITION_COMBINATION: List[Tuple[int, int]] = []
    for y in range(9):
        for x in range(9):
            ALL_POSITION_COMBINATION.append( (x,y) )
    
    TEST_LAYOUT: list[int] = [
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


    def __init__(self, sudo_layout:list[int]) -> None:

        assert isinstance(sudo_layout, list), "Err.. Valid layout!"
        assert all( isinstance(check_object, int) for check_object in sudo_layout) and len(sudo_layout) == Board.REGION_AMMOUNT, "Err.. Layout have wrong data!"

        self.MAP_OF_REGION: List[Region]  = [ Region(*key) for key in Board.ALL_POSITION_COMBINATION]
        
        # creat main map collecting region
        for region, value in zip( self.MAP_OF_REGION, sudo_layout):
            region.set_value(value)

        # creat smaller object collecting region
        self.MAP_OF_HORIZONTAL_LINE: List[Line_horizontal] = [ Line_horizontal(i, self.MAP_OF_REGION) for i in range(9) ]
        self.MAP_OF_VERTICAL_LINE: List[Line_vertical] = [ Line_vertical(i, self.MAP_OF_REGION) for i in range(9) ]

        self.MAP_OF_SECTOR: List[Sector] = []
        for c in range(3):
            for r in range(3):
                self.MAP_OF_SECTOR.append( Sector(r, c, self.MAP_OF_REGION) )


        