from urllib3.util.retry import Retry
import requests
from requests.adapters import HTTPAdapter
from intercom2.json import IntercomFormatEncoder, IntercomFormatDecoder
import json


def wrap_response(response):
    """
    Monkey-patches a response object to have our custom json loader by default.
    Mutates the original object and then returns it for convenience.
    """
    original_json = response.json

    def wrapped_json(*args, **kwargs):
        return original_json(*args, cls=IntercomFormatDecoder, **kwargs)

    response.json = wrapped_json
    return response


class Client:
    def __init__(self, token, max_retries=8, delay=5):
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Intercom-Version": "2.0"
        })
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=delay,
            status_forcelist=[429],
            allowed_methods=frozenset({'DELETE', 'GET', 'HEAD', 'OPTIONS', 'PUT', 'TRACE', 'POST'})
        )

        self.session.mount('https://', HTTPAdapter(max_retries=retry_strategy))

    def get(self, *args, **kwargs):
        r = self.session.get(*args, **kwargs)
        return wrap_response(r)

    def get_list(self, *args, **kwargs):
        li = self.session.get(*args, **kwargs)
        while True:
            for item in li.json().get('data', []):
                yield item
            starting_after = li.json().get('pages', {}).get(
                'next', {}).get('starting_after', None)
            if starting_after:
                params = kwargs.pop('params', {})
                params['starting_after'] = starting_after
                kwargs['params'] = params
                li = self.session.get(*args, **kwargs)
            else:
                break

    def put(self, *args, **kwargs):
        d = kwargs.pop('json', None)
        if d:
            kwargs['data'] = json.dumps(d, cls=IntercomFormatEncoder)
        r = self.session.put(*args, **kwargs)
        return wrap_response(r)

    def post(self, *args, **kwargs):
        d = kwargs.pop('json', None)
        if d:
            kwargs['data'] = json.dumps(d, cls=IntercomFormatEncoder)
        r = self.session.post(*args, **kwargs)
        return wrap_response(r)

    def post_list(self, *args, **kwargs):
        li = self.session.post(*args, **kwargs)
        while True:
            for item in li.json().get('data', []):
                yield item
            starting_after = li.json().get('pages', {}).get(
                'next', {}).get('starting_after', None)
            if starting_after:
                params = kwargs.pop('json', {})
                params['pagination'] = params.get('pagination', {})
                params['pagination']['starting_after'] = starting_after
                kwargs['json'] = params
                li = self.session.post(*args, **kwargs)
            else:
                break

    def delete(self, *args, **kwargs):
        d = kwargs.pop('json', None)
        if d:
            kwargs['data'] = json.dumps(d, cls=IntercomFormatEncoder)
        r = self.session.delete(*args, **kwargs)
        return wrap_response(r)

    def request(self, *args, **kwargs):
        d = kwargs.pop('json', None)
        if d:
            kwargs['data'] = json.dumps(d, cls=IntercomFormatEncoder)
        r = self.session.request(*args, **kwargs)
        return wrap_response(r)
