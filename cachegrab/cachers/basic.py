import os
import json
import requests
import collections
import functools

from cachegrab.utils.utils import make_path
from cachegrab.utils.hash import hash_md5


class BasicCachingGetter(object):
    """
    Simple cache controller for the most basic use case: wrapping requests, and saving the response as a json.
    Really basic, no frills base use case. 
    """
    default_cachepath = './cache/'

    def __init__(self, basepath=None):
        basepath = basepath if basepath is not None else BasicCachingGetter.default_cachepath
        self.basepath = basepath
        self.hash = hash_md5
        make_path(basepath)

    @staticmethod
    def json_fetch_and_cache(cachePath, url):
        """
        Fetches a URL and saves the result as a json.
        :param cachePath:
        :param url:
        :return:
        """
        response = requests.get(url)
        response = response.json()
        with open(cachePath, 'w') as f:
            json.dump(response, f)
        return response

    def get(self, url, flush=False):
        """
        Wraps requests.get(), saves the response as a json file. 
        :param url: Target URL
        :param flush: Refresh cache by forcing a request
        :return:
        """

        cachePath = "{}/{}.json".format(self.basepath, self.hash(url))

        # Try to extract the file. If it fails, fall through
        data = None
        if os.path.exists(cachePath) and not flush:
            with open(cachePath, 'r') as f:
                try:
                    data = json.load(f)
                except ValueError:
                    pass

        if data is None:
            data = BasicCachingGetter.json_fetch_and_cache(cachePath, url)

        return data


class memoized(object):
    '''Basic Memoizing Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    From the python website, https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
    '''

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

    def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__

    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)
