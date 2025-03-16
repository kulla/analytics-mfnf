from wikimedia import WikimediaAPIClient
from .sitemap import parse_sitemap


class MFNF:
    def __init__(self, wikimedia_client=WikimediaAPIClient()):
        self.wikimedia_client = wikimedia_client

    def get_sitemap(self):
        return parse_sitemap(
            self.wikimedia_client.get_wikitext("Mathe für Nicht-Freaks: Sitemap")
        )
