# Data Analysis

# Statistical Analysis

import pandas as pd

def get_processedData():
    return pd.read_csv('linear_regression_results.csv')

def show_signi():
    df = get_processedData()
    df['Significance'] = ['*' if x <= 0.05 else '' for x in df['P-values']]
    print(df)
    return df