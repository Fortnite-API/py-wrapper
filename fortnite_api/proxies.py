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

from typing import Any, Callable, Dict, Generic, Iterable, Iterator, List, SupportsIndex, Union, cast, overload

from typing_extensions import Self, TypeVar

T = TypeVar('T')
K_co = TypeVar('K_co', covariant=True, default='str')
V_co = TypeVar('V_co', covariant=True, default='Any')


class TransformerListProxy(Generic[T, K_co, V_co], List[T]):
    """
    .. attributetable:: fortnite_api.proxies.TransformerListProxy

    A proxy for a list that allows for half-created type T objects to be stored in the list. This is an internal
    optimization that allows objects to be created only as-needed when the list is accessed.

    This class has been exposed to the documentation because it may be useful for some high level users. However, you
    can consider this as just a ``List[T]`` unless needed otherwise.

    It is important to note that this class is not thread-safe, so it should not be accessed
    concurrently from multiple threads. If you wish to access this class concurrently, you
    should use a lock to ensure that only one thread is accessing the class at a time.

    This class holds the invariant that when any public method is called, the list will be transformed into a list of
    type T. This means that when the list is accessed, the data will be transformed into the correct type. This is done
    to ensure that the data is always in a consistent state.
    """

    def __init__(self, raw_data: Iterable[Dict[K_co, V_co]], /, transform_data: Callable[[Dict[K_co, V_co]], T]) -> None:
        self._transform_data: Callable[[Dict[K_co, V_co]], T] = transform_data
        super().__init__(cast(List[T], raw_data))

    def _transform_at(self, index: SupportsIndex) -> T:
        # Transforms the data at the index.
        data = super().__getitem__(index)
        if isinstance(data, dict):
            # Narrow the type of data to Dict[str, Any]
            raw_data: Dict[K_co, V_co] = data
            result = self._transform_data(raw_data)
            super().__setitem__(index, result)
        else:
            result = data

        return result

    def _transform_all(self):
        for index, entry in enumerate(self):
            if isinstance(entry, dict):
                raw_data: Dict[K_co, V_co] = entry
                result = self._transform_data(raw_data)
                super().__setitem__(index, result)

    def transform_all(self) -> Self:
        """A method that transforms all the data in the list to type ``T``."""
        self._transform_all()
        return self

    # Allows for indexing of the list.
    @overload
    def __getitem__(self, index: SupportsIndex) -> T: ...

    @overload
    def __getitem__(self, index: slice) -> List[T]: ...

    def __getitem__(self, index: Union[SupportsIndex, slice]) -> Union[List[T], T]:
        if isinstance(index, slice):
            # This is a slice, so we need to handle each item in the slice and set it to the transformed data.
            # For each index in the slice, transform the data at that index then update the item list
            # with the transformed data.
            for i in range(*index.indices(len(self))):
                self._transform_at(i)

            return super().__getitem__(index)

        assert isinstance(index, SupportsIndex)
        return self._transform_at(index)

    def __contains__(self, key: object) -> bool:
        # If the user is looking for contains, we need to transform all the data so this is correct
        self._transform_all()
        return super().__contains__(key)

    def __reversed__(self) -> Iterator[T]:
        # Calling reversed will transform this list to a new list of type T
        # This means we need to transform all the data beforehand.
        self._transform_all()
        return super().__reversed__()

    # For all of the comparison methods, we need to transform all the data so that the comparison is correct.
    def __gt__(self, value: List[T]) -> bool:
        self._transform_all()
        return super().__gt__(value)

    def __ge__(self, value: List[T]) -> bool:
        self._transform_all()
        return super().__ge__(value)

    def __lt__(self, value: List[T]) -> bool:
        self._transform_all()
        return super().__lt__(value)

    def __le__(self, value: List[T]) -> bool:
        self._transform_all()
        return super().__le__(value)

    def __eq__(self, value: object) -> bool:
        self._transform_all()
        return super().__eq__(value)

    def __ne__(self, value: object) -> bool:
        self._transform_all()
        return super().__ne__(value)

    def __iter__(self) -> Iterator[T]:
        for index in range(super().__len__()):
            yield self._transform_at(index)
