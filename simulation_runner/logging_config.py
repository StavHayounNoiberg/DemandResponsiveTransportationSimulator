from datetime import datetime
import logging
import os


def setup_logging(log_dir: str = 'logs', log_level: int = logging.INFO):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger()
    logger.setLevel(log_level)

    current_time = datetime.now().strftime("%Y%m%d-%H%M")
    file_name = f"{current_time}.log"

    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(os.path.join(log_dir, file_name))
    c_handler.setLevel(log_level)
    f_handler.setLevel(log_level)

    log_format = '[%(asctime)s] [%(filename)s] [%(threadName)s] [%(funcName)s] [%(levelname)s] %(message)s'
    c_format = logging.Formatter(log_format)
    f_format = logging.Formatter(log_format)
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    if not logger.handlers:
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)
