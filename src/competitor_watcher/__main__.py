from competitor_watcher.data_loading import data_loader
from competitor_watcher.data_analysis import analyze
from loguru import logger

@logger.catch
def main():
    try:
        data_loader()
        analyze()
    except Exception as e:
        logger.error(f"Error: {e}")
        raise e


if __name__ == "__main__":
    main()

