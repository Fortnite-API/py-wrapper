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

from typing import TYPE_CHECKING, Any, Dict, Union, Tuple

if TYPE_CHECKING:
    from .types.account import Account as AccountPayload


class Account:
    """Represents a account.
    
    .. container:: operations

        .. describe:: x == y

            Checks if the two accounts are equal.
        
        .. describe:: x != y

            Checks if two accounts are not equal.
        
        .. describe:: str(x)
            
            Returns the account's name.
        
        .. describe:: hash(x)

            Returns the account's hash.

    Attributes
    -----------
    id: :class:`str`
        The id of the user.
    name: :class:`str`
        The display name of the user.
    raw_data: :class:`dict`
        The raw data from request. Can be used for saving and re-creating the class.
    external_auths: Dict[Any, Any]
        The external auths of the user. Please note this will be empty until the User
        lookup feature is enabled.
    """
    __slots__: Tuple[str, ...] = ('id', 'name', 'raw_data', 'external_auths')

    def __init__(self, data: AccountPayload) -> None:
        self.id: str = data['id']
        self.name: str = data['name']
        self.raw_data: AccountPayload = data
        self.external_auths: Dict[Any, Any] = data.get('external_auths', {}) # Adding when User lookup feature is enabled
        
    def __str__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash((self.id, self.name))
    
    def __eq__(self, o: Union[object, Account]) -> bool:
        if not isinstance(o, Account):
            return False
        
        return self.id == o.id 
    
    def __ne__(self, o: Union[object, Account]) -> bool:
        return not self.__eq__(o)
    