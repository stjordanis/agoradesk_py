from agoradesk_py.agoradesk import AgoraDesk

__author__ = "marvin8"
__copyright__ = "(C) 2021 https://codeberg.org/MarvinsCryptoTools/agoradesk_py"
__version__ = "0.1.0"


# Test Authentication
# ======================================
def test_ok_api_key(maker_api) -> None:
    actual = maker_api.myself()
    assert actual["success"] is True
    assert "response" in actual
    assert isinstance(actual["response"], dict) is True


def test_handles_invalid_key() -> None:
    local_api = AgoraDesk(api_key="invalid key")
    actual = local_api.myself()
    assert actual["success"] is False


def test_handles_none_key() -> None:
    local_api = AgoraDesk(api_key=None)
    actual = local_api.myself()
    assert actual["success"] is False
    assert actual["message"] == "API ERROR"
