class Map:

    def __init__(self, data):
        self.blank_image = data['images']['blank']
        self.poi_image = data['images']['blank']
        self.pois = [POI(x) for x in data['pois']]
        self.raw_data = data


class POI:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.location = POILocation(data['location'])
        self.raw_data = data


class POILocation:

    def __init__(self, data):
        self.x = data['x']
        self.y = data['y']
        self.z = data['z']
        self.raw_data = data
