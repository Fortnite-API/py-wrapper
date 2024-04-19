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

from typing import TYPE_CHECKING, Any, Optional, Tuple, Union

if TYPE_CHECKING:
    import aiohttp
    import requests

__all__: Tuple[str, ...] = (
    "FortniteAPIException",
    "HTTPException",
    "NotFound",
    "Forbidden",
    "ServiceUnavailable",
    "RateLimited",
    "Unauthorized",
    "BetaAccessNotEnabled",
    "BetaUnknownException",
)


class FortniteAPIException(Exception):
    """The base for all Fortnite API exceptions.

    This class inherits from :class:`Exception`.

    Attributes
    ----------
    message: :class:`str`
        The error message describing the exception.
    """

    pass


class HTTPException(FortniteAPIException):
    """Represents a base HTTP Exception. Every HTTP exception inherits from this class.

    Attributes
    ----------
    message: Optional[:class:`str`]
        The error message describing the exception, if any.
    response: Union[:class:`aiohttp.ClientResponse`, :class:`requests.Response`]
        The response that was returned from the API. If the client is running async, it will be an aiohttp response,
        otherwise it will be a requests response.
    data: Any
        The raw data that was returned from the API.
    """

    def __init__(
        self, message: Optional[str], response: Union[aiohttp.ClientResponse, requests.Response], data: Any, /
    ) -> None:
        self.message: Optional[str] = message
        self.response: Union[aiohttp.ClientResponse, requests.Response] = response
        self.data: Any = data
        super().__init__(message)

    @property
    def status_code(self) -> int:
        """Returns the status code of the response.

        Returns
        -------
        :class:`int`
            The status code of the response.
        """
        if isinstance(self.response, requests.Response):
            return self.response.status_code

        return self.response.status


class NotFound(HTTPException):
    """Exception raised when a resource is not found.

    This class inherits from :class:`fortnite_api.HTTPException`.
    """

    pass


class Forbidden(HTTPException):
    """Exception raised when the requested operation is forbidden.

    This class inherits from :class:`fortnite_api.HTTPException`.
    """

    pass


class ServiceUnavailable(HTTPException):
    """Exception raised when the services of Fortnite API are unavailable.

    This class inherits from :class:`fortnite_api.HTTPException`.
    """

    pass


class RateLimited(HTTPException):
    """Exception raised when the client has been rate limited.

    This class inherits from :class:`fortnite_api.HTTPException`.
    """

    pass


class Unauthorized(HTTPException):
    """Exception raised when the client is unauthorized to access the requested resource.

    This class inherits from :class:`fortnite_api.HTTPException`.
    """

    pass


class BetaAccessNotEnabled(FortniteAPIException):
    """Exception raised when a user tries to access a feature or functionality that requires beta access,
    but the beta access is not enabled.

    This class inherits :class:`fortnite_api.FortniteAPIException`.

    Attributes
    ----------
    message: :class:`str`
        The error message describing the exception.
    """

    pass


class BetaUnknownException(FortniteAPIException):
    """Exception raised when an unknown exception occurs while trying to access a beta feature.

    This class inherits :class:`fortnite_api.FortniteAPIException`.

    Attributes
    ----------
    message: :class:`str`
        The error message describing the exception.
    original: :class:`fortnite_api.HTTPException`
        The original exception that occurred.
    """

    def __init__(self, *, original: HTTPException) -> None:
        super().__init__(
            f"An unknown exception occurred while trying to access a beta feature. Original exception: {original}"
        )
        self.original: HTTPException = original
