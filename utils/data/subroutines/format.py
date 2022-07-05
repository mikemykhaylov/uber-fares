import logging

import pandas as pd
from geopy import distance

from utils.data.helpers import DataProcessor


class DataFormatter(DataProcessor):
    """This is a class representation of a data formatter

    The class is used to instantiate a data formatter that will format the raw
    data that is fed into it. It is essentially an :py:class:`utils.data.helpers.DataProcessor`
    with an additional formatting method.

    """

    def format_data(self):
        """Formats and initially validates the raw data

        Returns:
            None

        """
        df = self.df

        # Key is just the entry id and unnamed is the same as pickup_datetime
        df = df.drop(["key", "Unnamed: 0"], axis=1, errors="ignore")

        self.logger.info(f"Initial data shape: {df.shape}")

        # Dropping duplicates
        df = df.drop_duplicates()

        self.logger.info(f"Data shape after removing duplicates: {df.shape}")

        # Convert to date and localize the timezone to NY time
        # This is important to see hourly patterns in NY
        df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"], format="%Y-%m-%d %H:%M:%S %Z")
        df["pickup_datetime"] = df["pickup_datetime"].dt.tz_convert("US/Eastern")

        # Extract  date information
        df["year"] = df["pickup_datetime"].dt.year
        df["month"] = df["pickup_datetime"].dt.month
        df["day"] = df["pickup_datetime"].dt.day
        df["hour"] = df["pickup_datetime"].dt.hour
        df["weekday"] = df["pickup_datetime"].dt.weekday
        df["weekend"] = df["weekday"].between(5, 6)

        df = df.drop(columns=["pickup_datetime"])

        # Convert passenger count to int

        df["passenger_count"] = df["passenger_count"].astype(int)

        # Shorten the names
        # Reminder: Latitude is y (-90, 90), longitude is x (-180, 180)
        df = df.rename(
            columns={
                "pickup_longitude": "lon0",
                "pickup_latitude": "lat0",
                "dropoff_longitude": "lon1",
                "dropoff_latitude": "lat1",
                "fare_amount": "fare",
            })

        # Filtering by such rules:
        # 1. Latitude has to be absolutely less than 90
        # 2. Longitude has to be absolutely less than 180
        # We do it here because the distance calculation is based on these values

        invalid_latitudes = (abs(df[["lat0", "lat1"]]) <= 90).all(axis=1)
        invalid_longitudes = (abs(df[["lon0", "lon1"]]) <= 180).all(axis=1)
        invalid_coordinates = invalid_latitudes & invalid_longitudes

        df = df[invalid_coordinates]
        self.logger.info(f"Data shape after removing invalid coordinates: {df.shape}")

        # For each entry we calculate the distance travelled
        self.logger.info("Calculating pickup to drop-off distances. This might take a while...")
        df = self.parallelize_dataframe(df, self.get_distances)

        # Reorder columns for convenience
        columns = df.columns.tolist()
        columns.remove("fare")
        columns.append("fare")

        df = df.reindex(columns=columns)

        self.logger.info(f"Final data shape: {df.shape}")
        self.df = df

    @staticmethod
    def get_distances(df):
        """Adds the distance between pickup and drop-off to a portion of DataFrame

        Args:
          df(DataFrame): DataFrame

        Returns:
          DataFrame: DataFrame with distances

        """
        distances = []
        for _, row in df.iterrows():
            distances.append(distance.distance((row["lat0"], row["lon0"]), (row["lat1"], row["lon1"])).km)
        df["distance"] = distances
        return df


def format_data():
    """Wraps the :py:class:`utils.data.subroutines.format.DataFormatter` for direct execution by Makefile

    Returns:
        None

    """
    logger = logging.getLogger(__name__)
    logger.info("Reading data")
    preprocessor = DataFormatter("data/raw", "uber.csv")

    logger.info("Formatting and initially validating the raw data")
    preprocessor.format_data()

    logger.info("Saving data")
    preprocessor.write_data("data/interim", "1_initial_exploration.csv")
