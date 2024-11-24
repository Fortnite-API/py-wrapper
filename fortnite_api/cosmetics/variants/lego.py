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
from typing import TYPE_CHECKING, Any, Optional, Union, overload

from ...enums import GameLanguage
from ...http import HTTPClientT
from ...utils import get_with_fallback, simple_repr
from ..br import CosmeticBr
from ..common import Cosmetic, CosmeticImages

if TYPE_CHECKING:
    from ...http import HTTPClient, SyncHTTPClient

__all__: tuple[str, ...] = ('VariantLego',)


@simple_repr
class VariantLego(Cosmetic[dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.VariantLego

    Represents a Lego cosmetic variant.

    This class inherits from :class:`fortnite_api.Cosmetic`.

    .. container:: operations

        .. describe:: repr(x)

            Returns a representation of the account in the form of a string.

    Attributes
    ----------
    cosmetic_id: :class:`str`
        The ID of the cosmetic that this lego cosmetic variant is based on.
    sound_library_tags: List[:class:`str`]
        The sound library tags of the lego cosmetic variant.
    images: Optional[:class:`fortnite_api.CosmeticImages`]
        The images of the lego cosmetic variant.
    path: Optional[:class:`str`]
        The path of the lego cosmetic variant. Will be ``None`` if
        the API response does not contain a path.

        .. opt-in:: INCLUDE_PATHS
    """

    __slots__: tuple[str, ...] = ('cosmetic_id', 'sound_library_tags', 'images', 'path')

    def __init__(self, *, data: dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.cosmetic_id: str = data['cosmeticId']
        self.sound_library_tags: list[str] = get_with_fallback(data, 'soundLibraryTags', list)

        _images = data.get('images')
        self.images: Optional[CosmeticImages[HTTPClientT]] = _images and CosmeticImages(data=_images, http=http)
        self.path: Optional[str] = data.get('path')

    @overload
    def fetch_cosmetic_br(
        self: VariantLego[HTTPClient], *, language: Optional[GameLanguage] = None
    ) -> Coroutine[Any, Any, CosmeticBr]: ...

    @overload
    def fetch_cosmetic_br(self: VariantLego[SyncHTTPClient], *, language: Optional[GameLanguage] = None) -> CosmeticBr: ...

    def fetch_cosmetic_br(
        self, *, language: Optional[GameLanguage] = None
    ) -> Union[Coroutine[Any, Any, CosmeticBr], CosmeticBr]:
        """|coro|

        Fetches the Battle Royale cosmetic that this lego cosmetic variant is based on.

        Parameters
        ----------
        language: Optional[:class:`fortnite_api.GameLanguage`]
            The language to fetch the cosmetic in.

        Returns
        -------
        :class:`fortnite_api.CosmeticBr`
            The Battle Royale cosmetic that this lego cosmetic variant is based on.
        """
        return self._http.get_cosmetic_br(self.cosmetic_id, language=language and language.value)
