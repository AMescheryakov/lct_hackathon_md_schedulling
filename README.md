# hack_doctor_schedul

## Version 0.0.1

A short description of the project.

## Project Organization

```text
    ├── LICENSE
    ├── Makefile               <- Makefile with commands like `make data` or `make train`
    ├── README.md              <- The top-level README for developers using this project.
    ├── data
    │   ├── external           <- Data from third party sources.
    │   ├── interim            <- Intermediate data that has been transformed.
    │   ├── processed          <- The final, canonical data sets for modeling.
    │   └── raw                <- The original, immutable data dump.
    │
    ├── docs                   <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models                 <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks              <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                             the creator's initials, and a short `-` delimited description, e.g.
    │                             `01-jqp-initial-eda`.
    │
    ├── scripts                <- Top-level scripts that use hack_doctor_schedul package, e.g.
    │                             pipeline stages, optuna optimization, feature selection etc.
    │
    ├── setup.py               <- Makes project pip installable (pip install -e .) so src can be imported
    ├── src                    <- Source code for use in this project.
    │   └── hack_doctor_schedul
    │       ├── __init__.py    <- Makes src a Python module
    │       │
    │       ├── data           <- Scripts to download or generate data
    │       │   └── make_dataset.py
    │       │
    │       ├── features       <- Scripts to turn raw data into features for modeling
    │       │   └── build_features.py
    │       │
    │       ├── models         <- Scripts to train models and then use trained models to make
    │       │   │                 predictions
    │       │   ├── predict_model.py
    │       │   └── train_model.py
    │       │
    │       └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │           └── visualize.py
    │
    ├── environment.yaml       <- Conda project environment file (list all dependencies here)
    ├── pyproject.toml         <- General config with project metadata & tools configuration
    ├── .editorconfig          <- Editors (PyCharm, VS Code, etc) configuration
    ├── .env                   <- Environment variables file
    ├── .flake8                <- Flake8 & WPS linter configuration
    ├── .gitlab-ci.yml         <- GitLab CI configuration
    └── .pypirc                <- CMX Artifactory PyPI configuration
```

## Project Initialization

Add instructions here!
