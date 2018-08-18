import os
import errno
import json

def make_path(path):
    """ Make a path, ignoring already-exists error. Python 2/3 compliant.
    Catch any errors generated, and skip it if it's EEXIST.
    :param path: Path to create
    :return:
    """
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def freeze_sig(f=None, *args, **kwargs):
    """ Freeze a function signature for serialization
    :param f: function that is being memoized
    :param args: arguments fed to that function
    :param kwargs: keyword arguments fed to that function
    :return: JSONified string of function signature
    """
    name = f.__name__ if f is not None else None
    return json.dumps({'@args': args, '@kwargs': kwargs, '@name': name})

def thaw_sig(string):
    """ Unfreeze a frozen signature back to args and kwargs
    :param string: Frozen signature
    :return:
    """
    dd = json.loads(string)
    __args = dd.get('@args') # sanitize???
    __kwargs = dd.get('@kwargs')
    __name = dd.get('@name')
    return __name, __args, __kwargs


def load_cached_json(cachePath, default=None):
    """ Load cached data from a json file.
    :param cachePath: target file path
    :param default: return value on failure
    :return:
    """
    with open(cachePath, 'r') as fp:
        try:
            default = json.load(fp)
        except ValueError:
            print("🚧 functionality under construction")

    return default

def dump_cached_json(cachePath, data):
    """ Dumps data to a json file.
    :param cachePath: target file path
    :param data: data to store
    :return:
    """
    with open(cachePath, 'w') as fp:
        json.dump(data, fp)
