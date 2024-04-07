"""
MIT License

Copyright (c) 2019-present Luc1412

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

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
        if (size & (size - 1) != 0) or size <= 0:
            raise ValueError('Size must be a positive power of 2')
        url_without_type = self.url.replace('.png', '')
        return url_without_type + '_' + str(size) + '.png'

    def __str__(self):
        return self.url
