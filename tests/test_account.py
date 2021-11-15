"""Contains pytest tests for account related api calls."""
# pylint: disable=missing-function-docstring

__author__ = "marvin8"
__copyright__ = "(C) 2021 https://codeberg.org/MarvinsCryptoTools/agoradesk_py"
__version__ = "0.1.0"


def test_account_info(maker_api) -> None:
    result = maker_api.account_info("Magicflyingcow")
    assert result["success"] is True


def test_dashboard(maker_api) -> None:
    result = maker_api.dashboard()
    assert result["success"] is True


def test_dashboard_buyer(maker_api) -> None:
    result = maker_api.dashboard_buyer()
    assert result["success"] is True


def test_dashboard_seller(maker_api) -> None:
    result = maker_api.dashboard_seller()
    assert result["success"] is True


def test_dashboard_canceled(maker_api) -> None:
    result = maker_api.dashboard_canceled()
    assert result["success"] is True


def test_dashboard_closed(maker_api) -> None:
    result = maker_api.dashboard_closed()
    assert result["success"] is True


def test_dashboard_released(maker_api) -> None:
    result = maker_api.dashboard_released()
    assert result["success"] is True


def test_wallet_xmr(maker_api) -> None:
    result = maker_api.wallet_xmr()
    assert result["success"] is True


def test_logout(maker_api) -> None:
    # Todo: workout how to best test this method
    # result =maker_api.logout()
    # assert result["success"] is True
    pass


def test_myself(maker_api) -> None:
    result = maker_api.myself()
    assert result["success"] is True


def test_notifications(maker_api) -> None:
    result = maker_api.notifications()
    assert result["success"] is True


def test_notifications_mark_as_read(maker_api) -> None:
    actual = maker_api.notifications_mark_as_read("liuyqnxdrtynowgfldua")
    assert actual["success"] is False
    assert actual["status"] == 400


def test_recent_messages(maker_api) -> None:
    result = maker_api.recent_messages()
    assert result["success"] is True
