import os
import json
import requests
import collections
import functools

from cachegrab.utils.utils import make_path, load_cached_json, dump_cached_json, freeze_sig
from cachegrab.utils.hash import hash_md5
from cachegrab.cachers.static import StaticCacheMethods


class BasicCachingGetter(object):
    """Simple cache controller for the most basic use case: wrapping requests, and saving the response as a json.
    Really basic, no frills base use case. 
    """
    default_cachepath = './cache/'
    flushKey = '_flush'

    def __init__(self, basepath=None):
        basepath = basepath if basepath is not None else BasicCachingGetter.default_cachepath
        self.basepath = basepath
        self.hash = hash_md5
        self.load = load_cached_json
        self.dump = dump_cached_json
        make_path(basepath)

    def __call__(self, fn, *fnargs, **fnkwargs):
        print("💰 Basic cacher called")

        @functools.wraps(fn)
        def new_fn(*fnargs, **fnkwargs):
            key = self.flushKey
            flush = fnkwargs.get(key)
            if flush:
                fnkwargs.pop(key)

            sig = freeze_sig(fn, *fnargs, **fnkwargs)
            cachePath = "{}/{}.json".format(self.basepath, hash_md5(sig))
            print("✬✬ Inner decorated function called")
            print("✬✬", sig)
            print("✬✬", cachePath)

            data = None
            if os.path.exists(cachePath) and not flush:
                print("✬✬ loading")
                data = self.load(cachePath)

            if data is None:
                print("✬✬ New fn call")
                data = fn(*fnargs, **fnkwargs)
                self.dump(cachePath, data)

            return data

        return new_fn




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
