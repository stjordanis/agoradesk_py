__author__ = "marvin8"
__copyright__ = "(C) 2021 https://codeberg.org/MarvinsCryptoTools/agoradesk_py"
__version__ = "0.1.0"


def test_contact_create_and_cancel(taker_api, local_cash_sale) -> None:
    created_trade = taker_api.contact_create(
        ad_id=local_cash_sale, amount=20, msg="Hello, this is a test trade."
    )
    print(f"\n\nCreate Trade response: {created_trade}")
    assert created_trade["success"] is True

    trade_id = created_trade["response"]["actions"]["contact_url"].split("/")[-1]

    cancel_trade = taker_api.contact_cancel(trade_id=trade_id)
    assert cancel_trade["success"] is True
