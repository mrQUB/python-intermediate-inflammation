"""Module containing mechanism for calculating standard deviation between datasets.
"""

import glob
import os
import numpy as np
from inflammation import models, views


class CSVDataSource:
    """
    Loads all the inflammation CSV files within a specified directory.
    """

    def __init__(self, dir_path):
        self.dir_path = dir_path

    def load_inflammation_data(self):
        data_file_paths = glob.glob(os.path.join(self.dir_path, 'inflammation*.csv'))
        if len(data_file_paths) == 0:
            raise ValueError(f"No inflammation CSV files found in path {self.dir_path}")
        data = map(models.load_csv, data_file_paths)
        return list(data)


class JSONDataSource:
    """
    Loads patient data with inflammation values from JSON files within a specified folder.
    """

    def __init__(self, dir_path):
        self.dir_path = dir_path

    def load_inflammation_data(self):
        data_file_paths = glob.glob(os.path.join(self.dir_path, 'inflammation*.json'))
        if len(data_file_paths) == 0:
            raise ValueError(f"No inflammation JSON files found in path {self.dir_path}")
        data = map(models.load_json, data_file_paths)
        return list(data)


def compute_standard_deviation_by_data(data):
    means_by_day = map(models.daily_mean, data)
    means_by_day_matrix = np.stack(list(means_by_day))
    daily_standard_deviation = np.std(means_by_day_matrix, axis=0)
    return daily_standard_deviation


def analyse_data(data_source):
    data = data_source.load_inflammation_data()
    daily_standard_deviation = compute_standard_deviation_by_data(data)
    return daily_standard_deviation


def controller(infiles):
    _, extension = os.path.splitext(infiles[0])
    if extension == '.json':
        data_source = JSONDataSource(os.path.dirname(infiles[0]))
    elif extension == '.csv':
        data_source = CSVDataSource(os.path.dirname(infiles[0]))
    else:
        raise ValueError(f'Unsupported data file format: {extension}')
    data_result = analyse_data(data_source)
    return data_result


def view(data_result):
    graph_data = {'standard deviation by day': data_result}
    views.visualize(graph_data)
