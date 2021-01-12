# Chips & Circuits

© 2021 "All Rights Reserved"


### Requirements
* UMLet (VSCode extension)
* Python 3+
* Matplotlib


### Usage

To use program, run in command line:
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
