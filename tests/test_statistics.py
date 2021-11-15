"""Contains pytest tests for statistics related api calls."""
# pylint: disable=missing-function-docstring

__author__ = "marvin8"
__copyright__ = "(C) 2021 https://codeberg.org/MarvinsCryptoTools/agoradesk_py"
__version__ = "0.1.0"


def test_moneroaverage_ticker_all_currencies(taker_api) -> None:
    result = taker_api.moneroaverage()
    assert result["success"] is True


def test_moneroaverage_aud(taker_api) -> None:
    result = taker_api.moneroaverage(currency="AUD")
    assert result["success"] is True
