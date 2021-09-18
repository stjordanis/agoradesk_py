__author__ = "marvin8"
__copyright__ = "(C) 2021 https://codeberg.org/MarvinsCryptoTools/agoradesk_py"
__version__ = "0.1.0"


def test_buy_monero_online_aud_page1(default_api) -> None:
    result = default_api.buy_monero_online(currency_code="AUD", page=1)
    assert result["success"] is True


def test_buy_monero_online_aud_au(default_api) -> None:
    result = default_api.buy_monero_online(currency_code="AUD", country_code="AU")
    assert result["success"] is True


def test_buy_monero_online_aud_osko_333_33(default_api) -> None:
    result = default_api.buy_monero_online(
        currency_code="AUD", payment_method="osko-payid", amount=333.33
    )
    assert result["success"] is True


def test_buy_bitcoins_online_aud_333_page1(default_api) -> None:
    result = default_api.buy_bitcoins_online(currency_code="AUD", amount=333, page=1)
    assert result["success"] is True


def test_sell_monero_online_aud_au_paypal(default_api) -> None:
    result = default_api.sell_monero_online(
        currency_code="AUD", country_code="AU", payment_method="osko-payid"
    )
    assert result["success"] is True


def test_sell_bitcoins_online_aud(default_api) -> None:
    result = default_api.sell_bitcoins_online(currency_code="AUD")
    assert result["success"] is True


def test_buy_monero_with_cash(default_api) -> None:
    result = default_api.buy_monero_with_cash(
        currency_code="AUD", country_code="AU", lat="-26.75823", lon="152.85062"
    )
    assert result["success"] is True


def test_sell_bitcoins_with_cash_333_page1(default_api) -> None:
    result = default_api.sell_bitcoins_with_cash(
        currency_code="AUD",
        country_code="AU",
        lat="-26.75823",
        lon="152.85062",
        amount=333,
        page=1,
    )
    assert result["success"] is True
