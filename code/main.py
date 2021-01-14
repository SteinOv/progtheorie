from sys import argv, exit
from classes.board import Board
from stats.stats import get_stats
from visualization.output_3D import plot_output3D
from visualization.output_2D import plot_output2D
import csv
from importlib import import_module
import time
import os


def main():
    """run the main program"""
    
    # ensure proper usage
    if not (len(argv) in [2, 3]):
        print("Usage: python3 main.py <chip_id> <netlist_id>")
        print("or")
        print("Usage: python3 main.py stats")
        exit(1)
    
    if argv[1] == 'stats':
        get_stats()
        exit(0)


    algorithms = []

    # TODO
    for filename in os.listdir('algorithms/'):
        if filename.endswith(".py"):
            algorithms.append(filename[:-3])

    while True:
        # prompt user for desired algorithm
        print("Which algorithm would you like to run?")
        
        # display algorithms to choose from
        for algo in algorithms:
            print(algo)

        command = input("> ")

        # check if algorithm exists
        if command in algorithms:
            algorithm = str(command)
            break
    
    while True:
        # prompt user for desired number of solutions
        print("How many solutions do you want to generate?")

        # break if positive integer
        try:
            n_solutions = int(input("> "))
            if n_solutions > 0:
                break
        except:
            pass


    # import algorithm
    alg = import_module(f"algorithms.{algorithm}")
    alg_func = getattr(alg, algorithm)


    # get id's and folder
    chip_id, netlist_id = argv[1:3]
    folder = f"../data/chip_{chip_id}"
    
    # get correct files
    chip_file = f"{folder}/print_{chip_id}.csv"
    netlist_file = f"{folder}/netlist_{netlist_id}.csv"


    # find number of solution desired by user
    for i in range(n_solutions):
        # create a board to solve
        board = Board(chip_file, netlist_file) # TODO misschien niet elke keer een nieuwe board

        # run algorithm and check how long it takes to find solution
        start = time.time()
        alg_func(board)
        total_time = time.time() - start

        # get the cost of this solution
        cost = board.cost

        # filename for costs output
        costs_file = "costs.csv"

        # write column names if file doesn't exist yet
        if costs_file not in os.listdir(f'statistics/'):
            with open(f"statistics/{costs_file}", 'a') as file:
                file.write("costs,total_time,algorithm")

        # write costs in file
        with open(f"statistics/{costs_file}", 'a') as file:
            # costs, total_time, algorithm
            file.write(f"\n{cost}, {total_time}, {algorithm}")


    # name of ouput file
    output_file = "output.csv"

    with open(f"{folder}/{output_file}", "w") as file:
        writer = csv.writer(file)

        # write header row
        writer.writerow(["net", "wires"])

        # write net connections and routes
        for net in board.nets:
            writer.writerow([str(net.connect), str(net.route)])

        # TODO
        writer.writerow([f"chip_{chip_id}_net_{netlist_id}", cost])

    # create output plot
    if board.height > 0:
        plot_output3D(output_file, folder, board)
    else:
        plot_output2D(output_file, folder)
        

if __name__ == "__main__":
    main()