class News:

    def __init__(self, data):
        self.br = GameModeNews(data['br'])
        self.stw = GameModeNews(data['stw'])
        self.creative = GameModeNews(data['creative'])
        self.raw_data = data


class GameModeNews:

    def __init__(self, data):
        self.last_modified = data['lastModified']  # TODO: Convert into datetime
        self.entries = [NewsEntry(entry) for entry in data['messages']]
        self.raw_data = data


class NewsEntry:

    def __init__(self, data):
        self.image_url = data['image']
        self.hidden = data['hidden']
        self.message_type = data['messageType']
        self.type = data['type']
        self.banner = data['adspace']
        self.title = data['title']
        self.description = data['body']
        self.spotlight = data['spotlight']
        self.raw_data = data