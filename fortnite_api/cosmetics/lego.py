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

from typing import TYPE_CHECKING, Any, Coroutine, Dict, List, Optional, Tuple, Union, overload

from ..asset import Asset
from ..enums import GameLanguage
from ..http import HTTPClientT
from ..utils import get_with_fallback, simple_repr
from .br import CosmeticBr
from .common import Cosmetic, CosmeticImages

if TYPE_CHECKING:
    from ..http import HTTPClient, SyncHTTPClient

__all__: Tuple[str, ...] = ('CosmeticLego', 'CosmeticLegoImages')


@simple_repr
class CosmeticLegoImages(CosmeticImages[HTTPClientT]):
    """
    .. attributetable:: fortnite_api.CosmeticLegoImages

    A class representing the images of a lego cosmetic.

    This class inherits from :class:`fortnite_api.CosmeticImages`.

    Attributes
    ----------
    wide: Optional[:class:`fortnite_api.Asset`]
        The wide image of the lego cosmetic.
    """

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        _wide = data.get('wide')
        self.wide: Optional[Asset[HTTPClientT]] = _wide and Asset(http=http, url=_wide)


@simple_repr
class CosmeticLego(Cosmetic[HTTPClientT]):
    """
    .. attributetable:: fortnite_api.CosmeticLego

    Represents a Lego cosmetic.

    This class inherits from :class:`fortnite_api.Cosmetic`.

    Attributes
    ----------
    cosmetic_id: :class:`str`
        The ID of the cosmetic that this lego cosmetic is based on.
    sound_library_tags: List[:class:`str`]
        The sound library tags of the lego cosmetic.
    images: Optional[:class:`fortnite_api.CosmeticLegoImages`]
        The images of the lego cosmetic.
    path: Optional[:class:`str`]
        The path of the lego cosmetic.
    """

    __slots__: Tuple[str, ...] = ('cosmetic_id', 'sound_library_tags', 'images', 'path')

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.cosmetic_id: str = data['cosmeticId']
        self.sound_library_tags: List[str] = get_with_fallback(data, 'soundLibraryTags', list)

        _images = data.get('images')
        self.images: Optional[CosmeticLegoImages[HTTPClientT]] = _images and CosmeticLegoImages(data=_images, http=http)
        self.path: Optional[str] = data.get('path')

    @overload
    def fetch_cosmetic_br(
        self: CosmeticLego[HTTPClient], *, language: Optional[GameLanguage] = None
    ) -> Coroutine[Any, Any, CosmeticBr]: ...

    @overload
    def fetch_cosmetic_br(self: CosmeticLego[SyncHTTPClient], *, language: Optional[GameLanguage] = None) -> CosmeticBr: ...

    def fetch_cosmetic_br(
        self, *, language: Optional[GameLanguage] = None
    ) -> Union[Coroutine[Any, Any, CosmeticBr], CosmeticBr]:
        """|coro|

        Fetches the Battle Royale cosmetic that this lego cosmetic is based on.

        Parameters
        ----------
        language: Optional[:class:`fortnite_api.GameLanguage`]
            The language to fetch the cosmetic in.

        Returns
        -------
        :class:`fortnite_api.CosmeticBr`
            The Battle Royale cosmetic that this lego cosmetic is based on.
        """
        return self._http.get_cosmetic_br(self.cosmetic_id, language=language and language.value)
