# resources: https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
import math

class Node:
    def __init__(self, x, y, prevNode):
        self.x = x
        self.y = y
        self.prevNode = prevNode

class StarNode:
    def __init__(self, x, y, prevNode, f, g, h):
        self.x = x
        self.y = y
        self.prevNode = prevNode
        self.f = f
        self.g = g
        self.h = h

# Our trusty old spider
class Spider:
    def __init__(self, grid, x, y):
        self.x = x
        self.y = y
        self.grid = grid
        self.antX = -1
        self.antY = -1
        self.lastAntX = -1
        self.lastAntY = -1
        self.perceivedAntCoords = []
        self.perceivedPath = []
        self.antDirCoords = []

    def updateXY(self, choice):
        self.lastX = self.x
        self.lastY = self.y

        # find out XY of spider
        if choice is 0:
            self.Breadth_First_Search()
        elif choice is 1:
            self.Depth_First_Search()
        elif choice is 2:
            self.searchHeuristicOne()
        elif choice is 3:
            self.searchHeuristicTwo()
        elif choice is 4:
            self.combinedHeuristic()



        # if (self.outOfBounds() is False):
            # self.decideMovement()

    # Locate ant via BFS
    def Search_for_Ant(self):
        self.lastAntX = self.antX
        self.lastAntY = self.antY
        for row in range(20):
            for  col in range(20):
                if self.grid[row][col].hasAnt is True:
                    self.antX = row
                    self.antY = col
                    print("Found ant! " + str(self.antX) + ", " + str(col))
                    print("Last coordinates of ant! " + str(self.lastAntX) + ", " + str(self.lastAntY))
                    return

    def Breadth_First_Search(self):
        if (len(self.antDirCoords) == 0): #otherwise we know where the ant will end up
            self.Search_for_Ant()

        if (len(self.perceivedPath) > 0):
            self.x = self.perceivedPath[0].x
            self.y = self.perceivedPath[0].y
            print("Spider is currently: " + str(self.x) + ", " + str(self.y))
            print("ant is currently: " + str(self.antX) + ", " + str(self.antY))
            if (self.perceivedPath[0].prevNode is not None):
                self.perceivedPath[0] = self.perceivedPath[0].prevNode
            return

        if (self.lastAntY is not -1 and self.lastAntX is not -1):
            self.antDirCoords = self.determineAntDirectionCoordinates()
            print("The ant is moving in the following direction: " + str(self.antDirCoords[0]) + ", " + str(self.antDirCoords[1]))

        queue = [Node(self.x, self.y, None)]
        directionsY = {
            'left': -1,
            'right': 1
        }
        directionsX = {
            'down': 1,
            'up': -1
        }
        path = []
        visited = []

        while (len(queue) > 0):
            current = queue.pop(0)
            # print("Currently removed from queue: " + str(current.x) + ", " + str(current.y))
            # if (current.prevNode is not None):
            #     print("Parent: " + str(current.prevNode.x) + ", " + str(current.prevNode.y))
            visited.append(current)

            if (current.x == self.antX and current.y == self.antY):  # found target, must return path
                path = self.getPath(current)
                self.x = path[0].x
                self.y = path[0].y

                if (len(self.perceivedAntCoords) > 0 and self.antX == self.perceivedAntCoords[0] and self.antY == self.perceivedAntCoords[1]):
                    self.perceivedPath = path[1::]

                if (len(self.antDirCoords) > 0 and len(self.perceivedAntCoords) is 0):
                    self.perceivedAntCoords = [self.antX+((len(path)+1)*self.antDirCoords[0]), self.antY+((len(path)+1)*self.antDirCoords[1])]
                    print("Perceived ant coordinates: " + str(self.perceivedAntCoords[0]),
                          ", " + str(self.perceivedAntCoords[1]))

                if (len(self.perceivedAntCoords) > 0):
                    self.antX = self.perceivedAntCoords[0]
                    self.antY = self.perceivedAntCoords[1]
                print("Spider is currently: " + str(self.x) + ", " + str(self.y))
                return

            #get child nodes in 9 directions
            if (self.outOfBounds(current.x, current.y+directionsY['left']) is False and self.hasVisited(current.x, current.y+directionsY['left'], visited) is False and self.hasVisited(current.x, current.y+directionsY['left'], queue) is False):
                queue.append(Node(current.x, current.y+directionsY['left'], current)) #left

            if (self.outOfBounds(current.x, current.y+directionsY['right']) is False and self.hasVisited(current.x, current.y+directionsY['right'], visited) is False and self.hasVisited(current.x, current.y+directionsY['right'], queue) is False):
                queue.append(Node(current.x, current.y+directionsY['right'], current)) #right

            if (self.outOfBounds(current.x+directionsX['down'], current.y) is False and self.hasVisited(current.x+directionsX['down'], current.y, visited) is False and self.hasVisited(current.x+directionsX['down'], current.y, queue) is False):
                queue.append(Node(current.x+directionsX['down'], current.y, current)) #down

            if (self.outOfBounds(current.x+directionsX['down'], current.y+directionsY['left']) is False and self.hasVisited(current.x+directionsX['down'], current.y+directionsY['left'], visited) is False and self.hasVisited(current.x+directionsX['down'], current.y+directionsY['left'], queue) is False):
                queue.append(Node(current.x+directionsX['down'], current.y+directionsY['left'], current)) #down left

            if (self.outOfBounds(current.x+directionsX['down'], current.y+directionsY['right']) is False and self.hasVisited(current.x+directionsX['down'], current.y+directionsY['right'], visited) is False and self.hasVisited(current.x+directionsX['down'], current.y+directionsY['right'], queue) is False):
                queue.append(Node(current.x+directionsX['down'], current.y+directionsY['right'], current)) #down right

            if (self.outOfBounds(current.x+(directionsX['up']*2), current.y+directionsY['left']) is False and self.hasVisited(current.x+(directionsX['up']*2), current.y+directionsY['left'], visited) is False and self.hasVisited(current.x+(directionsX['up']*2), current.y+directionsY['left'], queue) is False):
                queue.append(Node(current.x+(directionsX['up']*2), current.y+directionsY['left'], current)) #up up left

            if (self.outOfBounds(current.x+directionsX['up'], current.y+(directionsY['left']*2)) is False and self.hasVisited(current.x+directionsX['up'], current.y+(directionsY['left']*2), visited) is False and self.hasVisited(current.x+directionsX['up'], current.y+(directionsY['left']*2), queue) is False):
                queue.append(Node(current.x+directionsX['up'], current.y+(directionsY['left']*2), current)) #up left left

            if (self.outOfBounds(current.x+(directionsX['up']*2), current.y+directionsY['right']) is False and self.hasVisited(current.x+(directionsX['up']*2), current.y+directionsY['right'], visited) is False and self.hasVisited(current.x+(directionsX['up']*2), current.y+directionsY['right'], queue) is False):
                queue.append(Node(current.x+(directionsX['up']*2), current.y+directionsY['right'], current)) #up up right

            if (self.outOfBounds(current.x+directionsX['up'], current.y+(directionsY['right']*2)) is False and self.hasVisited(current.x+directionsX['up'], current.y+(directionsY['right']*2), visited) is False and self.hasVisited(current.x+directionsX['up'], current.y+(directionsY['right']*2), visited) is False):
                queue.append(Node(current.x+directionsX['up'], current.y+(directionsY['right']*2), current)) #up right right

    # Locate ant via DFS
    def Depth_First_Search(self):
        if (len(self.antDirCoords) == 0): #otherwise we know where the ant will end up
            self.Search_for_Ant()

        if (len(self.perceivedPath) > 0):
            self.x = self.perceivedPath[0].x
            self.y = self.perceivedPath[0].y
            print("Spider is currently: " + str(self.x) + ", " + str(self.y))
            print("ant is currently: " + str(self.antX) + ", " + str(self.antY))
            if (self.perceivedPath[0].prevNode is not None):
                self.perceivedPath[0] = self.perceivedPath[0].prevNode
            return

        if (self.lastAntY is not -1 and self.lastAntX is not -1):
            self.antDirCoords = self.determineAntDirectionCoordinates()
            print("The ant is moving in the following direction: " + str(self.antDirCoords[0]) + ", " + str(self.antDirCoords[1]))

        queue = [Node(self.x, self.y, None)]
        directionsY = {
            'left': -1,
            'right': 1
        }
        directionsX = {
            'down': 1,
            'up': -1
        }
        path = []
        visited = []

        while (len(queue) > 0):
            current = queue.pop(0)
            visited.append(current)

            if (current.x == self.antX and current.y == self.antY):  # found target, must return path
                path = self.getPath(current)
                self.x = path[0].x
                self.y = path[0].y
                if (len(self.perceivedAntCoords) > 0 and self.antX == self.perceivedAntCoords[0] and self.antY == self.perceivedAntCoords[1]):
                    self.perceivedPath = path[1::]

                if (len(self.antDirCoords) > 0 and len(self.perceivedAntCoords) is 0):
                    self.perceivedAntCoords = [self.antX+((len(path)+1)*self.antDirCoords[0]), self.antY+((len(path)+1)*self.antDirCoords[1])]
                    print("Perceived ant coordinates: " + str(self.perceivedAntCoords[0]),
                          ", " + str(self.perceivedAntCoords[1]))

                if (len(self.perceivedAntCoords) > 0):
                    self.antX = self.perceivedAntCoords[0]
                    self.antY = self.perceivedAntCoords[1]
                print("Spider is currently: " + str(self.x) + ", " + str(self.y))
                return

            #get child nodes in 9 directions
            if (self.outOfBounds(current.x, current.y+directionsY['left']) is False and self.hasVisited(current.x, current.y+directionsY['left'], visited) is False and self.hasVisited(current.x, current.y+directionsY['left'], queue) is False):
                queue = [(Node(current.x, current.y+directionsY['left'], current))] + queue #left

            if (self.outOfBounds(current.x, current.y+directionsY['right']) is False and self.hasVisited(current.x, current.y+directionsY['right'], visited) is False and self.hasVisited(current.x, current.y+directionsY['right'], queue) is False):
                queue = [(Node(current.x, current.y+directionsY['right'], current))] + queue #right

            if (self.outOfBounds(current.x+directionsX['down'], current.y) is False and self.hasVisited(current.x+directionsX['down'], current.y, visited) is False and self.hasVisited(current.x+directionsX['down'], current.y, queue) is False):
                queue = [(Node(current.x+directionsX['down'], current.y, current))] + queue #down

            if (self.outOfBounds(current.x+directionsX['down'], current.y+directionsY['left']) is False and self.hasVisited(current.x+directionsX['down'], current.y+directionsY['left'], visited) is False and self.hasVisited(current.x+directionsX['down'], current.y+directionsY['left'], queue) is False):
                queue = [(Node(current.x+directionsX['down'], current.y+directionsY['left'], current))] + queue #down left

            if (self.outOfBounds(current.x+directionsX['down'], current.y+directionsY['right']) is False and self.hasVisited(current.x+directionsX['down'], current.y+directionsY['right'], visited) is False and self.hasVisited(current.x+directionsX['down'], current.y+directionsY['right'], queue) is False):
                queue = [(Node(current.x+directionsX['down'], current.y+directionsY['right'], current))] + queue #down right

            if (self.outOfBounds(current.x+(directionsX['up']*2), current.y+directionsY['left']) is False and self.hasVisited(current.x+(directionsX['up']*2), current.y+directionsY['left'], visited) is False and self.hasVisited(current.x+(directionsX['up']*2), current.y+directionsY['left'], queue) is False):
                queue = [(Node(current.x+(directionsX['up']*2), current.y+directionsY['left'], current))] + queue #up up left

            if (self.outOfBounds(current.x+directionsX['up'], current.y+(directionsY['left']*2)) is False and self.hasVisited(current.x+directionsX['up'], current.y+(directionsY['left']*2), visited) is False and self.hasVisited(current.x+directionsX['up'], current.y+(directionsY['left']*2), queue) is False):
                queue = [(Node(current.x+directionsX['up'], current.y+(directionsY['left']*2), current))] + queue #up left left

            if (self.outOfBounds(current.x+(directionsX['up']*2), current.y+directionsY['right']) is False and self.hasVisited(current.x+(directionsX['up']*2), current.y+directionsY['right'], visited) is False and self.hasVisited(current.x+(directionsX['up']*2), current.y+directionsY['right'], queue) is False):
                queue = [(Node(current.x+(directionsX['up']*2), current.y+directionsY['right'], current))] + queue #up up right

            if (self.outOfBounds(current.x+directionsX['up'], current.y+(directionsY['right']*2)) is False and self.hasVisited(current.x+directionsX['up'], current.y+(directionsY['right']*2), visited) is False and self.hasVisited(current.x+directionsX['up'], current.y+(directionsY['right']*2), visited) is False):
                queue = [(Node(current.x+directionsX['up'], current.y+(directionsY['right']*2), current))] + queue #up right right

    # Locate ant via A* Search
    # f(n) = g(n) + h(n)
    # f(n): total cost of path from n to goal
    # g(n): cost so far to reach n
    # h(n) estimated cost from n to goal
    def A_Star_Search(self):
        self.Search_for_Ant()
        queue = [StarNode(self.x, self.y, None, 0, 0, 0)]
        directionsY = {
            'left': -1,
            'right': 1
        }
        directionsX = {
            'down': 1,
            'up': -1
        }
        path = []
        visited = []

        while (len(queue) > 0):
            # get current node
            index = 0
            current = queue[0]

            # get best node out of queue, one with best total cost
            for count, element in enumerate(queue):
                if element.f < current.f:
                    current = element
                    # print("new current:" + str(current.x) + ", " + str(current.y))
                    index = count

            queue.pop(index)
            visited.append(current)

            # done
            if (current.x == self.antX and current.y == self.antY):  # found target, must return path
                path = self.getPath(current)
                self.x = path[0].x
                self.y = path[0].y
                return

            #get child nodes in 9 directions
            if (self.outOfBounds(current.x, current.y+directionsY['left']) is False):
                g = current.g + 1
                h = math.sqrt(math.pow(self.antX-current.x, 2)+ math.pow(self.antY-current.y+directionsY['left'], 2))
                f = g+h
                newNode = StarNode(current.x, current.y+directionsY['left'], current, f, g, h)

                if (self.hasVisited(current.x, current.y+directionsY['left'], queue) is True and self.hasVisited(current.x, current.y+directionsY['left'], visited) is False):
                    queue = self.updateCost(newNode, queue)
                else:
                    queue.append(newNode) #left

            if (self.outOfBounds(current.x, current.y+directionsY['right']) is False):
                g = current.g + 1
                h = math.sqrt(
                    math.pow(self.antX - current.x, 2) + math.pow(self.antY - current.y + directionsY['right'], 2))
                f = g + h
                newNode = StarNode(current.x, current.y+directionsY['right'], current, f, g, h)

                if (self.hasVisited(current.x, current.y+directionsY['right'], queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif(self.hasVisited(current.x, current.y+directionsY['right'], visited) is False):
                    queue.append(newNode) #right

            if (self.outOfBounds(current.x+directionsX['down'], current.y) is False):
                g = current.g + 1
                h = math.sqrt(
                    math.pow(self.antX - current.x + directionsX['down'], 2) + math.pow(self.antY - current.y, 2))
                f = g + h
                newNode = StarNode(current.x+directionsX['down'], current.y, current, f, g, h)

                if (self.hasVisited(current.x+directionsX['down'], current.y, queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+directionsX['down'], current.y, visited) is False):
                    queue.append(newNode) #down

            if (self.outOfBounds(current.x+directionsX['down'], current.y+directionsY['left']) is False):
                g = current.g + 1
                h = math.sqrt(math.pow(self.antX - current.x + directionsX['down'], 2) + math.pow(
                    self.antY - current.y + directionsY['left'], 2))
                f = g + h
                newNode = StarNode(current.x+directionsX['down'], current.y+directionsY['left'], current, f, g, h)

                if (self.hasVisited(current.x+directionsX['down'], current.y+directionsY['left'], queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+directionsX['down'], current.y+directionsY['left'], visited) is False):
                    queue.append(newNode) #down left

            if (self.outOfBounds(current.x+directionsX['down'], current.y+directionsY['right']) is False):
                g = current.g + 1
                h = math.sqrt(math.pow(self.antX - current.x + directionsX['down'], 2) + math.pow(
                    self.antY - current.y + directionsY['right'], 2))
                f = g + h
                newNode = StarNode(current.x+directionsX['down'], current.y+directionsY['right'], current, f, g, h)

                if (self.hasVisited(current.x+directionsX['down'], current.y+directionsY['right'], queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+directionsX['down'], current.y+directionsY['right'], visited) is False):
                    queue.append(newNode) #down right

            if (self.outOfBounds(current.x+(directionsX['up']*2), current.y+directionsY['left']) is False):
                g = current.g + 1
                h = math.sqrt(math.pow(self.antX - current.x + (directionsX['up'] * 2), 2) + math.pow(
                    self.antY - current.y + directionsY['left'], 2))
                f = g + h
                newNode = StarNode(current.x+(directionsX['up']*2), current.y+directionsY['left'], current, f, g, h)

                if (self.hasVisited(current.x+(directionsX['up']*2), current.y+directionsY['left'], queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+(directionsX['up']*2), current.y+directionsY['left'], visited) is False):
                    queue.append(newNode) #up up left

            if (self.outOfBounds(current.x+directionsX['up'], current.y+(directionsY['left']*2)) is False):
                g = current.g + 1
                h = math.sqrt(math.pow(self.antX - current.x + directionsX['up'], 2) + math.pow(
                    self.antY - current.y + (directionsY['left'] * 2), 2))
                f = g + h
                newNode = StarNode(current.x+directionsX['up'], current.y+(directionsY['left']*2), current, f, g, h)

                if (self.hasVisited(current.x+directionsX['up'], current.y+(directionsY['left']*2), queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+directionsX['up'], current.y+(directionsY['left']*2), visited) is False):
                    queue.append(newNode) #up left left

            if (self.outOfBounds(current.x+(directionsX['up']*2), current.y+directionsY['right']) is False):
                g = current.g + 1
                h = math.sqrt(math.pow(self.antX - current.x + (directionsX['up'] * 2), 2) + math.pow(
                    self.antY - current.y + directionsY['right'], 2))
                f = g + h
                newNode = StarNode(current.x+(directionsX['up']*2), current.y+directionsY['right'], current, f, g, h)

                if (self.hasVisited(current.x+(directionsX['up']*2), current.y+directionsY['right'], queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+(directionsX['up']*2), current.y+directionsY['right'], visited) is False):
                    queue.append(newNode) #up up right

            if (self.outOfBounds(current.x+directionsX['up'], current.y+(directionsY['right']*2)) is False):
                g = current.g + 1
                h = math.sqrt(math.pow(self.antX - current.x + (directionsX['up'] * 2), 2) + math.pow(
                    self.antY - current.y + (directionsY['right'] * 2), 2))
                f = g + h
                newNode = StarNode(current.x+directionsX['up'], current.y+(directionsY['right']*2), current, f, g, h)

                if (self.hasVisited(current.x+directionsX['up'], current.y+(directionsY['right']*2), queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+directionsX['up'], current.y+(directionsY['right']*2), visited) is False):
                    queue.append(newNode) #up right right
            # print(str(len(queue)))
        self.Search_for_Ant()
        queue = [StarNode(self.x, self.y, None, 0, 0, 0)]
        directionsY = {
            'left': -1,
            'right': 1
        }
        directionsX = {
            'down': 1,
            'up': -1
        }
        path = []
        visited = []

        while (len(queue) > 0):
            # get current node
            index = 0
            current = queue[0]

            # get best node out of queue, one with best total cost
            for count, element in enumerate(queue):
                if element.f < current.f:
                    current = element
                    # print("new current:" + str(current.x) + ", " + str(current.y))
                    index = count

            queue.pop(index)
            visited.append(current)

            # done
            if (current.x == self.antX and current.y == self.antY):  # found target, must return path
                path = self.getPath(current)
                self.x = path[0].x
                self.y = path[0].y
                return

            #get child nodes in 9 directions
            if (self.outOfBounds(current.x, current.y+directionsY['left']) is False):
                g = current.g + 1
                h = math.sqrt(math.pow(self.antX-current.x, 2)+ math.pow(self.antY-current.y+directionsY['left'], 2))
                f = g+h
                newNode = StarNode(current.x, current.y+directionsY['left'], current, f, g, h)

                if (self.hasVisited(current.x, current.y+directionsY['left'], queue) is True and self.hasVisited(current.x, current.y+directionsY['left'], visited) is False):
                    queue = self.updateCost(newNode, queue)
                else:
                    queue.append(newNode) #left

            if (self.outOfBounds(current.x, current.y+directionsY['right']) is False):
                g = current.g + 1
                h = math.sqrt(
                    math.pow(self.antX - current.x, 2) + math.pow(self.antY - current.y + directionsY['right'], 2))
                f = g + h
                newNode = StarNode(current.x, current.y+directionsY['right'], current, f, g, h)

                if (self.hasVisited(current.x, current.y+directionsY['right'], queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif(self.hasVisited(current.x, current.y+directionsY['right'], visited) is False):
                    queue.append(newNode) #right

            if (self.outOfBounds(current.x+directionsX['down'], current.y) is False):
                g = current.g + 1
                h = math.sqrt(
                    math.pow(self.antX - current.x + directionsX['down'], 2) + math.pow(self.antY - current.y, 2))
                f = g + h
                newNode = StarNode(current.x+directionsX['down'], current.y, current, f, g, h)

                if (self.hasVisited(current.x+directionsX['down'], current.y, queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+directionsX['down'], current.y, visited) is False):
                    queue.append(newNode) #down

            if (self.outOfBounds(current.x+directionsX['down'], current.y+directionsY['left']) is False):
                g = current.g + 1
                h = math.sqrt(math.pow(self.antX - current.x + directionsX['down'], 2) + math.pow(
                    self.antY - current.y + directionsY['left'], 2))
                f = g + h
                newNode = StarNode(current.x+directionsX['down'], current.y+directionsY['left'], current, f, g, h)

                if (self.hasVisited(current.x+directionsX['down'], current.y+directionsY['left'], queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+directionsX['down'], current.y+directionsY['left'], visited) is False):
                    queue.append(newNode) #down left

            if (self.outOfBounds(current.x+directionsX['down'], current.y+directionsY['right']) is False):
                g = current.g + 1
                h = math.sqrt(math.pow(self.antX - current.x + directionsX['down'], 2) + math.pow(
                    self.antY - current.y + directionsY['right'], 2))
                f = g + h
                newNode = StarNode(current.x+directionsX['down'], current.y+directionsY['right'], current, f, g, h)

                if (self.hasVisited(current.x+directionsX['down'], current.y+directionsY['right'], queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+directionsX['down'], current.y+directionsY['right'], visited) is False):
                    queue.append(newNode) #down right

            if (self.outOfBounds(current.x+(directionsX['up']*2), current.y+directionsY['left']) is False):
                g = current.g + 1
                h = math.sqrt(math.pow(self.antX - current.x + (directionsX['up'] * 2), 2) + math.pow(
                    self.antY - current.y + directionsY['left'], 2))
                f = g + h
                newNode = StarNode(current.x+(directionsX['up']*2), current.y+directionsY['left'], current, f, g, h)

                if (self.hasVisited(current.x+(directionsX['up']*2), current.y+directionsY['left'], queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+(directionsX['up']*2), current.y+directionsY['left'], visited) is False):
                    queue.append(newNode) #up up left

            if (self.outOfBounds(current.x+directionsX['up'], current.y+(directionsY['left']*2)) is False):
                g = current.g + 1
                h = math.sqrt(math.pow(self.antX - current.x + directionsX['up'], 2) + math.pow(
                    self.antY - current.y + (directionsY['left'] * 2), 2))
                f = g + h
                newNode = StarNode(current.x+directionsX['up'], current.y+(directionsY['left']*2), current, f, g, h)

                if (self.hasVisited(current.x+directionsX['up'], current.y+(directionsY['left']*2), queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+directionsX['up'], current.y+(directionsY['left']*2), visited) is False):
                    queue.append(newNode) #up left left

            if (self.outOfBounds(current.x+(directionsX['up']*2), current.y+directionsY['right']) is False):
                g = current.g + 1
                h = math.sqrt(math.pow(self.antX - current.x + (directionsX['up'] * 2), 2) + math.pow(
                    self.antY - current.y + directionsY['right'], 2))
                f = g + h
                newNode = StarNode(current.x+(directionsX['up']*2), current.y+directionsY['right'], current, f, g, h)

                if (self.hasVisited(current.x+(directionsX['up']*2), current.y+directionsY['right'], queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+(directionsX['up']*2), current.y+directionsY['right'], visited) is False):
                    queue.append(newNode) #up up right

            if (self.outOfBounds(current.x+directionsX['up'], current.y+(directionsY['right']*2)) is False):
                g = current.g + 1
                h = math.sqrt(math.pow(self.antX - current.x + (directionsX['up'] * 2), 2) + math.pow(
                    self.antY - current.y + (directionsY['right'] * 2), 2))
                f = g + h
                newNode = StarNode(current.x+directionsX['up'], current.y+(directionsY['right']*2), current, f, g, h)

                if (self.hasVisited(current.x+directionsX['up'], current.y+(directionsY['right']*2), queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+directionsX['up'], current.y+(directionsY['right']*2), visited) is False):
                    queue.append(newNode) #up right right
            # print(str(len(queue)))

    # Like A* search, but speeds up the process a bit
    # h = manhattan distance => abs(current x - goal x) + abs(current y - goal y)
    # http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
    def searchHeuristicOne(self):
        if (len(self.antDirCoords) == 0): #otherwise we know where the ant will end up
            self.Search_for_Ant()

        if (len(self.perceivedPath) > 0):
            self.x = self.perceivedPath[0].x
            self.y = self.perceivedPath[0].y
            print("Spider is currently: " + str(self.x) + ", " + str(self.y))
            print("ant is currently: " + str(self.antX) + ", " + str(self.antY))
            if (self.perceivedPath[0].prevNode is not None):
                self.perceivedPath[0] = self.perceivedPath[0].prevNode
            return

        if (self.lastAntY is not -1 and self.lastAntX is not -1):
            self.antDirCoords = self.determineAntDirectionCoordinates()
            print("The ant is moving in the following direction: " + str(self.antDirCoords[0]) + ", " + str(self.antDirCoords[1]))

        queue = [StarNode(self.x, self.y, None, 0, 0, 0)]
        directionsY = {
            'left': -1,
            'right': 1
        }
        directionsX = {
            'down': 1,
            'up': -1
        }
        path = []
        visited = []

        while (len(queue) > 0):
            # get current node
            index = 0
            current = queue[0]

            # get best node out of queue, one with best total cost
            for count, element in enumerate(queue):
                if element.f < current.f:
                    current = element
                    # print("new current:" + str(current.x) + ", " + str(current.y))
                    index = count

            queue.pop(index)
            visited.append(current)

            # done
            if (current.x == self.antX and current.y == self.antY):  # found target, must return path
                path = self.getPath(current)
                self.x = path[0].x
                self.y = path[0].y

                if (len(self.perceivedAntCoords) > 0 and self.antX == self.perceivedAntCoords[0] and self.antY == self.perceivedAntCoords[1]):
                    self.perceivedPath = path[1::]

                if (len(self.antDirCoords) > 0 and len(self.perceivedAntCoords) is 0):
                    self.perceivedAntCoords = [self.antX+((len(path)+1)*self.antDirCoords[0]), self.antY+((len(path)+1)*self.antDirCoords[1])]
                    print("Perceived ant coordinates: " + str(self.perceivedAntCoords[0]),
                          ", " + str(self.perceivedAntCoords[1]))

                if (len(self.perceivedAntCoords) > 0):
                    self.antX = self.perceivedAntCoords[0]
                    self.antY = self.perceivedAntCoords[1]
                print("Spider is currently: " + str(self.x) + ", " + str(self.y))
                return

            #get child nodes in 9 directions
            if (self.outOfBounds(current.x, current.y+directionsY['left']) is False):
                g = current.g + 1
                h = abs(current.x-self.antX) + abs(current.y+directionsY['left']-self.antY)
                f = g+h
                newNode = StarNode(current.x, current.y+directionsY['left'], current, f, g, h)

                if (self.hasVisited(current.x, current.y+directionsY['left'], queue) is True and self.hasVisited(current.x, current.y+directionsY['left'], visited) is False):
                    queue = self.updateCost(newNode, queue)
                else:
                    queue.append(newNode) #left

            if (self.outOfBounds(current.x, current.y+directionsY['right']) is False):
                g = current.g + 1
                h = abs(current.x-self.antX) + abs((current.y + directionsY['right'])-self.antY)
                f = g + h
                newNode = StarNode(current.x, current.y+directionsY['right'], current, f, g, h)

                if (self.hasVisited(current.x, current.y+directionsY['right'], queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif(self.hasVisited(current.x, current.y+directionsY['right'], visited) is False):
                    queue.append(newNode) #right

            if (self.outOfBounds(current.x+directionsX['down'], current.y) is False):
                g = current.g + 1
                h = abs((current.x + directionsX['down'])-self.antX) + abs(current.y-self.antY)
                f = g + h
                newNode = StarNode(current.x+directionsX['down'], current.y, current, f, g, h)

                if (self.hasVisited(current.x+directionsX['down'], current.y, queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+directionsX['down'], current.y, visited) is False):
                    queue.append(newNode) #down

            if (self.outOfBounds(current.x+directionsX['down'], current.y+directionsY['left']) is False):
                g = current.g + 1
                h = abs((current.x + directionsX['down'])-self.antX) + abs((current.y + directionsY['left'])-self.antY)
                f = g + h
                newNode = StarNode(current.x+directionsX['down'], current.y+directionsY['left'], current, f, g, h)

                if (self.hasVisited(current.x+directionsX['down'], current.y+directionsY['left'], queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+directionsX['down'], current.y+directionsY['left'], visited) is False):
                    queue.append(newNode) #down left

            if (self.outOfBounds(current.x+directionsX['down'], current.y+directionsY['right']) is False):
                g = current.g + 1
                h = abs((current.x + directionsX['down'])-self.antX) + abs((current.y + directionsY['right'])-self.antY)
                f = g + h
                newNode = StarNode(current.x+directionsX['down'], current.y+directionsY['right'], current, f, g, h)

                if (self.hasVisited(current.x+directionsX['down'], current.y+directionsY['right'], queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+directionsX['down'], current.y+directionsY['right'], visited) is False):
                    queue.append(newNode) #down right

            if (self.outOfBounds(current.x+(directionsX['up']*2), current.y+directionsY['left']) is False):
                g = current.g + 1
                h = abs((current.x + (directionsX['up'] * 2))-self.antX) + abs((current.y + directionsY['left'])-self.antY)
                f = g + h
                newNode = StarNode(current.x+(directionsX['up']*2), current.y+directionsY['left'], current, f, g, h)

                if (self.hasVisited(current.x+(directionsX['up']*2), current.y+directionsY['left'], queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+(directionsX['up']*2), current.y+directionsY['left'], visited) is False):
                    queue.append(newNode) #up up left

            if (self.outOfBounds(current.x+directionsX['up'], current.y+(directionsY['left']*2)) is False):
                g = current.g + 1
                h = abs((current.x + directionsX['up'])-self.antX) + abs((current.y + (directionsY['left'] * 2))-self.antY)
                f = g + h
                newNode = StarNode(current.x+directionsX['up'], current.y+(directionsY['left']*2), current, f, g, h)

                if (self.hasVisited(current.x+directionsX['up'], current.y+(directionsY['left']*2), queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+directionsX['up'], current.y+(directionsY['left']*2), visited) is False):
                    queue.append(newNode) #up left left

            if (self.outOfBounds(current.x+(directionsX['up']*2), current.y+directionsY['right']) is False):
                g = current.g + 1
                h = abs((current.x + (directionsX['up'] * 2))-self.antX) + abs((current.y + directionsY['right'])-self.antY)
                f = g + h
                newNode = StarNode(current.x+(directionsX['up']*2), current.y+directionsY['right'], current, f, g, h)

                if (self.hasVisited(current.x+(directionsX['up']*2), current.y+directionsY['right'], queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+(directionsX['up']*2), current.y+directionsY['right'], visited) is False):
                    queue.append(newNode) #up up right

            if (self.outOfBounds(current.x+directionsX['up'], current.y+(directionsY['right']*2)) is False):
                g = current.g + 1
                h = abs((current.x + (directionsX['up']))-self.antX) + abs((current.y + (directionsY['right'] * 2))-self.antY)
                f = g + h
                newNode = StarNode(current.x+directionsX['up'], current.y+(directionsY['right']*2), current, f, g, h)

                if (self.hasVisited(current.x+directionsX['up'], current.y+(directionsY['right']*2), queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+directionsX['up'], current.y+(directionsY['right']*2), visited) is False):
                    queue.append(newNode) #up right right
            # print(str(len(queue)))

    # Like A* search, but speeds up the process a bit
    # calculates ant's perceived end goal when the spider will approach it
    def searchHeuristicTwo(self):
        if (len(self.antDirCoords) == 0): #otherwise we know where the ant will end up
            self.Search_for_Ant()

        if (len(self.perceivedPath) > 0):
            self.x = self.perceivedPath[0].x
            self.y = self.perceivedPath[0].y
            print("Spider is currently: " + str(self.x) + ", " + str(self.y))
            print("ant is currently: " + str(self.antX) + ", " + str(self.antY))
            if (self.perceivedPath[0].prevNode is not None):
                self.perceivedPath[0] = self.perceivedPath[0].prevNode
            return

        if (self.lastAntY is not -1 and self.lastAntX is not -1):
            self.antDirCoords = self.determineAntDirectionCoordinates()
            print("The ant is moving in the following direction: " + str(self.antDirCoords[0]) + ", " + str(self.antDirCoords[1]))

        queue = [StarNode(self.x, self.y, None, 0, 0, 0)]
        directionsY = {
            'left': -1,
            'right': 1
        }
        directionsX = {
            'down': 1,
            'up': -1
        }
        path = []
        visited = []

        while (len(queue) > 0):
            # get current node
            index = 0
            current = queue[0]

            # get best node out of queue, one with best total cost
            for count, element in enumerate(queue):
                if element.f < current.f:
                    current = element
                    # print("new current:" + str(current.x) + ", " + str(current.y))
                    index = count

            queue.pop(index)
            visited.append(current)

            # done
            if (current.x == self.antX and current.y == self.antY):  # found target, must return path
                path = self.getPath(current)
                self.x = path[0].x
                self.y = path[0].y

                if (len(self.perceivedAntCoords) > 0 and self.antX == self.perceivedAntCoords[0] and self.antY == self.perceivedAntCoords[1]):
                    self.perceivedPath = path[1::]

                if (len(self.antDirCoords) > 0 and len(self.perceivedAntCoords) is 0):
                    self.perceivedAntCoords = [self.antX+((len(path)+1)*self.antDirCoords[0]), self.antY+((len(path)+1)*self.antDirCoords[1])]
                    print("Perceived ant coordinates: " + str(self.perceivedAntCoords[0]),
                          ", " + str(self.perceivedAntCoords[1]))

                if (len(self.perceivedAntCoords) > 0):
                    self.antX = self.perceivedAntCoords[0]
                    self.antY = self.perceivedAntCoords[1]
                print("Spider is currently: " + str(self.x) + ", " + str(self.y))
                return

            #get child nodes in 9 directions
            if (self.outOfBounds(current.x, current.y+directionsY['left']) is False):
                g = current.g + 1
                h = math.sqrt(math.pow(self.antX-current.x, 2)+ math.pow(self.antY-current.y+directionsY['left'], 2))
                f = g+h
                newNode = StarNode(current.x, current.y+directionsY['left'], current, f, g, h)

                if (self.hasVisited(current.x, current.y+directionsY['left'], queue) is True and self.hasVisited(current.x, current.y+directionsY['left'], visited) is False):
                    queue = self.updateCost(newNode, queue)
                else:
                    queue.append(newNode) #left

            if (self.outOfBounds(current.x, current.y+directionsY['right']) is False):
                g = current.g + 1
                h = math.sqrt(
                    math.pow(self.antX - current.x, 2) + math.pow(self.antY - current.y + directionsY['right'], 2))
                f = g + h
                newNode = StarNode(current.x, current.y+directionsY['right'], current, f, g, h)

                if (self.hasVisited(current.x, current.y+directionsY['right'], queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif(self.hasVisited(current.x, current.y+directionsY['right'], visited) is False):
                    queue.append(newNode) #right

            if (self.outOfBounds(current.x+directionsX['down'], current.y) is False):
                g = current.g + 1
                h = math.sqrt(
                    math.pow(self.antX - current.x + directionsX['down'], 2) + math.pow(self.antY - current.y, 2))
                f = g + h
                newNode = StarNode(current.x+directionsX['down'], current.y, current, f, g, h)

                if (self.hasVisited(current.x+directionsX['down'], current.y, queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+directionsX['down'], current.y, visited) is False):
                    queue.append(newNode) #down

            if (self.outOfBounds(current.x+directionsX['down'], current.y+directionsY['left']) is False):
                g = current.g + 1
                h = math.sqrt(math.pow(self.antX - current.x + directionsX['down'], 2) + math.pow(
                    self.antY - current.y + directionsY['left'], 2))
                f = g + h
                newNode = StarNode(current.x+directionsX['down'], current.y+directionsY['left'], current, f, g, h)

                if (self.hasVisited(current.x+directionsX['down'], current.y+directionsY['left'], queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+directionsX['down'], current.y+directionsY['left'], visited) is False):
                    queue.append(newNode) #down left

            if (self.outOfBounds(current.x+directionsX['down'], current.y+directionsY['right']) is False):
                g = current.g + 1
                h = math.sqrt(math.pow(self.antX - current.x + directionsX['down'], 2) + math.pow(
                    self.antY - current.y + directionsY['right'], 2))
                f = g + h
                newNode = StarNode(current.x+directionsX['down'], current.y+directionsY['right'], current, f, g, h)

                if (self.hasVisited(current.x+directionsX['down'], current.y+directionsY['right'], queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+directionsX['down'], current.y+directionsY['right'], visited) is False):
                    queue.append(newNode) #down right

            if (self.outOfBounds(current.x+(directionsX['up']*2), current.y+directionsY['left']) is False):
                g = current.g + 1
                h = math.sqrt(math.pow(self.antX - current.x + (directionsX['up'] * 2), 2) + math.pow(
                    self.antY - current.y + directionsY['left'], 2))
                f = g + h
                newNode = StarNode(current.x+(directionsX['up']*2), current.y+directionsY['left'], current, f, g, h)

                if (self.hasVisited(current.x+(directionsX['up']*2), current.y+directionsY['left'], queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+(directionsX['up']*2), current.y+directionsY['left'], visited) is False):
                    queue.append(newNode) #up up left

            if (self.outOfBounds(current.x+directionsX['up'], current.y+(directionsY['left']*2)) is False):
                g = current.g + 1
                h = math.sqrt(math.pow(self.antX - current.x + directionsX['up'], 2) + math.pow(
                    self.antY - current.y + (directionsY['left'] * 2), 2))
                f = g + h
                newNode = StarNode(current.x+directionsX['up'], current.y+(directionsY['left']*2), current, f, g, h)

                if (self.hasVisited(current.x+directionsX['up'], current.y+(directionsY['left']*2), queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+directionsX['up'], current.y+(directionsY['left']*2), visited) is False):
                    queue.append(newNode) #up left left

            if (self.outOfBounds(current.x+(directionsX['up']*2), current.y+directionsY['right']) is False):
                g = current.g + 1
                h = math.sqrt(math.pow(self.antX - current.x + (directionsX['up'] * 2), 2) + math.pow(
                    self.antY - current.y + directionsY['right'], 2))
                f = g + h
                newNode = StarNode(current.x+(directionsX['up']*2), current.y+directionsY['right'], current, f, g, h)

                if (self.hasVisited(current.x+(directionsX['up']*2), current.y+directionsY['right'], queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+(directionsX['up']*2), current.y+directionsY['right'], visited) is False):
                    queue.append(newNode) #up up right

            if (self.outOfBounds(current.x+directionsX['up'], current.y+(directionsY['right']*2)) is False):
                g = current.g + 1
                h = math.sqrt(math.pow(self.antX - current.x + directionsX['up'], 2) + math.pow(
                    self.antY - current.y + (directionsY['right'] * 2), 2))
                f = g + h
                newNode = StarNode(current.x+directionsX['up'], current.y+(directionsY['right']*2), current, f, g, h)

                if (self.hasVisited(current.x+directionsX['up'], current.y+(directionsY['right']*2), queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+directionsX['up'], current.y+(directionsY['right']*2), visited) is False):
                    queue.append(newNode) #up right right
            # print(str(len(queue)))

    # combining HeuristicOne and HeuristicTwo
    def combinedHeuristic(self):
        if (len(self.antDirCoords) == 0): #otherwise we know where the ant will end up
            self.Search_for_Ant()

        if (len(self.perceivedPath) > 0):
            self.x = self.perceivedPath[0].x
            self.y = self.perceivedPath[0].y
            print("Spider is currently: " + str(self.x) + ", " + str(self.y))
            print("ant is currently: " + str(self.antX) + ", " + str(self.antY))
            if (self.perceivedPath[0].prevNode is not None):
                self.perceivedPath[0] = self.perceivedPath[0].prevNode
            return

        if (self.lastAntY is not -1 and self.lastAntX is not -1):
            self.antDirCoords = self.determineAntDirectionCoordinates()
            print("The ant is moving in the following direction: " + str(self.antDirCoords[0]) + ", " + str(self.antDirCoords[1]))

        queue = [StarNode(self.x, self.y, None, 0, 0, 0)]
        directionsY = {
            'left': -1,
            'right': 1
        }
        directionsX = {
            'down': 1,
            'up': -1
        }
        path = []
        visited = []

        while (len(queue) > 0):
            # get current node
            index = 0
            current = queue[0]

            # get best node out of queue, one with best total cost
            for count, element in enumerate(queue):
                if element.f < current.f:
                    current = element
                    # print("new current:" + str(current.x) + ", " + str(current.y))
                    index = count

            queue.pop(index)
            visited.append(current)

            # done
            if (current.x == self.antX and current.y == self.antY):  # found target, must return path
                path = self.getPath(current)
                self.x = path[0].x
                self.y = path[0].y

                if (len(self.perceivedAntCoords) > 0 and self.antX == self.perceivedAntCoords[0] and self.antY == self.perceivedAntCoords[1]):
                    self.perceivedPath = path[1::]

                if (len(self.antDirCoords) > 0 and len(self.perceivedAntCoords) is 0):
                    self.perceivedAntCoords = [self.antX+((len(path)+1)*self.antDirCoords[0]), self.antY+((len(path)+1)*self.antDirCoords[1])]
                    print("Perceived ant coordinates: " + str(self.perceivedAntCoords[0]),
                          ", " + str(self.perceivedAntCoords[1]))

                if (len(self.perceivedAntCoords) > 0):
                    self.antX = self.perceivedAntCoords[0]
                    self.antY = self.perceivedAntCoords[1]
                print("Spider is currently: " + str(self.x) + ", " + str(self.y))
                return

            #get child nodes in 9 directions
            if (self.outOfBounds(current.x, current.y+directionsY['left']) is False):
                g = current.g + 1
                h = self.calculateCombinedHeuristic(current.x, current.y+directionsY['left'])
                f = g+h
                newNode = StarNode(current.x, current.y+directionsY['left'], current, f, g, h)

                if (self.hasVisited(current.x, current.y+directionsY['left'], queue) is True and self.hasVisited(current.x, current.y+directionsY['left'], visited) is False):
                    queue = self.updateCost(newNode, queue)
                else:
                    queue.append(newNode) #left

            if (self.outOfBounds(current.x, current.y+directionsY['right']) is False):
                g = current.g + 1
                h = self.calculateCombinedHeuristic(current.x, current.y + directionsY['right'])
                f = g + h
                newNode = StarNode(current.x, current.y+directionsY['right'], current, f, g, h)

                if (self.hasVisited(current.x, current.y+directionsY['right'], queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif(self.hasVisited(current.x, current.y+directionsY['right'], visited) is False):
                    queue.append(newNode) #right

            if (self.outOfBounds(current.x+directionsX['down'], current.y) is False):
                g = current.g + 1
                h = self.calculateCombinedHeuristic(current.x + directionsX['down'], current.y)
                f = g + h
                newNode = StarNode(current.x+directionsX['down'], current.y, current, f, g, h)

                if (self.hasVisited(current.x+directionsX['down'], current.y, queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+directionsX['down'], current.y, visited) is False):
                    queue.append(newNode) #down

            if (self.outOfBounds(current.x+directionsX['down'], current.y+directionsY['left']) is False):
                g = current.g + 1
                h = self.calculateCombinedHeuristic(current.x + directionsX['down'], current.y + directionsY['left'])
                f = g + h
                newNode = StarNode(current.x+directionsX['down'], current.y+directionsY['left'], current, f, g, h)

                if (self.hasVisited(current.x+directionsX['down'], current.y+directionsY['left'], queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+directionsX['down'], current.y+directionsY['left'], visited) is False):
                    queue.append(newNode) #down left

            if (self.outOfBounds(current.x+directionsX['down'], current.y+directionsY['right']) is False):
                g = current.g + 1
                h = self.calculateCombinedHeuristic(current.x + directionsX['down'], current.y + directionsY['right'])
                f = g + h
                newNode = StarNode(current.x+directionsX['down'], current.y+directionsY['right'], current, f, g, h)

                if (self.hasVisited(current.x+directionsX['down'], current.y+directionsY['right'], queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+directionsX['down'], current.y+directionsY['right'], visited) is False):
                    queue.append(newNode) #down right

            if (self.outOfBounds(current.x+(directionsX['up']*2), current.y+directionsY['left']) is False):
                g = current.g + 1
                h = self.calculateCombinedHeuristic(current.x + (directionsX['up'] * 2), current.y + directionsY['left'])
                f = g + h
                newNode = StarNode(current.x+(directionsX['up']*2), current.y+directionsY['left'], current, f, g, h)

                if (self.hasVisited(current.x+(directionsX['up']*2), current.y+directionsY['left'], queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+(directionsX['up']*2), current.y+directionsY['left'], visited) is False):
                    queue.append(newNode) #up up left

            if (self.outOfBounds(current.x+directionsX['up'], current.y+(directionsY['left']*2)) is False):
                g = current.g + 1
                h = self.calculateCombinedHeuristic(current.x + directionsX['up'], current.y + (directionsY['left'] * 2))
                f = g + h
                newNode = StarNode(current.x+directionsX['up'], current.y+(directionsY['left']*2), current, f, g, h)

                if (self.hasVisited(current.x+directionsX['up'], current.y+(directionsY['left']*2), queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+directionsX['up'], current.y+(directionsY['left']*2), visited) is False):
                    queue.append(newNode) #up left left

            if (self.outOfBounds(current.x+(directionsX['up']*2), current.y+directionsY['right']) is False):
                g = current.g + 1
                h = self.calculateCombinedHeuristic(current.x + (directionsX['up'] * 2), current.y + directionsY['right'])
                f = g + h
                newNode = StarNode(current.x+(directionsX['up']*2), current.y+directionsY['right'], current, f, g, h)

                if (self.hasVisited(current.x+(directionsX['up']*2), current.y+directionsY['right'], queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+(directionsX['up']*2), current.y+directionsY['right'], visited) is False):
                    queue.append(newNode) #up up right

            if (self.outOfBounds(current.x+directionsX['up'], current.y+(directionsY['right']*2)) is False):
                g = current.g + 1
                h = self.calculateCombinedHeuristic(current.x + directionsX['up'], current.y + (directionsY['right'] * 2))
                f = g + h
                newNode = StarNode(current.x+directionsX['up'], current.y+(directionsY['right']*2), current, f, g, h)

                if (self.hasVisited(current.x+directionsX['up'], current.y+(directionsY['right']*2), queue) is True):
                    queue = self.updateCost(newNode, queue)
                elif (self.hasVisited(current.x+directionsX['up'], current.y+(directionsY['right']*2), visited) is False):
                    queue.append(newNode) #up right right
            # print(str(len(queue)))

    # average of distance formula + manhattan formula
    # x and y = potential coordinates, not current
    def calculateCombinedHeuristic(self, x, y):
        distance = math.sqrt(math.pow(self.antX-x, 2) + math.pow(self.antY-y, 2))
        manhattan = abs(x-self.antX)+abs(y-self.antY)
        return (distance+manhattan)/2


    def updateCost(self, starnode, queueList):
        for index, element in enumerate(queueList):
            if element.x == starnode.x and element.y == starnode.y:
                # print("starnode: " + str(starnode.g))
                # print("our node " + str(element.g))
                if element.g > starnode.g:
                    queueList[index] = starnode
        return queueList

    def getPath(self, node):
        path = [node]
        while (node.prevNode is not None):
            path.append(node.prevNode)
            print("Here is the path recommended: " + str(node.x) + ", " + str(node.y))
            node = node.prevNode

        return path[1::-1] #so that the closest node to spider is first

    # Checks if spider is able to move within grid
    def outOfBounds(self, x, y):
        if (x >= 0 and x < 20 and y >= 0 and y < 20):
            return False
        else:
            # print("out of bounds" + str(x) + ", " + str(y))
            return True

    def hasVisited(self, x, y, visitedList):
        for node in visitedList:
            if node.x == x and node.y == y:
                # print("We have visited " + str(x) + ", " + str(y))
                return True

        return False

    # determines ant direction coordinates.. i.e. what direction the ant is moving
    def determineAntDirectionCoordinates(self):
        return [self.antX-self.lastAntX, self.antY-self.lastAntY]

    # decide new x and y for spider with respect to where the ant is
    # spider can move right, left, down, down left, and down right by 1 square
    # spider can move up similar to a knight in chess
    def decideMovement(self):
        if (self.antIsDown() is True):  # ant is down, down left, down right
            self.moveDown()
            if (self.antIsLeft() is True):
                self.moveLeft()
            elif (self.antIsRight() is True):
                self.moveRight()
        elif (self.antIsUp() is True): #up left, as knight
            if (self.antIsLeft() is True):
                if (self.antX <= self.x-2): #if ant is up by more than 2 blocks
                    self.moveUp()
                    self.moveUp()
                    self.moveLeft()
                else:
                    self.moveUp()
                    self.moveLeft()
                    self.moveLeft()
            if (self.antIsRight() is True):
                if (self.antX <= self.x-2): #if ant is up by more than 2 blocks
                    self.moveUp()
                    self.moveUp()
                    self.moveRight()
                else:
                    self.moveUp()
                    self.moveRight()
                    self.moveRight()
        elif (self.antIsLeft() is True): # ant is left
            self.moveLeft()
        elif (self.antIsRight() is True): # ant is right
            self.moveRight()

    def moveLeft(self):
        self.y -= 1

    def moveRight(self):
        self.y += 1  # ant is to the right of the spider

    def moveDown(self):
        self.x += 1  # ant is directly below the spider

    def moveUp(self):
        self.x -= 1

    def antIsLeft(self):
        if (self.antY < self.y):
            return True
        else: return False

    def antIsRight(self):
        if (self.antY > self.y):
            return True
        else: return False

    def antIsDown(self):
        if (self.antX > self.x):
            return True
        else: return False

    def antIsUp(self):
        if (self.antX < self.x):
            return True
        else: return False