# Chips & Circuits

© 2021 "All Rights Reserved"

This program contains several algorithms, which use heuristics to solve the Chips & Circuits problems. These problems contain multiple gates that have to be connected with wires. This connection between two gates is called a net. The goal of the problem is to place all nets in the most cost efficient manner. The nets are allowed to intersect, but are not allowed to overlap.

Costs are calculated as follows:
n = total length of all nets
k = number of intersections
Costs = n + 300 * k



### Requirements
* This codebase is written entirely in Python 3.8.
* The following extension is needed to visualize the ULM diagram:
    * UMLet (VSCode extension)
* Requirements.txt contains all necessary packages to run the code successfully. Install the requirements with the following command:
```
pip install -r requirements.txt 
```


### Usage
To use the program, run in the command line:

To find solutions
```
python3 main.py <chip_id> <netlist_id>
```

To get statistics
```
python3 main.py <chip_id> <netlist_id>
```
<br>

* User should save data in `data` folder
* Data should be stored in .csv format in folder `data/chip_<chip_id>/`
* Chip file: `print_<chip_id>.csv`
* Netlist file: `netlist_<netlist_id>.csv`
* See `data/chip_0/` for examples of input files
<br>

* Output is stored in folder `data/chip_<chip_id>/`
* Output consists of `output.csv` and `output_plot.png`

### Structure
* The following list describes the most important folders and files in the project, and where to find them: 
* /code: contains all the code of this project
    * /code/algorithms: contains the code for algorithms
    * /code/classes: contains the three classes required for this case
    * /code/visualisation: contains plotly code for visualization 
* /data: contains the various data files that are needed to fill and visualize the graph

## Contributors: 
* Samson van der Sande
* Anouk Hooijschuur
* Stein Overtoom 
