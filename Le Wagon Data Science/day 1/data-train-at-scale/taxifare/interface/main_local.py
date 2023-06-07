import numpy as np
import pandas as pd

from google.cloud import bigquery
from pathlib import Path
from colorama import Fore, Style
from dateutil.parser import parse

from taxifare.params import *
from taxifare.ml_logic.data import clean_data
from taxifare.ml_logic.preprocessor import preprocess_features
from taxifare.ml_logic.registry import save_model, save_results, load_model
from taxifare.ml_logic.model import compile_model, initialize_model, train_model



def preprocess_and_train(min_date:str = '2009-01-01', max_date:str = '2015-01-01') -> None:
    """
    - Query the raw dataset from Le Wagon's BigQuery dataset
    - Cache query result as a local CSV if it doesn't exist locally
    - Clean and preprocess data
    - Train a Keras model on it
    - Save the model
    - Compute & save a validation performance metric
    """

    print(Fore.MAGENTA + "\n ⭐️ Use case: preprocess_and_train" + Style.RESET_ALL)
    LOCAL_DATA_PATH = Path('~').joinpath(".lewagon", "mlops", "data").expanduser()
    GCP_PROJECT_WAGON = "wagon-public-datasets"
    BQ_DATASET = "taxifare"
    DATA_SIZE = "200k"  # raw_200k is a randomly sampled materialized view from "raw_all" data table
    MIN_DATE = '2009-01-01'
    MAX_DATE = '2015-01-01'
    COLUMN_NAMES_RAW = ('fare_amount',	'pickup_datetime', 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude', 'passenger_count')
    GCP_PROJECT = "wagon-bootcamp-383712"
    query = f"""
        SELECT {",".join(COLUMN_NAMES_RAW)}
        FROM {GCP_PROJECT_WAGON}.{BQ_DATASET}.raw_{DATA_SIZE}
        WHERE pickup_datetime BETWEEN '{MIN_DATE}' AND '{MAX_DATE}'
        ORDER BY pickup_datetime
        """

    # Retrieve `query` data from BigQuery or from `data_query_cache_path` if the file already exists!
    data_query_cache_path = Path(LOCAL_DATA_PATH).joinpath("raw", f"query_{MIN_DATE}_{MAX_DATE}_{DATA_SIZE}.csv")

    if data_query_cache_path.is_file():
        print("load local file...")
        df = pd.read_csv(data_query_cache_path, parse_dates=['pickup_datetime'])

    else:
        print("Querying Big Query server...")
        from google.cloud import bigquery

        client = bigquery.Client(project=GCP_PROJECT)
        query_job = client.query(query)
        result = query_job.result()
        df = result.to_dataframe()
    # Save it locally to accelerate the next queries!
    df.to_csv(data_query_cache_path, header=True, index=False)
    data = df

    # Clean data using data.py
    data = clean_data(data)

    # Create (X_train, y_train, X_val, y_val) without data leaks
    # No need for test sets, we'll report val metrics only
    split_ratio = 0.02 # About one month of validation data

    # YOUR CODE HERE
    test_length = int(len(data) * split_ratio)
    val_length = int((len(data) - test_length) * split_ratio)
    train_length = len(data) - val_length - test_length

    df_train = data.iloc[:train_length, :].sample(frac=1)
    df_val = data.iloc[train_length: train_length + val_length, :].sample(frac=1)

    X_train = df_train.drop("fare_amount", axis=1)
    y_train = df_train[["fare_amount"]]

    X_val = df_val.drop("fare_amount", axis=1)
    y_val = df_val[["fare_amount"]]


    # Create (X_train_processed, X_val_processed) using `preprocessor.py`
    # Luckily, our preprocessor is stateless: we can `fit_transform` both X_train and X_val without data leakage!
    # YOUR CODE HERE
    X_train_processed = preprocess_features(X_train)
    X_val_processed = preprocess_features(X_val)


    # Train a model on the training set, using `model.py`
    model = None
    learning_rate = 0.0005
    batch_size = 256
    patience = 2

    # YOUR CODE HERE
    input_shape = X_train_processed.shape[1:]
    model = initialize_model(input_shape)
    model = compile_model(model)
    history = train_model(model, X_train_processed, y_train, X_val_processed, y_val)


    # Compute the validation metric (min val_mae) of the holdout set
    val_mae = np.min(history.history['val_mae'])

    # Save trained model
    params = dict(
        learning_rate=learning_rate,
        batch_size=batch_size,
        patience=patience
    )

    save_results(params=params, metrics=dict(mae=val_mae))
    save_model(model=model)

    print("✅ preprocess_and_train() done")


def pred(X_pred: pd.DataFrame = None) -> np.ndarray:
    print(Fore.MAGENTA + "\n ⭐️ Use case: pred" + Style.RESET_ALL)

    if X_pred is None:
        X_pred = pd.DataFrame(dict(
            pickup_datetime=[pd.Timestamp("2013-07-06 17:18:00", tz='UTC')],
            pickup_longitude=[-73.950655],
            pickup_latitude=[40.783282],
            dropoff_longitude=[-73.984365],
            dropoff_latitude=[40.769802],
            passenger_count=[1],
        ))

    model = load_model()
    X_processed = preprocess_features(X_pred)
    y_pred = model.predict(X_processed)

    print(f"✅ pred() done")

    return y_pred


if __name__ == '__main__':
    try:
        preprocess_and_train()
        # preprocess()
        # train()
        pred()
    except:
        import sys
        import traceback

        import ipdb
        extype, value, tb = sys.exc_info()
        traceback.print_exc()
        ipdb.post_mortem(tb)
