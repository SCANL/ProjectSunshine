import logging


def setup_logger(name, log_file, level=logging.INFO, formatting='%(asctime)s %(levelname)s %(message)s'):
    formatter = logging.Formatter(formatting, '%Y-%m-%d %H:%M:%S')

    handler = logging.FileHandler(log_file, mode='a')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
