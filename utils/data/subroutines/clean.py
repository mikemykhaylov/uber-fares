import logging

from pandas import DataFrame

from utils.data.helpers import DataProcessor


class DataCleaner(DataProcessor):
    """This is a class representation of a data cleaner

    The class is used to instantiate a data cleaner that will clean
    the formatted data that is fed into it. It is essentially an
    :py:class:`utils.data.helpers.DataProcessor` with an additional cleaning method

    """

    @staticmethod
    def fill_missing_data(df: DataFrame):
        """Fills missing data with median values

        Returns:
            None

        """

        # For each column, if there is a missing value, fill it with the median of the column
        for col in df.columns:
            if df[col].isnull().sum() > 0:
                df[col] = df[col].fillna(df[col].median())

        return df

    def clip_outliers(self, df: DataFrame, column_list: list[str]):
        """Clips outliers from the data

        Returns:
            None

        """

        # For each column, clip it to +-1.5 * interquartile range
        for col in column_list:
            q1, q3 = df[col].quantile([0.25, 0.75])
            iqr = q3 - q1
            df[col] = df[col].clip(q1 - 1.5 * iqr, q3 + 1.5 * iqr)
            self.logger.info(f"Clipping {col} within numbers {q1 - 1.5 * iqr} and {q3 + 1.5 * iqr}")

        return df

    def clean_data(self):
        """Cleans formatted data by removing outliers

        Returns:
            None

        """
        df = self.df

        self.logger.info(f"Initial data shape: {df.shape}")

        df = self.fill_missing_data(df)

        # Filtering by such rules:
        # 1. Passengers can't be more than 6
        # 2. Fares have to be more than 0
        # 3. Distance has to be more than 0

        df = df[df['passenger_count'].between(1, 6)]
        self.logger.info(f"Data shape after removing invalid passengers: {df.shape}")

        df = df[df["fare"] > 0]
        self.logger.info(f"Data shape after removing invalid fares: {df.shape}")

        # We remove entries with non-positive distance
        df = df[(df["distance"] > 0)]
        self.logger.info(f"Data shape after removing zero- and impossible-distance trips: {df.shape}")

        # Because standard deviation is very affected by extreme outliers
        # it makes sense to get rid of them first before calculating z-score
        # Namely, all distances more than 100km (arbitrary limit)
        # can be considered incorrect

        df = df[df["distance"] <= 100]

        self.logger.info(f"Data shape after removing extreme distances: {df.shape}")

        # Another metric that is affected by extreme outliers is the price per km
        # We remove entries with price per km more than 10$/km (arbitrary limit)

        df = df[df['fare'] / df['distance'] <= 10]

        self.logger.info(f"Data shape after removing extreme prices per km: {df.shape}")

        df = self.clip_outliers(df, column_list=["lon0", "lat0", "lon1", "lat1", "distance", "fare"])

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
