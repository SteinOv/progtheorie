import pandas as pd

def get_stats():
    """displays summary statistics per algorithm"""
    # get the data
    df = pd.read_csv("stats/costs.csv")

    # print summary statistics
    print(df.groupby(df.algorithm).agg(['std', 'mean', 'median', 'min', 'max']))
