import sys

from loguru import logger

from competitor_watcher.data_loading import data_loader
from competitor_watcher.data_analysis import analyze


# @logger.catch(onerror=lambda _: sys.exit(1), reraise=True)
def main():
    try:
        data_loader()
        analyze()
    except Exception as e:
        logger.error(f"Error: {e}")
        raise e


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level="TRACE")
    main()

