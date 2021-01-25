import csv
import random
from sys import argv, exit
from itertools import combinations
import pandas as pd


# ensure proper usage
if not len(argv) == 2:
    print("Usage: python3 random_netlist.py <chip_id>")
    exit(1)

# get chip id
chip_id = argv[1]

# store gates
gates = []

# read print file
with open(f"../../data/chip_{chip_id}/print_{chip_id}.csv", 'r') as file:
    data = csv.reader(file)
    next(data)

    for line in data:
        gates.append(line[0])


# copy print file
df = pd.read_csv(f"../../data/chip_{chip_id}/print_{chip_id}.csv")
df.to_csv("../../data/chip_3/print_3.csv", index=False)





# all possible nets
all_combinations = list(combinations(gates, 2))
print(len(all_combinations))

for i in all_combinations:
    print(i)

# nets in netlist
nets = []

for i in range(30):
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






















