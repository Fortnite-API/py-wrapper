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

import copy
from typing import TYPE_CHECKING, Generic, TypeVar, Union, overload

from .http import HTTPClient, HTTPClientT, SyncHTTPClient

DictT = TypeVar('DictT', bound='Mapping[Any, Any]')

if TYPE_CHECKING:
    from collections.abc import Mapping
    from typing import Any

    from .client import Client, SyncClient

__all__: tuple[str, ...] = ('IdComparable', 'Hashable', 'ReconstructAble')


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


class ReconstructAble(Generic[DictT, HTTPClientT]):
    """
    Denotes a class that can be reconstructed from a raw data dictionary, such as
    one returned from any API endpoint.
    """

    # Denotes an internal method that is used to store the instance raw api data,
    # and is used to serve this data back to the user when the to_dict method is called.
    __raw_data: DictT

    # The internal http client that is used to make requests.
    _http: HTTPClientT

    # Denotes that any subclass should have both the data and http params passed to its init.
    # The library has been built with this in mind, and
    # by default any class that inherits from this protocol will have this __init__ method.
    def __init__(self, *, data: DictT, http: HTTPClientT) -> None:
        self.__raw_data: DictT = data
        self._http: HTTPClientT = http

    # The from_dict method is a class method that allows the user to create an instance
    # of this class from the underlying raw dictionary type returned from the API. This
    # method is overloaded to allow for both the async and sync clients to be passed, whilst
    # still keeping the correct HTTPClient type.

    @overload
    @classmethod
    def from_dict(
        cls: type[ReconstructAble[Any, SyncHTTPClient]], data: DictT, *, client: SyncClient
    ) -> ReconstructAble[DictT, SyncHTTPClient]: ...

    @overload
    @classmethod
    def from_dict(
        cls: type[ReconstructAble[Any, HTTPClient]], data: DictT, *, client: Client
    ) -> ReconstructAble[DictT, HTTPClient]: ...

    @classmethod
    def from_dict(cls, data: DictT, *, client: Union[Client, SyncClient]) -> Any:
        """Reconstructs this class from a raw dictionary object. This is useful for when you
        store the raw data and want to reconstruct the object later on.

        Parameters
        ----------
        data: Dict[Any, Any]
            The raw data to reconstruct the object from.
        client: Union[:class:`fortnite_api.Client`, :class:`fortnite_api.SyncClient`]
            The currently used client to reconstruct the object with. Can either be a sync or async client.
        """
        # Even if we did an instance check here, Pyright cannot understand the narrowing of "http"
        # from the "client" parameter. We must ignore this error.
        http: HTTPClientT = client.http  # type: ignore
        return cls(data=data, http=http)

    def to_dict(self) -> DictT:
        """Turns this object into a raw dictionary object. This is useful for when you
        want to store the raw data and reconstruct the object later on.

        Returns
        -------
        Dict[Any, Any]
            The raw data of this object. Note that this is a deep copy of the raw data,
            and not a reference to the underlying raw data this object was constructed with.
        """
        # NOTE: copy.deepcopy is used to prevent the user from modifying the raw data
        # and causing unexpected behavior. The module itself is being used because
        # we want to allow Mapping[K, V] types to be used as the raw data (for typed dicts)
        return copy.deepcopy(self.__raw_data)
