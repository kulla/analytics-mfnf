import requests


class WikimediaAPIClient:
    def __init__(self, domain="de.wikibooks.org", http_client=requests.Session()):
        self.domain = domain
        self.http_client = http_client

    def api_query(self, **params) -> dict:
        api_url = f"https://{self.domain}/w/api.php"
        api_params = {"action": "query", "format": "json", **params}

        response = self.http_client.get(api_url, params=api_params)
        response.raise_for_status()

        return response.json()["query"]
