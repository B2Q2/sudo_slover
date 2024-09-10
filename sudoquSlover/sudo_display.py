#/sudo_display

from GUI.unit import *
from GUI.packing import *
from special_type.positon import *
from sudo_structure import Board
from GUI.signs import *

CONSOLE_UNIT.SET_SIZE(1,1)
cmd_unit = CONSOLE_UNIT()

def display_sudo(sudo_board:Board):
    scale_w = 2
    scale_h = 1
    grid_width = 11 * scale_w
    grid_hight = 11 * scale_h
    cmd_unit.RESIZE_GRID(grid_width,grid_hight)

    fields: List[Packing] = []
    position: List[Position] = []

    for region in sudo_board.MAP_OF_REGION:
        value = region.value

        x = region.position.x
        y = region.position.y
        pos = Position(x + x//3, y + y//3)
        pos.scale(scale_w, scale_h)

        pf = Packing.field(value)
        
        fields.append(pf)
        position.append(pos)

    # add all object to GRID
    for pf, pos in zip(fields, position):
        cmd_unit.ADD_PACKING_TO_GRID(pf, pos)

    # draw grid
    packing_line_horizontal = Packing.line_horizontal(grid_width, SIGNS.HEAVY_HORIZONTAL)
    packing_line_vertical = Packing.line_vertical(grid_hight, SIGNS.HEAVY_VERTICAL)
    packing_line_horizontal_vertical = Packing.field( SIGNS.HEAVY_VERTICAL_AND_HORIZONTAL)

    # straight
    cmd_unit.ADD_PACKING_TO_GRID(packing_line_vertical, Position(6,0))
    cmd_unit.ADD_PACKING_TO_GRID(packing_line_vertical, Position(14,0))
    cmd_unit.ADD_PACKING_TO_GRID(packing_line_horizontal, Position(0,3))
    cmd_unit.ADD_PACKING_TO_GRID(packing_line_horizontal, Position(0,7))
    # cross
    cmd_unit.ADD_PACKING_TO_GRID(packing_line_horizontal_vertical, Position(6,3))
    cmd_unit.ADD_PACKING_TO_GRID(packing_line_horizontal_vertical, Position(14,3))
    cmd_unit.ADD_PACKING_TO_GRID(packing_line_horizontal_vertical, Position(6,7))
    cmd_unit.ADD_PACKING_TO_GRID(packing_line_horizontal_vertical, Position(14,7))
    # ---
    cmd_unit.UPDATE_BUFFER()
    cmd_unit.UPDATE_SCREEN()

def display_sudo_possiblites(sudo_board:Board):
    scale_w = 2
    scale_h = 1
    grid_width = 35 * scale_w
    grid_hight = 35 * scale_h
    cmd_unit.RESIZE_GRID(grid_width,  grid_hight)

    cubes: list[Packing] = []
    position: list[Position] = []

    for region in sudo_board.MAP_OF_REGION:
        possib = region.get_possibilites()

        # make small space between numbers
        cb: Packing =  Packing.cube(3, possib)
        for cb_pos in cb.shape:
            cb_pos.scale(scale_w, scale_h)

        # set cube position on GRID
        x = region.position.x
        y = region.position.y
        pos = Position(x , y)
        pos.scale(4*scale_w, 4*scale_h) 

        cubes.append(cb)   
        position.append(pos)
    
    # add all object to GRID
    for pf, pos in zip(cubes, position):
        cmd_unit.ADD_PACKING_TO_GRID(pf, pos)

    # draw grid
    packing_line_heavy_horizontal = Packing.line_horizontal(grid_width, SIGNS.HEAVY_HORIZONTAL)
    packing_line_heavy_vertical = Packing.line_vertical(grid_hight, SIGNS.HEAVY_VERTICAL)
    packing_line_heavy_horizontal_vertical = Packing.field( SIGNS.HEAVY_VERTICAL_AND_HORIZONTAL)
    packing_line_light_horizontal = Packing.line_horizontal(grid_width, SIGNS.LIGHT_HORIZONTAL)
    packing_line_light_vertical = Packing.line_vertical(grid_hight, SIGNS.LIGHT_VERTICAL)
    packing_line_light_horizontal_vertical = Packing.field( SIGNS.LIGHT_VERTICAL_AND_HORIZONTAL)

    #light
    for x in range(3*scale_w,grid_width, 4*scale_w):
        cmd_unit.ADD_PACKING_TO_GRID(packing_line_light_vertical, Position(x,0))
    for y in range(3*scale_h,grid_hight, 4*scale_h):
        cmd_unit.ADD_PACKING_TO_GRID(packing_line_light_horizontal, Position(0,y))
    for x in range(3*scale_w,grid_width, 4*scale_w):
        for y in range(3*scale_h,grid_hight, 4*scale_h):
            cmd_unit.ADD_PACKING_TO_GRID(packing_line_light_horizontal_vertical, Position(x,y) )
    
    # #heavy
    for x in range(11*scale_w,grid_width, 12*scale_w):
        cmd_unit.ADD_PACKING_TO_GRID(packing_line_heavy_vertical, Position(x,0))
    for y in range(11*scale_h,grid_hight, 12*scale_h):
        cmd_unit.ADD_PACKING_TO_GRID(packing_line_heavy_horizontal, Position(0,y))
    for x in range(11*scale_w,grid_width, 12*scale_w):
        for y in range(11*scale_h,grid_hight, 12*scale_h):
            cmd_unit.ADD_PACKING_TO_GRID(packing_line_heavy_horizontal_vertical, Position(x,y) )

    # ---
    cmd_unit.UPDATE_BUFFER()
    cmd_unit.UPDATE_SCREEN()
