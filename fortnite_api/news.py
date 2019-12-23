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
        self.motds = [NewsMotd(item_data) for item_data in data.get('motds')] if data.get('motds') else None
        self.messages = [NewsMessage(item_data) for item_data in data.get('messages')] if data.get('messages') else None
        self.raw_data = data


class NewsMotd:
    """Represents News of a specific game mode.

    Attributes
    -----------
    id: :class:`str`
        The id of the motd.
    title: :class:`str`
        The title of the motd.
    body: Optional[:class:`str`]
        The body of the motd.
    image_url: :class:`str`
        The url of the image in 1920x1080.
    tile_image_url: :class:`str`
        The url of the tile image in 1024x512.
    hidden: :class:`bool`
        Whether the motd is hidden.
    spotlight: :class:`bool`
        Whether the motd is in spotlight.
    type: :class:`str`
        The type of the entry.
    raw_data: :class:`dict`
        The raw data from request. Can be used for saving and re-creating the class.
    """

    def __init__(self, data):
        self.id = data.get('id')
        self.title = data.get('title')
        self.body = data.get('body')
        self.image_url = data.get('image')
        self.tile_image_url = data.get('tileImage')
        self.hidden = data.get('hidden')
        self.spotlight = data.get('spotlight')
        self.type = data.get('type')
        self.entry_type = data.get('entryType')
        self.raw_data = data


class NewsMessage:
    """Represents News of a specific game mode.

    Attributes
    -----------
    image_url: :class:`str`
        The url of the image.
    hidden: :class:`bool`
        Whether the entry is hidden.
    message_type: Optional[:class:`str`]
        The type of the message.
    type: :class:`str`
        The type of the entry.
    banner: :class:`str`
        The banner of the entry.
    title: :class:`str`
        The title of the entry.
    body: :class:`str`
        The body of the entry.
    spotlight: :class:`bool`
        Whether the entry is in spotlight.
    raw_data: :class:`dict`
        The raw data from request. Can be used for saving and re-creating the class.
    """

    def __init__(self, data):
        self.image_url = data.get('image')
        self.hidden = data.get('hidden')
        self.message_type = data.get('messageType')
        self.type = data.get('type')
        self.banner = data.get('adspace')
        self.title = data.get('title')
        self.body = data.get('body')
        self.spotlight = data.get('spotlight')
        self.raw_data = data
