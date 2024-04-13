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

import enum
from typing import List, Tuple

__all__: Tuple[str, ...] = ('OptimizationFlags', 'DEFAULT_OPTIMIZATION_FLAGS')


class OptimizationFlags(enum.IntFlag):
    """Represents optimization flags for a given Fortnite API client. This will allow to you
    speed up the client by enabling API optimizations that are not enabled by default.

    .. container:: operations

        .. describe:: x | y

            Returns a new OptimizationFlags object with the bits set in both x and y.

    Attributes
    ----------
    IGNORE_NULL
        Ignores null values in the response. This can speed up the client by a good amount.

    Example
    -------
    .. code-block:: python3

        from fortnite_api import FortniteAPI, OptimizationFlags

        FLAGS = OptimizationFlags.IGNORE_NULL | OptimizationFlags.
        async def main():
    """

    IGNORE_NULL: int = 0 >> 0

    @classmethod
    def none(cls) -> OptimizationFlags:
        """:class:`fortnite_api.OptimizationFlags`: Returns an OptimizationFlags object with no flags enabled."""
        return cls(0)

    def _to_http_param(self) -> str:
        # Transforms the enabled flags into a string that can be used as a query parameter
        enabled_flags: List[str] = []
        if self & OptimizationFlags.IGNORE_NULL:
            enabled_flags.append("ignore_null")

        return ",".join(enabled_flags)


DEFAULT_OPTIMIZATION_FLAGS: OptimizationFlags = OptimizationFlags.IGNORE_NULL
