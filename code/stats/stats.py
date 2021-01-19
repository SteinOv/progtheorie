import pandas as pd

def get_stats():
    """displays summary statistics per algorithm"""
    # get the data
    df = pd.read_csv("./data/stats/costs.csv")

    # print summary statistics
    print(df.groupby([df.chip_id_netlist_id, df.algorithm]).agg(['std', 'mean', 'median', 'min', 'max']))
