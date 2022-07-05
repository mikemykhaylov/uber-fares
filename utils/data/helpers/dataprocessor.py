import logging
import multiprocessing
from abc import ABC

import numpy as np
import pandas as pd
from pandas import DataFrame


class DataProcessor(ABC):
    """Abstract class for reading and writing data
    from the Kaggle Uber Fares dataset

    Attributes:
        df(DataFrame): DataFrame to be worked on
        logger(Logger): Logger instance to log events happening inside the class
    """

    def __init__(self, data_path, file_name):
        """Initializes the class and reads the DataFrame in the memory

        Args:
            data_path(str): Path to the file to read
            file_name(str): Name of the file to read

        """
        self.df: DataFrame = pd.read_csv(f"{data_path}/{file_name}")
        self.logger = logging.getLogger(__name__)

    def write_data(self, data_path, file_name):
        """Writes DataFrame to CSV.

        Args:
            data_path(str): Path to the file to write to
            file_name(str): Name of the file to write to

        Returns:
            None

        """
        self.df.to_csv(f"{data_path}/{file_name}", index=False)

    @staticmethod
    def parallelize_dataframe(df, func):
        """Parallelizes the mapping of the non-vectorized functions to the DataFrame

        Taken from https://stackoverflow.com/questions/40357434/pandas-df-iterrows-parallelization

        Args:
            df(DataFrame): DataFrame to parallelize
            func(function): Function to map

        Returns:
            DataFrame: Transformed DataFrame

        """
        num_cores = multiprocessing.cpu_count()
        num_partitions = num_cores
        df_split = np.array_split(df, num_partitions)
        with multiprocessing.Pool(num_cores) as pool:
            df = pd.concat(pool.map(func, df_split))
        return df
