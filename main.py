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
    """run main program"""
    # ensure proper usage
    if not (len(argv) in [2, 3]):
        print("Usage: python3 main.py <chip_id> <netlist_id>")
        print("or")
        print("Usage: python3 main.py stats")
        exit(1)
    
    # get statistics
    if argv[1] == 'stats':
        get_stats()
        exit(0)

    # list of algorithms
    algorithms = []

    # append existing algorithms
    for filename in os.listdir('code/algorithms/'):
        if filename.endswith(".py") and not filename.startswith("__"):
            algorithms.append(filename[:-3])

    # prompt user for desired algorithm
    while True:
        print("Which algorithm would you like to run?")
        
        # display algorithms
        for algorithm in algorithms:
            print(algorithm)

        # get user input
        command = input("> ")

        # check if algorithm exists
        if command in algorithms:
            algorithm = str(command)
            break
    
    # prompt user for desired number of solutions
    while True:
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

    # for every desired solution
    for i in range(n_solutions):
        # run algorithm and track time
        start = time.time()
        algorithm = alg_class(board)
        algorithm.run()
        total_time = time.time() - start
        
        # get cost of solution
        cost = algorithm.board.cost

        # check if best solution
        if cost < best_solution.cost or not best_solution.cost:
            best_solution = algorithm.board

        # filename for costs
        costs_file = "costs.csv"

        # create ouput folder
        output_folder = "data/output/"
        try:
            os.mkdir(output_folder)
        except OSError:
            pass

        # write header row
        if costs_file not in os.listdir(output_folder):
            with open(f"{output_folder}{costs_file}", 'a') as file:
                file.write("costs,total_time,algorithm,chip_id_netlist_id")

        # write costs
        with open(f"{output_folder}{costs_file}", 'a') as file:
            file.write(f"\n{cost}, {total_time}, {algorithm}, {chip_id}_{netlist_id}")

    # filename for output
    output_file = "output.csv"

    # write output
    with open(f"{output_folder}/{output_file}", "w", newline='') as file:
        writer = csv.writer(file)

        # write header row
        writer.writerow(["net","wires"])

        # write net connections and routes
        for net in best_solution.nets:
            writer.writerow([str(net.connect).replace(" ", ""),
                             str(net.route).replace(" ", "")])

        # write footer row
        writer.writerow([f"chip_{chip_id}_net_{netlist_id}", best_solution.cost])

    # create output plot
    if best_solution.height > 0:
        plot_output3D(output_file, output_folder, best_solution)
    else:
        plot_output2D(output_file, output_folder)
        

if __name__ == "__main__":
    main()