class FortniteAPIException(Exception):
    pass


class NotFound(FortniteAPIException):
    pass


class Forbidden(FortniteAPIException):
    pass


class MissingSearchParameter(FortniteAPIException):
    pass


class MissingIDParameter(FortniteAPIException):
    pass


class ServiceUnavailable(FortniteAPIException):
    pass


class RateLimited(FortniteAPIException):
    pass


class Unauthorized(FortniteAPIException):
    pass
