# Python wrapper for [Fortnite-API.com](https://fortnite-api.com)

This library offers a complete **sync** and **async** wrapper around the endpoints of [Fortnite-API.com](https://fortnite-api.com)

## Installation
```
pip install fortnite-api
```

## Documentation
Here is a quick overview how to start.<br><br>
First we need to import the api and initialize client.
```python
import fortnite-api

fortnite_client = fortnite-api.FortniteClient()
```
###### Parameters
- `api_key` [str] (Optional) - Enter the API key you will get if you requested a higher rate limit
- `async` [bool] (Optional) - Specify if the API should run async. Default is set to `false`
###### Attributes
- `cosmetics` - All cosmetic endpoints
- `shop` - All shop endpoints
- `news` - All news endpoints

<br><br>
Now we can use the client:
### Cosmetics
```python
fortnite_client.cosmetics.fetch_all()
```
Get all Br cosmetics.
###### Parameters
- `language` [GameLanguage] (Optional) - Specify the language of the shop. Default is set to english
###### Returns
Returns a list of `BrCosmetic` objects.

___

```python
fortnite_client.cosmetics.search_by_id()
```
Search one o multiple items by their id.
###### Parameters
- `*cosmetic_id` - One or multiple cosmetic ids.
- `language` [GameLanguage] (Optional) - Specify the language of the shop. Default is set to english
###### Returns
Returns a list of `BrCosmetic` objects. `None` if not found.

___

```python
fortnite_client.cosmetics.search_all()
```
Search all cosmetics which fit to the search parameters
###### Parameters
- `**search_parameters` - All search parameters are listed on the [Fortnite-API.com Docs](https://fortnite-api.com/documentation). Remember that Python does not use a camel case. So e.g. `searchLanguage` becomes `search_language`
- `language` [GameLanguage] (Optional) - Specify the language of the shop. Default is set to english
###### Returns
Returns a list of `BrCosmetic` objects. `None` if not found.

___

```python
fortnite_client.cosmetics.search_first()
```
Search the first cosmetics which fit to the search parameters
###### Parameters
- `**search_parameters` (Optional) - All search parameters are listed on the [Fortnite-API.com Docs](https://fortnite-api.com/documentation). Remember that Python does not use a camel case. So e.g. `searchLanguage` becomes `search_language`
- `language` [GameLanguage] (Optional) - Specify the language of the shop. Default is set to english
###### Returns
Returns a `BrCosmetic` objects. `None` if not found.
___
### Shop 
```python
fortnite_client.shop.fetch()
```
Get the latest Fortnite shop.
###### Parameters
- `language` [GameLanguage] (Optional) - Specify the language of the shop. Default is set to english

###### Returns
Returns a `Shop` object.
___
### News
```python
fortnite_client.news.fetch()
```
Get the latest Fortnite news of all game modes.
###### Parameters
- `language` [GameLanguage] (Optional) - Specify the language of the shop. Default is set to english

###### Returns
Returns a `News` object.

___


```python
fortnite_client.news.fetch_by_type()
```
Get the latest Fortnite news of a specified game mode.
###### Parameters
- `news_type` [NewsType] - Specify the news type.
- `language` [GameLanguage] (Optional) - Specify the language of the shop. Default is set to english

###### Returns
Returns a `GameModeNews` object.

## Contribute
Every type of contribution is appreciated!

## License
- Fortnite-API Wrapper (MIT) [License](https://github.com/Fortnite-API/python-wrapper/blob/master/LICENSE)
- requests (Apache) [License](https://github.com/psf/requests/blob/master/LICENSE)
- aiohttp (Apache) [License](https://github.com/aio-libs/aiohttp/blob/6a5ab96bd9cb404b4abfd5160fe8f34a29d941e5/LICENSE.txt)
