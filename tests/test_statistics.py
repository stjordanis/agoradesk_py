__author__ = "marvin8"
__copyright__ = "(C) 2021 https://codeberg.org/MarvinsCryptoTools/agoradesk_py"
__version__ = "0.1.0"


def test_moneroaverage_ticker_all_currencies(api2) -> None:
    result = api2.moneroaverage()
    assert result["success"] is True


def test_moneroaverage_aud(api2) -> None:
    result = api2.moneroaverage(currency="AUD")
    assert result["success"] is True
