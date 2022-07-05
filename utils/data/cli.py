import logging

import click

from utils.data.make_dataset import make_dataset
from utils.data.subroutines import clean_data, format_data, enrich_data


@click.group()
def cli():
    """
    CLI for the data module.
    """
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)


@cli.command()
def pipe():
    """Processes dataset through the whole pipeline

    Returns:
        None
    """
    make_dataset()


@cli.command()
def format():  # noqa
    """Formats raw data

    Returns:
        None
    """
    format_data()


@cli.command()
def clean():
    """Cleans formatted data by removing outliers

    Returns:
        None
    """
    clean_data()


@cli.command()
def enrich():
    """Enriches clean data by adding data from external datasets

    Returns:
        None
    """
    enrich_data()


if __name__ == '__main__':
    cli()
