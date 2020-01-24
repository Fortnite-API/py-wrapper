import re
from datetime import datetime


class AES:

    def __init__(self, data):
        self.aes = data.get('aes')
        self.build = data.get('build')
        self.version = re.search(r'\d\d.\d\d', self.build)[0] if self.build else None
        try:
            self.last_update = datetime.strptime(data.get('date'), '%Y-%m-%dT%H:%M:%S%z')
        except ValueError:
            self.last_update = None
        self.raw = data
