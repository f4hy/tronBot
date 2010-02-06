#!/usr/bin/python

"""Template for your tron bot"""

import tron

import random

Found = False
DEBUG = False

turn = 0

mytail = []


if DEBUG:
    log = open('log.txt','w')
    log.write("logfile\n")
    log.close()

def which_move(board):
    global Found
    global mytail
    global turn

    turn += 1
    
    if DEBUG:
        log = open('log.txt','a')
        log.write("turn :" + repr(turn) + "\n")
        log.write("my tail :" + repr(mytail) + "\n")
        
    mytail.append(board.me())
    
    def safemoves():                    # Return moves they wont move to
        
        safe = []
        
        # danger = board.adjacent(board.them())


        
        for move in board.moves():
            if board.rel(move) not in board.adjacent(board.them()):
                safe.append(move)

        # if DEBUG:
        #     log.write("me" + repr(board.me()) + "\n")
        #     log.write("them" + repr(board.them()) + "\n")
        #     log.write("moves"+ repr(board.moves()) + "\n")
        #     log.write("safemoves"+ repr(safe) + "\n")

        
        return safe

    def isWall(x):
        if x in mytail:
            return False
        return not board.passable(x)


    if Found is False:
        adj = board.adjacent(board.me())
        if True in map(isWall,adj):
            
            if DEBUG:
                log.write("FOUND WALL \n")
                log.write(repr(adj) + "\n")
                log.write(repr(map(isWall,adj)) + "\n")
            Found = True

    if not board.moves():
        # if DEBUG:
        #      log.write("no moves")
        if DEBUG:
            log.close()
        return tron.NORTH
        
    if len(board.moves()) == 1:         # If only one move take it
        # if DEBUG:
        #      log.write("one move")
        if DEBUG:
            log.close()
        return board.moves()[0]

    sm = safemoves()

    if len(sm) == 1:         # If only one move take it
        # if DEBUG:
        #      log.write("one safe move")
        if DEBUG:
            log.close()
        return sm[0]

    # if DEBUG:
    #     log.write("safe moves:\n")
    #     log.write(repr(safemoves()) + "\n")



    if sm:
        trymoves = sm
    else:
        trymoves = board.moves()

    distances = {}
    
    for direction in trymoves:
        tile = board.rel(direction)
        distances[direction] = 0
        if Found:
            test = board.passable
        else:
            test = isWall
        while board.passable(tile):
            distances[direction] = distances[direction] + 1
            tile = board.rel(direction,tile)
            
    mymoves = trymoves

    bestmove = trymoves[0]

    for move in trymoves:
        if Found:
            if distances[move] > distances[bestmove]:
                bestmove = move
        else:
            if distances[move] < distances[bestmove]:
                bestmove = move

    if DEBUG:
        log.close()
    return bestmove

    # if all fails random
    #return tron.SOUTH
    return random.choice(trymoves)


# you do not need to modify this part


        

for board in tron.Board.generate():
    tron.move(which_move(board))
