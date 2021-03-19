class Anime:
    def __init__(self, title, db_name, url):
        self.title = None
        self.db_name = None
        self.url = None
        self.season = None
        self.latest_title_on_overview = None
        self.newepisodes = []
        self.episodes = []
        self.amount_of_episodes = None
        self.batched = False


class Episode:
    def __init__(self, number, link):
        self.number = None
        self.link = None
