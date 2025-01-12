import os
import pandas as pd
import yaml


class DataManagement:
    def __init__(self):
        self.path = os.path.join("database")
        with open(os.path.join(self.path, "info.yaml"), "r", encoding="utf8") as f:
            self.conf = yaml.safe_load(f)

        self.loaded_data = {}

    def get_data_names(self):
        return list(self.conf["databases"].keys())

    def read_data(self, data_name):
        if data_name in self.loaded_data:
            return self.loaded_data[data_name]

        data_file = self.conf["databases"][data_name]
        path = os.path.join(self.path, f"{data_file}.csv")
        df = pd.read_csv(path)
        self.loaded_data[data_name] = df


        setattr(self, data_name, df)
        return df

    def get_loaded_data(self):
        return self.loaded_data
