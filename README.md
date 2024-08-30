# Sync/Async Python wrapper for [Fortnite-API.com](https://fortnite-api.com)

[![Support](https://discordapp.com/api/guilds/621452110558527502/widget.png?style=shield)](https://discord.gg/T4tyYDK)
![GitHub issues](https://img.shields.io/github/issues/Fortnite-API/py-wrapper?logo=github)
[![PyPI](https://img.shields.io/pypi/v/fortnite-api)](https://pypi.org/project/fortnite-api)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fortnite-api?label=python%20version&logo=python&logoColor=yellow)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/fortnite-api)](https://pypi.org/project/fortnite-api)
[![Documentation](https://img.shields.io/readthedocs/fortnite-api)](https://fortnite-api.readthedocs.io/)

Welcome to the Fortnite API Python wrapper! This library offers a complete **async** and **sync** wrapper around the endpoints of [Fortnite-API.com](https://fortnite-api.com)

The library's focus is to provide a simple and easy-to-use interface to interact with the API. The library is designed to be as user-friendly as possible, and it is easy to get started with. If you have any questions or need help, feel free to join the [official Discord server](https://discord.gg/T4tyYDK).

## Installation

Note that **Python 3.8 or higher is required.**

```sh
# Linux/macOS
python3 -m pip install fortnite-api

# Windows
py -3 -m pip install fortnite-api
```

To install the developer version, you can use the following command:

```sh
git clone https://github.com/Fortnite-API/py-wrapper
cd py-wrapper
python3 -m pip install .
```

### Optional Dependencies

- `speed`: An optional dependency that installs [`orjson`](https://github.com/ijl/orjson) for faster JSON serialization and deserialization.

```sh
# Linux/macOS
python3 -m pip install fortnite-api[speed]

# Windows
py -3 -m pip install fortnite-api[speed]
```

## API Key

For most endpoints, you do not need an API key. However, some endpoints, such as fetching statistics, require an API key. To use these endpoints, you need to set the `api_key` parameter in the constructor.

```python
import asyncio
import fortnite_api

async def main():
    async with fortnite_api.Client(api_key="your_api_key"):
        stats = await client.fetch_br_stats(name='some_username')
        print(stats)

if __name__ == "__main__":
    asyncio.run(main())
```

### Generating an API Key

You can generate an API key on <https://dash.fortnite-api.com/account> by logging in with your Discord account.

## Quick Example

### Asynchronous Example

```python
import asyncio
import fortnite_api 

async def main() -> None:
    async with fortnite_api.Client() as client:
        all_cosmetics: fortnite_api.CosmeticsAll = await client.fetch_cosmetics_all()

        for br_cosmetic in all_cosmetics.br:
            print(br_cosmetic.name) 

if __name__ == "__main__":
    asyncio.run(main())
```

### Synchronous Example

```python
import fortnite_api

def main() -> None:
    client = fortnite_api.SyncClient()
    all_cosmetics: fortnite_api.CosmeticsAll = client.fetch_cosmetics_all()

    for br_cosmetic in all_cosmetics.br:
        print(br_cosmetic.name)

if __name__ == "__main__":
    main()
```

More examples can be found in the `examples/` directory of the repository.

## Links

- [Python Wrapper Documentation](https://fortnite-api.readthedocs.io/en/rewrite/)
- [FortniteAPI API Documentation](https://fortnite-api.com)
- [Official Discord Server](https://discord.gg/T4tyYDK)

## Contribute

Every type of contribution is appreciated.

## Licenses

- Fortnite-API Wrapper (MIT) [License](https://github.com/Fortnite-API/py-wrapper/blob/master/LICENSE)
- requests (Apache) [License](https://github.com/psf/requests/blob/master/LICENSE)
- aiohttp (Apache) [License](https://github.com/aio-libs/aiohttp/blob/6a5ab96bd9cb404b4abfd5160fe8f34a29d941e5/LICENSE.txt)
