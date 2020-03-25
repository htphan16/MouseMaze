from EnvState import *
from Node import *
from search import *
from sys import argv

def main(filename, search, heuristic):
	try:
		if argv[2] == "single_dfs":
			search = single_dfs
			heuristic = None
			print(search(filename))
		elif argv[2] == "single_bfs":
			search = single_bfs
			heuristic = None
			print(search(filename))
		elif argv[2] == "single_gbfs":
			search = single_gbfs
			heuristic = None
			print(search(filename))
		elif argv[2] == "single_astar":
			search = single_astar
			heuristic = None
			print(search(filename))
		elif argv[2] == "multi_astar":
			search = multi_astar
			try:
				if argv[1] == 'multiprize-tiny.txt' or argv[1] == 'multiprize-micro.txt':
					filename = argv[1]
			except TypeError:
				print("Please enter the available heuristic names: multiprize-tiny.txt, multiprize-micro.txt\n")
			heuristic = None
			print(search(filename))
		elif argv[2] == "single_gbfs_with_heuristic":
			search = single_gbfs_with_heuristic
			try:
				if argv[3] == "manhattan":
					heuristic = manhattan
				elif argv[3] == "euclidean":
					heuristic = euclidean
				print(search(filename, heuristic))
			except TypeError:
				print("Please enter the available heuristic names: manhattan, euclidean\n")
		elif argv[2] == "single_astar_with_heuristic":
			search = single_astar_with_heuristic
			try:
				if argv[3] == "manhattan":
					heuristic = manhattan
				elif argv[3] == "euclidean":
					heuristic = euclidean
				print(search(filename, heuristic))
			except TypeError:
				print("Please enter the available heuristic names: manhattan, euclidean\n")
		
	except TypeError:
		print("Please enter the available search names: single_dfs, single_bfs, single_gbfs, single_astar, single_gbfs_with_heuristic, single_astar_with_heuristic\n")


if __name__ == '__main__':
    main(argv[1], argv[2], argv[3])

