import requests
from intercom2.json import IntercomFormatEncoder, IntercomFormatDecoder
import json
from time import sleep


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
            "Intercom-Version": "2.3"
        })
        self.MAX_RETRIES = max_retries
        self.DELAY = delay

    def get(self, *args, **kwargs):
        retries = 1
        while retries <= self.MAX_RETRIES:
            r = self.session.get(*args, **kwargs)
            if r.status_code != 429:
                break
            retries += 1
            sleep(self.DELAY*retries)
        return wrap_response(r)

    def get_list(self, *args, **kwargs):
        retries = 1
        while retries <= self.MAX_RETRIES:
            li = self.session.get(*args, **kwargs)
            if li.status_code != 429:
                break
            retries += 1
            sleep(self.DELAY*retries)
        while True:
            for item in li.json().get('data', []):
                yield item
            starting_after = li.json().get('pages', {}).get(
                'next', {}).get('starting_after', None)
            if starting_after:
                params = kwargs.pop('params', {})
                params['starting_after'] = starting_after
                kwargs['params'] = params
                retries = 1
                while retries <= self.MAX_RETRIES:
                    li = self.session.get(*args, **kwargs)
                    if li.status_code != 429:
                        break
                    retries += 1
                    sleep(self.DELAY*retries)
            else:
                break

    def put(self, *args, **kwargs):
        d = kwargs.pop('json', None)
        if d:
            kwargs['data'] = json.dumps(d, cls=IntercomFormatEncoder)
        retries = 1
        while retries <= self.MAX_RETRIES:
            r = self.session.put(*args, **kwargs)
            if r.status_code != 429:
                break
            retries += 1
            sleep(self.DELAY*retries)
        return wrap_response(r)

    def post(self, *args, **kwargs):
        d = kwargs.pop('json', None)
        if d:
            kwargs['data'] = json.dumps(d, cls=IntercomFormatEncoder)
        retries = 1
        while retries <= self.MAX_RETRIES:
            r = self.session.post(*args, **kwargs)
            if r.status_code != 429:
                break
            retries += 1
            sleep(self.DELAY*retries)
        return wrap_response(r)

    def post_list(self, *args, **kwargs):
        retries = 1
        while retries <= self.MAX_RETRIES:
            li = self.session.post(*args, **kwargs)
            if li.status_code != 429:
                break
            retries += 1
            sleep(self.DELAY*retries)
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
                retries = 1
                while retries <= self.MAX_RETRIES:
                    li = self.session.post(*args, **kwargs)
                    if li.status_code != 429:
                        break
                    retries += 1
                    sleep(self.DELAY*retries)
            else:
                break

    def delete(self, *args, **kwargs):
        d = kwargs.pop('json', None)
        if d:
            kwargs['data'] = json.dumps(d, cls=IntercomFormatEncoder)
        retries = 1
        while retries <= self.MAX_RETRIES:
            r = self.session.delete(*args, **kwargs)
            if r.status_code != 429:
                break
            retries += 1
            sleep(self.DELAY*retries)
        return wrap_response(r)

    def request(self, *args, **kwargs):
        d = kwargs.pop('json', None)
        if d:
            kwargs['data'] = json.dumps(d, cls=IntercomFormatEncoder)
        retries = 1
        while retries <= self.MAX_RETRIES:
            r = self.session.request(*args, **kwargs)
            if r.status_code != 429:
                break
            retries += 1
            sleep(self.DELAY*retries)
        return wrap_response(r)
