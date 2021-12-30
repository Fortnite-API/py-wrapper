"""
MIT License

Copyright (c) 2019-present Luc1412

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json

import aiohttp
import requests

from .errors import ServiceUnavailable, RateLimited, Unauthorized, NotFound, Forbidden

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
        except json.JSONDecodeError:
            data = {'error': response.text}
        if response.status_code == 200:
            return data
        elif response.status_code == 401:
            raise Unauthorized(data.get('error', 'Error message not provided!'))
        elif response.status_code == 403:
            raise Forbidden(data.get('error', 'Error message not provided!'))
        elif response.status_code == 404:
            raise NotFound(data.get('error', 'Error message not provided!'))
        elif response.status_code == 429:
            raise RateLimited(data.get('error', 'Error message not provided!'))
        elif response.status_code == 503:
            raise ServiceUnavailable(data.get('error', 'Error message not provided!'))
        else:
            raise Exception(data.get('error', 'Error message not provided') + '. Status Code: {0}'
                            .format(str(response.status_code)))


class AsyncHTTPClient:

    def __init__(self):
        self.headers = {}

    def add_header(self, key, val):
        self.headers[key] = val

    def remove_header(self, key):
        return self.headers.pop(key)

    async def get(self, endpoint, params=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(BASE_URL + endpoint, params=params, headers=self.headers) as response:
                try:
                    data = await response.json()
                except aiohttp.ContentTypeError:
                    data = {'error': await response.text()}
                if response.status == 200:
                    return data
                if response.status == 401:
                    raise Unauthorized(data.get('error', 'Error message not provided!'))
                elif response.status == 403:
                    raise Forbidden(data.get('error', 'Error message not provided!'))
                elif response.status == 404:
                    raise NotFound(data.get('error', 'Error message not provided!'))
                elif response.status == 429:
                    raise RateLimited(data.get('error', 'Error message not provided!'))
                elif response.status == 503:
                    raise ServiceUnavailable(data.get('error', 'Error message not provided!'))
                else:
                    raise Exception(data.get('error', 'Error message not provided') + '. Status Code: {0}'
                                    .format(str(response.status)))
