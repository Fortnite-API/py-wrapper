import math


class Banner:

    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')
        self.category = data.get('category')
        self.full_usage_rights = data.get('fullUsageRights')

        images = data.get('images', {}) if data.get('images') else {}
        self.small_icon = BrBannerImage(images.get('smallIcon')) if images.get('smallIcon') else None
        self.icon = BrBannerImage(images.get('icon')) if images.get('icon') else None
        self.raw_data = data


class BannerColor:

    def __init__(self, data):
        self.id = data.get('id')
        self.color = data.get('color')
        self.category = data.get('category')
        self.sub_category_group = data.get('subCategoryGroup')
        self.raw_data = data


class BrBannerImage:
    """Represents a Battle Royale cosmetic image.

    Attributes
    -----------
    url: :class:`str`
        The hash of the image.
    """

    def __init__(self, url):
        self.url = url

    def url_as(self, size):
        if size < 0 or type(math.sqrt(size)) is float:
            raise TypeError('Size must be a power of 2.')
        url_without_type = self.url.replace('.png', '')
        return url_without_type + '_' + size + '.png'

    def __str__(self):
        return self.url
