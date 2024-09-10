#!user/bin/python

from sudo_structure import *
from sudo_display import *
from sudo_detector import *

layout_pociag_na_wypasie = [
    0, 0, 0,    0, 7, 0,    0, 5, 0,
    0, 0, 9,    4, 0, 0,    0, 0, 0,
    0, 0, 0,    0, 2, 0,    1, 0, 0,

    0, 0, 0,    0, 0, 0,    0, 0, 6,
    1, 0, 7,    0, 8, 0,    0, 0, 0,
    4, 3, 0,    9, 0, 0,    2, 0, 0,

    0, 6, 0,    1, 0, 0,    9, 8, 2,
    3, 0, 8,    0, 4, 6,    0, 0, 0,
    0, 0, 0,    0, 0, 0,    0, 0, 0,
]

layout_hard_thinking = [
    7, 0, 0,    0, 0, 0,    0, 0, 0,
    0, 3, 0,    2, 0, 0,    0, 0, 0,
    0, 0, 5,    7, 0, 0,    0, 1, 8,
    
    0, 0, 4,    0, 0, 5,    9, 0, 0,
    0, 0, 0,    0, 0, 1,    4, 8, 0,
    0, 6, 0,    8, 3, 0,    5, 0, 1,

    0, 0, 3,    0, 0, 0,    0, 0, 7,
    0, 0, 2,    0, 0, 0,    0, 0, 5,
    0, 0, 0,    5, 0, 0,    8, 6, 0,

]

layout_last_in_book = [
    7, 8, 0,    0, 2, 0,    0, 0, 0,
    0, 0, 6,    0, 0, 0,    0, 0, 0,
    0, 0, 0,    6, 0, 1,    0, 0, 4,

    4, 6, 0,    0, 0, 5,    0, 0, 2,
    0, 3, 0,    1, 0, 8,    0, 0, 0,
    0, 0, 0,    0, 7, 0,    0, 1, 0,

    0, 0, 0,    0, 1, 7,    5, 0, 0,
    0, 2, 0,    3, 0, 0,    1, 8, 0,
    0, 0, 0,    0, 0, 0,    0, 3, 0,
]


sudo_board = Board(layout_last_in_book)

print( "\n >> SUDOKU was initiated! " )
display_sudo(sudo_board)

detec = Detector(sudo_board)

stack = 0
MAX_stack = 9
while not( detec.sudo_slove() ):

    detec.lineholider()
    detec.ultimateone()
    detec.pairinline()
    detec.scan()

    stack += 1
    if stack >= MAX_stack:
        print("\n >> OVER STACK!")
        display_sudo(sudo_board)
        display_sudo_possiblites(sudo_board)
        break
    else:
        print("*", stack)
else:
    print( "\n >> SUDOKU was successfully solved! " )
    display_sudo(sudo_board)
