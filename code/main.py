from sys import argv, exit
from board import Board
import csv


def main():

    # ensure proper usage
    if len(argv) != 3:
        print("Usage: python3 main.py <chip_id> <netlist_id> ")
        exit(1)
    
    chip_id, netlist_id = argv[1:]

    chip_file = f"../data/chip_{chip_id}/print_{chip_id}.csv"
    netlist_file = f"../data/chip_{chip_id}/netlist_{netlist_id}.csv"

    board = Board(chip_file, netlist_file)

    with open(f"../data/chip_{chip_id}/output.csv", "w") as file:
        writer = csv.writer(file)

        # write header row
        writer.writerow(["net", "wires"])

        # write net connections and routes
        for net in board.nets:
            writer.writerow([str(net.connect), str(net.route)])

        writer.writerow([f"chip_{chip_id}_net_{netlist_id}", board.cost])

    

        



if __name__ == "__main__":
    main()


'''

Net.route = [(3,4), (3,5), ...]

output: "(1,2)","[(1,5),(2,5),(3,5),(4,5),(5,5),(6,5)]"



'''