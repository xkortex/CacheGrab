import os
import errno

def make_path(path):
    """
    Make a path, ignoring already-exists error. Python 2/3 compliant.
    Catch any errors generated, and skip it if it's EEXIST.
    :param path: Path to create
    :return:
    """
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise