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

from collections.abc import Coroutine
from typing import TYPE_CHECKING, Any, Generic, Optional, Union, overload

from typing_extensions import Self

from .http import HTTPClientT, Route
from .utils import MISSING

if TYPE_CHECKING:
    from .http import HTTPClient, SyncHTTPClient


__all__: tuple[str, ...] = ('Asset',)


class _AssetRoute(Route):
    def __init__(self, url: str) -> None:
        self.BASE_URL = ''  # type: ignore
        self.url: str = url
        self.method: str = 'GET'


class Asset(Generic[HTTPClientT]):
    """
    .. attributetable:: fortnite_api.Asset

    Represents an asset given to the client. An asset can represent any image or video that
    has been fetched from the API.

    Examples
    --------
    .. code-block:: python3
        :caption: Fetching a cosmetic and reading the icon data:

        cosmetic = await client.fetch_cosmetic_br('CID_028_Athena_Commando_F')
        images = cosmetic.images
        if images is not None and images.icon is not None:
            icon: bytes = await images.icon.read()
    """

    __slots__: tuple[str, ...] = ('_http', '_url', '_max_size', '_size')

    def __init__(self, *, http: HTTPClientT, url: str, max_size: Optional[int] = MISSING, size: int = MISSING) -> None:
        self._http: HTTPClientT = http
        self._url: str = url

        # The maximum size of the asset, if any. If provided, the url's default size is the maximum size.
        # MISSING for not supported, None for no max size, int for max size.
        self._max_size: Optional[int] = max_size

        # The current size of this asset. Will only be set if the asset was resized.
        self._size: int = size

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, self.__class__):
            return False

        return self.url == __o.url

    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)

    def __hash__(self) -> int:
        return hash(self.url)

    def __repr__(self) -> str:
        return f'<Asset url={self.url!r}>'

    @property
    def url(self) -> str:
        """:class:`str`: The url of the asset."""
        if self._size is MISSING:
            return self._url

        # Resize the URL from the size
        return f'{self._url[:-4]}_{self._size}.png'

    @property
    def can_resize(self) -> bool:
        """
        Returns
        --------
        :class:`bool`
            Whether this asset can be resized.
        """
        return self._max_size is not MISSING

    @property
    def max_size(self) -> Optional[int]:
        """
        Returns
        --------
        Optional[:class:`int`]
            The max size of the asset. If ``None``, there is no max size. If `-1`, resizing is not allowed.
        """
        if self._max_size is MISSING:
            return -1

        return self._max_size

    def resize(self, size: int) -> Self:
        """Resizes the asset to the given size.

        Parameters
        ----------
        size: :class:`int`
            The size to resize the asset to. This must be a power of 2.

        Returns
        --------
        :class:`fortnite_api.Asset`
            The resized asset.

        Raises
        ------
        ValueError
            This asset does not support resizing.
        """
        if self._max_size is MISSING:
            raise ValueError('This asset does not support resizing.')

        if (size & (size - 1) != 0) or size <= 0:
            raise TypeError('Size must be a power of 2.')

        if self._max_size is not None:
            if size > self._max_size:
                raise ValueError(f'Size must be less than or equal to {self._max_size}.')

        self._size = size
        return self

    @overload
    def read(self: Asset[HTTPClient], /) -> Coroutine[Any, Any, bytes]: ...

    @overload
    def read(self: Asset[SyncHTTPClient], /) -> bytes: ...

    def read(self) -> Union[Coroutine[Any, Any, bytes], bytes]:
        """|maybecoro|

        Retrieves the content of this asset as a :class:`bytes` object. This is only a coroutine if the client is
        an async client, otherwise it is a regular method.

        Returns
        --------
        :class:`bytes`
            The image bytes.
        """
        return self._http.request(_AssetRoute(self.url))
