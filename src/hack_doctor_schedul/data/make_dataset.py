# -*- coding: utf-8 -*-
import logging
from pathlib import Path

import hydra
from dotenv import find_dotenv, load_dotenv
from omegaconf import DictConfig


@hydra.main(config_path="configs", config_name="config")
def main(cfg: DictConfig) -> None:
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')


if __name__ == "__main__":
    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
