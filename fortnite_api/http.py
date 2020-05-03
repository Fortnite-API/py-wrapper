import aiohttp
import requests

from .errors import ServiceUnavailable, RateLimited, Unauthorized, NotFound

BASE_URL = 'https://fortnite-api.com/v2/'


class SyncHTTPClient:

    def __init__(self):
        self.headers = {}

    def add_header(self, key, val):
        self.headers[key] = val

    def remove_header(self, key):
        return self.headers.pop(key)

    def get(self, endpoint, params=None):
        response = requests.get(BASE_URL + endpoint, params=params, headers=self.headers)
        data = response.json()
        if response.status_code == 200:
            return data
        elif response.status_code == 401:
            raise Unauthorized(data.get('error', 'Error message not provided!'))
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
                data = await response.json()
                if response.status == 200:
                    return data
                if response.status == 401:
                    raise Unauthorized(data.get('error', 'Error message not provided!'))
                elif response.status == 404:
                    raise NotFound(data.get('error', 'Error message not provided!'))
                elif response.status == 429:
                    raise RateLimited(data.get('error', 'Error message not provided!'))
                elif response.status == 503:
                    raise ServiceUnavailable(data.get('error', 'Error message not provided!'))
                else:
                    raise Exception(data.get('error', 'Error message not provided') + '. Status Code: {0}'
                                    .format(str(response.status)))
