import datetime
from urllib.parse import quote
from typing import List

import requests


class WikimediaAPIClient:
    def __init__(self, domain="de.wikibooks.org", http_client=requests.Session()):
        self.domain = domain
        self.http_client = http_client

        self.http_client.headers.update(
            {
                "User-Agent": f"MFNFBot/0.1 (https://github.com/kulla/analytics-mfnf; github.mail@kulla.me) requests/{requests.__version__}",
            }
        )

    def get_pageviews(self, page_title: str):
        start_date = "20160101"
        end_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime(
            "%Y%m%d"
        )
        page_title = quote(page_title, safe="")
        api_url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{self.domain}/all-access/all-agents/{page_title}/daily/{start_date}/{end_date}"

        response = self.http_client.get(api_url)

        if response.status_code == 404:
            return []

        response.raise_for_status()

        views = response.json()["items"]

        return [(item["timestamp"][:8], item["views"]) for item in views]

    def get_wikitext(self, page_title: str) -> str:
        query_result = self.query_prop(
            "revisions",
            page_title,
            rvprop="content",
            rvslots="main",
            rvlimit=1,
        )
        if "revisions" in query_result:
            return query_result["revisions"][0]["slots"]["main"]["*"]

        raise ValueError(f"No revisions found for '{page_title}'")

    def get_edit_comments(self, page_title: str) -> List[str]:
        query_result = self.query_list_prop(
            "revisions", page_title, rvprop="comment", rvlimit="max"
        )

        return [revision["comment"] for revision in query_result]

    def get_current_redirects(self, page_title: str) -> List[str]:
        query_result = self.query_list_prop("redirects", page_title, rdlimit="max")

        return [redirect["title"] for redirect in query_result]

    def query_list_prop(self, prop, page_title: str, **params):
        query_result, continue_params = self.query_for_page(prop, page_title, **params)
        values = query_result.get(prop, [])

        assert isinstance(values, list), f"Expected list, got {type(values)}"

        if continue_params:
            return values + self.query_list_prop(
                prop, page_title, **params, **continue_params
            )
        return values

    def query_prop(self, prop, page_title: str, **params):
        query_result, _ = self.query_for_page(prop, page_title, **params)

        return query_result

    def query_for_page(self, prop, page_title: str, **params):
        query_result = self.query(prop, titles=page_title, **params)
        values = query_result.get("query", {}).get("pages", {}).values()
        if len(values) == 1:
            return next(iter(values)), query_result.get("continue", None)
        raise ValueError(f"Page '{page_title}' not found or multiple pages found")

    def query(self, prop, **params) -> dict:
        api_url = f"https://{self.domain}/w/api.php"
        api_params = {"action": "query", "format": "json", "prop": prop, **params}

        response = self.http_client.get(api_url, params=api_params)
        response.raise_for_status()

        return response.json()
