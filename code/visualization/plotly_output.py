# Import dependencies
import plotly.graph_objs as go
import plotly.express as px
import csv
import ast
import pandas as pd
    

def plot_output(output_csv, output_folder, board):

    # store coordinates of nets
    x_line = []      
    y_line = []
    z_line = []

    # open the output file
    with open(f"{output_folder}/{output_csv}") as f:
        for line in csv.reader(f):
            # skip first and last line
            if line[0][0] == '(':
                # convert string list to list
                coordinates = ast.literal_eval(line[1])

                # if no coordinates go to next net
                if not coordinates:
                    continue
                
                # seperate lists for each line/net
                x_line.append([])
                y_line.append([])
                z_line.append([])

                # seperate x, y coordinates for each net
                for x, y, z in coordinates:
                    x_line[-1].append(x)
                    y_line[-1].append(y)
                    z_line[-1].append(z)

    x = []
    y = []
    z = []
    name = []

    for i in range(len(x_line)):
        for j in range(len(x_line[i])):
            x.append(x_line[i][j])
            y.append(y_line[i][j])
            z.append(z_line[i][j])
            name.append(i)

    df = pd.DataFrame(dict(
        X=x, 
        Y=y, 
        Z=z,
        name=name
    ))

    fig = px.line_3d(df, x='X', y='Y', z='Z', line_group="name")
    

    fig.add_scatter3d(
            x=[board.gates[gate].loc[0] for gate in board.gates],
            y=[board.gates[gate].loc[1] for gate in board.gates],
            z=[board.gates[gate].loc[2] for gate in board.gates],
            mode="markers", 
            marker_symbol="square",
            marker_color="red"
            
        )

    fig.show()

    
    
    


    
