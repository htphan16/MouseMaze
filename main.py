import copy
import time
from EnvState import *
from Node import *
from search import *

def main(filename, search):
	print(search(filename))

main('1prize-large.txt', single_astar)

