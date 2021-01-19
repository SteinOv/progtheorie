from sys import argv, exit
from code.classes.board import Board
from code.stats.stats import get_stats
from code.visualization.output_3D import plot_output3D
from code.visualization.output_2D import plot_output2D
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

    # save all existing algorithms
    for filename in os.listdir('code/algorithms/'):
        if filename.endswith(".py") and not filename.startswith("__"):
            algorithms.append(filename[:-3])

    # prompt user for desired algorithm
    while True:
        print("Which algorithm would you like to run?")
        
        # display algorithms to choose from
        for algorithm in algorithms:
            print(algorithm)

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
    alg = import_module(f"code.algorithms.{algorithm}")
    alg_class = getattr(alg, algorithm)

    # get id's and folder
    chip_id, netlist_id = argv[1:3]
    folder = f"data/chip_{chip_id}"
    
    # get correct files
    chip_file = f"{folder}/print_{chip_id}.csv"
    netlist_file = f"{folder}/netlist_{netlist_id}.csv"

    # create board
    board = Board(chip_file, netlist_file)

    best_solution = board
    # find number of solution desired by user
    for i in range(n_solutions):
        # run algorithm and check how long it takes to find solution
        start = time.time()
        algorithm = alg_class(board)
        algorithm.run()
        total_time = time.time() - start
        
        # get the cost of this solution
        cost = algorithm.board.cost

        # check if best solution
        if cost < best_solution.cost or not best_solution.cost:
            best_solution = algorithm.board

        # filename for costs output
        costs_file = "costs.csv"


        # create stats folder
        stats_folder = "data/stats/"
        try:
            os.mkdir(stats_folder)
        except OSError:
            pass

        # write column names if file doesn't exist yet
        if costs_file not in os.listdir(stats_folder):
            with open(f"{stats_folder}{costs_file}", 'a') as file:
                file.write("costs,total_time,algorithm,chip_id_netlist_id")

        # write costs in file
        with open(f"{stats_folder}{costs_file}", 'a') as file:
            # costs, total_time, algorithm
            file.write(f"\n{cost}, {total_time}, {algorithm}, {chip_id}_{netlist_id}")


    # name of ouput file
    output_file = "output.csv"

    # write output file
    with open(f"{folder}/{output_file}", "w", newline='') as file:
        writer = csv.writer(file)

        # write header row
        writer.writerow(["net","wires"])

        # write net connections and routes
        for net in best_solution.nets:
            writer.writerow([str(net.connect).replace(" ", ""), str(net.route).replace(" ", "")])

        # TODO
        writer.writerow([f"chip_{chip_id}_net_{netlist_id}",best_solution.cost])

    # create output plot
    if best_solution.height > 0:
        plot_output3D(output_file, folder, best_solution)
    else:
        plot_output2D(output_file, folder)
        

if __name__ == "__main__":
    main()