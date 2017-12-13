import json
import requests
from time import sleep
from datetime import datetime


class DummyRequests(object):
    pass

def get(url, params=None, delay=0.25, **kwargs):
    """Dummy version of requests.get(). Sends a GET request.

    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary or bytes to be sent in the query string for the :class:`Request`.
    :param delay: Spoof delay time (seconds)
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    dummyresponse = requests.Response()

    data = {"totalSize": 1, "done": True, "records": [{"attributes": {"type": "Opportunity", "url": "/services/data/foo/bar"}, "Name": "FooBar Opportunity AAA", "AccountId": "1337BEEF", "CreatedDate": "2015-07-13T07:30:24.000+0000", "IsWon": False, "IsClosed": True, "Amount": 31415.926}], "RetrievedDate": datetime.now().isoformat()}
    dummyresponse._content =  bytes(json.dumps(data), 'utf8')

    sleep(delay)
    return dummyresponse
