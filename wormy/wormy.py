# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

# Edited by Bryan Christensen A01694831

import random, pygame, sys
from pygame.locals import *

FPS = 2
WINDOWWIDTH = 780
WINDOWHEIGHT = 540
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
GRAY      = ( 80,  80,  80)
DARKGRAY  = ( 40,  40,  40)
RATTLEDARK= (139,  73,  28)
RATTLELIGHT=(255, 205, 110)
GOLD      = (255, 215,   0)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Squirmy')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    # initialize lists to contain the game "objects"
    wormCoords = []
    direction = []
    apple = []
    stones = []
    numApples = 3
    goldenApplePresent = False
    goldenApple = getRandomLocation()
    goldTimer = 1

    # create 2 worms with random start points
    for i in range(2):
        startx = random.randint(5, CELLWIDTH - 6)
        starty = random.randint(5, CELLHEIGHT - 6)
        wormCoords.append([{'x': startx,     'y': starty},
                          {'x': startx - 1, 'y': starty},
                          {'x': startx - 2, 'y': starty}])
        direction.append(RIGHT)
    

    # Start with apples in random places.
    for i in range(numApples):
        apple.append(getRandomLocation())

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                # worm 0 movement
                if (event.key == K_LEFT) and direction[0] != RIGHT:
                    direction[0] = LEFT
                elif (event.key == K_RIGHT) and direction[0] != LEFT:
                    direction[0] = RIGHT
                elif (event.key == K_UP) and direction[0] != DOWN:
                    direction[0] = UP
                elif (event.key == K_DOWN) and direction[0] != UP:
                    direction[0] = DOWN
                # worm 1 movement
                elif (event.key == K_a) and direction[1] != RIGHT:
                    direction[1] = LEFT
                elif (event.key == K_d) and direction[1] != LEFT:
                    direction[1] = RIGHT
                elif (event.key == K_w) and direction[1] != DOWN:
                    direction[1] = UP
                elif (event.key == K_s) and direction[1] != UP:
                    direction[1] = DOWN
                # move both worms
                elif (event.key == K_KP4):
                    if direction[0] != RIGHT:
                        direction[0] = LEFT
                    if direction[1] != RIGHT:
                        direction[1] = LEFT
                elif (event.key == K_KP6):
                    if direction[0] != LEFT:
                        direction[0] = RIGHT
                    if direction[1] != LEFT:
                        direction[1] = RIGHT
                elif (event.key == K_KP8):
                    if direction[0] != DOWN:
                        direction[0] = UP
                    if direction[1] != DOWN:
                        direction[1] = UP
                elif (event.key == K_KP2):
                    if direction[0] != UP:
                        direction[0] = DOWN
                    if direction[1] != UP:
                        direction[1] = DOWN
                # shed skin
                elif (event.key == K_RSHIFT):
                    for segment in wormCoords[0]:
                        stones.append(segment)
                elif (event.key == K_e):
                    for segment in wormCoords[1]:
                        stones.append(segment)
                elif event.key == K_ESCAPE:
                    terminate()
                    

        
        for i in range(len(wormCoords)): # 2 worms
            
            # move the worm by adding a segment in the direction it is moving
            if direction[i] == UP:
                newHead = {'x': wormCoords[i][HEAD]['x'], 'y': wormCoords[i][HEAD]['y'] - 1}
            elif direction[i] == DOWN:
                newHead = {'x': wormCoords[i][HEAD]['x'], 'y': wormCoords[i][HEAD]['y'] + 1}
            elif direction[i] == LEFT:
                newHead = {'x': wormCoords[i][HEAD]['x'] - 1, 'y': wormCoords[i][HEAD]['y']}
            elif direction[i] == RIGHT:
                newHead = {'x': wormCoords[i][HEAD]['x'] + 1, 'y': wormCoords[i][HEAD]['y']}
            wormCoords[i].insert(0, newHead)

            # check if the worm has hit itself, other worm, stone obstacles, or the edge
            # check wall
            if wormCoords[i][HEAD]['x'] == -1 or wormCoords[i][HEAD]['x'] == CELLWIDTH or wormCoords[i][HEAD]['y'] == -1 or wormCoords[i][HEAD]['y'] == CELLHEIGHT:
                return # game over
            # check self
            for wormBody in wormCoords[i][1:]:
                if wormBody == wormCoords[i][HEAD]:
                    return # game over
            # check other worm
            for wormBody in wormCoords[i][1:]:
                if wormBody == wormCoords[(i+1)%2][HEAD]:
                    return # game over
            # check for stone skins
            if wormCoords[i][HEAD] in stones:
                    return # game over


            # check if worm has eaten an apple
            eat = False
            for a in range(numApples):
                if wormCoords[i][HEAD] == apple[a]:
                    eat = True # don't remove worm's tail segment
                    newLocation = getRandomLocation()
                    # if new location is already occupied by a stone wall or apple
                    # find an unoccupied location
                    while newLocation in stones or newLocation in apple:
                        newLocation = getRandomLocation()
                    apple[a] = newLocation  # set a new apple somewhere
            if goldenApplePresent:
                if wormCoords[i][HEAD] == goldenApple:
                    eat = True
                    goldenApplePresent = False
                    goldTimer = 1
                    # temp speed up and increase in score
                    if direction[i] == UP:
                        newHead = {'x': wormCoords[i][HEAD]['x'], 'y': wormCoords[i][HEAD]['y'] - 1}
                    elif direction[i] == DOWN:
                        newHead = {'x': wormCoords[i][HEAD]['x'], 'y': wormCoords[i][HEAD]['y'] + 1}
                    elif direction[i] == LEFT:
                        newHead = {'x': wormCoords[i][HEAD]['x'] - 1, 'y': wormCoords[i][HEAD]['y']}
                    elif direction[i] == RIGHT:
                        newHead = {'x': wormCoords[i][HEAD]['x'] + 1, 'y': wormCoords[i][HEAD]['y']}
                    wormCoords[i].insert(0, newHead)
            if not eat:
                del wormCoords[i][-1] # remove worm's tail segment

        goldTimer += 1
        if goldTimer % 100 == 0:
            if not goldenApplePresent:
                newLocation = getRandomLocation()
                # if new location is already occupied by a stone wall or apple
                # find an unoccupied location
                while newLocation in stones or newLocation in apple:
                    newLocation = getRandomLocation()
                goldenApple = newLocation  # set a golden apple somewhere
            goldenApplePresent = not goldenApplePresent
        
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        for i in range(len(wormCoords)): # draw all worms
            drawWorm(i, wormCoords[i])
            drawScore(i, len(wormCoords[i]) - 3)
        for i in range(numApples):
            drawApple(apple[i])
        if goldenApplePresent:
            drawGoldApple(goldenApple)
        drawStones(stones)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Squirmy!', True, RATTLEDARK, DARKGRAY)
    titleSurf2 = titleFont.render('Squirmy!', True, RATTLELIGHT)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

def drawScore(worm, score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    if worm == 0:
        scoreRect.topleft = (60, 10)
    else:
        scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(worm, wormCoords):
    if worm % 2 == 0:
        body = RATTLEDARK
        diamond = RATTLELIGHT
    else:
        body = RATTLELIGHT
        diamond = RATTLEDARK
        
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, body, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, diamond, wormInnerSegmentRect)


def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)

def drawGoldApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, GOLD, appleRect)

def drawStones(stoneCoords):
    for coord in stoneCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        stone = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGRAY, stone)
        inStone = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GRAY, inStone)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()
