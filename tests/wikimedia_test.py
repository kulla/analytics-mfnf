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


def test_get_current_redirects_success(wikimedia_client):
    redirects = wikimedia_client.get_current_redirects("Mathe für Nicht-Freaks")

    assert redirects == ["MfNF", "Serlo"]


def test_get_current_redirects_success_no_redirects(wikimedia_client):
    redirects = wikimedia_client.get_current_redirects(
        "Mathe für Nicht-Freaks: Analysis 1"
    )

    assert redirects == []


def test_api_query_success(wikimedia_client):
    result = wikimedia_client.api_query(prop="info", titles="Mathe für Nicht-Freaks")

    assert result["pages"]["68442"]["title"] == "Mathe für Nicht-Freaks"


def test_api_query_http_error(mocked_wikimedia_client, mock_http_client):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = HTTPError(
        "404 Client Error: Not Found for url"
    )
    mock_http_client.get.return_value = mock_response

    with pytest.raises(HTTPError, match="404 Client Error: Not Found for url"):
        mocked_wikimedia_client.api_query(prop="info", titles="Python")
