# -*- coding: utf-8 -*-

from .endpoints import *
from .http import SyncHTTPClient, AsyncHTTPClient


class FortniteAPI:
    r"""A number of options can be passed to the :class:`FortniteAPI`.

    Parameters
    -----------
    api_key: :class:`str`
        The API key from Fortnite-API.com\profile to authenticate.
    run_async: Optional[:class:`bool`]
        A boolean whether the API should run in async mode or not.
        Defaults set to ``True``, in which case the api runs sync.

    Attributes
    -----------
    cosmetics: Union[:class:`SyncCosmeticEndpoints`, :class:`AsyncCosmeticEndpoints`]
        The Cosmetic endpoints. The class depends whether the api runs sync or async.
    creator_code: Union[:class:`SyncCreatorCodeEndpoints`, :class:`AsyncCreatorCodeEndpoints`]
         The Creator Code endpoints. The class depends whether the api runs sync or async.
    news: Union[:class:`SyncNewsEndpoints`, :class:`AsyncNewsEndpoints`]
        The News endpoints. The class depends whether the api runs sync or async.
    shop: Union[:class:`SyncShopEndpoints`, :class:`AsyncShopEndpoints`]
        The Shop endpoints. The class depends whether the api runs sync or async.
    """

    def __init__(self, api_key: str = None, run_async: bool = False):
        if type(api_key) is not str:
            raise TypeError('api_key require a value of type {0}'.format(str(str)))
        self.http = SyncHTTPClient() if not run_async else AsyncHTTPClient()
        if api_key:
            self.http.add_header('x-api-key', api_key)

        self.aes = SyncAESEndpoints(self) if not run_async else AsyncAESEndpoints(self)
        self.cosmetics = SyncCosmeticsEndpoints(self) if not run_async else AsyncCosmeticsEndpoints(self)
        self.creator_code = SyncCreatorCodeEndpoints(self) if not run_async else AsyncCreatorCodeEndpoints(self)
        self.news = SyncNewsEndpoints(self) if not run_async else AsyncNewsEndpoints(self)
        self.shop = SyncShopEndpoints(self) if not run_async else AsyncShopEndpoints(self)
        self.stats = SyncStatsEndpoints(self) if not run_async else AsyncStatsEndpoints(self)
