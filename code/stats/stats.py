import pandas as pd


def get_stats():
    """displays summary statistics per algorithm"""
    # read data
    df = pd.read_csv("./data/output/costs.csv")

    # print descriptive statistics
    print(df.groupby([df.chip_id_netlist_id, df.algorithm]).agg(
        ['std', 'mean', 'median', 'min', 'max']
        ))
