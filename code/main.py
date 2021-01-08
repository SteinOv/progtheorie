from sys import argv, exit
from board import Board
from output import plot_output
import csv


def main():
    """run the main program"""
    # ensure proper usage
    if len(argv) != 3:
        print("Usage: python3 main.py <chip_id> <netlist_id> ")
        exit(1)
    
    # TODO
    chip_id, netlist_id = argv[1:3]
    folder = f"../data/chip_{chip_id}"

    # TODO
    chip_file = f"{folder}/print_{chip_id}.csv"
    netlist_file = f"{folder}/netlist_{netlist_id}.csv"

    # TODO
    board = Board(chip_file, netlist_file)

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
    plot_output(output_file, folder)


if __name__ == "__main__":
    main()