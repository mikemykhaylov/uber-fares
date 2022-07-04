import logging

import joblib
import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV

from utils.models.helpers.make_model import adaboost_model


def train_model(input_path, output_path, mode, max_depth, n_estimators):
    """Trains the ML model and scores its performance

    Args:
      input_path(str): Path to the data folder
      output_path: Path to write the models to
      mode(str): Trainer mode, "train" is for training, "cv" for cross-validation, "grid" for grid search
      max_depth(int): Max depth of the Decision Tree regressor
      n_estimators(int): Number of estimators of the Ada Booster

    Returns:
        None

    """

    logger = logging.getLogger(__name__)
    logger.info("Training models from processed data")

    logger.info("Reading and converting data")
    df: DataFrame = pd.read_csv(f"{input_path}/processed_features.csv")

    X = df.iloc[:, :-1]
    Y = df.iloc[:, -1]

    model = adaboost_model(max_depth=max_depth, n_estimators=n_estimators)

    if mode == "cv":
        logger.info("Cross validating ML model. Go grab some coffee cause this will take some time...")
        r_squared = cross_val_score(model, X, Y, cv=5, n_jobs=-1).mean()
    else:
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

        if mode == "grid":
            parameters = {"estimator__base_estimator__max_depth": np.arange(20, 30)}
            model = GridSearchCV(model, parameters, n_jobs=-1)
            logger.info("Grid searching for ML model. Go grab some coffee cause this will take some time...")
        else:
            logger.info("Training ML model. Go grab some coffee cause this will take some time...")
        model.fit(X_train, Y_train)
        r_squared = model.score(X_test, Y_test)

    logger.info(f"Accuracy on test set is {r_squared}")

    if mode != "cv":
        logger.info("Saving ML model")

        model_name = "model.joblib"
        joblib.dump(model, f"{output_path}/{model_name}")
        logger.info("Model saved")
