from .decorators import export


@export
def calculate_time(time_, unit):
    """
    A function for abbreviated time commands to convert time in seconds according to unit of time given.
    :param time_: int
    :param unit: str
    :return: time in seconds.
    """
    if unit in ['hr', 'hour', 'hours', 'h']:
        return time_ * 3600
    elif unit in ['mins', 'min', 'minute', 'minutes', 'm']:
        return time_ * 60
    elif unit in ['sec', 'seconds', 'secs', 's']:
        return time_
    elif unit in ['days', 'day', 'd']:
        return time_ * 86400
    else:
        return False
