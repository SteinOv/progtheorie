# Import dependencies
import plotly
import plotly.graph_objs as go
import csv
import ast

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



    # Configure Plotly to be rendered inline in the notebook.
    plotly.offline.init_notebook_mode()

    # Configure the trace.
    trace = go.Scatter3d(
        x=[board.gates[gate].loc[0] for gate in board.gates],
        y=[board.gates[gate].loc[1] for gate in board.gates],
        z=[board.gates[gate].loc[2] for gate in board.gates],
        mode='markers',
        marker={
            'size': 10,
            'opacity': 0.8,
        }
    )

    # Configure the layout.
    layout = go.Layout(
        margin={'l': 0, 'r': 0, 'b': 0, 't': 0}
    )

    data = [trace]

    plot_figure = go.Figure(data=data, layout=layout)

    # Render the plot.
    plotly.offline.iplot(plot_figure)


    
