from hashlib import md5
from collections import Hashable


def hash_md5(stringable, strict=True):
    """

    :param stringable:
    :return:
    """
    if strict and not isinstance(stringable, Hashable):
        raise TypeError('Argument of type {} is not hashable. '
                        'Use a hashable object, or set strict=False'.format(type(stringable)))

    
    md5_key = md5(str(stringable)).hexdigest()
    return md5_key