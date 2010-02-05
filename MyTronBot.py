#!/usr/bin/python

"""Template for your tron bot"""

import tron

import random

def which_move(board):

    # fill in your code here. it must return one of the following directions:
    #   tron.NORTH, tron.EAST, tron.SOUTH, tron.WEST

    # For now, choose a legal move randomly.
    # Note that board.moves will produce [NORTH] if there are no
    # legal moves available.


    if len(board.moves()) == 1:         # If only one move take it

        return board.moves()[0]

    distances = {}
    
    for direction in board.moves():
        tile = board.rel(direction)
        distances[direction] = 0
        while board.passable(tile):
            distances[direction] = distances[direction] + 1
            tile = board.rel(direction,tile)
            
    mymoves = board.moves()

    bestmove = board.moves()[0]

    for move in board.moves():
        if distances[move] > distances[bestmove]:
            bestmove = move

    return bestmove

    # if all fails random
    return tron.SOUTH
    #return random.choice(board.moves())


# you do not need to modify this part
for board in tron.Board.generate():
    tron.move(which_move(board))
