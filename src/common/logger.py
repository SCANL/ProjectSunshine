import logging


def setup_logger(name: str, log_file: str, level: int = logging.INFO, formatting: str = '%(asctime)s %(levelname)s %(message)s') -> logging.Logger:
    """
        Set up a logger with the specified configuration.
        Args:
            name (str): The name of the logger.
            log_file (str): The path to the log file.
            level (int): The logging level (default is logging.INFO).
            formatting (str): The log message formatting using a format string (default is '%(asctime)s %(levelname)s %(message)s').
                The format string can include placeholders such as '%(asctime)s' for timestamp, '%(levelname)s' for log level, and '%(message)s' for the log message.
        Returns:
            logging.Logger: The configured logger.
    """
    formatter = logging.Formatter(formatting, '%Y-%m-%d %H:%M:%S')

    handler = logging.FileHandler(log_file, mode='a')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
