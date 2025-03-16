import requests


class WikimediaAPIClient:
    def __init__(self, domain="de.wikibooks.org", http_client=requests.Session()):
        self.domain = domain
        self.http_client = http_client

    def get_wikitext(self, page_title: str) -> str:
        query_result = self.api_query_for_page(
            page_title,
            prop="revisions",
            rvprop="content",
            rvslots="main",
        )
        if "revisions" in query_result:
            return query_result["revisions"][0]["slots"]["main"]["*"]

        raise ValueError(f"No revisions found for '{page_title}'")

    def get_current_redirects(self, page_title: str) -> list:
        query_result = self.api_query_for_page(
            page_title, prop="redirects", rdlimit="max"
        )
        if "redirects" in query_result:
            return [redirect["title"] for redirect in query_result["redirects"]]
        return []

    def api_query_for_page(self, page_title: str, **params) -> dict:
        query_result = self.api_query(titles=page_title, **params)
        values = query_result.get("pages", {}).values()
        if len(values) == 1:
            return next(iter(values))
        raise ValueError(f"Page '{page_title}' not found or multiple pages found")

    def api_query(self, **params) -> dict:
        api_url = f"https://{self.domain}/w/api.php"
        api_params = {"action": "query", "format": "json", **params}

        response = self.http_client.get(api_url, params=api_params)
        response.raise_for_status()

        return response.json()["query"]
