from wikimedia import WikimediaAPIClient
from .sitemap import parse_sitemap


class MFNF:
    def __init__(self, wikimedia_client=WikimediaAPIClient()):
        self.wikimedia_client = wikimedia_client

    def get_sitemap(self):
        return parse_sitemap(
            self.wikimedia_client.get_wikitext("Mathe für Nicht-Freaks: Sitemap")
        )

    def get_old_titles(self, page_title):
        def parse_old_title(comment):
            text_indicator = " verschob die Seite "
            text_indicator_index = comment.find(text_indicator)

            if text_indicator_index == -1:
                return None

            link_start = comment[text_indicator_index + len(text_indicator) :]
            link_end = link_start.find("]]")

            if link_start.startswith("[[") and link_end != -1:
                return link_start[2:link_end]

            return None

        edit_comments = self.wikimedia_client.get_edit_comments(page_title)
        old_titles = [parse_old_title(comment) for comment in edit_comments]

        return [old_title for old_title in old_titles if old_title is not None]
