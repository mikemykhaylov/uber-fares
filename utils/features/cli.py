import logging

import click

from utils.features import build_features


@click.group()
def cli():
    """
    CLI for the features module.
    """
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)


@cli.command()
def build():  # noqa
    """Builds features

    Returns:
        None
    """
    build_features()


if __name__ == '__main__':
    cli()
