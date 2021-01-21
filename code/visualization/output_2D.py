import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import csv
import ast

def plot_output2D(output_csv, output_folder):
    """creates plot from output file"""
    # store connected gates
    gates = {}

    # store coordinates of nets
    x_line = []      
    y_line = []

    # open output file
    with open(f"{output_folder}/{output_csv}") as file:
        for line in csv.reader(file):
            # only read rows with coordinates
            if line[0][0] == '(':
                # convert list as string to list
                coordinates = ast.literal_eval(line[1])

                # if no coordinates skip row
                if not coordinates:
                    continue
                
                # seperate lists for each line/net
                x_line.append([])
                y_line.append([])

                # seperate x, y coordinates for each net TODO plot directly
                for x, y, z in coordinates:
                    x_line[-1].append(x)
                    y_line[-1].append(y)
                
                # tuple of connected gate numbers
                connected_gates = ast.literal_eval(line[0])

                # save connected gates and its coordinates
                gates[connected_gates[0]] = coordinates[0]
                gates[connected_gates[1]] = coordinates[-1]
                
    # create figure
    plt.figure()
    ax = plt.axes()

    # set size of grid
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))

    # create lines on plot
    for x, y in zip(x_line, y_line):
        ax.plot(x, y, c='b')

    # create gates on plot
    for gate in gates:
        x, y, z = gates[gate]
        ax.scatter(x, y, s=150, c='r', marker='s')

    # create plot with grid
    plt.grid()
    plt.show()

    # save plot
    plt.savefig(f"{output_folder}/output_plot")
