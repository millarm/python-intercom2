import requests
from intercom2.json import DateTimeEncoder, DateTimeDecoder
import json


def json_decoder(self, *args):
    return json.loads(self.content, cls=DateTimeDecoder)


requests.models.Response.json = json_decoder


class Client:
    def __init__(self, token):
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Intercom-Version": "2.0"
        })

    def get(self, *args, **kwargs):
        r = self.session.get(*args, **kwargs)
        return r

    def get_list(self, *args, **kwargs):
        li = self.session.get(*args, **kwargs)
        while True:
            for item in li.json().get('data', []):
                yield item
            starting_after = li.json().get('pages', {}).get('next', {}).get('starting_after', None)
            if starting_after:
                params = kwargs.pop('params', {})
                params['starting_after'] = starting_after
                kwargs['params'] = params
                li = scelf.session.get(*args, **kwargs)
            else:
                break

    def put(self, *args, **kwargs):
        d = kwargs.pop('json', None)
        if d:
            kwargs['data'] = json.dumps(d, cls=DateTimeEncoder)
        r = self.session.put(*args, **kwargs)
        r.json = json_decoder
        return r

    def post(self, *args, **kwargs):
        d = kwargs.pop('json', None)
        if d:
            kwargs['data'] = json.dumps(d, cls=DateTimeEncoder)
        r = self.session.post(*args, **kwargs)
        r.json = json_decoder
        return r

    def post_list(self, *args, **kwargs):
        li = self.session.post(*args, **kwargs)
        while True:
            for item in li.json().get('data', []):
                yield item
            starting_after = li.json().get('pages', {}).get('next', {}).get('starting_after', None)
            if starting_after:
                params = kwargs.pop('json', {})
                params['pagination'] = params.get('pagination', {})
                params['pagination']['starting_after'] = starting_after
                kwargs['json'] = params
                print(params)
                li = self.session.post(*args, **kwargs)
            else:
                break


    def delete(self, *args, **kwargs):
        d = kwargs.pop('json', None)
        if d:
            kwargs['data'] = json.dumps(d, cls=DateTimeEncoder)
        r = self.session.delete(*args, **kwargs)
        r.json = json_decoder
        return r

    def request(self, *args, **kwargs):
        d = kwargs.pop('json', None)
        if d:
            kwargs['data'] = json.dumps(d, cls=DateTimeEncoder)
        r = self.session.request(*args, **kwargs)
        r.json = json_decoder
        return r
