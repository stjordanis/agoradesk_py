"""See https://agoradesk.com/api-docs/v1."""
# pylint: disable=too-many-lines
# Large API. Lots of lines can't be avoided.
import json
import logging
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import arrow
import httpx

__author__ = "marvin8"
__copyright__ = "(C) 2021 https://codeberg.org/MarvinsCryptoTools/agoradesk_py"
__version__ = "0.1.0"

# set logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("requests.packages.urllib3").setLevel(logging.INFO)
logging.getLogger("urllib3.connectionpool").setLevel(logging.INFO)
logger = logging.getLogger(__name__)

URI_API = "https://agoradesk.com/api/v1/"


class AgoraDesk:
    """AgoraDesk / LocalMonero API object.

    Documentation: https://agoradesk.com/api-docs/v1
    """

    # pylint: disable=too-many-public-methods
    # API provides this many methods, I can't change that

    def __init__(self, api_key: Optional[str], debug: Optional[bool] = False) -> None:
        self.api_key = ""
        if api_key:
            self.api_key = api_key
        self.debug = debug

        if self.debug:
            logging.getLogger("requests.packages.urllib3").setLevel(logging.DEBUG)
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        logger.debug("creating instance of AgoraDesk API with api_key %s", self.api_key)

    def _api_call(
        self,
        api_method: str,
        http_method: Optional[str] = "GET",
        query_values: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        api_call_url = URI_API + api_method

        headers = {
            "Content-Type": "application/json",
            "User-Agent": f"agoradesk_py/{__version__} "
            f"https://codeberg.org/MarvinsCryptoTools/agoradesk_py",
            "Authorization": self.api_key,
        }

        logger.debug("API Call URL: %s", api_call_url)
        logger.debug("Headers     : %s", headers)
        logger.debug("HTTP Method : %s", http_method)
        logger.debug("Query Values: %s", query_values)
        logger.debug("Query Values as Json:\n%s", json.dumps(query_values))

        result: Dict[str, Any] = {
            "success": False,
            "message": "Invalid Method",
            "response": None,
            "status": None,
        }

        try:
            response = None
            if http_method == "POST":
                if query_values:
                    response = httpx.post(
                        url=api_call_url,
                        headers=headers,
                        content=json.dumps(query_values),
                    )
                else:
                    response = httpx.post(
                        url=api_call_url,
                        headers=headers,
                    )

            else:
                response = httpx.get(
                    url=api_call_url, headers=headers, params=query_values
                )

            logger.debug(response)
            result["response"] = json.loads(response.text)
            result["status"] = response.status_code
            if response.status_code == 200:
                result["success"] = True
                result["message"] = "OK"
            else:
                result["message"] = "API ERROR"

            return result
        except httpx.ConnectError as error:
            result["message"] = str(error)
            result["status"] = 600
            result["response"] = {"error": {"message": error}}
            return result
        except json.decoder.JSONDecodeError:
            result["message"] = "Not JSON"
            if response:
                result["status"] = response.status_code
                result["response"] = {"error": {"message": response.text}}
            return result

    # Account related API Methods
    # ===========================

    def account_info(self, username: str) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/getUserByUsername
        """
        return self._api_call(api_method=f"account_info/{username}")

    def dashboard(self) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/getUserDashboard
        """
        return self._api_call(api_method="dashboard")

    def dashboard_buyer(self) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/getUserDashboardBuyer
        """
        return self._api_call(api_method="dashboard/buyer")

    def dashboard_seller(self) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/getUserDashboardSeller
        """
        return self._api_call(api_method="dashboard/seller")

    def dashboard_canceled(self) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/getUserDashboardCanceled
        """
        return self._api_call(api_method="dashboard/canceled")

    def dashboard_closed(self) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/getUserDashboardClosed
        """
        return self._api_call(api_method="dashboard/closed")

    def dashboard_released(self) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/getUserDashboardReleased
        """

        return self._api_call(api_method="dashboard/released")

    def logout(self) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/logout
        """

        return self._api_call(api_method="logout", http_method="POST")

    def myself(self) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/getTokenOwnerUserData
        """

        return self._api_call(api_method="myself")

    def notifications(self) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/getUserNotifications
        """

        return self._api_call(api_method="notifications")

    def notifications_mark_as_read(self, notification_id: str) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/markNotificationRead
        """

        return self._api_call(
            api_method=f"notifications/mark_as_read/{notification_id}",
            http_method="POST",
        )

    def recent_messages(self) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/getRecemtMessages
        """

        return self._api_call(api_method="recent_messages")

    # Trade related API Methods
    # ===========================

    #     post/feedback/{username} ??? Give feedback to a user
    def feedback(
        self, username: str, feedback: str, msg: Optional[str]
    ) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/setUserFeedback
        """

        params = {"feedback": feedback}
        if msg:
            params["msg"] = msg
        return self._api_call(
            api_method=f"feedback/{username}",
            http_method="POST",
            query_values=params,
        )

    #     Todo:
    #     post/trade/contact_release/{trade_id} ??? Release trade escrow
    #     post/contact_fund/{trade_id} ??? Fund a trade
    #     post/contact_dispute/{trade_id} ??? Start a trade dispute

    #     post/contact_mark_as_paid/{trade_id} ??? Mark a trade as paid
    def contact_mark_as_paid(self, trade_id: str) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/markPaid
        """
        return self._api_call(
            api_method=f"contact_mark_as_paid/{trade_id}", http_method="POST"
        )

    #     post/contact_cancel/{trade_id} ??? Cancel the trade
    def contact_cancel(
        self,
        trade_id: str,
    ) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/cancelTrade
        """
        return self._api_call(
            api_method=f"contact_cancel/{trade_id}",
            http_method="POST",
        )

    #     Todo:
    #     post/contact_escrow/{trade_id} ??? Enable escrow

    #     get/contact_messages/{trade_id} ??? Get trade messages
    def contact_messages(
        self, trade_id: str, after: Optional[arrow.Arrow] = None
    ) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/getTradeMessages
        """
        if after:
            reply = self._api_call(
                api_method=f"contact_messages/{trade_id}",
                query_values={"after": after.to("UTC").isoformat()},
            )
        else:
            reply = self._api_call(api_method=f"contact_messages/{trade_id}")

        return reply

    #     post/contact_create/{ad_id} ??? Start a trade
    def contact_create(
        self,
        ad_id: str,
        amount: float,
        msg: Optional[str] = None,
    ) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/startTrade
        """
        payload: Dict[str, Any] = {"amount": amount}
        if msg:
            payload["msg"] = msg
        return self._api_call(
            api_method=f"contact_create/{ad_id}",
            http_method="POST",
            query_values=payload,
        )

    #     get/contact_info/{trade_id} ??? Get a trade by trade ID
    def contact_info(self, trade_ids: Union[str, List[str]]) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/getTradeById and
        https://agoradesk.com/api-docs/v1#operation/getTradesInBulk
        """
        api_method = "contact_info"
        if isinstance(trade_ids, list):
            params = "?contacts="
            for trade_id in trade_ids:
                params += f"{trade_id},"
            params = params[0:-1]
        else:
            params = f"/{trade_ids}"
        api_method += params
        return self._api_call(api_method=api_method)

    #     Todo: Add image upload functionality
    #     post/contact_message_post/{trade_id} ??? Send a chat message/attachment
    def contact_message_post(
        self, trade_id: str, msg: Optional[str] = None
    ) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/sendChatMessage
        """
        payload = {"msg": msg}
        return self._api_call(
            api_method=f"contact_message_post/{trade_id}",
            http_method="POST",
            query_values=payload,
        )

    #     Todo:
    #     get/contact_message_attachment/{trade_id}/{attachment_id}

    # Advertisement related API Methods
    # ================================

    def ad_create(
        self,
        country_code: str,
        currency: str,
        trade_type: str,
        asset: str,
        price_equation: str,
        track_max_amount: bool,
        require_trusted_by_advertiser: bool,
        verified_email_required: Optional[bool] = None,
        online_provider: Optional[str] = None,
        msg: Optional[str] = None,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None,
        limit_to_fiat_amounts: Optional[str] = None,
        payment_method_details: Optional[str] = None,
        first_time_limit_asset: Optional[float] = None,
        require_feedback_score: Optional[int] = None,
        account_info: Optional[str] = None,
        payment_window_minutes: Optional[int] = None,
        floating: Optional[bool] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
    ) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/createAd
        """

        # pylint: disable=too-many-arguments
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-branches
        # API takes this many arguments, I can't change that
        # Too many locals and too many branches goes hand in hand
        # with too many arguments
        params: Dict[str, Any] = {
            "countrycode": country_code,
            "currency": currency,
            "trade_type": trade_type,
            "asset": asset,
            "price_equation": price_equation,
            "track_max_amount": 1 if track_max_amount else 0,
            "require_trusted_by_advertiser": 1 if require_trusted_by_advertiser else 0,
        }
        if verified_email_required:
            params["verified_email_required"] = 1 if verified_email_required else 0
        if online_provider:
            params["online_provider"] = online_provider
        if msg:
            params["msg"] = msg
        if min_amount:
            params["min_amount"] = min_amount
        if max_amount:
            params["max_amount"] = max_amount
        if limit_to_fiat_amounts:
            params["limit_to_fiat_amounts"] = limit_to_fiat_amounts
        if payment_method_details:
            params["payment_method_details"] = payment_method_details
        if first_time_limit_asset:
            params["first_time_limit_asset"] = first_time_limit_asset
        if require_feedback_score:
            params["require_feedback_score"] = require_feedback_score
        if account_info:
            params["account_info"] = account_info
        if payment_window_minutes:
            params["payment_window_minutes"] = payment_window_minutes
        if floating:
            params["floating"] = 1 if floating else 0
        if lat:
            params["lat"] = lat
        if lon:
            params["lon"] = lon

        return self._api_call(
            api_method="ad-create",
            http_method="POST",
            query_values=params,
        )

    def ad(
        self,
        ad_id: str,
        country_code: Optional[str] = None,
        currency: Optional[str] = None,
        trade_type: Optional[str] = None,
        asset: Optional[str] = None,
        price_equation: Optional[str] = None,
        track_max_amount: Optional[bool] = None,
        require_trusted_by_advertiser: Optional[bool] = None,
        verified_email_required: Optional[bool] = None,
        online_provider: Optional[str] = None,
        msg: Optional[str] = None,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None,
        limit_to_fiat_amounts: Optional[str] = None,
        payment_method_details: Optional[str] = None,
        first_time_limit_asset: Optional[float] = None,
        require_feedback_score: Optional[int] = None,
        account_info: Optional[str] = None,
        payment_window_minutes: Optional[int] = None,
        floating: Optional[bool] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        visible: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/editAd
        """

        # pylint: disable=invalid-name
        # Don't want to change the name of the method from what the API call is
        # pylint: disable=too-many-arguments
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-branches
        # API takes this many arguments, I can't change that
        # Too many locals and too many branches goes hand in hand
        # with too many arguments
        params: Dict[str, Union[str, float, bool]] = {}
        if country_code:
            params["countrycode"] = country_code
        if currency:
            params["currency"] = currency
        if trade_type:
            params["trade_type"] = trade_type
        if asset:
            params["asset"] = asset
        if price_equation:
            params["price_equation"] = price_equation
        if track_max_amount:
            params["track_max_amount"] = 1 if track_max_amount else 0
        if require_trusted_by_advertiser:
            params["require_trusted_by_advertiser"] = (
                1 if require_trusted_by_advertiser else 0
            )
        if verified_email_required:
            params["verified_email_required"] = 1 if verified_email_required else 0
        if online_provider:
            params["online_provider"] = online_provider
        if msg:
            params["msg"] = msg
        if min_amount:
            params["min_amount"] = min_amount
        if max_amount:
            params["max_amount"] = max_amount
        if limit_to_fiat_amounts:
            params["limit_to_fiat_amounts"] = limit_to_fiat_amounts
        if payment_method_details:
            params["payment_method_details"] = payment_method_details
        if first_time_limit_asset:
            params["first_time_limit_asset"] = first_time_limit_asset
        if require_feedback_score:
            params["require_feedback_score"] = require_feedback_score
        if account_info:
            params["account_info"] = account_info
        if payment_window_minutes:
            params["payment_window_minutes"] = payment_window_minutes
        if floating:
            params["floating"] = 1 if floating else 0
        if lat:
            params["lat"] = lat
        if lon:
            params["lon"] = lon
        if visible:
            params["visible"] = 1 if visible else 0

        return self._api_call(
            api_method=f"ad/{ad_id}",
            http_method="POST",
            query_values=params,
        )

    def ad_equation(self, ad_id: str, price_equation: str) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/updateFormula
        """
        return self._api_call(
            api_method=f"ad-equation/{ad_id}",
            http_method="POST",
            query_values={"price_equation": price_equation},
        )

    def ad_delete(self, ad_id: str) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/deleteAd
        """
        return self._api_call(api_method=f"ad-delete/{ad_id}", http_method="POST")

    def ads(
        self,
        country_code: Optional[str] = None,
        currency: Optional[str] = None,
        trade_type: Optional[str] = None,
        visible: Optional[bool] = None,
        asset: Optional[str] = None,
        payment_method_code: Optional[str] = None,
    ) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/getYourAds
        """

        # pylint: disable=too-many-arguments
        # API takes this many arguments, I can't change that

        params = {}
        if country_code:
            params["countrycode"] = country_code
        if currency:
            params["currency"] = currency
        if trade_type:
            params["trade_type"] = trade_type
        if visible is not None and visible:
            params["visible"] = "1"
        elif visible is not None and not visible:
            params["visible"] = "0"
        if asset:
            params["asset"] = asset
        if payment_method_code:
            params["payment_method_code"] = payment_method_code

        if len(params) == 0:
            return self._api_call(api_method="ads")

        return self._api_call(api_method="ads", query_values=params)

    def ad_get(self, ad_ids: List[str]) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/getAdById and
        https://agoradesk.com/api-docs/v1#operation/getAdsInBulk
        """
        api_method = "ad-get"
        params = None
        ids = str(ad_ids)[1:-1].replace(" ", "").replace("'", "")

        if len(ad_ids) == 1:
            api_method += f"/{ids}"
        else:
            params = {"ads": ids}
        return self._api_call(api_method=api_method, query_values=params)

    def payment_methods(self, country_code: Optional[str] = None) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/paymentMethods and
        https://agoradesk.com/api-docs/v1#operation/countryHasPaymentMethod
        """
        api_method = "payment_methods"
        if country_code:
            api_method += f"/{country_code}"
        return self._api_call(api_method=api_method)

    def country_codes(self) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/countryCodes
        """
        return self._api_call(api_method="countrycodes")

    def currencies(self) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/currencyCodes
        """
        return self._api_call(api_method="currencies")

    def equation(self, price_equation: str, currency: str) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/priceFormula
        """
        return self._api_call(
            api_method="equation",
            http_method="POST",
            query_values={"price_equation": price_equation, "currency": currency},
        )

    # Public ad search related API Methods
    # ====================================

    def _generic_online(
        self,
        direction: str,
        main_currency: str,
        exchange_currency: str,
        country_code: Optional[str] = None,
        payment_method: Optional[str] = None,
        amount: Optional[float] = None,
        page: Optional[int] = None,
    ) -> Dict[str, Any]:

        # pylint: disable=too-many-arguments

        add_to_api_method = ""
        if country_code:
            add_to_api_method = f"/{country_code}"
        if payment_method:
            add_to_api_method += f"/{payment_method}"

        params = self._generic_search_parameters(amount, page)

        return self._api_call(
            api_method=f"{direction}-{main_currency}-online/"
            f"{exchange_currency}{add_to_api_method}",
            query_values=params,
        )

    @staticmethod
    def _generic_search_parameters(amount, page):
        params = None
        if amount and not page:
            params = {"amount": f"{amount}"}
        elif amount and page:
            params = {"amount": f"{amount}", "page": f"{page}"}
        elif not amount and page:
            params = {"page": f"{page}"}
        return params

    def buy_monero_online(
        self,
        currency_code: str,
        country_code: Optional[str] = None,
        payment_method: Optional[str] = None,
        amount: Optional[float] = None,
        page: Optional[int] = None,
    ) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/getOnlineSellXmrByCurrencyCode and
        https://agoradesk.com/api-docs/v1#operation/getOnlineSellXmrByCurrencyCodeAndCountryCode and                    # noqa: E501   pylint: disable=line-too-long
        https://agoradesk.com/api-docs/v1#operation/getOnlineSellXmrByCurrencyCodeAndPaymentMethodCode and              # noqa: E501   pylint: disable=line-too-long
        https://agoradesk.com/api-docs/v1#operation/getOnlineSellXmrByCurrencyCodeAndCountryCodeAndPaymentMethodCode    # noqa: E501   pylint: disable=line-too-long
        """

        # pylint: disable=too-many-arguments

        return self._generic_online(
            direction="buy",
            main_currency="monero",
            exchange_currency=currency_code,
            country_code=country_code,
            payment_method=payment_method,
            amount=amount,
            page=page,
        )

    def buy_bitcoins_online(
        self,
        currency_code: str,
        country_code: Optional[str] = None,
        payment_method: Optional[str] = None,
        amount: Optional[float] = None,
        page: Optional[int] = None,
    ) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/getOnlineSellBtcByCurrencyCode
        https://agoradesk.com/api-docs/v1#operation/getOnlineSellBtcByCurrencyCodeAndCountryCode and                    # noqa: E501   pylint: disable=line-too-long
        https://agoradesk.com/api-docs/v1#operation/getOnlineSellBtcByCurrencyCodeAndPaymentMethodCode and              # noqa: E501   pylint: disable=line-too-long
        https://agoradesk.com/api-docs/v1#operation/getOnlineSellBtcByCurrencyCodeAndCountryCodeAndPaymentMethodCode    # noqa: E501   pylint: disable=line-too-long
        """

        # pylint: disable=too-many-arguments

        return self._generic_online(
            direction="buy",
            main_currency="bitcoins",
            exchange_currency=currency_code,
            country_code=country_code,
            payment_method=payment_method,
            amount=amount,
            page=page,
        )

    def sell_monero_online(
        self,
        currency_code: str,
        country_code: Optional[str] = None,
        payment_method: Optional[str] = None,
        amount: Optional[float] = None,
        page: Optional[int] = None,
    ) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/getOnlineBuyXmrByCurrencyCode
        https://agoradesk.com/api-docs/v1#operation/getOnlineBuyXmrByCurrencyCodeAndCountryCode and                    # noqa: E501   pylint: disable=line-too-long
        https://agoradesk.com/api-docs/v1#operation/getOnlineBuyXmrByCurrencyCodeAndPaymentMethodCode and              # noqa: E501   pylint: disable=line-too-long
        https://agoradesk.com/api-docs/v1#operation/getOnlineBuyXmrByCurrencyCodeAndCountryCodeAndPaymentMethodCode    # noqa: E501   pylint: disable=line-too-long
        """

        # pylint: disable=too-many-arguments

        return self._generic_online(
            direction="sell",
            main_currency="monero",
            exchange_currency=currency_code,
            country_code=country_code,
            payment_method=payment_method,
            amount=amount,
            page=page,
        )

    def sell_bitcoins_online(
        self,
        currency_code: str,
        country_code: Optional[str] = None,
        payment_method: Optional[str] = None,
        amount: Optional[float] = None,
        page: Optional[int] = None,
    ) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/getOnlineBuyBtcByCurrencyCode
        https://agoradesk.com/api-docs/v1#operation/getOnlineBuyBtcByCurrencyCodeAndCountryCode and                    # noqa: E501   pylint: disable=line-too-long
        https://agoradesk.com/api-docs/v1#operation/getOnlineBuyBtcByCurrencyCodeAndPaymentMethodCode and              # noqa: E501   pylint: disable=line-too-long
        https://agoradesk.com/api-docs/v1#operation/getOnlineBuyBtcByCurrencyCodeAndCountryCodeAndPaymentMethodCode    # noqa: E501   pylint: disable=line-too-long
        """

        # pylint: disable=too-many-arguments

        return self._generic_online(
            direction="sell",
            main_currency="bitcoins",
            exchange_currency=currency_code,
            country_code=country_code,
            payment_method=payment_method,
            amount=amount,
            page=page,
        )

    def _generic_cash(
        self,
        direction: str,
        main_currency: str,
        exchange_currency: str,
        country_code: str,
        lat: str,
        lon: str,
        amount: Optional[float] = None,
        page: Optional[int] = None,
    ) -> Dict[str, Any]:
        # pylint: disable=too-many-arguments

        params = self._generic_search_parameters(amount, page)

        return self._api_call(
            api_method=f"{direction}-{main_currency}-with-cash/"
            f"{exchange_currency}/{country_code}/{lat}/{lon}",
            query_values=params,
        )

    def buy_monero_with_cash(
        self,
        currency_code: str,
        country_code: str,
        lat: str,
        lon: str,
        amount: Optional[float] = None,
        page: Optional[int] = None,
    ) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/getLocalSellXmrByCurrencyCodeAndCountryCode    # noqa: E501   pylint: disable=line-too-long
        """

        # pylint: disable=too-many-arguments

        return self._generic_cash(
            direction="buy",
            main_currency="monero",
            exchange_currency=currency_code,
            country_code=country_code,
            lat=lat,
            lon=lon,
            amount=amount,
            page=page,
        )

    def buy_bitcoins_with_cash(
        self,
        currency_code: str,
        country_code: str,
        lat: str,
        lon: str,
        amount: Optional[float] = None,
        page: Optional[int] = None,
    ) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/getLocalSellBtcByCurrencyCodeAndCountryCode    # noqa: E501   pylint: disable=line-too-long
        """

        # pylint: disable=too-many-arguments

        return self._generic_cash(
            direction="buy",
            main_currency="bitcoins",
            exchange_currency=currency_code,
            country_code=country_code,
            lat=lat,
            lon=lon,
            amount=amount,
            page=page,
        )

    def sell_monero_with_cash(
        self,
        currency_code: str,
        country_code: str,
        lat: str,
        lon: str,
        amount: Optional[float] = None,
        page: Optional[int] = None,
    ) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/getLocalBuyXmrByCurrencyCodeAndCountryCode    # noqa: E501   pylint: disable=line-too-long
        """

        # pylint: disable=too-many-arguments

        return self._generic_cash(
            direction="sell",
            main_currency="monero",
            exchange_currency=currency_code,
            country_code=country_code,
            lat=lat,
            lon=lon,
            amount=amount,
            page=page,
        )

    def sell_bitcoins_with_cash(
        self,
        currency_code: str,
        country_code: str,
        lat: str,
        lon: str,
        amount: Optional[float] = None,
        page: Optional[int] = None,
    ) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/getLocalBuyBtcByCurrencyCodeAndCountryCode    # noqa: E501   pylint: disable=line-too-long
        """

        # pylint: disable=too-many-arguments

        return self._generic_cash(
            direction="sell",
            main_currency="bitcoins",
            exchange_currency=currency_code,
            country_code=country_code,
            lat=lat,
            lon=lon,
            amount=amount,
            page=page,
        )

    # Statistics related API Methods
    # ==============================

    def moneroaverage(
        self, currency: Optional[str] = "ticker-all-currencies"
    ) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/getXmrTicker and
        https://agoradesk.com/api-docs/v1#operation/getXmrTickerByCurrencyCode
        """
        return self._api_call(api_method=f"moneroaverage/{currency}")

    # Wallet related API Methods
    # ===========================

    def wallet(self) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/getBtcWallet
        """
        return self._api_call(api_method="wallet")

    def wallet_balance(self) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/getBtcWalletBalance
        """
        return self._api_call(api_method="wallet-balance")

    def wallet_xmr(self) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/getXmrWallet
        """
        return self._api_call(api_method="wallet/XMR")

    def wallet_balance_xmr(self) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/getXmrWalletBalance
        """
        return self._api_call(api_method="wallet-balance/XMR")

    def wallet_addr(self) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/getBtcAddress
        """
        return self._api_call(api_method="wallet-addr")

    def wallet_addr_xmr(self) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/getXMRAddress
        """
        return self._api_call(api_method="wallet-addr/XMR")

    def fees(self) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/getBtcFee
        """
        return self._api_call(api_method="fees")

    def fees_xmr(self) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/getXmrFee
        """
        return self._api_call(api_method="fees/XMR")

    def wallet_send(
        self,
        address: str,
        amount: float,
        password: str,
        fee_level: str,
        otp: Optional[int] = None,
    ) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/withdrawBtc
        """
        # pylint: disable=too-many-arguments

        params = {
            "address": address,
            "amount": amount,
            "password": password,
            "fee_level": fee_level,
        }
        if otp:
            params["otp"] = otp

        return self._api_call(
            api_method="wallet-send", http_method="POST", query_values=params
        )

    def wallet_send_xmr(
        self,
        address: str,
        amount: float,
        password: str,
        fee_level: str,
        otp: Optional[int] = None,
    ) -> Dict[str, Any]:
        """See Agoradesk API.

        https://agoradesk.com/api-docs/v1#operation/withdrawXmr
        """
        # pylint: disable=too-many-arguments

        params = {
            "address": address,
            "amount": amount,
            "password": password,
            "fee_level": fee_level,
        }
        if otp:
            params["otp"] = otp

        return self._api_call(
            api_method="wallet-send/XMR", http_method="POST", query_values=params
        )
