import csv
import random
from sys import argv, exit
from itertools import combinations
import pandas as pd


# ensure proper usage
if not len(argv) == 3:
    print("Usage: python3 random_netlist.py <chip_id> <netlist_id>")
    exit(1)

# get id's
chip_id = argv[1]
netlist_id = argv[2]

# store gates
gates = []

# print file
print_file = f"../../data/chip_{chip_id}/print_{chip_id}.csv"

# read print file
with open(print_file, 'r') as file:
    data = csv.reader(file)
    next(data)

    for line in data:
        gates.append(line[0])

# copy print file
df = pd.read_csv(print_file)
df.to_csv("../../data/chip_3/print_3.csv", index=False)

# find length of netlist
df = pd.read_csv(f"../../data/chip_{chip_id}/netlist_{netlist_id}.csv")
netlist_length = len(df.iloc[:, 0])
print("netlist contains", netlist_length, "nets")

# all possible nets
all_combinations = list(combinations(gates, 2))
print("number of possible nets", len(all_combinations))

# nets in netlist
nets = []

for i in range(netlist_length):
    # choose random net
    net = random.choice(all_combinations)
    all_combinations.remove(net)
    nets.append(net)


# write netlist file
with open("../../data/chip_3/netlist_10.csv", 'w') as file:
    writer = csv.writer(file)
    
    # write header row
    writer.writerow(["chip_a","chip_b"])

    # write net connection
    for net in nets:
        writer.writerow([int(net[0]), int(net[1])])






















