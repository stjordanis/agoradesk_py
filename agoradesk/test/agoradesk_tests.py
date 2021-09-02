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

    def test_ad_create_show__update_and_delete(self) -> None:
        actual = self.api.ad_create(
            country_code="AU",
            currency="LTC",
            trade_type="ONLINE_BUY",
            asset="XMR",
            price_equation="coingeckoxmrltc*0.1",
            track_max_amount=False,
            require_trusted_by_advertiser=True,
            verified_email_required=True,
            online_provider="CRYPTOCURRENCY",
        )
        test_successful_response(self, actual, "add-create-mininmum")

        ad_id = actual["response"]["data"]["ad_id"]

        actual_single = self.api.ad_get(ad_ids=[ad_id])
        test_successful_response(self, actual_single, "ad_get/id")

        actual_complete = self.api.ad_create(
            country_code="AU",
            currency="LTC",
            trade_type="ONLINE_BUY",
            asset="XMR",
            price_equation="coingeckoxmrltc*0.1",
            track_max_amount=False,
            require_trusted_by_advertiser=True,
            verified_email_required=True,
            online_provider="CRYPTOCURRENCY",
            msg="Test Only, do not trade with this",
            min_amount=1.2,
            max_amount=5.72,
            limit_to_fiat_amounts="2,5",
            payment_method_details="monero address is 89xxxx",
            payment_window_minutes=15,
        )
        test_successful_response(self, actual_complete, "ad-create-all")
        ad_id2 = actual_complete["response"]["data"]["ad_id"]

        actual_local_buy = self.api.ad_create(
            country_code="AU",
            currency="AUD",
            trade_type="LOCAL_BUY",
            asset="XMR",
            price_equation="usdaud*coingeckoxmrusd*0.1",
            track_max_amount=False,
            require_trusted_by_advertiser=True,
            verified_email_required=True,
            msg="Test Only, do not trade with this",
            min_amount=1.2,
            max_amount=5.72,
            limit_to_fiat_amounts="2,5",
            payment_method_details="monero address is 89xxxx",
            payment_window_minutes=15,
            floating=True,
            lat=51.509865,
            lon=-0.118092,
        )
        test_successful_response(self, actual_local_buy, "ad-create-local_buy")
        ad_id3 = actual_local_buy["response"]["data"]["ad_id"]

        actual_price_equation = self.api.ad_equation(
            ad_id=ad_id3,
            price_equation="usdaud*coingeckoxmrusd*0.05",
        )
        test_successful_response(self, actual_price_equation, "ad-equation")

        actual_update = self.api.ad(
            ad_id=ad_id3,
            country_code="AU",
            currency="AUD",
            trade_type="LOCAL_BUY",
            asset="XMR",
            price_equation="usdaud*coingeckoxmrusd*0.1",
            track_max_amount=False,
            require_trusted_by_advertiser=True,
            verified_email_required=True,
            msg="Test Only, do not trade with this... I really mean this",
            min_amount=1.0,
            max_amount=6,
            payment_method_details="monero address is 89xxxx",
            payment_window_minutes=15,
            floating=True,
            lat=51.509865,
            lon=-0.118092,
        )
        test_successful_response(self, actual_update, "ad/{ad_id}")

        ad_ids = [ad_id, ad_id2, ad_id3]
        actual_multiple = self.api.ad_get(ad_ids=ad_ids)
        test_successful_response(self, actual_multiple, "ag-get?ads=...")

        actual_delete = self.api.ad_delete(ad_id)
        test_successful_response(self, actual_delete, "ad-delete")
        actual_delete2 = self.api.ad_delete(ad_id2)
        test_successful_response(self, actual_delete2, "ad-delete2")
        actual_delete3 = self.api.ad_delete(ad_id3)
        test_successful_response(self, actual_delete3, "ad-delete3")

    def test_ads(self) -> None:
        actual = self.api.ads()
        test_successful_response(self, actual, "ads")

    def test_ads_all_params(self) -> None:
        actual = self.api.ads(
            country_code="AU",
            currency="AUD",
            trade_type="ONLINE_SELL",
            visible=True,
            asset="XMR",
            payment_method_code="osko-payid",
        )
        test_successful_response(self, actual, "ads")

    def test_payment_methods(self) -> None:
        actual = self.api.payment_methods()
        test_successful_response(self, actual, "payment_methods")

    def test_payment_methods_country(self) -> None:
        actual = self.api.payment_methods(country_code="AU")
        test_successful_response(self, actual, "payment_methods/AU")

    def test_country_codes(self) -> None:
        actual = self.api.country_codes()
        test_successful_response(self, actual, "countrycodes")

    def test_currencies(self) -> None:
        actual = self.api.currencies()
        test_successful_response(self, actual, "currencies")

    def test_equation(self) -> None:
        actual = self.api.equation(
            price_equation="usdaud*coingeckoxmrusd*0.1", currency="AUD"
        )
        test_successful_response(self, actual, "equation")


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
