# %% 
from sys import argv, exit
from classes.board import Board
from visualization.output_3D import plot_output3D
from visualization.output_2D import plot_output2D
import csv
from importlib import import_module
import os


def main():
    """run the main program"""
    # ensure proper usage
    if not (len(argv) in [2, 3]):
        print("Usage: python3 main.py <chip_id> <netlist_id>")
        exit(1)

    algorithms = []

    for filename in os.listdir('algorithms/'):
        if filename.endswith(".py"):
            algorithms.append(filename[:-3])

    # prompt user for desired algorithm
    print("Which algorithm would you like to run?")
    print(algorithms)
    command = input("> ")

    if command in algorithms:
        algorithm = str(command)

    # prompt user for desired number of solutions
    print("How many solutions do you want to generate?")
    n_solutions = int(input("> "))


    # TODO
    chip_id, netlist_id = argv[1:3]
    folder = f"../data/chip_{chip_id}"
    

    # TODO
    chip_file = f"{folder}/print_{chip_id}.csv"
    netlist_file = f"{folder}/netlist_{netlist_id}.csv"
    

    # TODO
    board = Board(chip_file, netlist_file)

    for i in range(n_solutions):
        # Run algorithm
        alg = import_module(f"algorithms.{algorithm}")
        alg_func = getattr(alg, algorithm)
        alg_func(board)


    # TODO
    output_file = "output.csv"


    with open(f"{folder}/{output_file}", "w") as file:
        writer = csv.writer(file)

        # write header row
        writer.writerow(["net", "wires"])

        # write net connections and routes
        for net in board.nets:
            writer.writerow([str(net.connect), str(net.route)])

        # TODO
        writer.writerow([f"chip_{chip_id}_net_{netlist_id}", board.cost])

    # create output plot
    if board.height > 0:
        plot_output3D(output_file, folder, board)
    else:
        plot_output2D(output_file, folder)
    


if __name__ == "__main__":
    main()