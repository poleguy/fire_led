# https://www.toptal.com/python/in-depth-python-logging
import logging

from logging.handlers import TimedRotatingFileHandler

FORMAT = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s')
LOG_FILE = 'led_controller.log'


def get_file_handler():
    # Rotates logs automatically on run
    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMAT)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger
