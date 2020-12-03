from AGNESS_BOT import configs
from .decorators import export
import logging
import sys, os
import pathlib

LOG_FILE = configs.LOG_FILE


class CustomFormatter(logging.Formatter):
    """
    A custom formatter class which set colors and format.
    """
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
    high_green = '\033[0;92m'

    format = '[%(levelname)s] - |%(asctime)s| - [%(name)s : LN : %(lineno)d] - %(message)s'

    FORMATS = {
        logging.DEBUG: Purple + format + reset,
        logging.INFO: Green + format + reset,
        logging.WARNING: Yellow + format + reset,
        logging.ERROR: Red + format + reset,
        logging.CRITICAL: Bold_red + format + reset,

    }

    def format(self, record) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)


@export
def get_custom_logger(name, level=logging.DEBUG, console=True):
    """
    This function is supposed to be called whenever you want to make a logger.
    :param name: name of the module, set it to __name__
    :param level: level of logging. default if debug.
    :param console: do you want op on console or not? Default is true.
    :return: an instance of Logger class.
    """
    formatter = CustomFormatter()

    _logger = logging.Logger(name)

    try:
        if not os.path.exists(LOG_FILE):
            splitted = LOG_FILE.strip().split('/')
            dirs = '/'.join(splitted[:-1])
            pathlib.Path(dirs).mkdir(parents=True, exist_ok=True)
            open(f"{configs.BASE_DIR}/{LOG_FILE}", 'a').close()
        filehandler = logging.FileHandler(LOG_FILE)
        filehandler.setLevel(level)
        filehandler.setFormatter(formatter)
        _logger.addHandler(filehandler)
    except Exception as e:
        raise e

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(level)

    stream_handler.setFormatter(formatter)

    if console:
        _logger.addHandler(stream_handler)
    return _logger
