"""Test that the package works."""
from j5_zoloto import __version__


def test_package_version() -> None:
    """Test that we can read the package version."""
    assert __version__ is not None
