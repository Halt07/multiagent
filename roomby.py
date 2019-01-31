# Roomby (MultiAgent Systems program 2)
# by Bryan Christensen A01694831

import random, pygame, sys
from pygame.locals import *

FPS = 10
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

#Max Battery
MAXCHARGE = 200

HEAD = 0 # syntactic sugar: index of the worm's head
class Roomba:
    def __init__(self, x, y):
        self.x = x;
        self.y = y;
        self.charger = {'x': x, 'y':y}
        self.battery = MAXCHARGE
        self.charged = True
        self.direction = DOWN
        self.lastmove = 0
        self.lastposition = {'x': self.x, 'y': self.y}
        self.avoidcounter = 0

    def clean(self, room):
        if isinstance(room[self.x][self.y], Dirt):
            room[self.x][self.y].clean()

    def sensor(self, room):
        if(self.charged):
            dirty = False
            if(self.x > 0) and (self.y > 0):
                if not (room[self.x-1][self.y-1] is None and room[self.x][self.y-1] is None and room[self.x-1][self.y] is None):
                    self.__stuck()
            if(self.x < CELLWIDTH-1) and (self.y < CELLHEIGHT-1):
                if not (room[self.x+1][self.y] is None and room[self.x][self.y+1] is None and room[self.x+1][self.y+1] is None):
                    self.__stuck()
            if(self.x < CELLWIDTH-1) and (self.y > 0):
                if not (room[self.x+1][self.y] is None and room[self.x][self.y-1] is None and room[self.x+1][self.y-1] is None):
                    self.__stuck()
            if(self.x > 0) and (self.y < CELLHEIGHT-1):
                if not (room[self.x-1][self.y] is None and room[self.x][self.y+1] is None and room[self.x-1][self.y+1] is None):
                    self.__stuck()
    
    def __leftright(self):
        if(random.randint(0,1) == 0):
            return LEFT
        return RIGHT

    def __updown(self):
        if(random.randint(0,1) == 0):
            return UP
        return DOWN

    def __randdir(self):
        if(random.randint(0,1) == 0):
            return self.__leftright()
        return self.__updown()

    def __stuck(self):
        if(self.direction == UP):
            self.direction = self.__randdir()
        elif(self.direction == RIGHT):
            self.direction = self.__randdir()
        elif(self.direction == DOWN):
            self.direction = self.__randdir()
        elif(self.direction == LEFT):
            self.direction = self.__randdir()
        if(self.avoidcounter > 7):
            self.avoidcounter = 0

    def __avoidOb(self):
        if(self.direction == UP):
            self.direction = self.__leftright()
        elif(self.direction == RIGHT):
            self.direction = self.__updown()
        elif(self.direction == DOWN):
            self.direction = self.__leftright()
        elif(self.direction == LEFT):
            self.direction = self.__updown()
        self.avoidcounter += 1
        print(self.avoidcounter)
        if(self.avoidcounter > 3):
            self.__stuck()
        
    def __turn(self):
        if(self.charged):
            if(self.direction == UP):
                self.direction = self.__leftright()
            elif(self.direction == DOWN):
                self.direction = LEFT
            elif(self.direction == LEFT):
                self.direction = self.__updown()
            elif(self.direction == RIGHT):
                self.direction = DOWN
            else:
                self.direction = self.__randdir()
        else:
            if(self.x > self.charger['x']):
                self.direction = LEFT
            elif(self.y > self.charger['y']):
                self.direction = UP
            elif(self.x < self.charger['x']):
                self.direction = RIGHT
            elif(self.y < self.charger['y']):
                self.direction = DOWN
            else:
                self.direction = ''
                print(self.battery)

    def move(self, room, thismove):
        if(thismove != self.lastmove):
            if self.direction == UP and self.y-1 > -1 and room[self.x][self.y-1] is None:
                room[self.x][self.y] = None
                self.y -= 1
                room[self.x][self.y] = self
            elif self.direction == DOWN and self.y+1 < CELLHEIGHT and room[self.x][self.y+1] is None:
                room[self.x][self.y] = None
                self.y += 1
                room[self.x][self.y] = self
            elif self.direction == LEFT and self.x-1 > -1 and room[self.x-1][self.y] is None:
                room[self.x][self.y] = None
                self.x -= 1
                room[self.x][self.y] = self
            elif self.direction == RIGHT and self.x+1 < CELLWIDTH and room[self.x+1][self.y] is None:
                room[self.x][self.y] = None
                self.x += 1
                room[self.x][self.y] = self
            else:
                self.__turn()
            self.lastmove = thismove
            if(self.charged):
                self.battery -= 1
                if(self.battery < 1):
                    self.charged = False
            elif((self.x+1 == self.charger['x'] or self.x-1 == self.charger['x'] or self.x == self.charger['x']) and (self.y+1 == self.charger['y'] or self.y-1 == self.charger['y'] or self.y == self.charger['y'])):
                self.battery += 2
                if(self.battery >= MAXCHARGE):
                    self.charged = True
                    self.direction = self.__randdir()
            else:
                self.__turn()
                if(self.lastposition['x'] == self.x and self.lastposition['y'] == self.y):
                    self.__avoidOb()
                self.lastposition = {'x': self.x, 'y': self.y}

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
    def __init__(self, x, y, amount):
        self.x = x
        self.y = y
        self.dirt = amount

    def clean(self):
        if(self.dirt == HEAVY):
            self.dirt = MID
        elif(self.dirt == MID):
            self.dirt = LIGHT
        else:
            self = None

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
    dirt = []
    stones = []
    numApples = 3
    goldenApplePresent = False
    goldenApple = getRandomLocation()
    goldTimer = 1

    for i in range(CELLWIDTH):
        stones.append([])
        dirt.append([])
        for j in range(CELLHEIGHT):
            stones[i].append(None)
            dirt[i].append(None)

    # create 7 obstacles with random start points
    for i in range(20):
        start = getRandomLocation()
        while(not stones[start['x']][start['y']] is None):
            start = getRandomLocation()
        stones[start['x']][start['y']] = Obstacle(start['x'], start['y'], False)

    # create 2 moving obstacles with random start points
    for i in range(2):
        start = getRandomLocation()
        while(not stones[start['x']][start['y']] is None):
            start = getRandomLocation()
        stones[start['x']][start['y']] = Obstacle(start['x'], start['y'], True)

    # create 2 heavy dirt piles
    for i in range(2):
        start = getRandomLocation()
        while(not stones[start['x']][start['y']] is None) and (not dirt[start['x']][start['y']] is None):
            start = getRandomLocation()
        dirt[start['x']][start['y']] = Dirt(start['x'], start['y'], HEAVY)

    # create 4 mid dirt piles
    for i in range(4):
        start = getRandomLocation()
        while(not stones[start['x']][start['y']] is None) and (not dirt[start['x']][start['y']] is None):
            start = getRandomLocation()
        dirt[start['x']][start['y']] = Dirt(start['x'], start['y'], MID)

    # create 6 light dirt piles
    for i in range(6):
        start = getRandomLocation()
        while(not stones[start['x']][start['y']] is None) and (not dirt[start['x']][start['y']] is None):
            start = getRandomLocation()
        dirt[start['x']][start['y']] = Dirt(start['x'], start['y'], LIGHT)


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
                if isinstance(obj, Roomba):
                    obj.sensor(dirt)
                    obj.clean(dirt)
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_SPACE):
                    pass
                elif event.key == K_ESCAPE:
                    terminate()
        
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawObstacles(dirt)
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

def drawDirt(coord):
    if(coord.dirt == HEAVY):
        color = GOLD
    elif(coord.dirt == MID):
        color = RATTLELIGHT
    elif(coord.dirt == LIGHT):
        color = RATTLEDARK
    x = coord.x * CELLSIZE
    y = coord.y * CELLSIZE
    spec = pygame.Rect(x+1, y+1, CELLSIZE/5, CELLSIZE/5)
    pygame.draw.rect(DISPLAYSURF, color, spec)
    spec = pygame.Rect(x+4, y+8, CELLSIZE/4, CELLSIZE/4)
    pygame.draw.rect(DISPLAYSURF, color, spec)
    spec = pygame.Rect(x+12, y+3, CELLSIZE/5, CELLSIZE/5)
    pygame.draw.rect(DISPLAYSURF, color, spec)

def drawObstacles(stoneCoords):
    for row in stoneCoords:
        for coord in row:
            if isinstance(coord, Obstacle):
                drawObj(coord,RED)
            elif isinstance(coord, Roomba):
                drawObj(coord,GREEN)
            elif isinstance(coord, Dirt):
                drawDirt(coord)

def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()
