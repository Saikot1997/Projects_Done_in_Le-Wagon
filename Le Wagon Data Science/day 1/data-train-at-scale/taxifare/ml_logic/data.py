import pandas as pd

from google.cloud import bigquery
from colorama import Fore, Style
from pathlib import Path

from taxifare.params import *

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw data by
    - assigning correct dtypes to each column
    - removing buggy or irrelevant transactions
    """
    # Compress raw_data by setting types to DTYPES_RAW
    df = df.astype(DTYPES_RAW)

    # Remove buggy transactions
    df = df.dropna()

    # Remove geographically irrelevant transactions (rows)
    LAT_MIN = -90.0
    LAT_MAX = 90.0
    LON_MIN = -180.0
    LON_MAX = 180.0
    df = df[(df["pickup_latitude"].between(LAT_MIN, LAT_MAX)) &
            (df["pickup_longitude"].between(LON_MIN, LON_MAX)) &
            (df["dropoff_latitude"].between(LAT_MIN, LAT_MAX)) &
            (df["dropoff_longitude"].between(LON_MIN, LON_MAX))]


    print("✅ data cleaned")

    return df
