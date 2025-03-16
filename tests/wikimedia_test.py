import pytest
from unittest.mock import Mock
from requests.exceptions import HTTPError
from wikimedia import WikimediaAPIClient


@pytest.fixture
def mock_http_client():
    return Mock()


@pytest.fixture
def wikimedia_project():
    return WikimediaAPIClient()


@pytest.fixture
def mocked_wikimedia_project(mock_http_client):
    return WikimediaAPIClient(http_client=mock_http_client)


def test_api_query(wikimedia_project):
    result = wikimedia_project.api_query(prop="info", titles="Mathe für Nicht-Freaks")

    assert result["pages"]["68442"]["title"] == "Mathe für Nicht-Freaks"


def test_api_query_raises_exception(mocked_wikimedia_project, mock_http_client):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = HTTPError(
        "404 Client Error: Not Found for url"
    )
    mock_http_client.get.return_value = mock_response

    with pytest.raises(HTTPError, match="404 Client Error: Not Found for url"):
        mocked_wikimedia_project.api_query(titles="Python")
