class CustomException(Exception):
    """ Common base class for all non-exit exceptions. """

    def __init__(self, msg: str, *args, **kwargs):
        self.msg = msg

class ToManyValuesException(CustomException):
    pass


class InvalidSearchException(CustomException):
    pass