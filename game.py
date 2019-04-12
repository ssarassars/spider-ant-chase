# Source of base code: https://dr0id.bitbucket.io/legacy/pygame_tutorial00.html
import pygame
from assets.Rectangle import Rectangle
from Ant import Ant
from SpiderGrid import SpiderGrid
from Spider import Spider

sg = SpiderGrid() # grid for game
choice = 4 # BFS: 0, DFS: 1, A*Heuristic1: 2, A*Heuristic2: 3, A*Heuristic: 4

# define a main function
def main():
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("./images/logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Knight Spider")

    # screen size
    # screen = pygame.display.set_mode((0, 0), 500)
    screen = pygame.display.set_mode((1500, 1500))

    running = True

    drawHUD(screen)
    drawGrid(screen)

    numAnts = 1
    numSpiders = 1
    ants = []
    spiders = []

    #initial locations
    for index in range(numAnts):
        ants.append(Ant(20, 20))
        initLoc('ant', ants[index].x, ants[index].y, screen)

    for index in range(numSpiders):
        spiders.append(Spider(sg.rectangleGrid, index+5, index+5))
        initLoc('spider', spiders[index].x, spiders[index].y, screen)

    caught = 0
    lost = 0


    pygame.display.update()

    # main loop
    while running:
        # event handling, gets all event from the event queue
        pygame.display.update()
        startOver = False

        # for event in pygame.event.get():
        pygame.time.delay(50)

        for index in range(numAnts):
            ants[index].updateXY()

            if (ants[index].x < 0 or ants[index].x is 20 or ants[index].y < 0 or ants[index].y is 20):
                print("The spider failed to eat the ant.")
                lost = lost + 1
                drawGrid(screen)
                startOver = True

        for index in range(numSpiders):
            spiders[index].updateXY(choice)

        # check win
        for ant in ants:
            for spider in spiders:
                if (spider.x == ant.x and spider.y == ant.y):
                    print("Spider ate the ant!")
                    caught = caught + 1
                    drawGrid(screen)
                    startOver = True

        if (startOver is True):
            for index in range(numAnts):
                ants[index] = Ant(20, 20)
                initLoc('ant', ants[index].x, ants[index].y, screen)
            for index in range(numSpiders):
                spiders[index] = Spider(sg.rectangleGrid, index+5, index+5)
                initLoc('spider', spiders[index].x, spiders[index].y, screen)
        else:
            changeLoc(spider, spider.x, spider.y, screen)
            changeLoc(ant, ant.x, ant.y, screen)
            pygame.display.update()

        pygame.event.pump()
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            print("The spider caught the ant " + str(caught)+ " times!")
            print("The spider did not catch the ant " + str(lost)+ " times!")
            print("Caught/lost percentage: " + str((caught/(caught+lost))*100)+ " times!")
            print("Total games: " + str(caught+lost))
            running = False


# draws a grid
# https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame
def drawGrid(screen):
    offsetX = 475
    offsetY = 125
    block_size = 30
    x = 50
    y = 50
    width = 20
    height = 20
    for x in range(width):
        for y in range(height):
            rect = pygame.Rect(y * block_size + offsetX, x * block_size + offsetY, block_size, block_size)
            if (y % 2 is 0):
                if (x % 2 is 0):
                    pygame.draw.rect(screen, (129, 185, 191), rect)
                    sg.rectangleGrid[x][y] =  Rectangle(rect, (129, 185, 191), False)
                else:
                    pygame.draw.rect(screen, (229, 255, 255), rect)
                    sg.rectangleGrid[x][y] =  Rectangle(rect, (229, 255, 255), False)
            else:
                if (x % 2 is 0):
                    pygame.draw.rect(screen, (229, 255, 255), rect)
                    sg.rectangleGrid[x][y] =  Rectangle(rect, (229, 255, 255), False)
                else:
                    pygame.draw.rect(screen, (129, 185, 191), rect)
                    sg.rectangleGrid[x][y] =  Rectangle(rect, (129, 185, 191), False)

    pygame.display.update()

# draws HUD
def drawHUD(screen):
    screen.fill((255,255,255))
    pygame.font.init()
    myfont = pygame.font.SysFont('Arial', 30)
    textsurface = myfont.render('! Spooky Spider !', False, (0, 0, 0))
    screen.blit(textsurface, (700, 40))

# change location of spider or ant
def initLoc(creature, x, y, screen):
    if (creature == 'spider'):
        pygame.draw.rect(screen, (0, 0, 0), sg.rectangleGrid[x][y].rect)
    else:
        # oldRectangle = rectangleGrid[x][y]
        pygame.draw.rect(screen, (255, 0, 0), sg.rectangleGrid[x][y].rect)
        sg.rectangleGrid[x][y].hasAnt = True

def changeLoc(creature, x, y, screen):
    pygame.draw.rect(screen, (sg.rectangleGrid[creature.lastX][creature.lastY].color), sg.rectangleGrid[creature.lastX][creature.lastY])
    if isinstance(creature, Spider):
        pygame.draw.rect(screen, (0, 0, 0), sg.rectangleGrid[x][y].rect)
    elif isinstance(creature, Ant):
        sg.rectangleGrid[creature.lastX][creature.lastY].hasAnt = False
        sg.rectangleGrid
        pygame.draw.rect(screen, (255, 0, 0), sg.rectangleGrid[x][y].rect)
        sg.rectangleGrid[x][y].hasAnt = True
    pygame.display.update()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()