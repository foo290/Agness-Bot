from AGNESS_BOT import configs
import logging
import sys

LOG_FILE = configs.LOG_FILE


class CustomFormatter(logging.Formatter):
    Black = "\033[0;30m"
    Red = "\033[0;31m"
    Green = "\033[0;32m"
    Yellow = "\033[0;33m"
    Blue = "\033[0;34m"
    Purple = "\033[0;35m"
    Cyan = "\033[0;36m"
    White = "\033[0;37m"
    Bold_red = "\x1b[31;21m"
    reset = "\033[0m"

    format = '[%(levelname)s] - |%(asctime)s| - [%(name)s : LN : %(lineno)d] - %(message)s'

    FORMATS = {
        logging.DEBUG: Purple + format + reset,
        logging.INFO: Green + format + reset,
        logging.WARNING: Yellow + format + reset,
        logging.ERROR: Red + format + reset,
        logging.CRITICAL: Bold_red + format + reset
    }

    def format(self, record) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)


def get_custom_logger(name, level=logging.DEBUG, console=True):
    formatter = CustomFormatter()

    _logger = logging.Logger(name)

    try:
        filehandler = logging.FileHandler(LOG_FILE)
        filehandler.setLevel(level)
    except:
        pass
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(level)

    filehandler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    if console:
        _logger.addHandler(stream_handler)
    _logger.addHandler(filehandler)
    return _logger
