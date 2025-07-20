import logging
from uuid import uuid4

from sys import stdout

class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class CustomLogger(metaclass=SingletonMeta):

    def __init__(self):
        self.logger = logging.getLogger('root')
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(f'%(levelname)s - %(asctime)s - {uuid4()} - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def get_logger(self) -> logging.Logger:
        return self.logger


if __name__ == '__main__':
    logger = CustomLogger().get_logger()
    logger.debug('debug message')
    logger.info('info message')
    logger.error('error message')