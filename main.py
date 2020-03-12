import copy
import time
from envState import *
from Node import *
from single_bfs import *
from single_dfs import *
from single_gbfs import *
from single_astar import *

def main(filename, search):
	print(search(filename))

main(single_dfs('1-prize-open.txt'))

