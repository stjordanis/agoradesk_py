import os

import pytest

from agoradesk_py.agoradesk import AgoraDesk

__author__ = "marvin8"
__copyright__ = "(C) 2021 https://codeberg.org/MarvinsCryptoTools/agoradesk_py"
__version__ = "0.1.0"


@pytest.fixture(scope="session")
def default_api():
    api_key = os.environ["api_key"]
    yield AgoraDesk(api_key=api_key, debug=True)


@pytest.fixture(scope="session")
def api2():
    api_key = os.environ["api_key2"]
    yield AgoraDesk(api_key=api_key, debug=True)


@pytest.fixture
def local_cash_sale(default_api):
    actual_local_buy = default_api.ad_create(
        country_code="AU",
        currency="AUD",
        trade_type="LOCAL_BUY",
        asset="XMR",
        price_equation="usdaud*coingeckoxmrusd*0.1",
        track_max_amount=False,
        require_trusted_by_advertiser=True,
        msg="Test Only, do not trade with this",
        min_amount=1.2,
        max_amount=5.72,
        limit_to_fiat_amounts="2,5",
        lat=51.509865,
        lon=-0.118092,
        verified_email_required=False,
    )

    trade_id = None
    if actual_local_buy["success"]:
        trade_id = actual_local_buy["response"]["data"]["ad_id"]
    yield trade_id

    default_api.ad_delete(trade_id)
