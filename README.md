# agoradesk_py
Python interface for [AgoraDesk.com/LocalMonero.co API](https://agoradesk.com/api-docs/v1).

I am not associated with AgoraDesk.com or LocalMonero.co -- use this at your own risk!

# Requirements:
* httpx

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
**be aware of the API requests limit of 20 req/h**

TODO: fill in 

# Contribute
Do you have an idea or found a bug in agoradesk_py? Please file an issue and make a PR! :)

## Support
If you like the API and want to support me you can do so with
Monero: 
    88NszkQU9qsafT9obFaDZSi7RvHSM76exJ1vvgVShTwM4HjvLr7XjJ7jDkFGnxr3UsDXLgT5t569N6uB7Gn4znjAFjUuN1q