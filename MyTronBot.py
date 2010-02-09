#!/usr/bin/python
"""
Tron bot for http://csclub.uwaterloo.ca/contest

Built by Brendan Fahy.

"""

import tron

import random

Found = False
Attack = False
hasAttacked = False
DEBUG = False
onuboard1 = False
onuboard2 = False

turn = 0

mytail = []

u1 = ['###############', '#             #', '#           2 #', '#             #', '#   ###########', '#   #          ', '#   #          ', '#   #          ', '#   #          ', '#   #          ', '#   ###########', '#             #', '#           1 #', '#             #', '###############']
u2 = ['###############', '#             #', '#           1 #', '#             #', '#   ###########', '#   #          ', '#   #          ', '#   #          ', '#   #          ', '#   #          ', '#   ###########', '#             #', '#           2 #', '#             #', '###############']

if DEBUG:
    log = open('log.txt','w')
    log.write("logfile\n")
    log.close()

size = 0

mystartquad = 0
theirstartquad = 0
attackvect = None
endwith = None

def which_move(board):
    global Found
    global mytail
    global turn
    global size
    global Attack
    global mystartquad
    global theirstartquad
    global onuboard1, onuboard2
    global hasAttacked
    
    if DEBUG:
        log = open('log.txt','a')
#        log.write("board :" + repr(board.board) + "\n")

    # board.printboard()

    if turn == 0:
        mystartquad = board.quadrent(board.me())
        theirstartquad = board.quadrent(board.them())
        if board.board == u1:
            onuboard1 = True
            return tron.NORTH

        if board.board == u2:
            onuboard2 = True
            return tron.SOUTH
        if DEBUG:
            log.write("I start in q:" + repr(board.quadrent(board.me())) + "\n")
            log.write("They start in q:" + repr(board.quadrent(board.them())) + "\n")



        

    turn += 1

    # board.p("Should be false till attacked")
    # board.p(hasAttacked)
    
        
    mytail.append(board.me())

    # sys.stderr.write('turn' + turn + '\n')
    # board.p(board.me())


    def isWall(x):
        """ My tail is not a wall, when looking for a wall, ignore my tail"""
        if x in mytail:
            return False
        return not board.passable(x)

    if Found is False:                  # Have we found a wall?
        adj = board.adjacent(board.me())
        if True in map(isWall,adj):
            if DEBUG:
                log.write("FOUND WALL \n")
                # log.write(repr(adj) + "\n")
                # log.write(repr(map(isWall,adj)) + "\n")
            Found = True

    allmoves = board.moves()

        
    if len(allmoves) == 1:         # If only one move take it
        # if DEBUG:
        #      log.write("one move")
        if DEBUG:
            log.close()
        return allmoves[0]

    goodmoves = board.avoidends()
    sm = board.safemoves(goodmoves)
    # board.printboard()

    if len(goodmoves) == 1:         # If only one move take it
        if DEBUG:
            log.close()
        return goodmoves[0]
    if len(sm) == 1:         # If only one move take it
        if DEBUG:
            log.close()
        return sm[0]


    # if we have save moves only search them, otherwise search all moves
    if sm:
        trymoves = sm
    elif goodmoves:
        trymoves = goodmoves
    else:
        trymoves = allmoves

    if board.nopath():
        bestmove = spacesave(board,trymoves)
        if bestmove:
            return bestmove

                
    if not hasAttacked and onuboard1 and board.me()[0] < 7 :
        # board.p(hasAttacked)
        beginuattack(board)
        # board.p("uboard1\n")

            
    if not hasAttacked and onuboard2 and board.me()[0] > 7 :
        # board.p(hasAttacked)
        beginuattack(board)
        # board.p("uboard2\n")


    closetocenter = abs(board.me()[0] - board.height/2) + abs(board.me()[1] - board.width/2) < 4
    if closetocenter and not hasAttacked:
        if DEBUG:
            log.write("close to center?" + repr(abs(board.me()[0] - board.width/2) + abs(board.me()[1] - board.height/2) )+ "\n")
        Attack = True

    if Attack:
        beginattack(board)
        if DEBUG:
            log.write("begining attack with " + repr(attackvect) + "\n")
        Attack = False

    if attackvect:
        if attackvect in trymoves:
            bestmove = attackvect
        else:
            endattack()
            if DEBUG:
                log.write("ending attack\n")
            if endwith in trymoves:
                bestmove = endwith
            else:
                bestmove =  minmaxdistance(board,trymoves)
    else:
        bestmove =  minmaxdistance(board,trymoves)

    if DEBUG:
        log.close()
    return bestmove

    # if all fails random
    return random.choice(trymoves)

def endattack():
    global attackvect
    global endwith
    attackvect = None
    endwith == None

def beginuattack(board):
    global attackvect
    global endwith
    global hasAttacked
    hasAttacked = True

    attackvect = tron.WEST
    if onuboard1:
        endwith = tron.SOUTH
    if onuboard2:
        endwith = tron.NORTH
    

def beginattack(board):
    """
    |1|2|
    |3|4|
    """

    global attackvect
    global endwith
    global hasAttacked
    hasAttacked = True

    theirquad = board.quadrent(board.them())
    # log.write("them" + repr(board.them()) +"\n")
    # log.write("quads" + repr(mystartquad) + "," + repr(theirquad) +"\n")

    if mystartquad == 1:
        if board.quadrent(board.them()) == 2:
            attackvect = tron.EAST
            endwith = tron.SOUTH
        if board.quadrent(board.them()) == 3:
            attackvect = tron.SOUTH
            endwith = tron.EAST
    if mystartquad == 2:
        if board.quadrent(board.them()) == 1:
            attackvect = tron.WEST
            endwith = tron.SOUTH
        if board.quadrent(board.them()) == 4:
            attackvect = tron.SOUTH
            endwith = tron.WEST
    if mystartquad == 3:
        if board.quadrent(board.them()) == 1:
            attackvect = tron.NORTH
            endwith = tron.EAST
        if board.quadrent(board.them()) == 4:
            attackvect = tron.EAST
            endwith = tron.NORTH
    if mystartquad == 4:
        if board.quadrent(board.them()) == 2:
            attackvect = tron.NORTH
            endwith = tron.WEST
        if board.quadrent(board.them()) == 3:
            attackvect = tron.WEST
            endwith = tron.NORTH

    
def minmaxdistance(board,trymoves):

    def isWall(x):
        """ My tail is not a wall, when looking for a wall, ignore my tail"""
        if x in mytail:
            return False
        return not board.passable(x)

    
    distances = {}

    # compute distances to a wall in all directions
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

    # Move to where we have the most space
    for move in trymoves:
        if distances[move] == distances[bestmove]:
             bestmove = random.choice([bestmove,move])
             continue
        if Found:
            if distances[move] > distances[bestmove]:
                bestmove = move
        else:
            if distances[move] < distances[bestmove]:
                bestmove = move

    return bestmove
    
        
def spacesave(board,trymoves):

    decision = None
    # ORDER = list(tron.DIRECTIONS)
    
    for dir in trymoves:


        # where we will end up if we move this way
        dest = board.rel(dir)

        # destination is passable?
        if not board.passable(dest):
            continue

        # positions adjacent to the destination
        adj = board.adjacent(dest)

        # if any wall adjacent to the destination
        if any(board[pos] == tron.WALL for pos in adj):
            decision = dir
            break

    return decision

        
# Just always laeve this part
for board in tron.Board.generate():
    tron.move(which_move(board))
