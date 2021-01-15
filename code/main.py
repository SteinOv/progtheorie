from sys import argv, exit
from classes.board import Board
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
        print("Usage: python3 main.py <chip_id> <netlist_id> ")
        exit(1)

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
    alg_cls = getattr(alg, algorithm)
    


    # get id's and folder
    chip_id, netlist_id = argv[1:3]
    folder = f"../data/chip_{chip_id}"
    
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
        algorithm = alg_cls(board)
        algorithm.run()
        total_time = time.time() - start
        
        # get the cost of this solution
        cost = algorithm.board.cost

        # check if best solution
        if cost < best_solution.cost or not best_solution.cost:
            best_solution = algorithm.board


        # write costs in file
        with open(f"{folder}/costs.csv", 'a') as file:
            # costs, total_time, seed
            file.write(f"\n{cost}, {total_time}, {algorithm}")


    # name of ouput file
    output_file = "output.csv"

    # write output file
    with open(f"{folder}/{output_file}", "w") as file:
        writer = csv.writer(file)

        # write header row
        writer.writerow(["net", "wires"])

        # write net connections and routes
        for net in best_solution.nets:
            writer.writerow([str(net.connect), str(net.route)])

        # TODO
        writer.writerow([f"chip_{chip_id}_net_{netlist_id}", best_solution.cost])

    # create output plot
    if best_solution.height > 0:
        plot_output3D(output_file, folder, best_solution)
    else:
        plot_output2D(output_file, folder)
        

if __name__ == "__main__":
    main()