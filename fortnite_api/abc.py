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

from typing import Tuple

__all__: Tuple[str, ...] = ('IdComparable', 'Hashable')


class IdComparable:
    """
    .. attributetable:: fortnite_api.IdComparable

    Represents an object that can be compared to another object by id.

    .. container:: operations

        .. describe:: x == y

            Determine if two objects are equal.

        .. describe:: x != y

            Determine if two objects are not equal.
    """

    id: str

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, self.__class__):
            return False

        return self.id == __o.id

    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)


class Hashable(IdComparable):
    """
    .. attributetable:: fortnite_api.Hashable
    
    Represents a hashable object.

    This inherits :class:`fortnite_api.IdComparable` and adds a hash function.

    .. container:: operations

        .. describe:: hash(x)

            Return the hash of the object.
    """

    id: str

    def __hash__(self) -> int:
        return hash(self.id)
