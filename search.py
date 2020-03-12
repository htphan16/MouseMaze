import copy
import time
from envState import Maze
from envState import Cell
from Node import Node

### Adapted from array_stack
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


# Error: it runs forever

def single_dfs(filename):
    start_time = time.time()
    # output = copy.deepcopy(filename)
    # fn = output.replace('prize', 'prize_out')
    # outfile = open('test.txt','w')
    cell = Cell(Maze(filename)) # Make it clear that this is the initial state
    num_nodes = 0
    start_node = Node(cell.initial()) # This node represents the initial state
    if start_node.state.goal_test():
        # outfile.write(start_node.state.mouse)
        # path_cost = start_node.path_cost
        # num_nodes = 1
        return -1
        # return outfile, path_cost, num_nodes
    frontier = Stack()
    frontier.insert(start_node)
    explored = set()
    explored.add(start_node.hashed_state)
    while not frontier.is_empty():
        current_node = frontier.pop()
        action_list = current_node.state.actions()
        print("Action_list:", action_list)
        for action in action_list:
            print("Action:", action)
            # Figure out how to create a new node here, for the child
            # and then later make current_node that child's parent
            child_node = Node(current_node)    # Take a look at this line, and make sure that we're making
            # a new child get enqueued, and not current_node again
            child_node = child_node.setChildNode(current_node, action)
            print(child_node, "is our next child node.")
            print(child_node.state.mouse)
            print("Testing:", (child_node.hashed_state not in explored))
            print(child_node.hashed_state)
            print(explored)
            if child_node.hashed_state not in explored:
                if child_node.state.goal_test():
                    print("We have found a goal state!")
                    # outfile.write(child_node.state.mouse)
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

print(single_dfs('1prize-large.txt'))

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

# Error: it runs in a circle

def single_bfs(filename):
    start_time = time.time()
    # output = copy.deepcopy(filename)
    # fn = output.replace('prize', 'prize_out')
    # outfile = open('test.txt','w')
    cell = Cell(Maze(filename)) # Make it clear that this is the initial state
    num_nodes = 0
    start_node = Node(cell.initial()) # This node represents the initial state
    if start_node.state.goal_test():
        # outfile.write(start_node.state.mouse)
        # path_cost = start_node.path_cost
        # num_nodes = 1
        return -1
        # return outfile, path_cost, num_nodes
    frontier = Queue()
    frontier.enqueue(start_node)
    explored = set()
    explored.add(start_node.hashed_state)
    while not frontier.is_empty():
        current_node = frontier.dequeue()
        action_list = current_node.state.actions()
        print("Action_list:", action_list)
        for action in action_list:
            print("Action:", action)
            # Figure out how to create a new node here, for the child
            # and then later make current_node that child's parent
            child_node = Node(current_node)    # Take a look at this line, and make sure that we're making
            # a new child get enqueued, and not current_node again
            child_node = child_node.setChildNode(current_node, action)
            print(child_node, "is our next child node.")
            print(child_node.state.mouse)
            print("Testing:", (child_node.hashed_state not in explored))
            print(child_node.hashed_state)
            print(explored)
            if child_node.hashed_state not in explored:
                if child_node.state.goal_test():
                    print("We have found a goal state!")
                    # outfile.write(child_node.state.mouse)
                    path_cost = child_node.path_cost
                    num_nodes = len(explored)
                    print("Path cost: ", path_cost)
                    print("Number of expanded nodes: ", num_nodes)
                    end_time = time.time()
                    return end_time - start_time
                    # return outfile, path_cost, num_nodes
                frontier.enqueue(child_node)
                print("We just enqueued", child_node)
                explored.add(child_node.hashed_state) # For the purposes of A*, we want to not add things to this until they're actually explored
            print(current_node.state.mouse)

# print(single_bfs('1prize-large.txt'))

