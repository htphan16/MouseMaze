import copy
import time
from EnvState import Maze
from EnvState import Cell
from Node import Node
from queue import PriorityQueue

### Adapted from array_stack (CS 256 Data Structures Chapter 6 code)
'''LIFO queue structure for DFS'''
class Stack(object):
    def __init__(self):
        self.nodes = []
    def is_empty(self):
        return len(self.nodes) == 0
    def insert(self, node):
        self.nodes.append(node)
    def pop(self):
        if self.is_empty():
            raise Empty('Stack is empty')
        return self.nodes.pop()
    def top(self):
        if self.is_empty():
            raise Empty('Stack is empty')
        return self.nodes[-1]
    def getNodes(self):
        return self.nodes
    def numNodes(self):
        return len(self.nodes)
    def getStates(self):
        states = []
        for node in self.nodes:
            states.append(node.state)
        return states

def single_dfs(filename):
    start_time = time.time()
    cell = Cell(Maze(filename)) # Make it clear that this is the initial state
    num_nodes = 0
    start_node = Node(cell.initial()) # This node represents the initial state
    if start_node.state.goal_test():
        return -1
    frontier = Stack()
    frontier.insert(start_node)
    explored = set()
    explored.add(start_node.hashed_state)
    while not frontier.is_empty():
        current_node = frontier.pop()
        action_list = current_node.state.actions()
        for action in action_list:
            print("Action:", action)
            child_node = Node(current_node) 
            child_node = child_node.setChildNode(current_node, action)
            print(child_node, "is our next child node.")
            if child_node.hashed_state not in explored:
                if child_node.state.goal_test():
                    print("We have found a goal state!")
                    path_cost = child_node.path_cost
                    num_nodes = len(explored)
                    print("Path cost: ", path_cost)
                    print("Number of expanded nodes: ", num_nodes)
                    end_time = time.time()
                    return end_time - start_time
                frontier.insert(child_node)
                print("We just enqueued", child_node)
                explored.add(child_node.hashed_state) # For the purposes of A*, we want to not add things to this until they're actually explored
            print(current_node.state.mouse)

#print(single_dfs('1prize-large.txt'))

### Adapted from array_queue (CS 256 Data Structures Chapter 6 code)
class Queue(object):
    """FIFO queue implementation using a Python list as underlying storage."""
    DEFAULT_CAPACITY = 10          # moderate capacity for all new queues
    def __init__(self):
        """Create an empty queue."""
        self.nodes = [None] * Queue.DEFAULT_CAPACITY
        self.front = 0
        self.size = 0

    def __len__(self):
        """Return the number of elements in the queue."""
        return self.size

    def is_empty(self):
        return self.size == 0

    def enqueue(self, node):
        """Add an element to the back of queue."""
        if self.size == len(self.nodes):
            self.resize(2 * len(self.nodes))     # double the array size
        avail = (self.front + self.size) % len(self.nodes)
        self.nodes[avail] = node
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            raise ValueError('Queue is empty')
        answer = self.nodes[self.front]
        self.nodes[self.front] = None         # help garbage collection
        self.front = (self.front + 1) % len(self.nodes)
        self.size -= 1
        return answer

    def resize(self, cap):                  # we assume cap >= len(self)
        """Resize to a new list of capacity >= len(self)."""
        old = self.nodes                      # keep track of existing list
        self.nodes = [None] * cap              # allocate list with new capacity
        walk = self.front
        for k in range(self.size):            # only consider existing elements
            self.nodes[k] = old[walk]            # intentionally shift indices
            walk = (1 + walk) % len(old)         # use old size as modulus
        self.front = 0                        # front has been realigned

    def getNodes(self):
        return self.nodes

    def numNodes(self):
        return len(self.nodes)

    def getStates(self):
        states = []
        for node in self.nodes:
            states.append(node.state)
        return states

def single_bfs(filename):
    start_time = time.time()
    cell = Cell(Maze(filename)) # Make it clear that this is the initial state
    num_nodes = 0
    start_node = Node(cell.initial()) # This node represents the initial state
    if start_node.state.goal_test():
        return -1
    frontier = Queue()
    frontier.enqueue(start_node)
    explored = set()
    explored.add(start_node.hashed_state)
    while not frontier.is_empty():
        print("============FRONTIER", frontier)
        current_node = frontier.dequeue()
        action_list = current_node.state.actions()
        for action in action_list:
            print("Action:", action)
            child_node = Node(current_node)
            child_node = child_node.setChildNode(current_node, action)
            print(child_node, "is our next child node.")
            if child_node.hashed_state not in explored:
                if child_node.state.goal_test():
                    print("We have found a goal state!")
                    path_cost = child_node.path_cost
                    num_nodes = len(explored)
                    print("Path cost: ", path_cost)
                    print("Number of expanded nodes: ", num_nodes)
                    end_time = time.time()
                    return end_time - start_time
                frontier.enqueue(child_node)
                print("We just enqueued", child_node)
                print("Prize list: ", child_node.state.prize)
                explored.add(child_node.hashed_state) # For the purposes of A*, we want to not add things to this until they're actually explored
            print(current_node.state.mouse)


def manhattan(cur_node, filename):
    cell = Cell(Maze(filename))
    initial_node = Node(cell.initial())
    print(cur_node.state.mouse[0], cur_node.state.mouse[1])
    cur_node.heuristic = abs(cur_node.state.mouse[0] - initial_node.state.prize[0][0]) + abs(cur_node.state.mouse[1] - initial_node.state.prize[0][1])
    return cur_node.heuristic

'''Error: PriorityQueue does not work for cases where the successor nodes all take the same distance to the goal'''

def single_gbfs(filename):
    start_time = time.time()
    cell = Cell(Maze(filename)) # Make it clear that this is the initial state
    num_nodes = 0
    start_node = Node(cell.initial()) # This node represents the initial state
    start_node.heuristic = manhattan(start_node, filename)
    if start_node.state.goal_test():
        return -1
    frontier = PriorityQueue()
    frontier.put((start_node.heuristic, start_node))
    explored = set()
    explored.add(start_node.hashed_state)
    while not frontier.empty():
        current = frontier.get()
        current_node = current[1]
        current_node.heuristic = current[0]
        eval_value = current_node.heuristic
        action_list = current_node.state.actions()
        for action in action_list:
            print("Action:", action)
            child_node = Node(current_node)
            child_node = child_node.setChildNode(current_node, action)
            child_node.heuristic = manhattan(child_node, filename)
            # print("manhattan distance is ", child_node.heuristic)
            print(child_node, "is our next child node.")
            if child_node.hashed_state not in explored:
                if child_node.state.goal_test():
                    print("We have found a goal state!")
                    path_cost = child_node.path_cost
                    num_nodes = len(explored)
                    print("Path cost: ", path_cost)
                    print("Number of expanded nodes: ", num_nodes)
                    end_time = time.time()
                    return end_time - start_time
                frontier.put((child_node.heuristic, child_node))
                print("We just enqueued", child_node)
                explored.add(child_node.hashed_state) # For the purposes of A*, we want to not add things to this until they're actually explored
            print(current_node.state.mouse)


def single_astar(filename):
    start_time = time.time()
    cell = Cell(Maze(filename)) # Make it clear that this is the initial state
    num_nodes = 0
    start_node = Node(cell.initial()) # This node represents the initial state
    start_node.heuristic = manhattan(start_node, filename) + start_node.path_cost
    if start_node.state.goal_test():
        return -1
    frontier = PriorityQueue()
    frontier.put((start_node.heuristic, start_node))
    explored = set()
    explored.add(start_node.hashed_state)
    #print(frontier)
    while not frontier.empty():
        current = frontier.get()
        current_node = current[1]
        current_node.heuristic = current[0]
        eval_value = current_node.heuristic
        action_list = current_node.state.actions()
        for action in action_list:
            print("Action:", action)
            child_node = Node(current_node)
            child_node = child_node.setChildNode(current_node, action)
            child_node.heuristic = manhattan(child_node, filename) + child_node.path_cost
            # print("manhattan distance is ", child_node.heuristic)
            print(child_node, "is our next child node.")
            if child_node.hashed_state not in explored:
                if child_node.state.goal_test():
                    print("We have found a goal state!")
                    path_cost = child_node.path_cost
                    num_nodes = len(explored)
                    print("Path cost: ", path_cost)
                    print("Number of expanded nodes: ", num_nodes)
                    end_time = time.time()
                    return end_time - start_time
                frontier.put((child_node.heuristic, child_node))
                print("We just enqueued", child_node)
                explored.add(child_node.hashed_state) # For the purposes of A*, we want to not add things to this until they're actually explored
            #return frontier
            print(current_node.state.mouse)

# def euclidean(state, filename):

def multi_astar(filename):
    pass


