import random
import operator

ops = {"+": operator.add, "-": operator.sub}  # https://stackoverflow.com/questions/1740726/turn-string-into-operator

class Ant:
    def __init__(self, gridTotalX, gridTotalY, height=20, width=20):
        self.totalx = gridTotalX
        self.totaly = gridTotalY
        self.determineXY()
        self.determineDir()
        self.determineOperators()

    # determines where ant should originate from [0,x or y]
    def determineXY(self):
        self.x = random.randint(0, self.totalx-1)# determine x pos
        self.y = random.randint(0, self.totaly-1)# determine y pos
        # print("Ant's x and y: (" + str (self.x) + "," + str (self.y) + ")")

    # determines 1 out of 8 directions to go in..
    # i.e. (x+1, y) (x, y+1), (x+1, y+1), (x-1, y) (x, y-1) (x-1, y-1), (x+1, y-1), (x-1, y+1)
    def determineDir(self):
        # can be x +/- 0 or y +/- 1
        self.directionX = random.randint(0, 1)

        if (self.directionX is 0):
            self.directionY = 1
        else:
            self.directionY = random.randint(0, 1)

    # determines + or - for x and y
    def determineOperators(self):
        num1 = random.randint(0, 2)
        num2 = random.randint(0, 2)

        if (num1 % 2 is 0):
            self.operatorX = ops["+"]
        else:
            self.operatorX = ops["-"]
        if (num2 % 2 is 0):
            self.operatorY = ops["+"]
        else:
            self.operatorY = ops["-"]

    #updates xy coordinates so that we can traverse
    def updateXY(self):
        self.lastX = self.x
        self.lastY = self.y #last moves
        self.x = int (ops["+"](self.x, self.directionX))
        self.y = int (ops["+"](self.y, self.directionY))
        # print("Ant's x and y: (" + str (self.x) + "," + str (self.y) + ")")
