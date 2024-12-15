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

import datetime
from typing import Any, Generic

from .abc import ReconstructAble
from .cosmetics import (
    CosmeticBr,
    CosmeticCar,
    CosmeticInstrument,
    CosmeticLegoKit,
    CosmeticT,
    CosmeticTrack,
    VariantBean,
    VariantLego,
)
from .enums import CosmeticCategory
from .http import HTTPClientT
from .proxies import TransformerListProxy
from .utils import get_with_fallback, parse_time

__all__: tuple[str, ...] = ("NewCosmetic", "NewCosmetics")


class NewCosmetic(Generic[CosmeticT]):
    """
    .. attributetable:: fortnite_api.NewCosmetic

    Represents a response from the new cosmetics endpoint for a given cosmetic type. You can use the
    :attr:`type` to help you determine what :attr:`items` will be. The :attr:`items` will be a list of
    the corresponding cosmetic type:

    .. list-table::
        :header-rows: 1

        *   - :attr:`type`
            - Corresponding :attr:`items`
        *   - :attr:`fortnite_api.CosmeticCategory.BR`
            - List of :class:`~fortnite_api.CosmeticBr`
        *   - :attr:`fortnite_api.CosmeticCategory.TRACKS`
            - List of :class:`~fortnite_api.CosmeticTrack`
        *   - :attr:`fortnite_api.CosmeticCategory.INSTRUMENTS`
            - List of :class:`~fortnite_api.CosmeticInstrument`
        *   - :attr:`fortnite_api.CosmeticCategory.CARS`
            - List of :class:`~fortnite_api.CosmeticCar`
        *   - :attr:`fortnite_api.CosmeticCategory.LEGO`
            - List of :class:`~fortnite_api.VariantLego`
        *   - :attr:`fortnite_api.CosmeticCategory.LEGO_KITS`
            - List of :class:`~fortnite_api.CosmeticLegoKit`

    Attributes
    ----------
    type: :class:`fortnite_api.CosmeticCategory`
        The type of new cosmetics displayed.
    hash: Optional[:class:`str`]
        The hash of the new cosmetics. Can be ``None`` if no
        new cosmetics have been given for the cosmetic type.
    last_addition: :class:`datetime.datetime`
        The last addition of new cosmetics.
    items: List[:class:`fortnite_api.Cosmetic`]
        The new cosmetics. This corresponds to the type of new cosmetics.
        Can be empty if no new cosmetics have been given.
    """

    def __init__(
        self,
        *,
        type: CosmeticCategory,
        hash: str | None = None,
        last_addition: datetime.datetime | None = None,
        items: list[CosmeticT],
    ) -> None:
        self.type: CosmeticCategory = type
        self.hash: str | None = hash
        self.last_addition: datetime.datetime | None = last_addition
        self.items: list[CosmeticT] = items


class NewCosmetics(ReconstructAble[dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.NewCosmetics

    Represents a response from the new cosmetics endpoint.

    This class inherits from :class:`~fortnite_api.ReconstructAble`.

    Examples
    -------
    .. code-block:: python3
        :caption: Obtain all the new Battle Royale cosmetics.

        new_cosmetics = await client.fetch_cosmetics_new()
        new_br_cosmetics = new_cosmetics.br
        for cosmetic in new_br_cosmetics.items:
            print(cosmetic.name)

    Attributes
    ----------
    build: :class:`str`
        The build of Fortnite that these cosmetics were added in.
    previous_build: :class:`str`
        The previous build of Fortnite.
    date: :class:`datetime.datetime`
        The date of the new cosmetics.
    global_hash: :class:`str`
        The combined hash of all new cosmetics.
    global_last_addition: :class:`datetime.datetime`
        The last time a new cosmetic was added.
    br: :class:`fortnite_api.NewCosmetic`
        The new BR cosmetics.
    tracks: :class:`fortnite_api.NewCosmetic`
        The new track cosmetics.
    instruments: :class:`fortnite_api.NewCosmetic`
        The new instrument cosmetics.
    cars: :class:`fortnite_api.NewCosmetic`
        The new car cosmetics.
    lego: :class:`fortnite_api.NewCosmetic`
        The new lego cosmetic variants.
    lego_kits: :class:`fortnite_api.NewCosmetic`
        The new lego kit cosmetics.
    beans: :class:`fortnite_api.NewCosmetic`
        The new bean cosmetic variants.
    """

    def __init__(self, *, data: dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.build: str = data["build"]
        self.previous_build: str = data["previousBuild"]
        self.date: datetime.datetime = parse_time(data["date"])
        self.global_hash: str = data["hashes"]["all"]
        self.global_last_addition: datetime.datetime = parse_time(data["lastAdditions"]["all"])

        self._hashes = data["hashes"]
        self._items = data["items"]
        self._last_additions = data["lastAdditions"]

        self.br: NewCosmetic[CosmeticBr[HTTPClientT]] = self._parse_new_cosmetic(
            cosmetic_type=CosmeticCategory.BR,
            internal_key="br",
            cosmetic_class=CosmeticBr,
        )

        self.tracks: NewCosmetic[CosmeticTrack[HTTPClientT]] = self._parse_new_cosmetic(
            cosmetic_type=CosmeticCategory.TRACKS,
            internal_key="tracks",
            cosmetic_class=CosmeticTrack,
        )

        self.instruments: NewCosmetic[CosmeticInstrument[HTTPClientT]] = self._parse_new_cosmetic(
            cosmetic_type=CosmeticCategory.INSTRUMENTS,
            internal_key="instruments",
            cosmetic_class=CosmeticInstrument,
        )

        self.cars: NewCosmetic[CosmeticCar[HTTPClientT]] = self._parse_new_cosmetic(
            cosmetic_type=CosmeticCategory.CARS,
            internal_key="cars",
            cosmetic_class=CosmeticCar,
        )

        self.lego: NewCosmetic[VariantLego[HTTPClientT]] = self._parse_new_cosmetic(
            cosmetic_type=CosmeticCategory.LEGO,
            internal_key="lego",
            cosmetic_class=VariantLego,
        )

        self.lego_kits: NewCosmetic[CosmeticLegoKit[HTTPClientT]] = self._parse_new_cosmetic(
            cosmetic_type=CosmeticCategory.LEGO_KITS,
            internal_key="legoKits",
            cosmetic_class=CosmeticLegoKit,
        )

        self.beans: NewCosmetic[VariantBean[HTTPClientT]] = self._parse_new_cosmetic(
            cosmetic_type=CosmeticCategory.BEANS,
            internal_key="beans",
            cosmetic_class=VariantBean,
        )

    def _parse_new_cosmetic(
        self,
        *,
        cosmetic_type: CosmeticCategory,
        internal_key: str,
        cosmetic_class: type[CosmeticT],
    ) -> NewCosmetic[CosmeticT]:
        cosmetic_items: list[dict[str, Any]] = get_with_fallback(self._items, internal_key, list)

        last_addition_str = self._last_additions[internal_key]
        last_addition: datetime.datetime | None = last_addition_str and parse_time(last_addition_str)

        return NewCosmetic(
            type=cosmetic_type,
            hash=self._hashes.get(internal_key),
            last_addition=last_addition,
            items=TransformerListProxy(
                cosmetic_items,
                lambda x: cosmetic_class(data=x, http=self._http),
            ),
        )
