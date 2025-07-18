import pytest
from unittest.mock import Mock
from requests.exceptions import HTTPError
from wikimedia import WikimediaAPIClient


@pytest.fixture
def mock_http_client():
    return Mock()


@pytest.fixture
def wikimedia_client():
    return WikimediaAPIClient()


@pytest.fixture
def mocked_wikimedia_client(mock_http_client):
    return WikimediaAPIClient(http_client=mock_http_client)


def test_get_wikitext_success(wikimedia_client):
    wikitext = wikimedia_client.get_wikitext("Mathe für Nicht-Freaks: Analysis 1")

    assert wikitext.startswith("{{#invoke:Mathe für Nicht-Freaks/Seite|oben}}")


def test_get_pageviews_success(wikimedia_client):
    pageviews = wikimedia_client.get_pageviews("Mathe für Nicht-Freaks")

    assert pageviews[0] == ("20160101", 117)


def test_get_pageviews_when_title_contains_question_mark(wikimedia_client):
    pageviews = wikimedia_client.get_pageviews(
        "Mathe für Nicht-Freaks: Was ist Mathematik?"
    )

    assert pageviews[0] == ("20160101", 8)


def test_get_pageviews_when_no_data_is_available(wikimedia_client):
    pageviews = wikimedia_client.get_pageviews(
        "Mathe für Nicht-Freaks: Reelle Zahlen: Körperaxiome 2"
    )

    assert pageviews == []


def test_get_current_redirects_success(wikimedia_client):
    redirects = wikimedia_client.get_current_redirects("Mathe für Nicht-Freaks")

    assert redirects == ["MfNF", "Serlo"]


def test_get_current_redirects_success_no_redirects(wikimedia_client):
    redirects = wikimedia_client.get_current_redirects(
        "Mathe für Nicht-Freaks: Analysis 1"
    )

    assert redirects == []


def test_api_query_for_page_success(wikimedia_client):
    result, continue_params = wikimedia_client.query_for_page(
        "info", "Mathe für Nicht-Freaks"
    )

    assert result["title"] == "Mathe für Nicht-Freaks"
    assert continue_params is None


def test_api_query_http_error(mocked_wikimedia_client, mock_http_client):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = HTTPError(
        "404 Client Error: Not Found for url"
    )
    mock_http_client.get.return_value = mock_response

    with pytest.raises(HTTPError, match="404 Client Error: Not Found for url"):
        mocked_wikimedia_client.query("info", titles="Python")
