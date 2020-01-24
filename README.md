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
- Get a API key on https://fortnite-api.com/profile

## Documentation
Here is a quick overview how to start.<br><br>
First we need to import the api and initialize client.
```
import fortnite_api

api = fortnite_api.FortniteAPI()
```
###### Parameters
- `api_key` [str]  - Insert your API key from https://fortnite-api.com/profile
- `run_async` [bool] (Optional) - Specify if the API should run async. Default is set to `false`
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

### Shop 
```
api.shop.fetch()
```
Get the latest Fortnite shop.
###### Parameters
- `language` [GameLanguage] (Optional) - Specify the language of the shop. Default is set to english
###### Returns
Returns a `Shop` object. 

___

### AES 
```
api.shop.fetch()
```
Get the latest Fortnite AES Key. This also include version and build information.
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
- `slug` [str] - Specify a creator code.
###### Returns
Returns a `CreatorCode` object.

___

```
api.creator_code.exists()
```
Check if a creator code exists.
###### Parameters
- `slug` [str] - Specify a creator code.
###### Returns
Returns a `bool` object.

___


```
api.creator_code.search_all()
```
Search a creator code by name. All results are provided.
###### Parameters
- `slug` [str] - Specify a creator code.
###### Returns
Returns a `list` of `CreatorCode` objects.

___


```
api.creator_code.search_first()
```
Search a creator code by name. Only the first result is provided.
###### Parameters
- `slug` [str] - Specify a creator code.
###### Returns
Returns a `CreatorCode` object.

## Contribute
Every type of contribution is appreciated!

## License
- Fortnite-API Wrapper (MIT) [License](https://github.com/Fortnite-API/python-wrapper/blob/master/LICENSE)
- requests (Apache) [License](https://github.com/psf/requests/blob/master/LICENSE)
- aiohttp (Apache) [License](https://github.com/aio-libs/aiohttp/blob/6a5ab96bd9cb404b4abfd5160fe8f34a29d941e5/LICENSE.txt)
