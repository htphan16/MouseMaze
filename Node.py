from EnvState import Maze
from EnvState import Cell

class Node(object):
    '''Initialize an instance of a node with current state, hashed state, parent node, path_cost, action and heuristic'''
    def __init__(self, state):
        self.state = state
        self.hashed_state = hash(state)
        self.parent = None
        self.path_cost = 0
        self.action = ''
        self.heuristic = 0
    '''Define child node'''
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

