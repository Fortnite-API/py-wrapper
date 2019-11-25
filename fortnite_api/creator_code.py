from .user import User


class CreatorCode:

    def __init__(self, data):
        self.user = User({'id': data.get('id'), 'displayName': data.get('displayName')})
        self.disabled = data.get('status', '').lower() == 'disabled'
        self.name = data.get('slug')
        self.verified = data.get('verified', False)
        self.raw_data = data
