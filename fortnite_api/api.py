from .http import *
from .endpoints import *


class FortniteAPI:

    def __init__(self, api_key=None, run_async=False):
        self.http = SyncHTTPClient() if not run_async else AsyncHTTPClient()
        if api_key is not None:
            self.http.add_header('x-api-key', api_key)
        self.cosmetics = SyncCosmeticsEndpoints(self) if not run_async else AsyncCosmeticsEndpoints(self)
        self.news = SyncNewsEndpoints(self) if not run_async else AsyncNewsEndpoints(self)
        self.shop = SyncShopEndpoints(self) if not run_async else AsyncShopEndpoints(self)
