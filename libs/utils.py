import pandas as pd




def rolling_mean(dataframe, cols, window_size):
    for col in cols:
        dataframe[f"{col}_{window_size}_average"] = dataframe[col].rolling(window=window_size).mean()

    return dataframe