import requests


class WikimediaAPIClient:
    def __init__(self, domain="de.wikibooks.org", http_client=requests.Session()):
        self.domain = domain
        self.http_client = http_client

    def api_query(self, action: str, **params) -> dict:
        params["action"] = action
        params["format"] = "json"
        response = self.http_client.get(
            f"https://{self.domain}/w/api.php", params=params
        )
        response.raise_for_status()
        return response.json()["query"]
