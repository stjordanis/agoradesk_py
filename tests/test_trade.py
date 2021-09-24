import arrow

__author__ = "marvin8"
__copyright__ = "(C) 2021 https://codeberg.org/MarvinsCryptoTools/agoradesk_py"
__version__ = "0.1.0"


def test_contact_create_get_info_send_and_get_msg_and_cancel(
    taker_api, local_cash_sale
) -> None:
    time_at_start = arrow.now("Australia/Brisbane")

    created_trade = taker_api.contact_create(
        ad_id=local_cash_sale, amount=10, msg="Hello, this is a test trade."
    )
    print(f"\n\nCreate Trade response: {created_trade}")
    assert created_trade["success"] is True

    trade_id = created_trade["response"]["actions"]["contact_url"].split("/")[-1]

    info = taker_api.contact_info(trade_id=trade_id)
    assert info["success"] is True
    response = info["response"]
    print(f"Contact Info: {response}")

    message_post = taker_api.contact_message_post(
        trade_id=trade_id, msg="This is another message"
    )
    assert message_post["success"] is True

    messages = taker_api.contact_messages(trade_id=trade_id)
    assert messages["success"] is True

    messages = taker_api.contact_messages(trade_id=trade_id, after=time_at_start)
    assert messages["success"] is True

    response = messages["response"]
    print(f"Messages: {response}")

    cancel_trade = taker_api.contact_cancel(trade_id=trade_id)
    assert cancel_trade["success"] is True
