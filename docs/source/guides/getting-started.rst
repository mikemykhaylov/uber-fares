Getting started
===============

Requirements
------------
Most of this project's data is stored in `Google Cloud <https://cloud.google.com>`_, so it is necessary to have `Google Cloud SDK <https://cloud.google.com/sdk/docs/quickstart>`_ installed. `Anaconda <https://www.anaconda.com/products/individual>`_ or `Mamba <https://github.com/mamba-org/mamba>`_ installation is also advised

Initialization
--------------
.. tip::
    You should really try `Mamba <https://github.com/mamba-org/mamba>`_, conda dependency resolver will take a very long time

.. code-block:: bash

    make environment                # Creates either pip or conda virtual environment
    make requirements               # Installs requirements for pip

Now you are all set to explore my project. Below are a few things that you might want to do

Getting the data
----------------
You most certainly want to get the data before you recreate some analysis or Machine Learning. There are a few ways to do so, depending on whether you want to modify the preprocessing pipeline.

Pulling data from GCS (recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The easiest way to get the data is to pull it from Google `Cloud Storage <https://cloud.google.com/storage>`_. It is also much quicker, as the processsing pipeline is compute-intensive. **Recommended** if you don't want to modify the pipeline

.. code-block:: bash

    make gcs_data_pull              # Downloads all data from the Cloud Storage

Recreating the data pipeline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. warning::
    Data enrichment takes a veeery long time and will use all CPU cores

If you want to modify the pipeline in any way, you can download only the raw data and let your machine do the rest

.. code-block:: bash

    make gcs_data_pull_raw          # Downloads only raws data from the Cloud Storage
    make data                       # Transforms raw data into data ready for exploration
    make features                   # Builds features for ML from processed data

| You can also run the pipeline steps one by one to save up on expensive computation. Namely,
| ``make data`` is equivalent to:

.. code-block:: bash

    make data-format                # Formats raw data
    make data-clean                 # Cleans formatted data
    make data-enrich                # Enriches clean data with external datasets

Running the notebooks
---------------------
If you are interested in the data explorations, visualisations and model experiments, you can check out the `Jupyter Notebooks <https://jupyter.org/>`_ in ``/notebooks``. Just start the Jupyter Server and dive in!

.. code-block:: bash

    jupyter notebook

Training the models
-------------------
While I originally tuned and trained the model on Google Cloud `Vertex AI <https://cloud.google.com/vertex-ai>`_, you can also train the models locally.

.. warning::
    Local hyperparameter tuning is strongly discouraged unless you have lots of CPU cores and free time. Personally I don't, so I didn't bother implementing it

.. code-block:: bash

    make model                      # Trains model

Using the models for predictions
--------------------------------
At the moment there is no way to directly feed the data to the model. You can check out my cool demo though.