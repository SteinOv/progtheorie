import plotly.graph_objs as go
import plotly.express as px
import csv
import ast
import pandas as pd


def plot_output3D(output_csv, output_folder, board):
    """creates plot from csv file"""
    # store coordinates of nets
    x_df = []
    y_df = []
    z_df = []
    nets_df = []

    # open output file
    with open(f"{output_folder}/{output_csv}") as file:
        for i, line in enumerate(csv.reader(file)):
            # only read rows with coordinates
            if line[0][0] == '(':
                # convert list as string to list
                coordinates = ast.literal_eval(line[1])

                # if no coordinates skip row
                if not coordinates:
                    continue

                # add coordinates
                for x, y, z in coordinates:
                    x_df.append(x)
                    y_df.append(y)
                    z_df.append(z)
                    nets_df.append(i)

    # create dataframe
    df = pd.DataFrame(dict(X=x_df, Y=y_df, Z=z_df, nets=nets_df))

    # plot nets
    fig = px.line_3d(df, x='X', y='Y', z='Z', color="nets")
    
    # add gates to plot
    fig.add_scatter3d(
            x=[board.gates[gate].loc[0] for gate in board.gates],
            y=[board.gates[gate].loc[1] for gate in board.gates],
            z=[board.gates[gate].loc[2] for gate in board.gates],
            mode="markers+text",
            marker_symbol="square",
            marker_color="red",
            marker_size=12,
            text=list(range(1, len(board.gates) + 1)),
            textposition="middle center",
            name="gates"
        )

    # set grid steps
    fig.update_layout (
        scene = dict (
            xaxis = dict(dtick=1),
            yaxis = dict(dtick=1),
            zaxis = dict(dtick=1)
        )
    )
    # change font size
    fig.layout.font.size = 10

    # show plot
    fig.show()

    
    
    


    
