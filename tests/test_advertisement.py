"""Contains pytest tests for advertisement related api calls."""
# pylint: disable=missing-function-docstring

__author__ = "marvin8"
__copyright__ = "(C) 2021 https://codeberg.org/MarvinsCryptoTools/agoradesk_py"
__version__ = "0.1.0"


def test_ad_create_show_and_delete(maker_api) -> None:
    actual = maker_api.ad_create(
        country_code="AU",
        currency="LTC",
        trade_type="ONLINE_BUY",
        asset="XMR",
        price_equation="coingeckoxmrltc*0.1",
        track_max_amount=False,
        require_trusted_by_advertiser=True,
        online_provider="CRYPTOCURRENCY",
    )
    print(actual)
    assert actual["success"] is True
    ad_id = actual["response"]["data"]["ad_id"]

    actual_complete = maker_api.ad_create(
        country_code="AU",
        currency="LTC",
        trade_type="ONLINE_BUY",
        asset="XMR",
        price_equation="coingeckoxmrltc*0.1",
        track_max_amount=False,
        require_trusted_by_advertiser=True,
        online_provider="CRYPTOCURRENCY",
        msg="Test Only, do not trade with this",
        min_amount=1.2,
        max_amount=5.72,
        limit_to_fiat_amounts="2,5",
        payment_method_details="monero address is 89xxxx",
        payment_window_minutes=15,
    )
    assert actual_complete["success"] is True
    ad_id2 = actual_complete["response"]["data"]["ad_id"]

    actual_single = maker_api.ad_get(ad_ids=[ad_id2])
    assert actual_single["success"] is True

    ad_ids = [ad_id, ad_id2]
    actual_multiple = maker_api.ad_get(ad_ids=ad_ids)
    assert actual_multiple["success"] is True

    actual_delete = maker_api.ad_delete(ad_id)
    assert actual_delete["success"] is True
    actual_delete2 = maker_api.ad_delete(ad_id2)
    assert actual_delete2["success"] is True


def test_ad_equation(maker_api, local_cash_sale):
    assert local_cash_sale is not None

    actual = maker_api.ad_equation(
        ad_id=local_cash_sale,
        price_equation="usdaud*coingeckoxmrusd*0.05",
    )
    assert actual["success"] is True


def test_ad_update(maker_api, local_cash_sale):
    assert local_cash_sale is not None

    actual = maker_api.ad(
        ad_id=local_cash_sale,
        country_code="AU",
        currency="AUD",
        trade_type="LOCAL_BUY",
        asset="XMR",
        price_equation="usdaud*coingeckoxmrusd*0.1",
        track_max_amount=False,
        require_trusted_by_advertiser=True,
        msg="Test Only, do not trade with this... I really mean this",
        min_amount=50.00,
        max_amount=100.00,
        lat=51.509865,
        lon=-0.118092,
        verified_email_required=False,
        visible=True,
    )
    assert actual["success"] is True


def test_ads(maker_api) -> None:
    actual = maker_api.ads()
    assert actual["success"] is True


def test_ads_all_params(maker_api) -> None:
    actual = maker_api.ads(
        country_code="AU",
        currency="AUD",
        trade_type="ONLINE_SELL",
        visible=True,
        asset="XMR",
        payment_method_code="osko-payid",
    )
    assert actual["success"] is True


def test_payment_methods(maker_api) -> None:
    actual = maker_api.payment_methods()
    assert actual["success"] is True


def test_payment_methods_country(maker_api) -> None:
    actual = maker_api.payment_methods(country_code="AU")
    assert actual["success"] is True


def test_country_codes(maker_api) -> None:
    actual = maker_api.country_codes()
    assert actual["success"] is True


def test_currencies(maker_api) -> None:
    actual = maker_api.currencies()
    assert actual["success"] is True


def test_equation(maker_api) -> None:
    actual = maker_api.equation(
        price_equation="usdaud*coingeckoxmrusd*0.1", currency="AUD"
    )
    assert actual["success"] is True
