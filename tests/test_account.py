__author__ = "marvin8"
__copyright__ = "(C) 2021 https://codeberg.org/MarvinsCryptoTools/agoradesk_py"
__version__ = "0.1.0"


def test_account_info(default_api) -> None:
    result = default_api.account_info("Magicflyingcow")
    assert result["success"] is True


def test_dashboard(default_api) -> None:
    result = default_api.dashboard()
    assert result["success"] is True


def test_dashboard_buyer(default_api) -> None:
    result = default_api.dashboard_buyer()
    assert result["success"] is True


def test_dashboard_seller(default_api) -> None:
    result = default_api.dashboard_seller()
    assert result["success"] is True


def test_dashboard_canceled(default_api) -> None:
    result = default_api.dashboard_canceled()
    assert result["success"] is True


def test_dashboard_closed(default_api) -> None:
    result = default_api.dashboard_closed()
    assert result["success"] is True


def test_dashboard_released(default_api) -> None:
    result = default_api.dashboard_released()
    assert result["success"] is True


def test_wallet_xmr(default_api) -> None:
    result = default_api.wallet_xmr()
    assert result["success"] is True


def test_logout(default_api) -> None:
    # Todo: workout how to best test this method
    # result =default_api.logout()
    # assert result["success"] is True
    pass


def test_myself(default_api) -> None:
    result = default_api.myself()
    assert result["success"] is True


def test_notifications(default_api) -> None:
    result = default_api.notifications()
    assert result["success"] is True


def test_notifications_mark_as_read(default_api) -> None:
    actual = default_api.notifications_mark_as_read("liuyqnxdrtynowgfldua")
    assert actual["success"] is False
    assert actual["status"] == 400


def test_recent_messages(default_api) -> None:
    result = default_api.recent_messages()
    assert result["success"] is True
