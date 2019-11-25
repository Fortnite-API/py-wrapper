class NotFound(Exception):  # Add to search by ID
    pass


class MissingSearchParameter(Exception):
    pass


class MissingIDParameter(Exception):
    pass


class ServerOutage(Exception):
    pass
