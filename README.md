# Uber Fares Data Science

Uber Fares is a Data Science and Machine Learning I worked on in my free time. Its goals were to analyse the dataset of 200k NYC Uber rides and build a model to predict the price of the trip.

[![MIT License](https://img.shields.io/github/license/mmykhaylov/uber-fares)](https://github.com/mmykhaylov/uber-fares/blob/main/LICENSE)
[![Netlify](https://img.shields.io/netlify/2da9b75f-d673-4a74-bedf-b3f18117d9bf)](https://app.netlify.com/sites/uber-fares-docs/deploys)
![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/mmykhaylov/uber-fares?sort=semver)

## Features

During the project development I have...

- Downloaded the dataset from [Kaggle](https://www.kaggle.com/yasserh/uber-fares-dataset/code/)
- Formatted, cleaned, and enriched the dataset with additional data (NYC Neighborhoods and US Holidays)
- Created qualitative, spacial and temporal visualisations with Seaborn
- Iterated through several ML algorithms such as Polynomial regression, ElasticNet and Decision trees
- Tuned hyperparameters and trained the model on Google Cloud

## Documentation

Documentation is hosted on Netlify and built on [Sphinx](https://uber-fares-docs.netlify.app/)

## Project Structure

```
    ├── data
    │   ├── external            <- Data from third party sources.
    │   ├── interim             <- Intermediate data that has been transformed.
    │   ├── processed           <- The final, canonical data sets for modeling.
    │   └── raw                 <- The original, immutable data dump.
    ├── docs                    <- Sphinx Docs; see sphinx-doc.org for details
    ├── functions               <- Google Cloud Functions code
    │   ├── actual-fare-fn      <- Function for getting fare from Uber API
    │   └── ml-prediction-fn    <- Function for the predicting the fare with ML model
    ├── gcloud                  <- Google Cloud Vertex AI configs
    │   ├── hp_config.yml       <- Hyperparameter Tuning config
    │   └── train_config.yml    <- Training config
    ├── models                  <- Trained and serialized models
    ├── notebooks               <- Jupyter notebooks for explorations
    │   ├── 0.1_data_processing_tests
    │   ├── 0.2_exploration
    │   └── 0.3_machine_learning
    ├── references              <- Data dictionaries, manuals, and all other explanatory materials.
    ├── reports                 <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures             <- Generated graphics and figures to be used in reporting
    ├── utils                   <- Source code for all analysis
    │   ├── data                <- Scripts to preprocess data for analysis
    │   ├── features            <- Scripts to build features
    │   ├── models              <- Scripts to train models
    │   └── visualization       <- Scripts to produce visualisations
    ├── environment.yml         <- Template for conda environment creation
    ├── Makefile                <- Makefile with commands like `make data` or `make model`
    ├── pyproject.toml          <- Python project config file for packaging for Vertex AI
    ├── README.md               <- The top-level README for developers using this project.
    ├── requirements.txt        <- Pip requirements
    ├── test_environment.py     <- Script for testing the correct environment setup
    └── tox.ini                 <- tox file with settings for running tox; see tox.readthedocs.io
```

## Acknowledgements

- [Cookiecutter Data Science Project](https://drivendata.github.io/cookiecutter-data-science/)
- [Readme.so](https://readme.so/)
