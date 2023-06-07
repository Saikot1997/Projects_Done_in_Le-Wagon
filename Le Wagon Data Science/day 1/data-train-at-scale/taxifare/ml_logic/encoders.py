import math
import numpy as np
import pandas as pd
import pygeohash as gh

def transform_time_features(X: pd.DataFrame) -> np.ndarray:
    def extract_time_features(timestamp: str) -> list:
        dt = pd.to_datetime(timestamp)
        return [dt.weekday(), dt.month, dt.hour]

    time_features = np.array([extract_time_features(timestamp) for timestamp in X["pickup_datetime"]])
    return time_features


def transform_lonlat_features(X: pd.DataFrame) -> pd.DataFrame:
    def deg2rad(deg):
        return deg * (math.pi / 180)

    def distance(lat1, lon1, lat2, lon2):
        R = 6371  # Radius of the earth in km
        dlat = deg2rad(lat2 - lat1)
        dlon = deg2rad(lon2 - lon1)
        a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) * math.sin(
            dlon / 2) * math.sin(dlon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return distance

    X_transformed = X.copy()
    X_transformed["distance"] = distance(X["pickup_latitude"], X["pickup_longitude"], X["dropoff_latitude"],
                                         X["dropoff_longitude"])
    return X_transformed


def compute_geohash(X: pd.DataFrame, precision: int = 5) -> np.ndarray:
    """
    Add a geohash (ex: "dr5rx") of len "precision" = 5 by default
    corresponding to each (lon, lat) tuple, for pick-up, and drop-off
    """
    X_transformed = X.copy()
    X_transformed["pickup_geohash"] = X_transformed.apply(
        lambda row: gh.encode(row["pickup_latitude"], row["pickup_longitude"], precision=precision), axis=1)
    X_transformed["dropoff_geohash"] = X_transformed.apply(
        lambda row: gh.encode(row["dropoff_latitude"], row["dropoff_longitude"], precision=precision), axis=1)
    return X_transformed[["pickup_geohash", "dropoff_geohash"]].to_numpy()
