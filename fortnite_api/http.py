from io import BytesIO
from json import JSONDecodeError

import aiohttp
import requests

from .errors import ServerOutage

BASE_URL = 'https://fortnite-api.com/'


class SyncHTTPClient:

    def __init__(self):
        self.headers = {}

    def add_header(self, key, val):
        self.headers[key] = val

    def remove_header(self, key):
        return self.headers.pop(key)

    def get(self, endpoint, params=None):
        response = requests.get(BASE_URL + endpoint, params=params, headers=self.headers)
        try:
            data = response.json()
            return data
        except JSONDecodeError:
            raise ServerOutage('The Fortnite-API.com server is currently unavailable.')


class AsyncHTTPClient:

    def __init__(self):
        self.headers = {}
        self.session = aiohttp.ClientSession()

    def add_header(self, key, val):
        self.headers[key] = val

    def remove_header(self, key):
        return self.headers.pop(key)

    async def get(self, endpoint, params=None):
        async with self.session.get(BASE_URL + endpoint, params=params, headers=self.headers) as response:
            try:
                return response.json()
            except aiohttp.ContentTypeError:
                raise ServerOutage('The Fortnite-API.com server is currently unavailable.')

