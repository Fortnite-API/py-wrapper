class User:
    """Represents a user.

    Attributes
    -----------
    id: :class:`str`
        The id of the user.
    name: :class:`str`
        The display name of the user.
    raw_data: :class:`dict`
        The raw data from request. Can be used for saving and re-creating the class.
    """

    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('displayName')
        self.external_auths = None  # Adding when User lookup feature is enabled
        self.raw_data = data
