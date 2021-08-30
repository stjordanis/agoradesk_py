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


class AuthTests(unittest.TestCase):
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


class AccountTests(unittest.TestCase):
    def setUp(self) -> None:
        self.api = AgoraDesk(api_key=api_key, debug=True)

    def test_account_info(self) -> None:
        actual = self.api.account_info("Magicflyingcow")
        test_basic_response(self, actual, "account_info")

    def test_dashboard(self):
        actual = self.api.dashboard()
        test_basic_response(self, actual, "dashboard")

    def test_dashboard_buyer(self):
        actual = self.api.dashboard_buyer()
        test_basic_response(self, actual, "dashboard/buyer")

    def test_dashboard_seller(self):
        actual = self.api.dashboard_seller()
        test_basic_response(self, actual, "dashboard/seller")

    def test_dashboard_canceled(self):
        actual = self.api.dashboard_canceled()
        test_basic_response(self, actual, "dashboard/canceled")

    def test_dashboard_closed(self):
        actual = self.api.dashboard_closed()
        test_basic_response(self, actual, "dashboard/closed")

    def test_dashboard_released(self):
        actual = self.api.dashboard_released()
        test_basic_response(self, actual, "dashboard/released")

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


class StatisticsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.api = AgoraDesk(api_key=api_key, debug=True)

    def test_moneroaverage_ticker_all_currencies(self) -> None:
        actual = self.api.moneroaverage()
        test_basic_response(self, actual, "moneroaverage/ticker-all-currencies")

    def test_moneroaverage_aud(self) -> None:
        actual = self.api.moneroaverage(currency="AUD")
        test_basic_response(self, actual, "moneroaverage/AUD")


class WalletTest(unittest.TestCase):
    def setUp(self) -> None:
        self.api = AgoraDesk(api_key=api_key, debug=True)

    def test_wallet(self) -> None:
        actual = self.api.wallet()
        test_basic_response(self, actual, "wallet")

    def test_wallet_balance(self) -> None:
        actual = self.api.wallet_balance()
        test_basic_response(self, actual, "wallet-balance")

    def test_wallet_xrm(self) -> None:
        actual = self.api.wallet_xmr()
        test_basic_response(self, actual, "wallet/XMR")

    def test_wallet_balance_xmr(self) -> None:
        actual = self.api.wallet_balance_xmr()
        test_basic_response(self, actual, "wallet-balance/XMR")

    def test_wallet_addr(self) -> None:
        actual = self.api.wallet_addr()
        test_basic_response(self, actual, "wallet-addr")

    def test_wallet_addr_xmr(self) -> None:
        actual = self.api.wallet_addr_xmr()
        test_basic_response(self, actual, "wallet-addr/XMR")

    def test_fees(self) -> None:
        actual = self.api.fees()
        test_basic_response(self, actual, "fees")

    def test_fees_xmr(self) -> None:
        actual = self.api.fees_xmr()
        test_basic_response(self, actual, "fees/XMR")

    def test_wallet_send(self):
        # Todo: workout how to best test this method
        # actual = self.api.wallet_send(
        #     address="i6827278356r8ygrf78t",
        #     amount=0.1,
        #     password="password",
        #     fee_level="LOW",
        # )
        # test_basic_response(self, actual, "wallet-send")
        pass

    def test_wallet_send_xmr(self):
        # Todo: workout how to best test this method
        # actual = self.api.wallet_send_xmr(
        #     address="i6827278356r8ygrf78t",
        #     amount=0.1,
        #     password="password",
        #     fee_level="LOW",
        # )
        # test_basic_response(self, actual, "wallet-send/XMR")
        pass


if __name__ == "__main__":
    unittest.main()
