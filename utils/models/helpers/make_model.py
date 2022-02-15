from sklearn.compose import ColumnTransformer
from sklearn.ensemble import AdaBoostRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor


def adaboost_model(max_depth: int, n_estimators: int) -> Pipeline:
    """Creates a scikit learn pipeline for the given hyperparameters

    Args:
      max_depth(int): Max depth of the Decision Tree regressor
      n_estimators(int): Number of estimators of the Ada Booster

    Returns:

    """
    ct = ColumnTransformer(
        [("std", StandardScaler(), ["passenger_count", "distance"])],
        remainder="passthrough",
    )

    pipe = Pipeline([
        ("scaler", ct),
        (
            "estimator",
            AdaBoostRegressor(
                base_estimator=DecisionTreeRegressor(max_depth=max_depth),
                n_estimators=n_estimators,
            ),
        ),
    ])

    return pipe
