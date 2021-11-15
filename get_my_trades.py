"""Sample code to retrieve available trades and wallet transtions."""
# pylint: disable=unsubscriptable-object, invalid-name
import os

from agoradesk_py.agoradesk import AgoraDesk

if __name__ == "__main__":

    api = AgoraDesk(api_key=os.environ["api_key"])

    # Get information about logged in user
    me = api.myself()["response"]["data"]

    # Get information about all released trades
    api_response = api.dashboard_released()
    trades = api_response["response"]["data"]["contact_list"]

    # Get information about XMR wallet transactions
    wallet_transactions = api.wallet_xmr()["response"]["data"]

    for trade in trades:
        trade_data = trade["data"]
        trade_action = None
        if me["username"] == trade_data["buyer"]["username"]:
            trade_action = "bought"
        elif me["username"] == trade_data["seller"]["username"]:
            trade_action = "sold"
        print(
            f"I have {trade_action} "
            f"{trade_data['amount_xmr']} XMR with a fee of {trade_data['fee_xmr']} XMR "
            f"for {trade_data['amount']} {trade_data['currency']} "
            f"on {trade_data['released_at']} ({trade_data['contact_id']})"
        )

    for transaction in wallet_transactions["received_transactions_30d"]:
        print(
            f"Received {transaction['amount']} XMR on {transaction['created_at']} "
            f"for {transaction['description']}"
        )

    for transaction in wallet_transactions["sent_transactions_30d"]:
        print(
            f"Sent {transaction['amount']} XMR on {transaction['created_at']} "
            f"for {transaction['description']}"
        )
