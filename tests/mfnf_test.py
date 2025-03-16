import pytest

from mfnf import MFNF


@pytest.fixture
def mfnf():
    return MFNF()


def test_get_sitemap(mfnf):
    # There are at least 10 books in the sitemap as of 2025-03-16
    assert len(mfnf.get_sitemap().books) >= 10


def test_get_page_with_all_redirects(mfnf):
    redirects = mfnf.get_page_with_all_redirects("Mathe für Nicht-Freaks")

    assert redirects == {"Mathe für Nicht-Freaks", "MfNF", "Serlo"}

    redirects = mfnf.get_page_with_all_redirects(
        "Mathe für Nicht-Freaks: Trivialkriterium, Nullfolgenkriterium, Divergenzkriterium"
    )

    assert redirects == {
        "Mathe für Nicht-Freaks: Trivialkriterium, Nullfolgenkriterium, Divergenzkriterium",
        "Mathe für Nicht-Freaks: Reihe: Beispiele",
        "Mathe für Nicht-Freaks: Trivialkriterium",
    }


def test_get_old_titles(mfnf):
    old_titles = mfnf.get_old_titles(
        "Mathe für Nicht-Freaks: Epsilon-Delta-Kriterium der Stetigkeit"
    )

    assert old_titles == [
        "Mathe für Nicht-Freaks: Epsilon-Delta-Definition der Stetigkeit"
    ]
