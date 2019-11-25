class User:

    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('displayName')
        self.external_auths = None  # Adding when User lookup feature is enabled
        self.raw_data = data
