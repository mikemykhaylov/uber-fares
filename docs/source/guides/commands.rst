Commands
========
The Makefile contains the central entry points for common tasks related to this project. If you want to directly call my modules, each of them exposes a CLI, which is usually used when code is run by a machine (like in the Google Cloud `Vertex AI <https://cloud.google.com/vertex-ai>`_  pipeline). Nevertheless, unless you really need to, leave the direct invocations to the machines and enjoy an assortment of scripts for your every need in this project.

Setup
-----

- ``environment``
    Set up python interpreter environment
- ``requirements``
    Install Python Dependencies
- ``test_environment``
    Test python environment is setup correctly

Data pipeline
-------------
- ``data``
    Process dataset through the whole pipeline
- ``data-format``
    Format raw data by standardizing data, extracting and calculating useful metrics
- ``data-clean``
    Clean formatted data by removing outliers
- ``data-enrich``
    Enrich clean data by adding data from external datasets (NYC Neighborhoods and US Holidays)
- ``features``
    Create features

Model Training
--------------
- ``model``
    Train model
- ``vertex_hp_train``
    Run custom training job on Google Cloud Vertex AI
- ``vertex_hp_tune``
    Run hyperparameter tuning job on Google Cloud Vertex AI

Google Cloud Storage
--------------------
- ``gcs_data_pull``
    Download data from Google Cloud Storage
- ``gcs_data_pull_raw``
    Download raw data from Google Cloud Storage
- ``gcs_data_push``
    Upload data to Google Cloud Storage
- ``gcs_model_pull``
    Download models from Google Cloud Storage
- ``gcs_task_push``
    Upload model task to Google Cloud Storage

Miscellaneous
-------------
- ``clean``
    Delete all compiled Python files
- ``format``
    Format using yapf
- ``lint``
    Lint using flake8
- ``build``
    Build source distribution
