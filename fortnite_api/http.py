from json import JSONDecodeError

import aiohttp
import requests

from .errors import ServerOutage, RateLimited, Unauthorized, NotFound

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
            if response.status_code == 401:
                raise Unauthorized(data.get('error', 'Error message not provided!'))
            elif response.status_code == 404:
                raise NotFound(data.get('error', 'Error message not provided!'))
            elif response.status_code == 429:
                raise RateLimited(data.get('error', 'Error message not provided!'))
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
                data = await response.json()
                if response.status == 401:
                    raise Unauthorized(data.get('error', 'Error message not provided!'))
                elif response.status == 404:
                    raise NotFound(data.get('error', 'Error message not provided!'))
                elif response.status == 429:
                    raise RateLimited(data.get('error', 'Error message not provided!'))
                return data
            except aiohttp.ContentTypeError:
                raise ServerOutage('The Fortnite-API.com server is currently unavailable.')

