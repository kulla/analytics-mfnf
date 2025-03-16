import pandas as pd

from wikimedia import WikimediaAPIClient
from .sitemap import parse_sitemap


class MFNF:
    def __init__(self, wikimedia_client=WikimediaAPIClient()):
        self.wikimedia_client = wikimedia_client

    def aggregate_pageviews(self):
        def get_pageview_rows(target_title, book, section, page):
            book_name = book.name if book is not None else None
            section_name = section.name if section is not None else None
            page_name = page.name if page is not None else None

            for page_title in self.get_page_with_all_redirects(target_title):
                pageviews = self.wikimedia_client.get_pageviews(page_title)

                for timestamp, views in pageviews:
                    yield (
                        pd.to_datetime(timestamp),
                        page_title,
                        target_title,
                        book_name,
                        section_name,
                        page_name,
                        views,
                    )

        def get_rows():
            project = self.get_sitemap()

            yield from get_pageview_rows(project.href, None, None, None)
            n = 1

            for book in project.books:
                yield from get_pageview_rows(book.href, book, None, None)

                n += 1
                for section in book.sections:
                    for page in section.pages:
                        yield from get_pageview_rows(page.href, book, section, page)
                        n += 1

                        if n > 10:
                            break

        return pd.DataFrame.from_records(
            get_rows(),
            columns=[
                "timestamp",
                "page_title",
                "target_title",
                "book_name",
                "section_name",
                "page_name",
                "views",
            ],
        )

    def get_sitemap(self):
        return parse_sitemap(
            self.wikimedia_client.get_wikitext("Mathe für Nicht-Freaks: Sitemap")
        )

    def get_page_with_all_redirects(self, page_title):
        return_value = {page_title}

        return_value |= set(self.wikimedia_client.get_current_redirects(page_title))
        return_value |= set(self.get_old_titles(page_title))

        return return_value

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
