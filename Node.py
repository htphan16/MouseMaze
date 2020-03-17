from EnvState import Maze
from EnvState import Cell

class Node(object):
    '''Initialize an instance of a node with current state, parent node, path_cost and action'''
    def __init__(self, state):
        self.state = state
        self.hashed_state = hash(state)
        self.parent = None
        self.path_cost = 0
        self.action = ''
        self.heuristic = 0
    def getState(self):
        return self.state
    def getParentNode(self):
        return self.parent
    def setParentNode(self, parent):
        self.parent = parent
    def setAction(self, action):
        self.action = action
    def getAction(self):
        return self.action
    def getPathCost(self): #cost to get from initial node to a certain node
        return self.path_cost
    def setChildNode(self, parent, action):
        self.parent = parent
        self.action = action
        self.state = parent.state.transition(action)
        self.hashed_state = hash(self.state)
        self.path_cost = parent.path_cost + 1
        self.heuristic = 0
        return self
    def __le__(self, other):
        return (self.heuristic <= other.heuristic)
    def __lt__(self, other):
        return (self.heuristic < other.heuristic)

