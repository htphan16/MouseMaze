import copy
import time
from EnvState import Maze
from EnvState import Cell
from Node import Node
from queue import PriorityQueue
from math import sqrt
from random import random

### use Stack, Queue implementation for single_dfs, single_bfs
### use built-in method PriorityQueue for single_gbfs, single_astar and multi_astar

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


'''function to display path and output a file of maze with path marked by #'s'''
def display_path(filename, search, cur_node):
    cell = Cell(Maze(filename))
    initial_node = Node(cell.initial())
    mouse_pos = []
    while cur_node.state.mouse != initial_node.state.mouse:
        mouse_pos.append(cur_node.state.mouse)
        cur_node = cur_node.parent
    maze = Maze(filename).getMaze()
    new_maze = []
    outfile_name = "{}-out-{}.txt".format(filename.strip('.txt'), search)
    for i in range(len(maze)):
        line = []
        for j in range(len(maze[i])):
            if ([j, i]) in mouse_pos:
                line.append("#")
            else:
                if maze[i][j] == '%':
                    line.append('%')
                elif maze[i][j] == ' ':
                    line.append(' ')
                elif maze[i][j] == 'P':
                    line.append('P')
                elif maze[i][j] == '.':
                    line.append('.')
        new_maze.append(line)
    with open(outfile_name, 'w') as outfile:
        for line in new_maze:
            for char in line:
                outfile.write(char)
            outfile.write('\n')
    return new_maze

### Part 2: single_dfs
def single_dfs(filename):
    start_time = time.time()
    cell = Cell(Maze(filename))
    num_nodes = 0
    start_node = Node(cell.initial())
    if start_node.state.goal_test():
        print("We have found a goal state!")
        print("Path is as follows:")
        print(display_path(filename, 'single_dfs', start_node))
        path_cost = start_node.path_cost
        num_nodes = len(explored)
        print("Path cost: ", path_cost)
        print("Number of expanded nodes: ", num_nodes)
        end_time = time.time()
        print("Time taken is: ")
        return end_time - start_time
    frontier = Stack()
    frontier.insert(start_node)
    explored = set()
    explored.add(start_node.hashed_state)
    while not frontier.is_empty():
        current_node = frontier.pop()
        action_list = current_node.state.actions()
        for action in action_list:
            # print("Action:", action)
            child_node = Node(current_node) 
            child_node = child_node.setChildNode(current_node, action)
            if child_node.hashed_state not in explored:
                if child_node.state.goal_test():
                    print("We have found a goal state!")
                    print("Path is as follows:")
                    print(display_path(filename, 'single_dfs', child_node))
                    path_cost = child_node.path_cost
                    num_nodes = len(explored)
                    print("Path cost: ", path_cost)
                    print("Number of expanded nodes: ", num_nodes)
                    end_time = time.time()
                    print("Time taken is: ")
                    return end_time - start_time
                frontier.insert(child_node)
                # print("We just enqueued", child_node)
            explored.add(child_node.hashed_state)

### Part 3: single_bfs, single_gbfs, single_astar
def single_bfs(filename):
    start_time = time.time()
    cell = Cell(Maze(filename)) 
    start_node = Node(cell.initial()) 
    if start_node.state.goal_test():
        print("We have found a goal state!")
        print("Path is as follows:")
        print(display_path(filename, 'single_bfs', start_node))
        path_cost = start_node.path_cost
        num_nodes = len(explored)
        print("Path cost: ", path_cost)
        print("Number of expanded nodes: ", num_nodes)
        end_time = time.time()
        print("Time taken is: ")
        return end_time - start_time
    frontier = Queue()
    frontier.enqueue(start_node)
    explored = set()
    explored.add(start_node.hashed_state)
    while not frontier.is_empty():
        current_node = frontier.dequeue()
        action_list = current_node.state.actions()
        for action in action_list:
            # print("Action:", action)
            child_node = Node(current_node)
            child_node = child_node.setChildNode(current_node, action)
            if child_node.hashed_state not in explored:
                if child_node.state.goal_test():
                    print("We have found a goal state!")
                    print("Path is as follows:")
                    print(display_path(filename, 'single_bfs', child_node))
                    path_cost = child_node.path_cost
                    num_nodes = len(explored)
                    print("Path cost: ", path_cost)
                    print("Number of expanded nodes: ", num_nodes)
                    end_time = time.time()
                    print("Time taken is: ")
                    return end_time - start_time
                frontier.enqueue(child_node)
                # print("We just enqueued", child_node)
            explored.add(child_node.hashed_state)
             
### calculate manhattan distance from current position to goal 
def manhattan(cur_node, filename):
    cell = Cell(Maze(filename))
    initial_node = Node(cell.initial())
    cur_node.heuristic = abs(cur_node.state.mouse[0] - initial_node.state.prize[0][0]) + abs(cur_node.state.mouse[1] - initial_node.state.prize[0][1])
    return cur_node.heuristic

def euclidean(cur_node, filename):
    cell = Cell(Maze(filename))
    initial_node = Node(cell.initial())
    cur_node.heuristic = sqrt((cur_node.state.mouse[0] - initial_node.state.prize[0][0])**2 + (cur_node.state.mouse[1] - initial_node.state.prize[0][1])**2)
    return cur_node.heuristic

def euclidean_multi(cur_node, filename):
    cell = Cell(Maze(filename))
    initial_node = Node(cell.initial())
    cur_node.heuristic = sqrt((cur_node.state.mouse[0] - initial_node.state.prize[0][0])**2 + (cur_node.state.mouse[1] - initial_node.state.prize[0][1])**2)
    for prize in cur_node.state.prize:
        cur_node.heuristic = min(cur_node.heuristic, sqrt((cur_node.state.mouse[0] - prize[0])**2 + (cur_node.state.mouse[1] - prize[1])**2) + random())
    return cur_node.heuristic

def single_gbfs(filename):
    start_time = time.time()
    cell = Cell(Maze(filename)) 
    start_node = Node(cell.initial())
    start_node.heuristic = manhattan(start_node, filename)
    if start_node.state.goal_test():
        print("We have found a goal state!")
        print("Path is as follows:")
        print(display_path(filename, 'single_gbfs', start_node))
        path_cost = start_node.path_cost
        num_nodes = len(explored)
        print("Path cost: ", path_cost)
        print("Number of expanded nodes: ", num_nodes)
        end_time = time.time()
        print("Time taken is: ")
        return end_time - start_time
    frontier = PriorityQueue()
    frontier.put((start_node.heuristic, start_node))
    explored = set()
    explored.add(start_node.hashed_state)
    while not frontier.empty():
        current = frontier.get()
        current_node = current[1]
        current_node.heuristic = current[0]
        action_list = current_node.state.actions()
        for action in action_list:
            # print("Action:", action)
            child_node = Node(current_node)
            child_node = child_node.setChildNode(current_node, action)
            child_node.heuristic = manhattan(child_node, filename)
            if child_node.hashed_state not in explored:
                if child_node.state.goal_test():
                    print("We have found a goal state!")
                    print("Path is as follows:")
                    print(display_path(filename, 'single_gbfs', child_node))
                    path_cost = child_node.path_cost
                    num_nodes = len(explored)
                    print("Path cost: ", path_cost)
                    print("Number of expanded nodes: ", num_nodes)
                    end_time = time.time()
                    print("Time taken is: ")
                    return end_time - start_time
                frontier.put((child_node.heuristic, child_node))
                # print("We just enqueued", child_node)
            explored.add(child_node.hashed_state)

def single_gbfs_with_heuristic(filename, heuristic):
    start_time = time.time()
    cell = Cell(Maze(filename)) 
    start_node = Node(cell.initial())
    start_node.heuristic = heuristic(start_node, filename)
    if start_node.state.goal_test():
        print("We have found a goal state!")
        print("Path is as follows:")
        print(display_path(filename, 'single_gbfs_with_heuristic', start_node))
        path_cost = start_node.path_cost
        num_nodes = len(explored)
        print("Path cost: ", path_cost)
        print("Number of expanded nodes: ", num_nodes)
        end_time = time.time()
        print("Time taken is: ")
        return end_time - start_time
    frontier = PriorityQueue()
    frontier.put((start_node.heuristic, start_node))
    explored = set()
    explored.add(start_node.hashed_state)
    while not frontier.empty():
        current = frontier.get()
        current_node = current[1]
        current_node.heuristic = current[0]
        action_list = current_node.state.actions()
        for action in action_list:
            # print("Action:", action)
            child_node = Node(current_node)
            child_node = child_node.setChildNode(current_node, action)
            child_node.heuristic = heuristic(child_node, filename)
            if child_node.hashed_state not in explored:
                if child_node.state.goal_test():
                    print("We have found a goal state!")
                    print("Path is as follows:")
                    print(display_path(filename, 'single_gbfs_with_heuristic', child_node))
                    path_cost = child_node.path_cost
                    num_nodes = len(explored)
                    print("Path cost: ", path_cost)
                    print("Number of expanded nodes: ", num_nodes)
                    end_time = time.time()
                    print("Time taken is: ")
                    return end_time - start_time
                frontier.put((child_node.heuristic, child_node))
                # print("We just enqueued", child_node)
            explored.add(child_node.hashed_state)

def single_astar(filename):
    start_time = time.time()
    cell = Cell(Maze(filename)) 
    num_nodes = 0
    start_node = Node(cell.initial()) 
    start_node.heuristic = manhattan(start_node, filename) + start_node.path_cost
    if start_node.state.goal_test():
        print("We have found a goal state!")
        print("Path is as follows:")
        print(display_path(filename, 'single_astar', start_node))
        path_cost = start_node.path_cost
        num_nodes = len(explored)
        print("Path cost: ", path_cost)
        print("Number of expanded nodes: ", num_nodes)
        end_time = time.time()
        print("Time taken is: ")
        return end_time - start_time
    frontier = PriorityQueue()
    frontier.put((start_node.heuristic, start_node))
    explored = set()
    explored.add(start_node.hashed_state)
    while not frontier.empty():
        current = frontier.get()
        current_node = current[1]
        current_node.heuristic = current[0]
        action_list = current_node.state.actions()
        for action in action_list:
            # print("Action:", action)
            child_node = Node(current_node)
            child_node = child_node.setChildNode(current_node, action)
            child_node.heuristic = manhattan(child_node, filename) + child_node.path_cost
            if child_node.hashed_state not in explored:
                if child_node.state.goal_test():
                    print("We have found a goal state!")
                    print("Path is as follows:")
                    print(display_path(filename, 'single_astar', child_node))
                    path_cost = child_node.path_cost
                    num_nodes = len(explored)
                    print("Path cost: ", path_cost)
                    print("Number of expanded nodes: ", num_nodes)
                    end_time = time.time()
                    print("Time taken is: ")
                    return end_time - start_time
                frontier.put((child_node.heuristic, child_node))
                # print("We just enqueued", child_node)
            explored.add(child_node.hashed_state)

def single_astar_with_heuristic(filename, heuristic):
    start_time = time.time()
    cell = Cell(Maze(filename)) 
    num_nodes = 0
    start_node = Node(cell.initial()) 
    start_node.heuristic = heuristic(start_node, filename) + start_node.path_cost
    if start_node.state.goal_test():
        print("We have found a goal state!")
        print("Path is as follows:")
        print(display_path(filename, 'single_astar_with_heuristic', start_node))
        path_cost = start_node.path_cost
        num_nodes = len(explored)
        print("Path cost: ", path_cost)
        print("Number of expanded nodes: ", num_nodes)
        end_time = time.time()
        print("Time taken is: ")
        return end_time - start_time
    frontier = PriorityQueue()
    frontier.put((start_node.heuristic, start_node))
    explored = set()
    explored.add(start_node.hashed_state)
    while not frontier.empty():
        current = frontier.get()
        current_node = current[1]
        current_node.heuristic = current[0]
        action_list = current_node.state.actions()
        for action in action_list:
            # print("Action:", action)
            child_node = Node(current_node)
            child_node = child_node.setChildNode(current_node, action)
            child_node.heuristic = heuristic(child_node, filename) + child_node.path_cost
            if child_node.hashed_state not in explored:
                if child_node.state.goal_test():
                    print("We have found a goal state!")
                    print("Path is as follows:")
                    print(display_path(filename, 'single_astar_with_heuristic', child_node))
                    path_cost = child_node.path_cost
                    num_nodes = len(explored)
                    print("Path cost: ", path_cost)
                    print("Number of expanded nodes: ", num_nodes)
                    end_time = time.time()
                    print("Time taken is: ")
                    return end_time - start_time
                frontier.put((child_node.heuristic, child_node))
                # print("We just enqueued", child_node)
            explored.add(child_node.hashed_state)

### Part 4: In progress

def multi_astar(filename):
    start_time = time.time()
    cell = Cell(Maze(filename)) 
    num_nodes = 0
    nodes = []
    start_node = Node(cell.initial()) 
    start_node.heuristic = euclidean_multi(start_node, filename) + start_node.path_cost
    if start_node.state.goal_test():
        print("We have found a goal state!")
        print("Path is as follows:")
        print(display_path(filename, 'multi_astar', start_node))
        path_cost = start_node.path_cost
        num_nodes = len(explored)
        print("Path cost: ", path_cost)
        print("Number of expanded nodes: ", num_nodes)
        end_time = time.time()
        print("Time taken is: ")
        return end_time - start_time
    frontier = PriorityQueue()
    frontier.put((start_node.heuristic, start_node))
    ### nodes is the same as frontier, but only stores nodes and no heuristic values
    nodes.append(start_node)
    explored = set()
    explored.add(start_node.hashed_state)
    while not frontier.empty():
        current = frontier.get()
        current_node = current[1]
        nodes.remove(current_node)
        current_node.heuristic = current[0]
        action_list = current_node.state.actions()
        for action in action_list:
            print("Action:", action)
            child_node = Node(current_node)
            child_node = child_node.setChildNode(current_node, action)
            child_node.heuristic = euclidean_multi(child_node, filename) + child_node.path_cost
            print("eval value is ", child_node.heuristic)
            if child_node.hashed_state not in explored and child_node not in nodes:
                print("Testing: ", child_node.state.goal_test())
                if child_node.state.goal_test():
                    print("We have found a goal state!")
                    print("Path is as follows:")
                    print(display_path(filename, 'multi_astar', child_node))
                    path_cost = child_node.path_cost
                    num_nodes = len(explored)
                    print("Path cost: ", path_cost)
                    print("Number of expanded nodes: ", num_nodes)
                    end_time = time.time()
                    print("Time taken is: ")
                    return end_time - start_time
                frontier.put((child_node.heuristic, child_node))
                nodes.append(child_node)
                print("We just enqueued", child_node)
                print("number of prize left", len(current_node.state.prize))
                print(current_node.state.mouse)
            else:
                print("================")
        explored.add(child_node.hashed_state)
        print("Path cost: ", child_node.path_cost)

