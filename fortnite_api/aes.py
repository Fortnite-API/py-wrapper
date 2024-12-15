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

import dataclasses
import re
from collections.abc import Generator
from typing import TYPE_CHECKING, Any

from .abc import ReconstructAble
from .http import HTTPClientT
from .utils import parse_time, simple_repr

if TYPE_CHECKING:
    import datetime

__all__: tuple[str, ...] = ("Aes", "DynamicKey", "Version")

VERSION_REGEX: re.Pattern[str] = re.compile(r"(?P<version>[0-9]{2})\.(?P<subversion>[0-9]{2})")


@dataclasses.dataclass(init=True, eq=True, order=False)
class Version:
    """
    .. attributetable:: fortnite_api.Version

    Represents a version of a build of Fortnite.

    .. container:: operations

        .. describe:: repr(x)

            Returns a representation of the account in the form of a string.

        .. describe:: str(x)

            Returns the version in the form of a string. ":attr:`major`.:attr:`minor`"

        .. describe:: iter(x)

            Returns an iterator of the version. This will yield the major version and then the minor version.

            .. code-block:: python3

                major, minor = version

    Attributes
    ----------
    major: :class:`int`
        The major version.
    minor: :class:`int`
        The minor version.
    """

    major: int
    minor: int

    def __repr__(self) -> str:
        return f"<Version {self.major}.{self.minor}>"

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}"

    def __iter__(self) -> Generator[int]:
        yield self.major
        yield self.minor


@simple_repr
class Aes(ReconstructAble[dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.Aes

    Represents the object given to the client from the AES endpoint. This inherits
    from :class:`~fortnite_api.ReconstructAble`.

    .. container:: operations

        .. describe:: x == y

            Checks if the two Aes objects are equal.

        .. describe:: x != y

            Checks if two Aes objects are not equal.

        .. describe:: hash(x)

            Returns the Aes main key and build's hash.

        .. describe:: repr(x)

            Returns a representation of the Aes object in the form of a string.

    Examples
    --------
    .. code-block:: python3
        :caption: Fetching the current AES main key and build.

        aes = await client.fetch_aes()
        print(aes.main_key, aes.build)

    .. code-block:: python3
        :caption: Fetching the current version of Fortnite.

        aes = await client.fetch_aes()
        major, minor = aes.version
        print(f'Fortnite on version {major}.{minor}')


    Attributes
    ----------
    main_key: Optional[:class:`str`]
        The main encryption key. Can be ``None`` if the current versions key is not available yet.
    build: :class:`str`
        The current build where the Aes key refers to.
    version: Optional[:class:`fortnite_api.Version`]
        The current version where the Aes key refers to. This will only be ``None`` in the case that the API returned an invalid :attr:`build` value.
    updated: :class:`datetime.datetime`
        The date where the Aes was updates.
    dynamic_keys: List[:class:`fortnite_api.DynamicKey`]
        All current dynamic keys
    """

    __slots__: tuple[str, ...] = (
        "main_key",
        "build",
        "version",
        "updated",
        "dynamic_keys",
    )

    def __init__(self, *, data: dict[str, Any], http: HTTPClientT):
        super().__init__(data=data, http=http)

        self.main_key: str | None = data.get("mainKey")
        self.build: str = data["build"]

        # In the case that the API gives us an invalid version, we will set it to None
        self.version: Version | None = None
        version_info = VERSION_REGEX.findall(self.build)
        if version_info and len(version_info[0]) == 2:
            major, minor = version_info[0]
            self.version = Version(major=int(major), minor=int(minor))

        self.dynamic_keys: list[DynamicKey[HTTPClientT]] = [
            DynamicKey(data=entry, http=http) for entry in data.get("dynamicKeys", [])
        ]
        self.updated: datetime.datetime = parse_time(data["updated"])

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, self.__class__):
            return False

        return all(
            (
                self.build == __o.build,
                self.main_key == __o.main_key,
                self.dynamic_keys == __o.dynamic_keys,
            )
        )

    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)

    def __hash__(self) -> int:
        return hash((self.build, self.main_key))


@simple_repr
class DynamicKey(ReconstructAble[dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.DynamicKey

    Represents a dynamic key.

    .. container:: operations

        .. describe:: x == y

            Checks if the two dynamic keys are equal.

        .. describe:: x != y

            Checks if two dynamic keys are not equal.

        .. describe:: str(x)

            Returns the dynamic key's pak filename.

        .. describe:: hash(x)

            Returns the dynamic key's hash.

        .. describe:: repr(x)

            Returns a representation of the account in the form of a string.

    Attributes
    ----------
    pak_filename: :class:`str`
        The pak's filename.
    pak_guid: :class:`str`
        The pak's guid.
    key: :class:`str`
        The key.
    """

    __slots__: tuple[str, ...] = ("pak_filename", "pak_guid", "key")

    def __init__(self, *, data: dict[str, Any], http: HTTPClientT):
        super().__init__(data=data, http=http)

        self.pak_filename: str = data["pakFilename"]
        self.pak_guid: str = data["pakGuid"]
        self.key: str = data["key"]

    def __hash__(self) -> int:
        return hash((self.pak_filename, self.pak_guid, self.key))

    def __eq__(self, o: object | DynamicKey) -> bool:
        if not isinstance(o, DynamicKey):
            return False

        return self.pak_filename == o.pak_filename and self.pak_guid == o.pak_guid and self.key == o.key

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __str__(self) -> str:
        return self.pak_filename
