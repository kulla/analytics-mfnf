import pytest

from mfnf import MFNF


@pytest.fixture
def mfnf():
    return MFNF()


def test_get_sitemap(mfnf):
    # There are at least 10 books in the sitemap as of 2025-03-16
    assert len(mfnf.get_sitemap().books) >= 10
