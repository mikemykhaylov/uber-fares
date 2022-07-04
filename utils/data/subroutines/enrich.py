import json
import logging
from datetime import date
from pathlib import Path

import numpy as np
from holidays import US
from shapely.geometry import Point, shape

from utils.data.helpers import DataProcessor


class DataEnricher(DataProcessor):
    """This is a class representation of a data enricher

    The class is used to instantiate a data enricher that will add additional
    features to the cleaned data that is fed into it. Specifically, it adds
    the pickup/drop-off neighborhoods, as well as the US Holidays. It is
    essentially an :py:class:`utils.data.helpers.DataProcessor` with an additional enriching method.

    Attributes:
        nyc_neighborhoods(dict): Dictionary of NYC Neighborhoods and their geolocation
        nyc_holidays(US): DataFrame of all past US holidays

    """

    def __init__(self, data_path, file_name):
        """Initializes the class and reads the external data in memory

        Args:
            data_path(str): Path to the file to read
            file_name(str): Name of the file to read

        """
        super().__init__(data_path, file_name)
        # We have to specify the absolute path, because this file can be called
        # both by UNIX make, making . the project directory, and as a module from
        # make_dataset.py, making . the file location
        project_dir = Path(__file__).resolve().parents[3]

        geojson_path = str(project_dir) + "/data/external/nyc_neighborhoods.geo.json"
        with open(geojson_path) as f:
            self.nyc_neighborhoods = json.load(f)

        self.nyc_holidays = US(state="NY")

    def enrich_data(self):
        """Adds NYC neighborhoods and US holidays to cleaned data
        for geographic and temporal data analysis

        Returns:
            None

        """
        df = self.df

        self.logger.info("Enriching with neighborhoods. This might take a while...")
        df = self.parallelize_dataframe(df, self.get_neighborhoods)

        self.logger.info("Enriching with US holidays. This might take a while...")
        df = self.parallelize_dataframe(df, self.get_holidays)
        self.df = df

    def get_neighborhoods(self, df):
        """Adds the pickup and drop-off neighborhoods to a portion of DataFrame.
        Used only with :py:meth:`utils.data.helpers.DataProcessor.parallelize_dataframe` due to lack of
        shapely methods vectorization

        Args:
          df(DataFrame): DataFrame

        Returns:
          DataFrame: DataFrame with NYC Neighborhoods

        """

        # Taken from https://stackoverflow.com/questions/20776205/point-in-polygon-with-geojson-in-python
        def get_neighborhood(point):
            """Calculates the neighborhood to which the point belongs

            Args:
              point(Point): Geographical point

            Returns:
              str: Neighborhood string or Outside NYC if out of bounds

            """
            for feature in self.nyc_neighborhoods["features"]:
                polygon = shape(feature["geometry"])
                if polygon.contains(point):
                    return feature["properties"]["neighborhood"]
            return "Outside NYC"

        pickup_neighborhoods = []
        dropoff_neighborhoods = []

        for i, row in df.iterrows():
            pickup_point = Point(row["lon0"], row["lat0"])
            pickup_neighborhood = get_neighborhood(pickup_point)
            pickup_neighborhoods.append(pickup_neighborhood)

            dropoff_point = Point(row["lon1"], row["lat1"])
            dropoff_neighborhood = get_neighborhood(dropoff_point)
            dropoff_neighborhoods.append(dropoff_neighborhood)

        df["pickup_neighborhood"] = pickup_neighborhoods
        df["dropoff_neighborhood"] = dropoff_neighborhoods
        return df

    def get_holidays(self, df):
        """Adds the column determining whether there is a US holiday on the day

        Args:
          df(DataFrame): DataFrame

        Returns:
          DataFrame: DataFrame with US Holidays

        """
        is_holiday = []

        for i, row in df[['year', 'month', 'day']].astype(int).iterrows():
            ride_date = date(row['year'], row['month'], row['day'])
            is_holiday.append(ride_date in self.nyc_holidays)

        df["is_holiday"] = np.array(is_holiday) * 1
        return df


def enrich_data():
    """Wraps the :py:class:`utils.data.subroutines.enrich.DataEnricher` for direct execution by Makefile

    Returns:
        None

    """
    logger = logging.getLogger(__name__)
    logger.info("Reading data")
    preprocessor = DataEnricher("data/interim", "2_further_exploration.csv")

    logger.info("Enriching data for geographical and temporal analysis")
    preprocessor.enrich_data()

    logger.info("Saving data")
    preprocessor.write_data("data/interim", "3_geo_exploration.csv")
