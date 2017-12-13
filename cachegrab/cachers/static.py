import requests
import json

class StaticCacheMethods(object):
    """Static methods for use in conjunction with caching functions
    """
    def __init__(self):
        pass

    @staticmethod
    def json_fetch_and_cache(cachePath, url):
        """Fetches a URL and saves the result as a json.
        :param cachePath:
        :param url:
        :return:
        """
        response = requests.get(url)
        response = response.json()
        with open(cachePath, 'w') as f:
            json.dump(response, f)
        return response