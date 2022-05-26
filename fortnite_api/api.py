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

from typing import Optional
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

    def __init__(self, api_key: Optional[str] = None, run_async: bool = False) -> None:
        self.http = SyncHTTPClient() if not run_async else AsyncHTTPClient()
        if api_key:
            self.http.add_header('Authorization', api_key)

        self.aes = SyncAESEndpoints(self) if not run_async else AsyncAESEndpoints(self)
        self.banner = SyncBannerEndpoints(self) if not run_async else AsyncBannerEndpoints(self)
        self.cosmetics = SyncCosmeticsEndpoints(self) if not run_async else AsyncCosmeticsEndpoints(self)
        self.creator_code = SyncCreatorCodeEndpoints(self) if not run_async else AsyncCreatorCodeEndpoints(self)
        self.map = SyncMapEndpoints(self) if not run_async else AsyncMapEndpoints(self)
        self.news = SyncNewsEndpoints(self) if not run_async else AsyncNewsEndpoints(self)
        self.playlist = SyncPlaylistEndpoints(self) if not run_async else AsyncPlaylistEndpoints(self)
        self.shop = SyncShopEndpoints(self) if not run_async else AsyncShopEndpoints(self)
        self.stats = SyncStatsEndpoints(self) if not run_async else AsyncStatsEndpoints(self)
