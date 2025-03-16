import requests


class WikimediaAPIClient:
    def __init__(self, domain="de.wikibooks.org", http_client=requests.Session()):
        self.domain = domain
        self.http_client = http_client

    def get_wikitext(self, page_title: str) -> str:
        query_result = self.api_query(
            prop="revisions",
            titles=page_title,
            rvprop="content",
            rvslots="main",
        )
        values = query_result.get("pages", {}).values()
        if len(values) == 1:
            page_data = next(iter(values))
            if "revisions" in page_data:
                return page_data["revisions"][0]["slots"]["main"]["*"]

        raise ValueError(f"Page '{page_title}' not found or multiple pages found")

    def api_query(self, **params) -> dict:
        api_url = f"https://{self.domain}/w/api.php"
        api_params = {"action": "query", "format": "json", **params}

        response = self.http_client.get(api_url, params=api_params)
        response.raise_for_status()

        return response.json()["query"]
