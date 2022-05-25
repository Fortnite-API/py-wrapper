# Sync/Async Python wrapper for [Fortnite-API.com](https://fortnite-api.com)
![GitHub issues](https://img.shields.io/github/issues/Fortnite-API/py-wrapper?logo=github)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/fortnite-api)](https://pypi.org/project/fortnite-api)
[![PyPI](https://img.shields.io/pypi/v/fortnite-api)](https://pypi.org/project/fortnite-api)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fortnite-api?label=python%20version&logo=python&logoColor=yellow)
[![Support](https://discordapp.com/api/guilds/621452110558527502/widget.png?style=shield)](https://discord.gg/T4tyYDK)
<br><br>
This library offers a complete **sync** and **async** wrapper around the endpoints of [Fortnite-API.com](https://fortnite-api.com)

## Installation
```
pip install fortnite-api
```
- Get a API key on https://dash.fortnite-api.com/account

## Documentation
Here is a quick overview how to start.<br><br>
First we need to import the api and initialize client.
```
import fortnite_api

api = fortnite_api.FortniteAPI()
```
###### Parameters
- `api_key` [str] (Optional) - Insert your API key from https://dash.fortnite-api.com/account
- `run_async` [bool] (Optional) - Specify if the API should run async. Default value is `False`
###### Attributes
- `cosmetics` - All cosmetic endpoints
- `shop` - All shop endpoints
- `news` - All news endpoints

<br><br>
Now we can use the client:
### Cosmetics
```
api.cosmetics.fetch_all()
```
Get all Br cosmetics.
###### Parameters
- `language` [GameLanguage] (Optional) - Specify the language of the shop. Default is set to english
###### Returns
Returns a list of `BrCosmetic` objects.

```
api.cosmetics.fetch_new()
```
Get all new Br cosmetics.
###### Parameters
- `language` [GameLanguage] (Optional) - Specify the language of the shop. Default is set to english
###### Returns
Returns a `NewBrCosmetics` object.

___

```
api.cosmetics.search_by_id()
```
Search one o multiple items by their id.
###### Parameters
- `*cosmetic_id` - One or multiple cosmetic ids.
- `language` [GameLanguage] (Optional) - Specify the language of the shop. Default is set to english
###### Returns
Returns a list of `BrCosmetic` objects.

___

```
api.cosmetics.search_all()
```
Search all cosmetics which fit to the search parameters
###### Parameters
- `**search_parameters` - All search parameters are listed on the [Fortnite-API.com Docs](https://fortnite-api.com/documentation). Remember that Python does not use a camel case. So e.g. `searchLanguage` becomes `search_language`
- `language` [GameLanguage] (Optional) - Specify the language of the shop. Default is set to english
###### Returns
Returns a list of `BrCosmetic` objects.

___

```
api.cosmetics.search_first()
```
Search the first cosmetics which fit to the search parameters
###### Parameters
- `**search_parameters` (Optional) - All search parameters are listed on the [Fortnite-API.com Docs](https://fortnite-api.com/documentation). Remember that Python does not use a camel case. So e.g. `searchLanguage` becomes `search_language`
- `language` [GameLanguage] (Optional) - Specify the language of the shop. Default is set to english
###### Returns
Returns a `BrCosmetic` objects.

___

### Playlist
```
api.playlists.fetch_all()
```
Get all Br playlists.
###### Parameters
- `language` [GameLanguage] (Optional) - Specify the language of the playlists. Default is set to english
###### Returns
Returns a list of `Playlist` objects.

```
api.cosmetics.fetch_by_id()
```
Get a playlist by id.
###### Parameters
- `id` [str] - Specify the playlist id.
- `language` [GameLanguage] (Optional) - Specify the language of the shop. Default is set to english
###### Returns
Returns a `Playlist` object.

___


### Shop 
```
api.shop.fetch()
```
Get the latest Fortnite shop.
###### Parameters
- `language` [GameLanguage] (Optional) - Specify the language of the shop. Default is set to english
- `combined` [bool] (Optional) - Enable that `special_featured` and `special_daily` are moved into `featured` and `daily`
###### Returns
Returns a `Shop` object. 

___

### AES 
```
api.aes.fetch()
```
Get the latest Fortnite AES Key. This also include version and build information.
###### Parameters
- `key_format` [KeyFormat] (Optional) - Specify the AES key format. Default is set to HEX
###### Returns
Returns a `AES` object. 

___

### News
```
api.news.fetch()
```
Get the latest Fortnite news of all game modes.
###### Parameters
- `language` [GameLanguage] (Optional) - Specify the language of the shop. Default is set to english
###### Returns
Returns a `News` object.

___


```
api.news.fetch_by_type()
```
Get the latest Fortnite news of a specified game mode.
###### Parameters
- `news_type` [NewsType] - Specify the news type.
- `language` [GameLanguage] (Optional) - Specify the language of the shop. Default is set to english
###### Returns
Returns a `GameModeNews` object.

___

### Creator Code
```
api.creator_code.fetch()
```
Get information about a creator code.
###### Parameters
- `name` [str] - Specify a creator code.
###### Returns
Returns a `CreatorCode` object.

___

```
api.creator_code.exists()
```
Check if a creator code exists.
###### Parameters
- `name` [str] - Specify a creator code.
###### Returns
Returns a `bool` object.

___


```
api.creator_code.search_all()
```
Search a creator code by name. All results are provided.
###### Parameters
- `name` [str] - Specify a creator code.
###### Returns
Returns a `list` of `CreatorCode` objects.

___


```
api.creator_code.search_first()
```
Search a creator code by name. Only the first result is provided.
###### Parameters
- `name` [str] - Specify a creator code.
###### Returns
Returns a `CreatorCode` object.

___

### BR Stats
```
api.stats.fetch_by_name()
```
Returns stats of the requested player account.
###### Parameters
- `name` [str] - Sets the account name.
- `account_type` [AccountType] (Optional) - Sets the account type.
- `time_window` [TimeWindow] (Optional) - Sets the time window.
- `image` [StatsImageType] (Optional) - Sets the image platform.
###### Returns
Returns a `BrPlayerStats` object.

___

```
api.stats.fetch_by_id()
```
Returns stats of the requested player account by its account id.
###### Parameters
- `account_id` [str] - Sets the account id.
- `time_window` [TimeWindow] (Optional) - Sets the time window.
- `image` [StatsImageType] (Optional) - Sets the image platform.
###### Returns
Returns a `BrPlayerStats` object.

### Banner
```
api.cosmetics.fetch()
```
Get all banners.
###### Parameters
- `language` [GameLanguage] (Optional) - Specify the language of the banners. Default is set to english
###### Returns
Returns a `Banner` object.

___

```
api.cosmetics.fetch_colors()
```
Get all banner colors.
###### Returns
Returns a list of `BannerColor` objects.


### Map
```
api.map.fetch()
```
Get the current map information.
###### Parameters
- `language` [GameLanguage] (Optional) - Specify the language of the map pois. Default is set to english.
###### Returns
Returns a `Map` object.

___



## Contribute
Every type of contribution is appreciated!

## License
- Fortnite-API Wrapper (MIT) [License](https://github.com/Fortnite-API/python-wrapper/blob/master/LICENSE)
- requests (Apache) [License](https://github.com/psf/requests/blob/master/LICENSE)
- aiohttp (Apache) [License](https://github.com/aio-libs/aiohttp/blob/6a5ab96bd9cb404b4abfd5160fe8f34a29d941e5/LICENSE.txt)
