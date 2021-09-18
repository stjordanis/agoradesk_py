__author__ = "marvin8"
__copyright__ = "(C) 2021 https://codeberg.org/MarvinsCryptoTools/agoradesk_py"
__version__ = "0.1.0"


def test_wallet(default_api) -> None:
    result = default_api.wallet()
    assert result["success"] is True


def test_wallet_balance(default_api) -> None:
    result = default_api.wallet_balance()
    assert result["success"] is True


def test_wallet_xrm(default_api) -> None:
    result = default_api.wallet_xmr()
    assert result["success"] is True


def test_wallet_balance_xmr(default_api) -> None:
    result = default_api.wallet_balance_xmr()
    assert result["success"] is True


def test_wallet_addr(default_api) -> None:
    result = default_api.wallet_addr()
    assert result["success"] is True


def test_wallet_addr_xmr(default_api) -> None:
    result = default_api.wallet_addr_xmr()
    assert result["success"] is True


def test_fees(default_api) -> None:
    result = default_api.fees()
    assert result["success"] is True


def test_fees_xmr(default_api) -> None:
    result = default_api.fees_xmr()
    assert result["success"] is True


def test_wallet_send(default_api) -> None:
    # Todo: workout how to best test this method
    # result = default_api.wallet_send(
    #     address="i6827278356r8ygrf78t",
    #     amount=0.1,
    #     password="password",
    #     fee_level="LOW",
    # )
    # assert result["success"] is True
    pass


def test_wallet_send_xmr(default_api) -> None:
    # Todo: workout how to best test this method
    # result = default_api.wallet_send_xmr(
    #     address="i6827278356r8ygrf78t",
    #     amount=0.1,
    #     password="password",
    #     fee_level="LOW",
    # )
    # assert result["success"] is True
    pass
