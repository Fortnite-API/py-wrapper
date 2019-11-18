from datetime import datetime


class News:

    def __init__(self, data):
        self.br = GameModeNews(data.get('br'))
        self.stw = GameModeNews(data.get('stw'))
        self.creative = GameModeNews(data.get('creative'))
        self.raw_data = data


class GameModeNews:

    def __init__(self, data):
        try:
            self.last_modified = datetime.strptime(data.get('lastModified'), '%Y-%m-%dT%H:%M:%S%z')
        except ValueError:
            self.last_modified = None
        self.entries = [NewsEntry(entry) for entry in data.get('messages')]
        self.raw_data = data


class NewsEntry:

    def __init__(self, data):
        self.image_url = data.get('image')
        self.hidden = data.get('hidden')
        self.layout = data.get('layout')
        self.message_type = data.get('messageType')
        self.type = data.get('type')
        self.banner = data.get('adspace')
        self.title = data.get('title')
        self.description = data.get('body')
        self.spotlight = data.get('spotlight')
        self.raw_data = data
