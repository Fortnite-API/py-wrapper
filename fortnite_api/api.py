from .http import *
from .endpoints import *


class FortniteAPI:

    def __init__(self, api_key: str, run_async: bool = False):
        if type(api_key) is not str:
            raise TypeError('api_key require a value of type {0}'.format(str(str)))
        self.http = SyncHTTPClient() if not run_async else AsyncHTTPClient()
        self.http.add_header('x-api-key', api_key)

        self.cosmetics = SyncCosmeticsEndpoints(self) if not run_async else AsyncCosmeticsEndpoints(self)
        self.creator_code = SyncCreatorCodeEndpoints(self) if not run_async else AsyncCreatorCodeEndpoints(self)
        self.news = SyncNewsEndpoints(self) if not run_async else AsyncNewsEndpoints(self)
        self.shop = SyncShopEndpoints(self) if not run_async else AsyncShopEndpoints(self)
