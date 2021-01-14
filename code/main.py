from sys import argv, exit
from classes.board import Board
from visualization.output_3D import plot_output3D
from visualization.output_2D import plot_output2D
import csv
from importlib import import_module
import time


def main():
    """run the main program"""
    # ensure proper usage
    if not (len(argv) in [3, 4]):
        print("Usage: python3 main.py <chip_id> <netlist_id> <algorithm (optional)> ")
        exit(1)

    # set algorithm to default if none is given
    if len(argv) == 4:
        algorithm = argv[3]
    else:
        algorithm = "basic"


    # get id's and folder
    chip_id, netlist_id = argv[1:3]
    folder = f"../data/chip_{chip_id}"
    
    # get correct files
    chip_file = f"{folder}/print_{chip_id}.csv"
    netlist_file = f"{folder}/netlist_{netlist_id}.csv"
    

    # create a board to solve
    board = Board(chip_file, netlist_file)

    # Run algorithm
    alg = import_module(f"algorithms.{algorithm}")
    alg_func = getattr(alg, algorithm)

    # run algorithm and check how long it takes to find solution
    seed = 500
    start = time.time()
    alg_func(board, seed)
    total_time = time.time() - start

    # get the cost of this solution
    # cost = board.cost
    cost = 602349

    # write costs in file
    with open(f"{folder}/costs.csv", 'a') as file:
        # costs, total_time, seed
        file.write(f"\n{cost}, {total_time}, {seed}, {algorithm}")


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