# Roomby (MultiAgent Systems program 2)
# by Bryan Christensen A01694831

import random, pygame, sys
from pygame.locals import *

FPS = 5
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

#Direction Constants
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

#Dirt Amount Constants
HEAVY = 3
MID = 2
LIGHT = 1

HEAD = 0 # syntactic sugar: index of the worm's head
class Roomba:
    def __init__(self, x, y):
        self.x = x;
        self.y = y;
        self.charger = {'x': x, 'y':y}
        self.battery = 50
        self.charged = True
        self.direction = DOWN
        self.lastmove = 0

    def findRoomSize(self, room):
        pass

    def __sensor(self, room):
        pass
    
    def __turn(self):
        if(self.charged):
            if(self.direction == UP):
                self.direction = RIGHT
            elif(self.direction == DOWN):
                self.direction = LEFT
            elif(self.direction == LEFT):
                self.direction = UP
            elif(self.direction == RIGHT):
                self.direction = DOWN
        else:
            if(self.x > self.charger['x']):
                print(self.x, self.charger['x'])
                self.direction = LEFT
            elif(self.x < self.charger['x']):
                print(self.x, self.charger['x'])
                self.direction = RIGHT
            elif(self.y > self.charger['y']):
                print(self.y, self.charger['y'])
                self.direction = UP
            elif(self.y < self.charger['y']):
                print(self.y, self.charger['y'])
                self.direction = DOWN
            else:
                print(self.battery)
                self.direction = ''

    def move(self, room, thismove):
        if(thismove != self.lastmove):
            if self.direction == UP and self.y-1 > -1 and room[self.x][self.y-1] is None:
                room[self.x][self.y] = None
                self.x = self.x
                self.y = self.y - 1
                room[self.x][self.y] = self
            elif self.direction == DOWN and self.y+1 < CELLHEIGHT and room[self.x][self.y+1] is None:
                room[self.x][self.y] = None
                self.x = self.x
                self.y = self.y + 1
                room[self.x][self.y] = self
            elif self.direction == LEFT and self.x-1 > -1 and room[self.x-1][self.y] is None:
                room[self.x][self.y] = None
                self.x = self.x - 1
                self.y = self.y
                room[self.x][self.y] = self
            elif self.direction == RIGHT and self.x+1 < CELLWIDTH and room[self.x+1][self.y] is None:
                room[self.x][self.y] = None
                self.x = self.x + 1
                self.y = self.y
                room[self.x][self.y] = self
            else:
                self.__turn()
            self.lastmove = thismove
            if(self.charged):
                self.battery -= 1
                if(self.battery == 0):
                    self.charged = False
            elif(self.x == self.charger['x'] and self.y == self.charger['y']):
                self.battery += 1
                if(self.battery == 50):
                    self.charged = True
            else:
                self.__turn()

class Obstacle:
    def __init__(self, x, y, move):
        self.x = x
        self.y = y
        self.movable = move
        self.direction = UP
        self.lastmove = 0

    def __changeDirection(self):
        num = random.randint(0,8) #If none of below, continue in same direction as previous
        if(num == 0):
            self.direction = UP #look up
        elif(num == 1):
            self.direction = DOWN #look down
        elif(num == 2):
            self.direction = LEFT #look left
        elif(num == 3):
            self.direction = RIGHT #look right
        elif(num <= 5):
            self.direction = '' #don't move

    def move(self, room, thismove):
        if(self.movable and thismove != self.lastmove):
            if self.direction == UP and self.y-1 > -1 and room[self.x][self.y-1] is None:
                room[self.x][self.y] = None
                self.x = self.x
                self.y = self.y - 1
                room[self.x][self.y] = self
            elif self.direction == DOWN and self.y+1 < CELLHEIGHT and room[self.x][self.y+1] is None:
                room[self.x][self.y] = None
                self.x = self.x 
                self.y = self.y + 1
                room[self.x][self.y] = self
            elif self.direction == LEFT and self.x-1 > -1 and room[self.x-1][self.y] is None:
                room[self.x][self.y] = None
                self.x = self.x - 1
                self.y = self.y
                room[self.x][self.y] = self
            elif self.direction == RIGHT and self.x+1 < CELLWIDTH and room[self.x+1][self.y] is None:
                room[self.x][self.y] = None
                self.x = self.x + 1
                self.y = self.y
                room[self.x][self.y] = self
            self.__changeDirection()
            self.lastmove = thismove

class Dirt:
    def __init__(self, amount):
        pass

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Roomby')

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

    for i in range(CELLWIDTH):
        stones.append([])
        for j in range(CELLHEIGHT):
            stones[i].append(None)

    # create 7 obstacles with random start points
    for i in range(20):
        startx = random.randint(5, CELLWIDTH - 6)
        starty = random.randint(5, CELLHEIGHT - 6)
        while(not stones[startx][starty] is None):
            startx = random.randint(5, CELLWIDTH - 6)
            starty = random.randint(5, CELLHEIGHT - 6)
        stones[startx][starty] = Obstacle(startx, starty, False)

    # create 2 moving obstacles with random start points
    for i in range(2):
        startx = random.randint(5, CELLWIDTH - 6)
        starty = random.randint(5, CELLHEIGHT - 6)
        while(not stones[startx][starty] is None):
            startx = random.randint(5, CELLWIDTH - 6)
            starty = random.randint(5, CELLHEIGHT - 6)
        stones[startx][starty] = Obstacle(startx, starty, True)

    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    while(not stones[startx][starty] is None):
        startx = random.randint(5, CELLWIDTH - 6)
        starty = random.randint(5, CELLHEIGHT - 6)
    stones[startx][starty] = Roomba(startx, starty)

    while True: # main game loop
        thismove = random.randint(1,10000)
        for row in stones:
            for obj in row:
                if(not obj is None):
                    obj.move(stones, thismove)
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
        if goldenApplePresent:
            drawGoldApple(goldenApple)
        drawObstacles(stones)
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
    titleSurf1 = titleFont.render('Roomby!', True, RATTLEDARK, DARKGRAY)
    titleSurf2 = titleFont.render('Roomby!', True, RATTLELIGHT)

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


def drawObj(obj, color):
    if(not obj is None):
        x = obj.x * CELLSIZE
        y = obj.y * CELLSIZE
        obRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, color, obRect)

def drawGoldApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, GOLD, appleRect)

def drawObstacles(stoneCoords):
    for row in stoneCoords:
        for coord in row:
            if isinstance(coord, Obstacle):
                drawObj(coord,RED)
            elif isinstance(coord, Roomba):
                drawObj(coord,GREEN)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()
