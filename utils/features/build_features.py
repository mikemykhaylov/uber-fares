import logging

import pandas as pd
from sklearn.preprocessing import StandardScaler

from utils.data.helpers import DataProcessor


class FeatureBuilder(DataProcessor):
    """This is a class representation of a feature builder

    The class is used to instantiate a feature builder that will turn enriched
    data into ML-ready features. It is essentially an :py:class:`utils.data.helpers.DataProcessor`
    with an additional feature building method.

    """

    def build_features(self):
        """Builds features for Machine Learning

        One-hot encodes categorical features, transforms year to years passed since 2008

        Returns:
            None

        """
        df = self.df

        # Some columns are not useful for analysis such as coordinates or day
        # Others cannot be present, because they are derived from
        # the predicted variable, like price/km. Therefore, both are removed
        self.logger.info("Removing unused columns")
        df = df.drop(columns=["lon0", "lat0", "lon1", "lat1", "day", "price_per_km"])
        df = df[[
            "year",
            "month",
            "weekday",
            "hour",
            "is_holiday",
            "pickup_neighborhood",
            "passenger_count",
            "distance",
            "dropoff_neighborhood",
            "fare",
        ]]

        df[["year"]] = df[["year"]] - 2008

        df[[
            "month",
            "weekday",
            "hour",
            "pickup_neighborhood",
            "dropoff_neighborhood",
        ]] = df[[
            "month",
            "weekday",
            "hour",
            "pickup_neighborhood",
            "dropoff_neighborhood",
        ]].astype("category")

        df = df.join(pd.get_dummies(df[[
            "month",
            "weekday",
            "hour",
            "pickup_neighborhood",
            "dropoff_neighborhood",
        ]]))

        df = df.drop(columns=df[[
            "month",
            "weekday",
            "hour",
            "pickup_neighborhood",
            "dropoff_neighborhood",
        ]])

        columns = df.columns.to_list()
        columns.remove('fare')
        columns.append('fare')

        df = df[columns]

        std = StandardScaler()

        df[["passenger_count", "distance"]] = std.fit_transform(df[["passenger_count", "distance"]])

        self.df = df


def build_features():
    """Wraps the :py:class:`utils.features.FeatureBuilder` for direct execution by Makefile

    Returns:
        None

    """
    logger = logging.getLogger(__name__)
    logger.info("Reading data")
    preprocessor = FeatureBuilder("data/interim", "3_geo_exploration.csv")

    logger.info("Building features")
    preprocessor.build_features()

    logger.info("Saving data")
    preprocessor.write_data("data/processed", "processed_features.csv")
