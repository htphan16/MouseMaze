from envState import Maze
from envState import Cell

class Node(object):
    '''Initialize an instance of a node with current state, parent node, path_cost and action'''
    def __init__(self, state):
        self.state = state
        self.hashed_state = hash(state)
        self.parent = None
        self.path_cost = 0
        self.action = ''
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
        return self

# filename = 'multiprize-tiny.txt'
# cell = Cell(Maze(filename))
# initial_state = cell.initial()
# initial_node = Node(initial_state)
# print(initial_node.state.mouse)
# child_node = initial_node.setChildNode(initial_node, 'South')
# print(child_node.state.mouse)


