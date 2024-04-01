"""
MIT License

Copyright (c) 2019 Lucas Hardt

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
from typing import Any, Tuple, Dict, Protocol, Callable

try:
    import orjson

    _has_orjson: bool = True
except ImportError:
    import json

    _has_orjson: bool = False

__all__: Tuple[str, ...] = ('parse_time', 'copy_doc')


class Docable(Protocol):
    __doc__: str


if _has_orjson:

    def to_json(string: str) -> Dict[Any, Any]:
        return orjson.loads(string)

else:

    def to_json(string: str) -> Dict[Any, Any]:
        return json.loads(string)


def parse_time(timestamp: str) -> datetime.datetime:
    return datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S%z')


def copy_doc(obj: Docable) -> Callable[[Docable], Docable]:
    """Copy the docstring from another object"""

    def wrapped(funco: Docable) -> Docable:
        funco.__doc__ = obj.__doc__

    return wrapped


def prepend_doc(obj: Docable, sep: str = '') -> Callable[[Docable], Docable]:
    """A decorator used to prepend a docstring onto another object.

    .. code-block:: python3

        @prepend_doc(discord.Embed)
        def foo(self, *args, **kwargs):
            '''This is a doc string'''

        print(foo.__doc__)
        >>> 'discord.Embed doc string[sep]This is a doc string'
    """

    def wrapped(funco: Docable) -> Docable:
        funco.__doc__ = f'{obj.__doc__}{sep}{funco.__doc__}'

    return wrapped