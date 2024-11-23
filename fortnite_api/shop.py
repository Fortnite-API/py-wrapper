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
import re
from typing import Any, Generator, Optional

from typing_extensions import Self

from .abc import Hashable, ReconstructAble
from .asset import Asset
from .cosmetics import Cosmetic, CosmeticBr, CosmeticCar, CosmeticInstrument, CosmeticLegoKit, CosmeticTrack
from .enums import BannerIntensity
from .http import HTTPClientT
from .new_display_asset import NewDisplayAsset
from .proxies import TransformerListProxy
from .utils import get_with_fallback, parse_time

__all__: tuple[str, ...] = (
    "ShopEntryOfferTag",
    "ShopEntryBundle",
    "ShopEntryBanner",
    "ShopEntryLayout",
    "ShopEntryColors",
    "ShopEntry",
    "Shop",
    "TileSize",
)

# Matches a tile size: size_<int>_x_<int>
_TILE_SIZE_REGEX = re.compile(r"size_(?P<width>\d+)_x_(?P<height>\d+)", re.IGNORECASE)


class TileSize:
    """
    .. attributetable:: fortnite_api.TileSize

    Represents the size of a tile in the shop.

    .. container:: operations

        .. describe:: x == y

            Checks if two tile sizes are equal.

        .. describe:: x != y

            Checks if two tile sizes are not equal.

    Parameters
    ----------
    width: :class:`int`
        The width of the tile.
    height: :class:`int`
        The height of the tile.
    internal: :class:`str`
        The internal representation of the tile size. This can be the default Epic API value
        in the format ``Size_<width>_x_<height>``.

    Attributes
    ----------
    width: :class:`int`
        The width of the tile.
    height: :class:`int`
        The height of the tile.
    internal: :class:`str`
        The internal representation of the tile size. This can be the default Epic API value
        in the format ``Size_<width>_x_<height>``.
    """

    __slots__: tuple[str, ...] = ("width", "height", "internal")

    def __init__(self, *, width: int, height: int, internal: str) -> None:
        self.width: int = width
        self.height: int = height
        self.internal: str = internal

    def __repr__(self) -> str:
        return f"<TileSize width={self.width} height={self.height}>"

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, TileSize):
            return False

        return value.width == self.width and value.height == self.height

    @classmethod
    def from_value(cls: type[Self], value: str, /) -> Self:
        """Constructs a tile size from the value provided by the API. This method
        parses the passed value and ensures that it is in the correct format,
        ``Size_<width>_x_<height>``. It has been exposed in the case that
        the user wants to construct a tile size from a custom value.

        Parameters
        ----------
        value: :class:`str`
            The value to parse.

        Returns
        -------
        :class:`TileSize`
            The constructed tile size.

        Raises
        ------
        ValueError
            If the value is not in the correct format.
        """
        # Try and match the regex
        match = _TILE_SIZE_REGEX.match(value)
        if not match:
            # Epic only uses the tile sizing on the regex. If there isn't a match
            # we can safely assume an exception must be raised
            raise ValueError(f"Invalid tile size: {value!r}")

        return cls(
            width=int(match.group("width")),
            height=int(match.group("height")),
            internal=value,
        )


class ShopEntryOfferTag(Hashable, ReconstructAble[dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.ShopEntryOfferTag

    Represents a shop entry offer tag. This class inherits from :class:`~fortnite_api.ReconstructAble`.

    Attributes
    ----------
    id: :class:`str`
        The ID of the offer tag.
    text: :class:`str`
        The text of the offer tag.
    """

    __slots__: tuple[str, ...] = ("id", "text")

    def __init__(self, *, data: dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.id: str = data["id"]
        self.text: str = data["text"]


class ShopEntryBundle(ReconstructAble[dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.ShopEntryBundle

    Represents a shop entry bundle. This class inherits from :class:`~fortnite_api.ReconstructAble`.

    Attributes
    ----------
    name: :class:`str`
        The name of the bundle.
    info: :class:`str`
        The information of the bundle.
    image: :class:`fortnite_api.Asset`
        The image of the bundle.
    """

    __slots__: tuple[str, ...] = ("name", "info", "image")

    def __init__(self, *, data: dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.name: str = data["name"]
        self.info: str = data["info"]
        self.image: Asset[HTTPClientT] = Asset(url=data["image"], http=http)


class ShopEntryBanner(ReconstructAble[dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.ShopEntryBanner

    A class to represent a shop entry banner. This class inherits
    from :class:`~fortnite_api.ReconstructAble`.

    Attributes
    ----------
    value: :class:`str`
        The text of the banner.
    intensity: :class:`fortnite_api.BannerIntensity`
        The intensity of the banner.
    backend_value: :class:`str`
        The backend value of the banner.
    """

    __slots__: tuple[str, ...] = ("value", "intensity", "backend_value")

    def __init__(self, *, data: dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.value: str = data["value"]
        self.intensity: BannerIntensity = BannerIntensity(data["intensity"])
        self.backend_value: str = data["backendValue"]


class ShopEntryLayout(Hashable, ReconstructAble[dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.ShopEntryLayout

    Represents the layout of a shop entry. This class
    inherits from :class:`~fortnite_api.ReconstructAble`.

    Attributes
    ----------
    id: :class:`str`
        The ID of the layout.
    name: :class:`str`
        The name of the layout.
    category: Optional[:class:`str`]
        The category of the layout, if any.
    index: :class:`int`
        The index of the layout.
    rank: :class:`int`
        The rank of the layout used for sorting.
    show_ineligible_offers: :class:`str`
        Whether ineligible offers are displayed in the layout or not.
    background: Optional[:class:`fortnite_api.Asset`]
        The background asset of the layout, if any.
    use_wide_preview: :class:`bool`
        Whether the layout uses a wide preview or not.
    display_type: Optional[:class:`str`]
        The display type of the layout, if any specified.
    """

    __slots__: tuple[str, ...] = (
        "id",
        "name",
        "category",
        "index",
        "rank",
        "show_ineligible_offers",
        "background",
        "use_wide_preview",
        "display_type",
    )

    def __init__(self, *, data: dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.id: str = data["id"]
        self.name: str = data["name"]
        self.category: Optional[str] = data.get("category")
        self.index: int = data["index"]
        self.rank: int = data["rank"]
        self.show_ineligible_offers: str = data["showIneligibleOffers"]

        _background = data.get("background")
        self.background: Optional[Asset[HTTPClientT]] = _background and Asset(url=_background, http=http)

        self.use_wide_preview: bool = data.get('useWidePreview', False)
        self.display_type: Optional[str] = data.get('displayType')
        # Billboards include textureMetadata, stringMetadata and textMetadata


class ShopEntryColors(ReconstructAble[dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.ShopEntryColors

    Represents the colors of a shop entry. This class inherits from :class:`~fortnite_api.ReconstructAble`.

    Attributes
    ----------
    color1: :class:`str`
        The first color of background gradient.
    color2: Optional[:class:`str`]
        The second color of background gradient. If not present, the gradient only consists of two colors.
    color3: :class:`str`
        The third color of background gradient.
    text_background_color: Optional[:class:`str`]
        The fade out overlaying gradient color on which the text is displayed.
    """

    __slots__: tuple[str, ...] = ("color1", "color2", "color3", "text_background_color")

    def __init__(self, *, data: dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.color1: str = data['color1']
        self.color2: Optional[str] = data.get('color2')
        self.color3: str = data['color3']
        self.text_background_color: Optional[str] = data.get('textBackgroundColor')


class ShopEntry(ReconstructAble[dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.ShopEntry

    Represents an item shop entry. Each entry in the shop contains
    related cosmetics that are available in the shop. This class
    inherits from :class:`~fortnite_api.ReconstructAble`.

    .. container:: operations

        .. describe:: len(x)

            Returns the total amount of cosmetics in this entry.

            .. code-block:: python3

                shop = await client.fetch_shop()
                for entry in shop.entries:
                    print(f'Entry has {len(entry)} cosmetics.')

        .. describe:: iter(x)

            Returns an iterator of the cosmetics, working through one unique cosmetic type before
            continuing onto the next. Works in the following
            order: :class:`~fortnite_api.CosmeticBr`, :class:`~fortnite_api.CosmeticTrack`,
            :class:`~fortnite_api.CosmeticInstrument`, :class:`~fortnite_api.CosmeticCar`,
            :class:`~fortnite_api.CosmeticLegoKit`.

            .. code-block:: python3

                shop = await client.fetch_shop()
                for entry in shop.entries:
                    for cosmetic in entry:
                        print(cosmetic.id, cosmetic.type)

    Attributes
    ----------
    regular_price: :class:`int`
        The regular price of the entry.
    final_price: :class:`int`
        The final price of the entry. This is in case it is on sale.
    in_date: :class:`datetime.datetime`
        The date when this entry was added to the shop.
    out_date: :class:`datetime.datetime`
        The date when this entry will be removed from the shop.
    offer_tag: Optional[:class:`fortnite_api.ShopEntryOfferTag`]
        The offer tag of this entry, if any.
    bundle: Optional[:class:`fortnite_api.ShopEntryBundle`]
        The bundle that this entry belongs to, if any.
    banner: Optional[:class:`fortnite_api.ShopEntryBanner`]
        The banner information for this shop entry, if any.
    giftable: :class:`bool`
        Whether this entry is able to be gifted.
    refundable: :class:`bool`
        Whether this entry is refundable.
    sort_priority: :class:`int`
        The sort priority of this entry.
    layout_id: :class:`str`
        The layout ID of this entry.
    layout: Optional[:class:`fortnite_api.ShopEntryLayout`]
        The layout of this entry, if any.
    dev_name: :class:`str`
        The internal dev name of this entry.
    offer_id: :class:`str`
        The offer ID of this entry.
    display_asset_path: Optional[:class:`str`]
        The display asset path of this entry.
    tile_size: :class:`fortnite_api.TileSize`
        The tile size of this entry.
    new_display_asset_path: Optional[:class:`str`]
        The new display asset path of this entry.
    new_display_asset: :class:`fortnite_api.NewDisplayAsset`
        The new display asset of this entry.
    colors: :class:`fortnite_api.ShopEntryColors`
        The colors of this entry.
    br: List[:class:`fortnite_api.CosmeticBr`]
        The Battle Royale cosmetics in this entry.
    tracks: List[:class:`fortnite_api.CosmeticTrack`]
        The tracks in this entry.
    instruments: List[:class:`fortnite_api.CosmeticInstrument`]
        The instruments in this entry.
    cars: List[:class:`fortnite_api.CosmeticCar`]
        The cars in this entry.
    lego_kits: List[:class:`fortnite_api.CosmeticLegoKit`]
        The LEGO kits in this entry.
    """

    __slots__: tuple[str, ...] = (
        "regular_price",
        "final_price",
        "in_date",
        "out_date",
        "offer_tag",
        "bundle",
        "banner",
        "giftable",
        "refundable",
        "sort_priority",
        "layout_id",
        "layout",
        "dev_name",
        "offer_id",
        "display_asset_path",
        "tile_size",
        "new_display_asset_path",
        "new_display_asset",
        "colors",
        "br",
        "tracks",
        "instruments",
        "cars",
        "lego_kits",
    )

    def __init__(self, *, data: dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.regular_price: int = data["regularPrice"]
        self.final_price: int = data["finalPrice"]

        self.in_date: datetime.datetime = parse_time(data["inDate"])
        self.out_date: datetime.datetime = parse_time(data["outDate"])

        _offer_tag = data.get("offerTag")
        self.offer_tag: Optional[ShopEntryOfferTag[HTTPClientT]] = _offer_tag and ShopEntryOfferTag(
            data=_offer_tag, http=http
        )

        _bundle = data.get("bundle")
        self.bundle: Optional[ShopEntryBundle[HTTPClientT]] = _bundle and ShopEntryBundle(data=_bundle, http=http)

        _banner = data.get("banner")
        self.banner: Optional[ShopEntryBanner[HTTPClientT]] = _banner and ShopEntryBanner(data=_banner, http=http)

        self.giftable: bool = data["giftable"]
        self.refundable: bool = data["refundable"]
        self.sort_priority: int = data["sortPriority"]
        self.layout_id: str = data["layoutId"]

        _layout = data.get("layout")
        self.layout: Optional[ShopEntryLayout[HTTPClientT]] = _layout and ShopEntryLayout(data=_layout, http=http)

        self.dev_name: str = data["devName"]
        self.offer_id: str = data["offerId"]
        self.display_asset_path: Optional[str] = data.get("displayAssetPath")

        self.tile_size: TileSize = TileSize.from_value(data["tileSize"])

        self.new_display_asset_path: Optional[str] = data.get("newDisplayAssetPath")

        _new_display_asset = data.get("newDisplayAsset")
        self.new_display_asset: Optional[NewDisplayAsset[HTTPClientT]] = _new_display_asset and NewDisplayAsset(
            data=data["newDisplayAsset"], http=http
        )

        _colors = data.get("colors")
        self.colors: Optional[ShopEntryColors[HTTPClientT]] = _colors and ShopEntryColors(data=_colors, http=http)

        self.br: list[CosmeticBr[HTTPClientT]] = TransformerListProxy(
            get_with_fallback(data, "brItems", list),
            transform_data=lambda d: CosmeticBr(data=d, http=http),
        )

        self.tracks: list[CosmeticTrack[HTTPClientT]] = TransformerListProxy(
            get_with_fallback(data, "tracks", list),
            transform_data=lambda d: CosmeticTrack(data=d, http=http),
        )

        self.instruments: list[CosmeticInstrument[HTTPClientT]] = TransformerListProxy(
            get_with_fallback(data, "instruments", list),
            transform_data=lambda d: CosmeticInstrument(data=d, http=http),
        )

        self.cars: list[CosmeticCar[HTTPClientT]] = TransformerListProxy(
            get_with_fallback(data, "cars", list),
            transform_data=lambda d: CosmeticCar(data=d, http=http),
        )

        self.lego_kits: list[CosmeticLegoKit[HTTPClientT]] = TransformerListProxy(
            get_with_fallback(data, "legoKits", list),
            transform_data=lambda d: CosmeticLegoKit(data=d, http=http),
        )

    def __iter__(self) -> Generator[Cosmetic[dict[str, Any], HTTPClientT], None, None]:
        yield from self.br

        yield from self.tracks

        yield from self.instruments

        yield from self.cars

        yield from self.lego_kits

    def __len__(self):
        return len(self.br) + len(self.tracks) + len(self.instruments) + len(self.cars) + len(self.lego_kits)


class Shop(ReconstructAble[dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.Shop

    Represents the Fortnite shop.

    Attributes
    ----------
    hash: :class:`str`
        A unique hash that represents this shop.
    date: :class:`datetime.datetime`
        The date when this shop was last updated.
    vbuck_icon: :class:`fortnite_api.Asset`
        An asset of the V-Buck icon.
    entries: List[:class:`fortnite_api.ShopEntry`]
        A list of shop entries. Each entry contains cosmetics that are available in the shop.
    """

    __slots__: tuple[str, ...] = (
        "hash",
        "date",
        "vbuck_icon",
        "entries",
    )

    def __init__(self, *, data: dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.hash: str = data["hash"]
        self.date: datetime.datetime = parse_time(data["date"])

        self.vbuck_icon: Asset[HTTPClientT] = Asset(url=data["vbuckIcon"], http=http)

        _entries = get_with_fallback(data, "entries", list)
        self.entries: list[ShopEntry[HTTPClientT]] = [ShopEntry(data=item, http=http) for item in _entries]
