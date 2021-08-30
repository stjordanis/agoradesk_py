import os

from agoradesk import AgoraDesk

if __name__ == "__main__":

    api = AgoraDesk(api_key=os.environ["api_key"])

    # Get information about logged in user
    who_am_i = api.myself()["response"]["data"]

    # Get information about all released trades
    api_response = api.dashboard_released()
    trades = api_response["response"]["data"]["contact_list"]

    # Get information about XMR wallet transactions
    wallet_transactions = api.wallet_xmr()["response"]["data"]

    for trade in trades:
        trade_data = trade["data"]
        trade_action = None
        if who_am_i["username"] == trade_data["buyer"]["username"]:
            trade_action = "bought"
        elif who_am_i["username"] == trade_data["seller"]["username"]:
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

    notifications = api.notifications()["response"]["data"]
    print()
    print("Notifications:")
    print("==============")
    for notify in notifications:
        print(f"{notify['created_at']} {notify['msg']}  ({notify['id']})")

    api_response = api.notifications_mark_as_read(
        "7ca4d852-b2ee-4ca9-a4d8-52b2eeaca913"
    )
    print()
    print("Notifications/mark_as_read:")
    print("==============")
    if not api_response["success"]:
        print(f"Error: {api_response['response']['error']}")
    if "data" in api_response["response"]:
        print(api_response["response"]["data"])
