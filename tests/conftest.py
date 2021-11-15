"""Containing the PyTest fixtures."""
# pylint: disable=duplicate-code
import os

import pytest

from agoradesk_py.agoradesk import AgoraDesk

__author__ = "marvin8"
__copyright__ = "(C) 2021 https://codeberg.org/MarvinsCryptoTools/agoradesk_py"
__version__ = "0.1.0"


@pytest.fixture(scope="session")
def maker_api():
    """Create an AgoraDesk session for creating ads and most other single user
    tests."""
    api_key = os.environ["api_key"]
    yield AgoraDesk(api_key=api_key, debug=True)


@pytest.fixture(scope="session")
def taker_api():
    """Create and AgoraDesk session for opening trades from ads."""
    api_key = os.environ["api_key2"]
    yield AgoraDesk(api_key=api_key, debug=True)


@pytest.fixture
def local_cash_sale(maker_api):
    """Create a local cash sale advertisement."""
    actual_local_buy = maker_api.ad_create(
        country_code="AU",
        currency="AUD",
        trade_type="LOCAL_BUY",
        asset="XMR",
        price_equation="usdaud*coingeckoxmrusd",
        track_max_amount=False,
        require_trusted_by_advertiser=True,
        msg="Test Only, do not trade with this",
        min_amount=10,
        max_amount=100,
        lat=51.509865,
        lon=-0.118092,
        verified_email_required=False,
    )

    ad_id = None
    if actual_local_buy["success"]:
        ad_id = actual_local_buy["response"]["data"]["ad_id"]
    yield ad_id

    maker_api.ad_delete(ad_id)


@pytest.fixture
def online_buy(maker_api):
    """Creates an online buy advertisement."""
    actual_online_buy = maker_api.ad_create(
        country_code="AU",
        currency="LTC",
        trade_type="ONLINE_BUY",
        asset="XMR",
        price_equation="coingeckoxmrltc*0.1",
        track_max_amount=False,
        require_trusted_by_advertiser=True,
        online_provider="CRYPTOCURRENCY",
    )

    ad_id = None
    if actual_online_buy["success"]:
        ad_id = actual_online_buy["response"]["data"]["ad_id"]
    yield ad_id

    maker_api.ad_delete(ad_id)
