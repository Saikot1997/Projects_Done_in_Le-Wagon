class Olist():
    def __init__(self):
        pass
    def get_data(self):
        import os
        root_dir = os.path.dirname(os.path.dirname(__file__))
        csv_path = os.path.join(root_dir, "data", "csv")
        #import Panda
        import pandas as pd

        # list all files in csv folder
        file_names = [file for file in os.listdir(csv_path) if file.endswith(".csv")]

        data = {}
        for file in file_names:
            # create dataframe
            df = pd.read_csv(os.path.join(csv_path, file))
            # get key name
            key = file.replace(".csv", "").replace("_dataset", "").replace("olist_", "")

            # add dataframe to dictionary
            data[key] = df
        return data
