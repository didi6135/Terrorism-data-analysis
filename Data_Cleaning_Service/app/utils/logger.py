import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def log(message, level="info"):
    setup_logging()
    log_func = getattr(logging, level, logging.info)
    log_func(message)
