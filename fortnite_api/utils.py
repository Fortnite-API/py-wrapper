"""
MIT License

Copyright (c) 2019 Luc1412

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
from typing import Any, Callable, Dict, Hashable, Tuple, TypeVar

try:
    import orjson

    _has_orjson: bool = True
except ImportError:
    import json

    _has_orjson: bool = False

K_co = TypeVar('K_co', bound='Hashable', covariant=True)
V_co = TypeVar('V_co', covariant=True)
T = TypeVar('T')

__all__: Tuple[str, ...] = ('parse_time', 'copy_doc', 'prepend_doc', 'to_json')

BACKUP_TIMESTAMP: str = '0001-01-01T00:00:00'


class _MissingSentinel:
    __slots__ = ()

    def __eq__(self, other: Any) -> bool:
        return False

    def __bool__(self) -> bool:
        return False

    def __hash__(self) -> int:
        return 0

    def __repr__(self):
        return '...'


MISSING: Any = _MissingSentinel()


if _has_orjson:

    def to_json(string: str) -> Dict[Any, Any]:
        return orjson.loads(string)  # type: ignore

else:

    def to_json(string: str) -> Dict[Any, Any]:
        return json.loads(string)  # type: ignore


def parse_time(timestamp: str) -> datetime.datetime:
    # This can happen when the API is supposed to return a timestamp but there is no timestamp to give, so it yields an improper timestamp without a UTC offset.
    if timestamp == BACKUP_TIMESTAMP:
        return datetime.datetime.fromisoformat(timestamp)

    return datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S%z')


def copy_doc(obj: Any) -> Callable[[T], T]:
    """Copy the docstring from another object"""

    def wrapped(funco: T) -> T:
        if obj.__doc__:
            funco.__doc__ = obj.__doc__

        return funco

    return wrapped


def prepend_doc(obj: Any, sep: str = '') -> Callable[[T], T]:
    """A decorator used to prepend a docstring onto another object.

    .. code-block:: python3

        @prepend_doc(discord.Embed)
        def foo(self, *args, **kwargs):
            '''This is a doc string'''

        print(foo.__doc__)
        >>> '<<discord.Embed doc string>>[sep]This is a doc string'
    """

    def wrapped(funco: T) -> T:
        if funco.__doc__ and obj.__doc__:
            funco.__doc__ = f'{obj.__doc__}{sep}{funco.__doc__}'
        elif funco.__doc__:
            funco.__doc__ = f'{sep}{funco.__doc__}'

        return funco

    return wrapped


def remove_prefix(text: str) -> Callable[[T], T]:
    """A decorator used to remove a prefix from a docstring.

    .. code-block:: python3

        @remove_prefix('This is a doc string')
        def foo(self, *args, **kwargs):
            '''This is a doc string'''

        print(foo.__doc__)
        >>> 'This is a doc string'
    """

    def wrapped(funco: T) -> T:
        if funco.__doc__:
            funco.__doc__ = funco.__doc__.replace(text, '').strip()

        return funco

    return wrapped


def get_with_fallback(dict: Dict[K_co, V_co], key: K_co, default_factory: Callable[[], V_co]) -> V_co:
    result = dict.get(key, MISSING)
    if result is MISSING:
        # Use the default factory
        return default_factory()

    if not result:
        # Use the default factory
        return default_factory()

    return result
