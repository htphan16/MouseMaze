# Part 1
# State representation scheme
# Transition model
# Goal test
import copy

'''Read the maze as a list of strings, get index of every position in the maze'''
class Maze:
    def __init__(self, filename):
        self.filename = filename
        self.maze = []
        self.position = []
    def getMaze(self):
        file = open(self.filename,'r')  # open the files
        infile = file.readlines()   # read the files as a list of lines
        file.close()
        self.maze = [line.strip('\n') for line in infile] 
        return self.maze
    def readMazeIndex(self):
        for i in range(len(self.getMaze())):
            for j in range(len(self.getMaze()[i])):
                self.position.append([j,i])
        return self.position

class Cell(object):
    def __init__(self, maze):
        self.mouse = []
        self.prize = []
        self.maze = maze
    '''Set mouse position'''
    def setMouseIndex(self, mouse):
        self.mouse = mouse
    '''Remove prize from current prize list if mouse is in the prize cell, return new prize list'''
    def setPrizeIndex(self, prize):
        self.prize = prize
        if self.mouse in prize:
            prize.remove(self.mouse)
            self.prize = prize
    '''Get mouse position'''
    def getMouseIndex(self):
        return self.mouse
    '''Get prizes' positions'''
    def getPrizeIndex(self):
        return self.prize
    '''goNorth, goSouth, goEast, goWest functions
    return the mouse position when it moves North, South, East, West respectively'''
    def goNorth(self):
        if self.mouse[1]-1 >= 0:
            self.mouse = [self.mouse[0], self.mouse[1] - 1]
        return self.mouse
    def goSouth(self):
        if self.mouse[1]+1 <= len(self.maze.getMaze()):
            self.mouse = [self.mouse[0], self.mouse[1] + 1]
        return self.mouse
    def goEast(self):
        if self.mouse[0]+1 <= len(self.maze.getMaze()[0]):
            self.mouse = [self.mouse[0] + 1, self.mouse[1]]
        return self.mouse
    def goWest(self):
        if self.mouse[0]-1 >= 0:
            self.mouse = [self.mouse[0] - 1, self.mouse[1]]
        return self.mouse
    def initial(self): # Function to output the initial state (the original maze)
        for pos in self.maze.readMazeIndex():
            if self.maze.getMaze()[pos[1]][pos[0]] == 'P':
                self.setMouseIndex(pos)
            if self.maze.getMaze()[pos[1]][pos[0]] == '.':
                self.prize.append(pos)
        self.setPrizeIndex(self.prize)
        return self
    '''Compare two states'''
    def __eq__(self, other):
        return (self.mouse == other.mouse) and (self.prize == other.prize)
    '''Possible actions to be taken from a certain state'''
    def actions(self):
        actions = []
        for action in ['North', 'South', 'East', 'West']:
            if not self.__eq__(self.transition(action)):
                actions.append(action)
        return actions
    '''Transition function'''
    def transition(self, action):
        new = copy.deepcopy(self)
        if action == 'North' and new.maze.getMaze()[new.mouse[1] - 1][new.mouse[0]] != '%':
            new.setMouseIndex(new.goNorth())
            new.setPrizeIndex(new.prize)
            return new
        elif action == 'South' and new.maze.getMaze()[new.mouse[1] + 1][new.mouse[0]] != '%':
            new.setMouseIndex(new.goSouth())
            new.setPrizeIndex(new.prize)
            return new
        elif action == 'East' and new.maze.getMaze()[new.mouse[1]][new.mouse[0] + 1] != '%':
            new.setMouseIndex(new.goEast())
            new.setPrizeIndex(new.prize)
            return new
        elif action == 'West' and new.maze.getMaze()[new.mouse[1]][new.mouse[0] - 1] != '%':
            new.setMouseIndex(new.goWest())
            new.setPrizeIndex(new.prize)
            return new
        else:
            return self
    '''Goal test function'''
    def goal_test(self):
        if len(self.prize) != 0:
            return False
        else:
            return True
        
    def __hash__(self):
        return hash(tuple(self.mouse))
