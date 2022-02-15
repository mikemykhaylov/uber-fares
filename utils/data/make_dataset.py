import logging

from utils.data.subroutines import clean_data, format_data, enrich_data


def make_dataset():
    """Processes dataset through the whole pipeline

    Returns:
        None

    """
    logger = logging.getLogger(__name__)
    logger.info("Data formatting subroutine")
    format_data()

    logger.info("Data cleaning subroutine")
    clean_data()

    logger.info("Data enrichment subroutine")
    enrich_data()
