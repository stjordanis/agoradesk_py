import os
import unittest

from agoradesk import AgoraDesk

__author__ = "marvin8"
__copyright__ = "(C) 2021 https://codeberg.org/MarvinsCryptoTools/agoradesk_py"
__version__ = "0.1.0"

api_key = os.environ["api_key"]


def test_successful_response(unit_test, result, method_name):
    unit_test.assertTrue(result["success"], "%s failed" % method_name)
    unit_test.assertTrue("response" in result, "response not present in result")
    unit_test.assertTrue(isinstance(result["response"], dict), "response is not a dict")


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
        test_successful_response(self, actual, "account_info")

    def test_dashboard(self):
        actual = self.api.dashboard()
        test_successful_response(self, actual, "dashboard")

    def test_dashboard_buyer(self):
        actual = self.api.dashboard_buyer()
        test_successful_response(self, actual, "dashboard/buyer")

    def test_dashboard_seller(self):
        actual = self.api.dashboard_seller()
        test_successful_response(self, actual, "dashboard/seller")

    def test_dashboard_canceled(self):
        actual = self.api.dashboard_canceled()
        test_successful_response(self, actual, "dashboard/canceled")

    def test_dashboard_closed(self):
        actual = self.api.dashboard_closed()
        test_successful_response(self, actual, "dashboard/closed")

    def test_dashboard_released(self):
        actual = self.api.dashboard_released()
        test_successful_response(self, actual, "dashboard/released")

    def test_wallet_xmr(self):
        actual = self.api.wallet_xmr()
        test_successful_response(self, actual, "wallet_xmr")

    def test_logout(self):
        # Todo: workout how to best test this method
        # actual = self.api.logout()
        # test_successful_response(self, actual, "logout")
        pass

    def test_myself(self):
        actual = self.api.myself()
        test_successful_response(self, actual, "myself")

    def test_notifications(self):
        actual = self.api.notifications()
        test_successful_response(self, actual, "notifications")

    def test_notifications_mark_as_read(self):
        actual = self.api.notifications_mark_as_read("liuyqnxdrtynowgfldua")
        self.assertFalse(actual["success"], "ID not found")
        self.assertEqual(actual["status"], 400, "Status 400")

    def test_recent_messages(self) -> None:
        actual = self.api.recent_messages()
        test_successful_response(self, actual, "recent_messages")


class AdvertisementTest(unittest.TestCase):
    def setUp(self) -> None:
        self.api = AgoraDesk(api_key=api_key, debug=True)

    def test_payment_methods(self) -> None:
        actual = self.api.payment_methods()
        test_successful_response(self, actual, "payment_methods")


class AdSearchTest(unittest.TestCase):
    def setUp(self) -> None:
        self.api = AgoraDesk(api_key=api_key, debug=True)

    def test_buy_monero_online_aud_page1(self) -> None:
        actual = self.api.buy_monero_online(currency_code="AUD", page=1)
        test_successful_response(self, actual, "buy-monero-online/{currencycode}")

    def test_buy_monero_online_aud_au(self) -> None:
        actual = self.api.buy_monero_online(currency_code="AUD", country_code="AU")
        test_successful_response(
            self,
            actual,
            "buy-monero-online/{currencycode}/{countrycode}",
        )

    def test_buy_monero_online_aud_osko_333_33(self) -> None:
        actual = self.api.buy_monero_online(
            currency_code="AUD",
            payment_method="osko-payid",
            amount=333.33,
        )
        test_successful_response(
            self,
            actual,
            "buy-monero-online/{currencycode}/{payment_method}",
        )

    def test_buy_bitcoins_online_aud_333_page1(self) -> None:
        actual = self.api.buy_bitcoins_online(currency_code="AUD", amount=333, page=1)
        test_successful_response(self, actual, "buy-monero-online/{currencycode}")

    def test_sell_monero_online_aud_au_paypal(self) -> None:
        actual = self.api.sell_monero_online(
            currency_code="AUD", country_code="AU", payment_method="osko-payid"
        )
        test_successful_response(
            self,
            actual,
            "sell-monero-online/{currencycode}/{countrycode}/{payment_method}",
        )

    def test_sell_bitcoins_online_aud(self) -> None:
        actual = self.api.sell_bitcoins_online(currency_code="AUD")
        test_successful_response(self, actual, "sell-bitcoins-online/{currencycode}")

    def test_buy_monero_with_cash(self) -> None:
        actual = self.api.buy_monero_with_cash(
            currency_code="AUD",
            country_code="AU",
            lat="-26.75823",
            lon="152.85062",
        )
        test_successful_response(self, actual, "buy-monero-with_cash/...")

    def test_sell_bitcoins_with_cash_333_page1(self) -> None:
        actual = self.api.buy_bitcoins_with_cash(
            currency_code="AUD",
            country_code="AU",
            lat="-26.75823",
            lon="152.85062",
            amount=333,
            page=1,
        )
        test_successful_response(self, actual, "sell-bitcoins-with-cash/...")


class StatisticsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.api = AgoraDesk(api_key=api_key, debug=True)

    def test_moneroaverage_ticker_all_currencies(self) -> None:
        actual = self.api.moneroaverage()
        test_successful_response(self, actual, "moneroaverage/ticker-all-currencies")

    def test_moneroaverage_aud(self) -> None:
        actual = self.api.moneroaverage(currency="AUD")
        test_successful_response(self, actual, "moneroaverage/AUD")


class WalletTest(unittest.TestCase):
    def setUp(self) -> None:
        self.api = AgoraDesk(api_key=api_key, debug=True)

    def test_wallet(self) -> None:
        actual = self.api.wallet()
        test_successful_response(self, actual, "wallet")

    def test_wallet_balance(self) -> None:
        actual = self.api.wallet_balance()
        test_successful_response(self, actual, "wallet-balance")

    def test_wallet_xrm(self) -> None:
        actual = self.api.wallet_xmr()
        test_successful_response(self, actual, "wallet/XMR")

    def test_wallet_balance_xmr(self) -> None:
        actual = self.api.wallet_balance_xmr()
        test_successful_response(self, actual, "wallet-balance/XMR")

    def test_wallet_addr(self) -> None:
        actual = self.api.wallet_addr()
        test_successful_response(self, actual, "wallet-addr")

    def test_wallet_addr_xmr(self) -> None:
        actual = self.api.wallet_addr_xmr()
        test_successful_response(self, actual, "wallet-addr/XMR")

    def test_fees(self) -> None:
        actual = self.api.fees()
        test_successful_response(self, actual, "fees")

    def test_fees_xmr(self) -> None:
        actual = self.api.fees_xmr()
        test_successful_response(self, actual, "fees/XMR")

    def test_wallet_send(self):
        # Todo: workout how to best test this method
        # actual = self.api.wallet_send(
        #     address="i6827278356r8ygrf78t",
        #     amount=0.1,
        #     password="password",
        #     fee_level="LOW",
        # )
        # test_successful_response(self, actual, "wallet-send")
        pass

    def test_wallet_send_xmr(self):
        # Todo: workout how to best test this method
        # actual = self.api.wallet_send_xmr(
        #     address="i6827278356r8ygrf78t",
        #     amount=0.1,
        #     password="password",
        #     fee_level="LOW",
        # )
        # test_successful_response(self, actual, "wallet-send/XMR")
        pass


if __name__ == "__main__":
    unittest.main()
