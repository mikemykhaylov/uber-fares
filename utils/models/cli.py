import logging

import click

from utils.models import train_model


@click.group()
def cli():
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)


@cli.command()
@click.option("--output-path", type=str, envvar="AIP_MODEL_DIR")
@click.option("--mode", type=click.Choice(["train", "cv", "grid"]))
@click.option(
    "--max_depth",
    type=int,
    default=4,
    help="Max depth of decision tree",
    show_default=True,
)
@click.option(
    "--n_estimators",
    type=int,
    default=50,
    help="Number of AdaBoost boosts",
    show_default=True,
)
@click.argument("input_path", type=str)
def train(input_path, output_path, mode, max_depth, n_estimators):
    """Builds features

    Returns:
        None
    """
    train_model(input_path, output_path, mode, max_depth, n_estimators)


if __name__ == '__main__':
    cli()
