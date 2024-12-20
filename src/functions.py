## Importing Libraries

import pandas as pd
import os
import sys
from scipy import stats
from scipy.stats import shapiro, levene
from scipy.stats import ttest_ind
from scipy.stats import mannwhitneyu
from scipy.stats import chi2_contingency
import seaborn as sns
#from IPython.display import display

## EDA and Data Transformation Functions:

def exploration(df):

    ## "Exploration Function for DataFrame (percentage of missing values, data types, unique values, number of duplicate records, and main statistics)" 
    ## (In the case of duplicates, we change to keep=False so that all occurrences are counted).

    df_info = pd.DataFrame()

    df_info["% missing"] = round(df.isna().sum()/df.shape[0]*100, 2).astype(str)+"%"
    df_info["% non-missing"] = round(df.notna().sum()/df.shape[0]*100, 2).astype(str)+"%"
    df_info["data_type"] = df.dtypes
    df_info["num_unique_values"] = df.nunique()

    print(f"""The DataFrame has {df.shape[0]} rows and {df.shape[1]} columns.
It has {df.duplicated().sum()} duplicate records, which accounts for {round(df.duplicated().sum()/df.shape[0]*100,2)}% of the data. 

There are {len(list(df_info[(df_info["% missing"] != "0.0%")].index))} columns with missing data, and they are: 
{list(df_info[(df_info["% missing"] != "0.0%")].index)}

And with no missing values, there are {len(list(df_info[(df_info["% missing"] == "0.0%")].index))} columns, and they are: 
{list(df_info[(df_info["% missing"] == "0.0%")].index)}


Below is a breakdown of missing data, data types, and the number of values:""")

    display(df_info.head())

    ## Check for categorical columns and display info for those columns
    col_categoricals = df.select_dtypes(include = "O").columns
    if len(col_categoricals) > 0: 
        print("Main statistics for categorical columns:")
        display(df.describe(include="O").T)
    
    else: 
        print("\nThe DataFrame does not have categorical columns. \n")

    ## Check for numerical columns and display info for those columns
    col_numerical = df.select_dtypes(exclude = "O").columns
    if len(col_numerical) > 0: 
        print("Main statistics for numerical columns:")
        display(df.describe(exclude="O").T)

    return df_info


### Function to transform column to date / time type and split the column in 2: 

def transform_datetime_columns(df, timestamp_column):
    """
    Transform a 'timestamp' column to datetime, and split it into two separate columns: 'date' and 'time'.
    Also, convert 'date' to datetime and 'time' to timedelta.

    Parameters:
    df (pandas.DataFrame): DataFrame containing the column to transform
    timestamp_column (str): The name of the column to transform (it will be split into 'date' and 'time')

    Returns:
    pandas.DataFrame: DataFrame with transformed columns
    """
    # Convert the timestamp column to datetime
    df[timestamp_column] = pd.to_datetime(df[timestamp_column], errors='coerce')
    
    # Split the 'timestamp' column into 'date' and 'time'
    df['date'] = df[timestamp_column].dt.date
    df['time'] = df[timestamp_column].dt.time

    # Convert 'date' column to datetime type (if needed)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Convert 'time' column to timedelta (if needed)
    df['time'] = pd.to_timedelta(df['time'].astype(str), errors='coerce')
    
    return df
