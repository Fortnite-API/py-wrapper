import typing
from enum import Enum

from .aes import AES
from .cosmetics import BrCosmetic
from .creator_code import CreatorCode
from .enums import GameLanguage, MatchMethod, NewsType
from .errors import MissingSearchParameter, MissingIDParameter, NotFound
from .news import GameModeNews, News
from .shop import BrShop

_SEARCH_PARAMETERS = {
    'language': [None, [GameLanguage]],
    'search_language': ['searchLanguage', [GameLanguage]],
    'match_method': ['matchMethod', [MatchMethod]],
    'type': [None, [str, None]],
    'backend_type': ['backendType', [str, None]],
    'rarity': [None, [str, None]],
    'display_rarity': ['displayRarity', [str, None]],
    'backend_rarity': ['backendRarity', [str, None]],
    'name': [None, [str, None]],
    'short_description': ['shortDescription', [str, None]],
    'description': [None, [str, None]],
    'set': ['set', [str, None]],
    'set_text': ['setText', [str, None]],
    'series': [None, [str, None]],
    'backend_series': ['backendSeries', [str, None]],
    'has_small_icon': ['hasSmallIcon', [bool, None]],
    'has_icon': ['hasIcon', [bool, None]],
    'has_featured_image': ['hasFeaturedImage', [bool, None]],
    'has_background_image': ['hasBackgroundImage', [bool, None]],
    'has_cover_art': ['hasCoverArt', [bool, None]],
    'has_decal': ['hasDecal', [bool, None]],
    'has_variants': ['hasVariants', [bool, None]],
    'has_gameplay_tags': ['hasGameplayTags', [bool, None]],
    'gameplay_tag': ['gameplayTag', [str, None]]
}


def _parse_search_parameter(**search_parameters):
    parameters = {}  # TODO: Empty string as search parameter
    for key, value in search_parameters.items():
        search_parameter_data = _SEARCH_PARAMETERS.get(key)
        if search_parameter_data is None:
            continue
        if type(value) not in search_parameter_data[1]:
            types = ' or '.join([str(t) for t in search_parameter_data[1]])
            raise TypeError('{0} require a value of type {1}'.format(key, types))
        key = search_parameter_data[0] if search_parameter_data[0] else key
        value = value if not isinstance(value, Enum) else value.value if value is not None else '<null>'
        parameters[key] = str(value) if value is not None else '<null>'
    if len(parameters) == 0:
        raise MissingSearchParameter('at least one search parameter is required')
    return parameters


class SyncAESEndpoints:

    def __init__(self, client):
        self._client = client

    def fetch(self):
        data = self._client.http.get('aes')
        return AES(data['data'])


class AsyncAESEndpoints:

    def __init__(self, client):
        self._client = client

    async def fetch(self):
        data = await self._client.http.get('aes')
        return AES(data['data'])


class SyncCosmeticsEndpoints:

    def __init__(self, client):
        self._client = client

    def fetch_all(self, language=GameLanguage.ENGLISH):
        """Returns an list of all battle royale cosmetics.

        Parameters
        -----------
        language: :class:`GameLanguage`
            The language in which the cosmetics should be returned. Default is set to english.

        Returns
        --------
        List[:class:`BrCosmetic`]
            A list of all cosmetics.

        Raises
        -------
        Unauthorized
            You have not used a valid API key.
        RateLimited
            You reached the rate limit.
        ServiceUnavailable
            The Fortnite-API.com server is currently not available.
        """
        params = {'language': language.value}
        data = self._client.http.get('cosmetics/br', params=params)
        return [BrCosmetic(item_data) for item_data in data['data']]

    def search_by_id(self, *cosmetic_ids, language=GameLanguage.ENGLISH):
        """Returns an list of the requested battle royale cosmetic ids.

        Parameters
        -----------
        \*cosmetic_ids: :class:`str`
            The id of the cosmetic

        Returns
        --------
        List[:class:`BrCosmetic`]
            A list of all cosmetics.

        Raises
        -------
        Unauthorized
            You have not used a valid API key.
        RateLimited
            You reached the rate limit.
        ServiceUnavailable
            The Fortnite-API.com server is currently not available.
        """
        cosmetic_ids = list(cosmetic_ids)
        params = {'language': language.value}

        if len(cosmetic_ids) == 0:
            raise MissingIDParameter('at least one cosmetic id is required')

        endpoint = 'cosmetics/br/search/ids'
        endpoint += '?id=' + cosmetic_ids[0]
        del cosmetic_ids[0]
        endpoint += '&id='.join(cosmetic_ids)
        data = self._client.http.get(endpoint, params=params)
        return [BrCosmetic(item_data) for item_data in data['data']]

    def search_all(self, **search_parameters) -> typing.List[BrCosmetic]:
        data = self._client.http.get('cosmetics/br/search/all',
                                     params=_parse_search_parameter(**search_parameters))
        return [BrCosmetic(item_data) for item_data in data['data']]

    def search_first(self, **search_parameters) -> BrCosmetic:
        data = self._client.http.get('cosmetics/br/search',
                                     params=_parse_search_parameter(**search_parameters))
        return BrCosmetic(data['data'])


class AsyncCosmeticsEndpoints:

    def __init__(self, client):
        self._client = client

    async def fetch_all(self, language: GameLanguage = GameLanguage.ENGLISH) -> typing.List[BrCosmetic]:
        params = {'language': language.value}
        data = await self._client.http.get('cosmetics/br', params=params)
        return [BrCosmetic(item_data) for item_data in data['data']]

    async def search_by_id(self, *cosmetic_id: str, language: GameLanguage = GameLanguage.ENGLISH) -> typing.List[BrCosmetic]:
        cosmetic_ids = list(cosmetic_id)
        params = {'language': language.value}

        if len(cosmetic_ids) == 0:
            raise MissingIDParameter('at least one cosmetic id is required')

        endpoint = 'cosmetics/br/search/ids'
        endpoint += '?id=' + cosmetic_ids[0]
        del cosmetic_ids[0]
        endpoint += '&id='.join(cosmetic_ids)
        data = await self._client.http.get(endpoint, params=params)
        return [BrCosmetic(item_data) for item_data in data['data']]

    async def search_all(self, **search_parameters) -> typing.List[BrCosmetic]:
        data = await self._client.http.get('cosmetics/br/search/all',
                                           params=_parse_search_parameter(**search_parameters))
        return [BrCosmetic(item_data) for item_data in data['data']]

    async def search_first(self, **search_parameters) -> BrCosmetic:
        data = await self._client.http.get('cosmetics/br/search', params=_parse_search_parameter(**search_parameters))
        return BrCosmetic(data['data'])


class SyncCreatorCodeEndpoints:

    def __init__(self, client):
        self._client = client

    def fetch(self, slug: str) -> CreatorCode:
        params = {'slug': slug}
        data = self._client.http.get('creatorcode', params=params)
        return CreatorCode(data['data'])

    def exists(self, slug: str) -> bool:
        try:
            self.fetch(slug)
            return True
        except NotFound:
            return False

    def search_first(self, slug: str) -> CreatorCode:
        params = {'slug': slug}
        data = self._client.http.get('creatorcode/search', params=params)
        return CreatorCode(data['data'])

    def search_all(self, slug: str) -> typing.List[CreatorCode]:
        params = {'slug': slug}
        data = self._client.http.get('creatorcode/search/all', params=params)
        return [CreatorCode(creator_code_data) for creator_code_data in data['data']]


class AsyncCreatorCodeEndpoints:

    def __init__(self, client):
        self._client = client

    async def fetch(self, slug: str) -> CreatorCode:
        params = {'slug': slug}
        data = await self._client.http.get('creatorcode', params=params)
        return CreatorCode(data['data'])

    async def exists(self, slug: str) -> bool:
        try:
            await self.fetch(slug)
            return True
        except NotFound:
            return False

    async def search_first(self, slug: str) -> CreatorCode:
        params = {'slug': slug}
        data = await self._client.http.get('creatorcode/search', params=params)
        return CreatorCode(data['data'])

    async def search_all(self, slug: str) -> typing.List[CreatorCode]:
        params = {'slug': slug}
        data = await self._client.http.get('creatorcode/search/all', params=params)
        return [CreatorCode(creator_code_data) for creator_code_data in data['data']]


class SyncNewsEndpoints:

    def __init__(self, client):
        self._client = client

    def fetch(self, language: GameLanguage = GameLanguage.ENGLISH) -> News:
        params = {'language': language.value}
        data = self._client.http.get('news', params=params)
        return News(data['data'])

    def fetch_by_type(self, news_type: NewsType, language=GameLanguage.ENGLISH) -> GameModeNews:
        params = {'language': language.value}
        data = self._client.http.get('news/' + news_type.value, params=params)
        return GameModeNews(data['data'])


class AsyncNewsEndpoints:

    def __init__(self, client):
        self._client = client

    async def fetch(self, language: GameLanguage = GameLanguage.ENGLISH) -> News:
        params = {'language': language.value}
        data = await self._client.http.get('news', params=params)
        return News(data['data'])

    async def fetch_by_type(self, news_type: NewsType, language: GameLanguage = GameLanguage.ENGLISH) -> GameModeNews:
        params = {'language': language.value}
        data = await self._client.http.get('news/' + news_type.value, params=params)
        return GameModeNews(data['data'])


class SyncShopEndpoints:

    def __init__(self, client):
        self._client = client

    def fetch(self, language: GameLanguage = GameLanguage.ENGLISH) -> BrShop:
        params = {'language': language.value}
        data = self._client.http.get('shop/br', params=params)
        return BrShop(data['data'])


class AsyncShopEndpoints:

    def __init__(self, client):
        self._client = client

    async def fetch(self, language: GameLanguage = GameLanguage.ENGLISH) -> BrShop:
        params = {'language': language.value}
        data = await self._client.http.get('shop/br', params=params)
        return BrShop(data['data'])
