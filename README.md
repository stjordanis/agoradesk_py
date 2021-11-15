# agoradesk_py
Python interface for [AgoraDesk.com/LocalMonero.co API](https://agoradesk.com/api-docs/v1).

This is currently not a complete implementation of the Agoradesk API.

The following API calls are currently **not** supported.
-     #     post/trade/contact_release/{trade_id} • Release trade escrow
    #     post/contact_fund/{trade_id} • Fund a trade
    #     post/contact_dispute/{trade_id} • Start a trade dispute
    #     post/contact_escrow/{trade_id} • Enable escrow
    #     Todo: Add image upload functionality
    #     post/contact_message_post/{trade_id} • Send a chat message/attachment
    #     get/contact_message_attachment/{trade_id}/{attachment_id}


I offer no warranty of any kind -- use this at your own risk!

(I am not associated with AgoraDesk.com or LocalMonero.co.)

# Requirements:
* httpx
* arrow
* toml

# Install
`python setup.py install`

`pip install agoradesk_py`

# How to Use
This is an example about how you can use the library

```
#!/usr/bin/env python3

from agoradesk import AgoraDesk

api_key = <YourAPIKey>

api = AgoraDesk(api_key)

# Get information about all released trades
api_response = api.dashboard_released()

if api_response["success"]:
    trades = api_response["response"]["data"]["contact_list"]

    for trade in trades:
        trade_data = trade["data"]
        print(
            f"Traded "
            f"{trade_data['amount_xmr']} XMR with a fee of {trade_data['fee_xmr']} XMR "
            f"for {trade_data['amount']} {trade_data['currency']} "
            f"on {trade_data['released_at']}"
        )

else:
     print(f"Error: {api_response['response']['error']}")

```

# Running Tests
**Please be aware of the API requests limit of 20 req/h**

I use pytest. The tests depend on the two following environment variables being set to the api_keys of two testing
accounts at LocalMonero.co.
* api_key
* api_key2

Please be aware that:
* LocalMonero.co or AgoraDesk.com are not currently providing a testing setup and all testes are running in their production environment.
* For some tests to run successfully the account for `api_key2` needs to have a balance of currently about 0.1 XMR

To run the actual tests enter `pytest .` in the project directory.

# Contribute
Do you have an idea or found a bug in agoradesk_py? Please file an issue and/or submit a pull request! :)

Source code is currently on [Codeberg](https://codeberg.org) at https://codeberg.org/MarvinsCryptoTools/agoradesk_py

## Support
If you like the API and want to support me you can do so with
Monero:
    88NszkQU9qsafT9obFaDZSi7RvHSM76exJ1vvgVShTwM4HjvLr7XjJ7jDkFGnxr3UsDXLgT5t569N6uB7Gn4znjAFjUuN1q
