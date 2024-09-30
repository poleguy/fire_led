# https://www.toptal.com/python/in-depth-python-logging
import logging

from logging.handlers import RotatingFileHandler

FORMAT = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s')
LOG_FILE = '/run/shm/debug.log'


def get_file_handler():
    # Rotates logs automatically on run
    # https://stackoverflow.com/questions/24505145/how-to-limit-log-file-size-in-python
    # https://stackoverflow.com/questions/6167587/the-logging-handlers-how-to-rollover-after-time-or-maxbytes
    # limit size to avoid filling raspberry pi temp storage
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=10*1024*1024, backupCount=2)
    file_handler.setFormatter(FORMAT)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger
