import copy
import time
from EnvState import *
from Node import *
from search import *

def main(filename, search):
	print(search(filename))

main('multiprize-tiny.txt', single_bfs2)

