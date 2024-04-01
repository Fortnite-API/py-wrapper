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

from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

from .http import Route
from .utils import prepend_doc

if TYPE_CHECKING:
    from .http import HTTPClient, SyncHTTPClient

__all__: Tuple[str, ...] = ('SyncAsset', 'Asset')


class _AssetRoute(Route):
    def __init__(self, url: str) -> None:
        self.BASE_URL: None = None
        self.url: str = url
        self.method: str = 'GET'


class _BaseAsset:
    """
    .. container:: operations

        .. describe:: x == y

            Determine if two assets are equal.

        .. describe:: x != y

            Determine if two assets are not equal.

        .. describe:: hash(x)

            Returns the hash of the asset.

    """

    url: str

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, self.__class__):
            return False

        return self.url == __o.url

    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)

    def __hash__(self) -> int:
        return hash(self.url)


class SyncAsset(_BaseAsset):
    """Represents an asset given to the client. This can be from
    an image on a banner to a cosmetic image.

    Attributes
    ----------
    url: :class:`str`
        The url of the asset.
    """

    def __init__(self, http: SyncHTTPClient, url: str) -> None:
        self._http: SyncHTTPClient = http
        self.url: str = url

    def read(self) -> bytes:
        """Retrieves the content of this asset as a :class:`bytes` object.

        Returns
        --------
        :class:`bytes`
            The image bytes.
        """
        return self._http.request(_AssetRoute(self.url))


class Asset(_BaseAsset):
    """Represents an asset given to the client. This can be from
    an image on a banner to a cosmetic image.

    Attributes
    ----------
    url: :class:`str`
        The url of the asset.
    """

    def __init__(self, http: HTTPClient, url: str) -> None:
        self._http: HTTPClient = http
        self.url: str = url

    @prepend_doc(SyncAsset.read, sep='\n')
    async def read(self) -> bytes:
        """|coro|"""
        return await self._http.request(_AssetRoute(self.url))
