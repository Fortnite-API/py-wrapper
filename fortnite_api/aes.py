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

import re
from typing import TYPE_CHECKING, Tuple, List, Union

from .utils import parse_time

if TYPE_CHECKING:
    from .types.aes import (
        Aes as AesPayload,
        DynamicKey as DynamicKeyPayload,
    )

    import datetime

__all__: Tuple[str, ...] = ('AES', 'DynamicKey')

VERSION_REGEX: re.Pattern[str] = re.compile(r'(?P<version>[0-9]{2})\.(?P<subversion>[0-9]{2})')


class AES:
    """Represents a AES Code.

    .. container:: operations

        .. describe:: x == y

            Checks if the two AES objects are equal.

        .. describe:: x != y

            Checks if two AES objects are not equal.

        .. describe:: str(x)

            Returns the AES main key.

        .. describe:: hash(x)

            Returns the AES main key and build's hash.

    Attributes
    ----------
    main_key: :class:`str`
        The main encryption key.
    build: :class:`str`
        The current build where the AES key refers to.
    version: :class:`str`
        The current version where the AES key refers to.
    updated: :class:`datetime.datetime`
        The date where the AES was updates.
    dynamic_keys: List[:class:`DynamicKey`]
        All current dynamic keys
    raw_data: :class:`dict`
        The raw data from request. Can be used for saving and re-creating the class.
    """

    __slots__: Tuple[str, ...] = ('main_key', 'build', 'version', 'updated', 'dynamic_keys', 'raw_data')

    def __init__(self, data: AesPayload):
        self.main_key: str = data['mainKey']
        self.build: str = data['build']
        self.version: str = VERSION_REGEX.findall(self.build)[0]
        self.updated: datetime.datetime = parse_time(data['updated'])
        self.dynamic_keys: List[DynamicKey] = [DynamicKey(entry) for entry in data.get('dynamicKeys', [])]
        self.raw_data: AesPayload = data

    def __str__(self):
        return self.main_key

    def __eq__(self, o: Union[object, AES]):
        if not isinstance(o, AES):
            return False
        return self.build == o.build and self.main_key == o.main_key and self.dynamic_keys == o.dynamic_keys

    def __ne__(self, o: Union[object, AES]) -> bool:
        return not self.__eq__(o)

    def __hash__(self) -> int:
        return hash((self.build, self.main_key))


class DynamicKey:
    """Represents a dynamic key.

    .. containter:: operations

        .. describe:: x == y

            Checks if the two dynamic key's are equal.

        .. describe:: x != y

            Checks if two dynamic key's are not equal.

        .. describe:: str(x)

            Returns the dynamic key's pak filename.

        .. describe:: hash(x)

            Returns the dynamic key's hash.

    Attributes
    ----------
    pak_filename: :class:`str`
        The pak's filename.
    pak_guid: :class:`str`
        The pak's guid.
    key: :class:`str`
        The key.
    raw_data: :class:`dict`
        The raw data from request. Can be used for saving and re-creating the class.
    """

    __slots__: Tuple[str, ...] = ('pak_filename', 'pak_guid', 'key', 'raw_data')

    def __init__(self, data: DynamicKeyPayload):
        self.pak_filename: str = data['pakFilename']
        self.pak_guid: str = data['pakGuid']
        self.key: str = data['key']
        self.raw_data: DynamicKeyPayload = data

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
