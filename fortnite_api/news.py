from datetime import datetime


class News:
    """Represents Game News.

    Attributes
    -----------
    br: List[:class:`GameModeNews`]
        A list of Battle Royale news.
    stw: List[:class:`GameModeNews`]
        A list of Save the World news.
    creative: List[:class:`GameModeNews`]
        A list of Creative news.
    raw_data: :class:`dict`
        The raw data from request. Can be used for saving and re-creating the class.
    """

    def __init__(self, data):
        print(data)
        self.br = GameModeNews(data.get('br')) if data.get('br') else None
        self.stw = GameModeNews(data.get('stw')) if data.get('stw') else None
        self.creative = GameModeNews(data.get('creative')) if data.get('creative') else None
        self.raw_data = data


class GameModeNews:
    """Represents News of a specific game mode.

    Attributes
    -----------
    last_modified: :class:`datetime.datetime`
        The timestamp when the news where modified.
    entries: List[:class:`NewsEntry`]
        A list of news entries.
    raw_data: :class:`dict`
        The raw data from request. Can be used for saving and re-creating the class.
    """

    def __init__(self, data):
        self.hash = data.get('hash')
        try:
            self.date = datetime.strptime(data.get('date'), '%Y-%m-%dT%H:%M:%S%z')
        except (ValueError, TypeError):
            self.date = None
        self.image = data.get('image')
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
        self.sorting_priority = data.get('sortingPriority')
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
        self.title = data.get('title')
        self.body = data.get('body')
        self.image_url = data.get('image')
        self.adspace = data.get('adspace')
        self.raw_data = data
