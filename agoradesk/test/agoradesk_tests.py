import os
import unittest

from agoradesk import AgoraDesk

api_key = os.environ["api_key"]


def test_basic_response(unit_test, result, method_name):
    unit_test.assertTrue(result["success"], "%s failed" % method_name)
    unit_test.assertTrue(
        result["response"] is not None, "result not present in response"
    )
    unit_test.assertTrue(isinstance(result["response"], dict), "result is not a dict")


class AgoraDeskAuthTests(unittest.TestCase):
    def setUp(self) -> None:
        self.api = AgoraDesk(api_key=api_key, debug=True)

    def test_handles_invalid_key(self) -> None:
        self.api = AgoraDesk(api_key="invalid key")
        actual = self.api.myself()
        self.assertFalse(actual["success"], "Invalid key")

    def test_handles_none_key(self) -> None:
        self.api = AgoraDesk(api_key=None)
        actual = self.api.myself()
        self.assertFalse(actual["success"], "None key")
        self.assertEqual(actual["message"], "API ERROR", "None key")


class AgoraDeskAccountTests(unittest.TestCase):
    def setUp(self) -> None:
        self.api = AgoraDesk(api_key=api_key, debug=True)

    def test_account_info(self) -> None:
        actual = self.api.account_info("Magicflyingcow")
        test_basic_response(self, actual, "account_info")

    def test_dashboard(self):
        actual = self.api.dashboard()
        test_basic_response(self, actual, "dasboard")

    def test_dashboard_buyer(self):
        actual = self.api.dashboard_buyer()
        test_basic_response(self, actual, "dasboard_buyer")

    def test_dashboard_seller(self):
        actual = self.api.dashboard_seller()
        test_basic_response(self, actual, "dasboard_seller")

    def test_dashboard_canceled(self):
        actual = self.api.dashboard_canceled()
        test_basic_response(self, actual, "dasboard_canceled")

    def test_dashboard_closed(self):
        actual = self.api.dashboard_closed()
        test_basic_response(self, actual, "dasboard_closed")

    def test_dashboard_released(self):
        actual = self.api.dashboard_released()
        test_basic_response(self, actual, "dasboard_released")

    def test_wallet_xmr(self):
        actual = self.api.wallet_xmr()
        test_basic_response(self, actual, "wallet_xmr")

    def test_logout(self):
        # Todo: workout how to best test this method
        # actual = self.api.logout()
        # test_basic_response(self, actual, "logout")
        pass

    def test_myself(self):
        actual = self.api.myself()
        test_basic_response(self, actual, "myself")

    def test_notifications(self):
        actual = self.api.notifications()
        test_basic_response(self, actual, "notifications")

    def test_notifications_mark_as_read(self):
        actual = self.api.notifications_mark_as_read("liuyqnxdrtynowgfldua")
        self.assertFalse(actual["success"], "ID not found")
        self.assertEqual(actual["status"], 400, "Status 400")

    def test_recent_messages(self) -> None:
        actual = self.api.recent_messages()
        test_basic_response(self, actual, "recent_messages")


if __name__ == "__main__":
    unittest.main()
