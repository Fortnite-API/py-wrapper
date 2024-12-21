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
from typing import TYPE_CHECKING, Any, overload

from ...enums import CustomGender, GameLanguage, try_enum
from ...http import HTTPClientT
from ...utils import get_with_fallback
from ..br import CosmeticBr
from ..common import Cosmetic, CosmeticImages

if TYPE_CHECKING:
    from ...http import HTTPClient, SyncHTTPClient


class VariantBean(Cosmetic[dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.VariantBean

    This class represents the Bean variant of a cosmetic item. This stems from
    the Fortnite x Fall Guys collaboration, where Fortnite cosmetics were
    transformed into Fall Guys beans.

    This class inherits from :class:`fortnite_api.Cosmetic`.

    Attributes
    ----------
    cosmetic_id: Optional[:class:`str`]
        The ID of the cosmetic that this bean represents, if any.
    name: :class:`str`
        The name of this bean.
    gender: :class:`fortnite_api.CustomGender`
        Denotes the gender of this bean.
    gameplay_tags: List[:class:`str`]
        The gameplay tags associated with this bean.

        .. opt-in:: INCLUDE_GAMEPLAY_TAGS
    images: Optional[:class:`fortnite_api.CosmeticImages`]
        Any display images of this bean in the game. Will be ``None``
        if there are no images.
    path: Optional[:class:`str`]
        The game path of this bean. Will be ``None`` if there is no path
        in the API response.

        .. opt-in:: INCLUDE_PATHS
    """

    def __init__(self, *, data: dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.cosmetic_id: str | None = data.get("cosmetic_id")
        self.name: str = data["name"]
        self.gender: CustomGender = try_enum(CustomGender, data["gender"])
        self.gameplay_tags: list[str] = get_with_fallback(data, "gameplay_tags", list)

        _images = data.get("images")
        self.images: CosmeticImages[HTTPClientT] | None = _images and CosmeticImages(data=_images, http=http)
        self.path: str | None = data.get("path")

    @overload
    def fetch_cosmetic_br(
        self: VariantBean[HTTPClient], *, language: GameLanguage | None = None
    ) -> Coroutine[Any, Any, CosmeticBr]: ...

    @overload
    def fetch_cosmetic_br(self: VariantBean[SyncHTTPClient], *, language: GameLanguage | None = None) -> CosmeticBr: ...

    def fetch_cosmetic_br(self, *, language: GameLanguage | None = None) -> Coroutine[Any, Any, CosmeticBr] | CosmeticBr:
        """|coro|

        Fetches the Battle Royale cosmetic that this bean variant is based on.

        Parameters
        ----------
        language: Optional[:class:`fortnite_api.GameLanguage`]
            The language to fetch the cosmetic in.

        Returns
        -------
        :class:`fortnite_api.CosmeticBr`
            The Battle Royale cosmetic that this bean variant is based on.

        Raises
        ------
        ValueError
            The bean variant does not have a corresponding Battle Royale cosmetic.
            I.e. :attr`cosmetic_id` is ``None``.
        """
        cosmetic_id = self.cosmetic_id
        if cosmetic_id is None:
            raise ValueError("This bean variant does not have a corresponding Battle Royale cosmetic.")

        return self._http.get_cosmetic_br(cosmetic_id, language=language and language.value)
