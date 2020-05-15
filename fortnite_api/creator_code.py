from .account import Account


class CreatorCode:
    """Represents a Creator Code.

    Attributes
    -----------
    user: :class:`User`
        The user of the creator code.
    disabled: :class:`bool`
        Whether the Creator Code is disabled or not.
    code: :class:`str`
        The slug of the Creator Code
    verified: :class:`bool`
        Whether the Creator Code is verified or not.
    raw_data: :class:`dict`
        The raw data from request. Can be used for saving and re-creating the class.
    """

    def __init__(self, data):
        self.code = data.get('code')
        self.user = Account(data.get('account')) if data.get('account') else None
        self.disabled = data.get('status', '').lower() == 'disabled'
        self.verified = data.get('verified', False)
        self.raw_data = data
