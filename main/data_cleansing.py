import pandas as pd

def get_pd():
    # df = pd.read_csv('./data.csv') # Read csv file into a pandas dataframe
    df = pd.read_csv('main/data2.csv') # Read csv file into a pandas dataframe
    # df = remove_gb_suffix(df, 'Ram') # Remove GB suffix from Ram column
    # drop_columns(df, ['index', 'Product Name','Product URL', 'Brand','Upc', 'Star Rating'])
    drop_columns(df, ['Product_id'])
    # multiply_columns(df, 'Price', 'Sale')
    # df['Ram'] = pd.to_numeric(df['Ram'], errors='coerce')
    return df

def drop_columns(df, drop_columns):
    df = df.drop(drop_columns, axis=1)
    return df

def remove_gb_suffix(df, column_name):
    df[column_name] = df[column_name].str.replace(' GB', '')
    return df

# Remove rows with value from column_name
def remove_row (df, column_name, value):
    df = df[df[column_name] != value]
    return df

def multiply_columns(df, col1, col2):
    # Check if the columns exist in the DataFrame
    if col1 in df.columns and col2 in df.columns:
        # Multiply the columns element-wise and create a new column
        # df[f"{col1}_{col2}_product"] = df[col1] * df[col2]
        df[col1] = df[col1] * df[col2]
    else:
        print(f"Columns {col1} and {col2} not found in the DataFrame.")

# Function to extract numeric value from Ram column
def extract_ram_numeric(ram):
    return int(''.join(filter(str.isdigit, ram)))
