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
from typing import TYPE_CHECKING, Any, Callable, TypeVar, Union

K_co = TypeVar('K_co', bound='Hashable', covariant=True)
V_co = TypeVar('V_co', covariant=True)
T = TypeVar('T')

if TYPE_CHECKING:
    from collections.abc import Hashable

try:
    import orjson  # type: ignore

    _has_orjson: bool = True
except ImportError:
    import json

    _has_orjson: bool = False

__all__: tuple[str, ...] = ('parse_time', 'copy_doc', 'prepend_doc', 'to_json', 'MISSING')

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

    def to_json(string: Union[str, bytes]) -> dict[Any, Any]:
        return orjson.loads(string)  # type: ignore

else:

    def to_json(string: Union[str, bytes]) -> dict[Any, Any]:
        return json.loads(string)  # type: ignore


def parse_time(timestamp: str) -> datetime.datetime:
    # This can happen when the API is supposed to return a timestamp but there is no timestamp to give, so it yields an improper timestamp without a UTC offset.
    if timestamp == BACKUP_TIMESTAMP:
        return datetime.datetime.fromisoformat(timestamp).replace(tzinfo=datetime.timezone.utc)

    # If the timestamp str contains ms or us, strptime with them. If not, fallback
    # to default strptime.
    try:
        return datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f%z')
    except ValueError:
        return datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S%z')


def now() -> datetime.datetime:
    # Returns the current time in the same format as the API
    return datetime.datetime.now(datetime.timezone.utc)


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


def simple_repr(cls: type[T]) -> type[T]:
    # If this cls does not have __slots__, return it as is
    try:
        slots: list[str] = list(getattr(cls, '__slots__'))
    except AttributeError:
        return cls

    # Walk through all parents, if they gave slots as well, append them to the slots
    for parent in cls.__bases__:
        try:
            slots.extend(getattr(parent, '__slots__'))
        except AttributeError:
            pass

    # If the cls has __slots__, append the __repr__ method to it using the slots as what to show
    def __repr__(self: T) -> str:
        attrs = ', '.join(f'{attr}={getattr(self, attr)!r}' for attr in slots if not attr.startswith('_'))
        return f'<{cls.__name__} {attrs}>'

    setattr(cls, '__repr__', __repr__)

    return cls


def get_with_fallback(dict: dict[K_co, V_co], key: K_co, default_factory: Callable[[], V_co]) -> V_co:
    result = dict.get(key, MISSING)
    if result is MISSING:
        # Use the default factory
        return default_factory()

    if not result:
        # Use the default factory
        return default_factory()

    return result


# A function name that transform some large dict into something that can be used in a get
# request as a payload (so turns into camelCase from snake case, and transforms booleans into strings)
def _transform_dict_for_get_request(data: dict[str, Any]) -> dict[str, Any]:
    updated = data.copy()
    for key, value in updated.items():
        if isinstance(value, bool):
            updated[key] = str(value).lower()

        elif isinstance(value, dict):
            inner: dict[str, Any] = value  # narrow the dict type to pass it along (should always be [str, Any])
            updated[key] = _transform_dict_for_get_request(inner)

        if '_' in key:
            # Need to transform this to camelCase, so anything that is after "_" will be capitalized
            parts = key.split('_')
            updated[''.join(parts[0] + part.capitalize() for part in parts[1:])] = updated.pop(key)

    return updated
