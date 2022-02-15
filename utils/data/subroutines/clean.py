import logging

import numpy as np
from scipy import stats

from utils.data.helpers import DataProcessor


class DataCleaner(DataProcessor):
    """This is a class representation of a data cleaner

    The class is used to instantiate a data cleaner that will clean
    the formatted data that is fed into it. It is essentially an
    :py:class:`utils.data.helpers.DataProcessor` with an additional cleaning method

    """

    def clean_data(self):
        """Cleans formatted data by removing outliers

        Returns:
            None

        """
        df = self.df

        self.logger.info(f"Initial data shape: {df.shape}")

        # Because standard deviation is very affected by extreme outliers
        # it makes sense to get rid of them first before calculating z-score
        # Namely, all distances more than 50km (arbitrary limit)
        # can be considered incorrect

        df = df[df["distance"] <= 50]

        # Furthermore, one particularly effective metric which can determine
        # whether the entry is incorrect is price/km. It obviously has to be
        # small, so we can remove entries where it's more than 15 (arbitrary)
        df = df[df["price_per_km"] <= 20]

        self.logger.info(f"Data shape after removing extreme outliers: {df.shape}")

        # Taken from https://stackoverflow.com/questions/23199796/detect-and-exclude-outliers-in-a-pandas-dataframe
        # These columns are prone to outliers, such as
        # 1. Latitude and longitude switching or near-zero values
        # 2. Huge or near-zero distances
        # 3. Huge or near-zero fares

        outliers_df = df[["lon0", "lat0", "lon1", "lat1", "distance", "price_per_km"]]
        df = df[(np.abs(stats.zscore(outliers_df)) < 3).all(axis=1)]
        self.logger.info(f"Data shape after removing outliers: {df.shape}")
        self.df = df


def clean_data():
    """Wraps the :py:class:`utils.data.subroutines.clean.DataCleaner` for direct execution by Makefile

    Returns:
        None

    """
    logger = logging.getLogger(__name__)
    logger.info("Reading data")
    preprocessor = DataCleaner("data/interim", "1_initial_exploration.csv")

    logger.info("Cleaning formatted data by removing outliers")
    preprocessor.clean_data()

    logger.info("Saving data")
    preprocessor.write_data("data/interim", "2_further_exploration.csv")
