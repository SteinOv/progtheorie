# Chips & Circuits

© 2021 "All Rights Reserved"

This program contains several algorithms, which use heuristics to solve the Chips & Circuits problems. These problems contain multiple gates that have to be connected with wires. This connection between two gates is called a net. The goal of the problem is to place all nets in the most cost efficient manner. The nets are allowed to intersect, but are not allowed to overlap.

* :orange_circle: The orange line represents nets with a collision.
The green line represents an intersection.<br>
<img src="docs/images/Intersection and collision.png" alt="Intersection and collision" width="300px">

Costs are calculated as follows:<br>
n = total length of all nets<br>
k = number of intersections<br>
Cost = n + 300 * k<br>



### Requirements
* This codebase is written entirely in Python 3.8.
* The following extension is needed to visualize the UML diagram:
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
python3 main.py stats
```
<br>

* User should save data in `data` folder
* Data should be stored in .csv format in folder `data/chip_<chip_id>/`
* Chip file: `print_<chip_id>.csv`
* Netlist file: `netlist_<netlist_id>.csv`
* See `data/chip_0/` for examples of input files
<br>

* Output is stored in folder `data/stats/`
* Output consists of `output.csv` and `costs.csv`


### Algorithms
#### Basic algorithm
The Basic algorithm is based on the fastest possible route using the Manhattan Distance heuristic. It does not take intersections and collisions into account, therefore Basic does not find valid solutions. The costs of other algorithms can never be less than the costs resulting from the basic algorithm, so the costs of Basic can be seen as a lower bound for every other algorithm.
 

#### Bounded-Random algorithm
The Bounded-Random algorithm tries to find solutions to connect the gates one net at a time. The algorithm will try up to 500 times to find a solution for a specific net. If unsuccessful, the algorithm will reset. This maximum has been chosen because previous nets may have occupied so many locations that later nets cannot be solved.
 
The route of a net may deviate only 25 steps from the ideal route, which is based on the Manhattan Distance. To correct for the increased difficulty in placing consecutive nets, every consecutive net can deviate an extra 10 steps from the ideal route. Because of this constraint, solutions that require a higher deviation are not found by the algorithm.


#### A* algorithm
The A* algorithm finds the optimal solution for each individual net, but it does not take the routes of future nets into account. This results in a local optimum for the final solution.
 
The order in which the A* algorithm places nets, is passed in the algorithm as a parameter. The nets connected to the gates that have the most connections are laid first, because this will
increase the chance that the algorithm will find a solution where all the nets fit into the grid.

 
#### Hill Climber
Hill Climber is an optimization algorithm that starts with an existing solution, and then attempts to find a better solution by changing the prior solution step by step.

To eliminate as many intersections as possible, Hill Climber divides the nets into groups of three. For example, (0, 1, 2, 3, 4) is divided into (0, 1, 2), (1, 2, 3) and (2, 3, 4). For each group, all permutations are determined. For each permutation, the nets are placed with A* in that particular order. If a cost improvement is found, the original routes are replaced by the routes of the permutation with the lowest cost. The algorithm keeps searching for a better solution until no further improvements can be found.

After running the Hill Climber algorithm once, it will reach a local minimum. The algorithm can be run again, to reach a better local minimum. After several iterations it will reach a point where no better local minimum can be found. To prevent the algorithm from running indefinitely, the algorithm will stop searching if it does not find any cost improvement since the last iteration.





### Structure
* The following list describes the most important folders and files in the project, and where to find them: 
* /code: contains all the code of this project
    * /code/algorithms: contains the code for algorithms
    * /code/classes: contains the three classes required for this case
    * /code/visualisation: contains plotly code for visualization 
    * /code/stats: contains pandas code for statistics
* /data: contains the various data files that are needed to fill and visualize the graph
* /data/output: contains the output files
* /docs: contains the UML diagram <i>requires UMLet</i>

## Contributors: 
* Samson van der Sande
* Anouk Hooijschuur
* Stein Overtoom 
