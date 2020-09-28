class Anime:
    def __init__(self, title, db_name, url):
        self.title = None
        self.db_name = None
        self.url = None
        self.episodes = []


class Episode:
    def __init__(self, number, link):
        self.number = None
        self.link = None
