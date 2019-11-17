from io import BytesIO

import aiohttp
import requests

BASE_URL = 'https://fortnite-api.com/'


class SyncHTTPClient:

    def __init__(self):
        self.headers = {}

    def add_header(self, key, val):
        self.headers[key] = val

    def remove_header(self, key):
        return self.headers.pop(key)

    def get(self, endpoint, params=None, json=True):
        response = requests.get(BASE_URL + endpoint, params=params, headers=self.headers)
        if response.status_code != 200:
            return None  # TODO: Mby raise Error
        if json:
            return response.json()
        else:
            return response.content

    def download_image(self, url):
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            return None  # TODO: Mby raise Error
        return BytesIO(response.content)


class AsyncHTTPClient:

    def __init__(self):
        self.headers = {}
        self.session = aiohttp.ClientSession()

    def add_header(self, key, val):
        self.headers[key] = val

    def remove_header(self, key):
        return self.headers.pop(key)

    async def get(self, endpoint, params=None, json=True):
        async with self.session.get(BASE_URL + endpoint, params=params, headers=self.headers) as response:
            if response.status != 200:
                return None  # TODO: Mby raise Error
            if json:
                return await response.json()
            else:
                return await response.text()

    async def download_image(self, url):
        async with self.session.get(url) as response:
            if response.status != 200:
                return None  # TODO: Mby raise Error
            return BytesIO(await response.read())
