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
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

from .utils import parse_time, simple_repr

if TYPE_CHECKING:
    import datetime

__all__: Tuple[str, ...] = ('Aes', 'DynamicKey', 'Version')

VERSION_REGEX: re.Pattern[str] = re.compile(r'(?P<version>[0-9]{2})\.(?P<subversion>[0-9]{2})')


@simple_repr
@dataclasses.dataclass(init=True, eq=True, order=False, slots=True)
class Version:
    """
    .. attributetable:: fortnite_api.Version

    Represents a version of a build of Fortnite.

    .. container:: operations

        .. describe:: repr(x)

            Returns a representation of the account in the form of a string.

    Attributes
    ----------
    major: :class:`int`
        The major version.
    minor: :class:`int`
        The minor version.
    """

    major: int
    minor: int


@simple_repr
class Aes:
    """
    .. attributetable:: fortnite_api.Aes

    Represents the object given to the client from the AES endpoint.

    .. container:: operations

        .. describe:: x == y

            Checks if the two Aes objects are equal.

        .. describe:: x != y

            Checks if two Aes objects are not equal.

        .. describe:: hash(x)

            Returns the Aes main key and build's hash.

        .. describe:: repr(x)

            Returns a representation of the Aes object in the form of a string.

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
    raw_data: :class:`dict`
        The raw data from request. Can be used for saving and re-creating the class.
    """

    __slots__: Tuple[str, ...] = ('main_key', 'build', 'version', 'updated', 'dynamic_keys', 'raw_data')

    def __init__(self, data: Dict[str, Any]):
        self.main_key: Optional[str] = data.get('mainKey')
        self.build: str = data['build']

        # In the case that the API gives us an invalid version, we will set it to None
        self.version: Optional[Version] = None
        version_info = VERSION_REGEX.findall(self.build)
        if version_info and len(version_info[0]) == 2:
            major, minor = version_info[0]
            self.version = Version(major=int(major), minor=int(minor))

        self.dynamic_keys: List[DynamicKey] = [DynamicKey(entry) for entry in data.get('dynamicKeys', [])]
        self.updated: datetime.datetime = parse_time(data['updated'])
        self.raw_data: Dict[str, Any] = data

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
class DynamicKey:
    """
    .. attributetable:: fortnite_api.DynamicKey

    Represents a dynamic key.

    .. container:: operations

        .. describe:: x == y

            Checks if the two dynamic key's are equal.

        .. describe:: x != y

            Checks if two dynamic key's are not equal.

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

    __slots__: Tuple[str, ...] = ('pak_filename', 'pak_guid', 'key')

    def __init__(self, data: Dict[str, Any]):
        self.pak_filename: str = data['pakFilename']
        self.pak_guid: str = data['pakGuid']
        self.key: str = data['key']

    def __hash__(self) -> int:
        return hash((self.pak_filename, self.pak_guid, self.key))

    def __eq__(self, o: Union[object, DynamicKey]) -> bool:
        if not isinstance(o, DynamicKey):
            return False

        return self.pak_filename == o.pak_filename and self.pak_guid == o.pak_guid and self.key == o.key

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __str__(self) -> str:
        return self.pak_filename
