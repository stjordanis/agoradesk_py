"""
    See https://agoradesk.com/api-docs/v1
"""
import logging
import json
from typing import Optional
import http.client

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
    """
    AgoraDesk / LocalMonero API object

    Documentation: https://agoradesk.com/api-docs/v1
    """

    def __init__(self, api_key: Optional[str], debug: Optional[bool] = False) -> None:
        self.api_key = ""
        if api_key:
            self.api_key = api_key
        self.debug = debug

        if self.debug:
            http.client.HTTPConnection.debuglevel = 1
            logging.getLogger("requests.packages.urllib3").setLevel(logging.DEBUG)
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        logger.debug("creating instance of AgoraDesk API with api_key %s", self.api_key)

    def _api_call(
        self,
        api_method: str,
        http_method: Optional[str] = "GET",
        query_values: Optional[dict] = None,
    ) -> dict:
        api_call_url = URI_API + api_method

        headers = {
            "Content-Type": "application/json",
            "User-Agent": f"agoradesk_py/{__version__} "
            f"https://codeberg.org/MarvinsCryptoTools/agoradesk_py",
            "Authorization": self.api_key,
        }

        result = {
            "success": False,
            "message": "Invalid Method",
            "response": None,
            "status": None,
        }

        try:
            response = None
            if http_method == "GET":
                response = httpx.get(
                    url=api_call_url, headers=headers, params=query_values
                )

            elif http_method == "POST":
                response = httpx.post(
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
            result["message"] = error
            result["status"] = response.status_code
            result["response"] = {"error": {"message": error}}
            return result
        except json.decoder.JSONDecodeError:
            result["message"] = "Not JSON"
            result["status"] = response.status_code
            result["response"] = {"error": {"message": response.text}}
            return result

    # Account related API Methods
    # ===========================

    def account_info(self, username: str) -> dict:
        return self._api_call(api_method=f"account_info/{username}")

    def dashboard(self) -> dict:
        return self._api_call(api_method="dashboard")

    def dashboard_buyer(self) -> dict:
        return self._api_call(api_method="dashboard/buyer")

    def dashboard_seller(self) -> dict:
        return self._api_call(api_method="dashboard/seller")

    def dashboard_canceled(self) -> dict:
        return self._api_call(api_method="dashboard/canceled")

    def dashboard_closed(self) -> dict:
        return self._api_call(api_method="dashboard/closed")

    def dashboard_released(self) -> dict:
        return self._api_call(api_method="dashboard/released")

    def logout(self) -> dict:
        return self._api_call(api_method="logout", http_method="POST")

    def myself(self) -> dict:
        return self._api_call(api_method="myself")

    def notifications(self) -> dict:
        return self._api_call(api_method="notifications")

    def notifications_mark_as_read(self, notification_id: str) -> dict:
        return self._api_call(
            api_method=f"notifications/mark_as_read/{notification_id}",
            http_method="POST",
        )

    def recent_messages(self) -> dict:
        return self._api_call(api_method="recent_messages")

    # Wallet related API Methods
    # ===========================

    def wallet_xmr(self) -> dict:
        response = self._api_call(api_method="wallet/XMR")
        return response
