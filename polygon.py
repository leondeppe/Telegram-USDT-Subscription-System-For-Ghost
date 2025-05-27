import requests
import json
from time import sleep
import add_members as am
from creds import *


def check_total_balances(wallet):
    url = f"https://api.polygonscan.com/api?module=account&action=tokentx&address={MY_USDT_WALLET}&contractaddress={USDT_CONTRACT}&startblock=0&endblock=99999999&sort=asc&apikey={POLYGONSCAN_API_KEY}"

    response = requests.get(url)
    data = response.json()

    # total balance of each wallet
    total_balances = {}
    for i in data["result"]:
        addr = i["from"].lower()
        cash = int(i["value"]) // 10 ** 6

        if addr not in total_balances:
            total_balances[addr] = cash
        else:
            total_balances[addr] += cash

    if wallet not in total_balances:
        return 0

    return total_balances[wallet]


def check_payments():
    url = f"https://api.polygonscan.com/api?module=account&action=tokentx&address={MY_USDT_WALLET}&contractaddress={USDT_CONTRACT}&startblock=0&endblock=99999999&sort=asc&apikey={POLYGONSCAN_API_KEY}"

    response = requests.get(url)
    data = response.json()

    # total balance of each wallet
    total_balances = {}
    for i in data["result"]:
        addr = i["from"].lower()
        cash = int(i["value"]) // 10 ** 6

        if addr not in total_balances:
            total_balances[addr] = cash
        else:
            total_balances[addr] += cash

    with open("addresses.json", mode="r") as addresses_raw:
        addresses = json.load(addresses_raw)

    for k, v in addresses.items():
        addresses_key = v[1]
        if addresses_key not in total_balances:
            continue
        
        difference = total_balances[addresses_key] - v[3]
        if difference >= LOWEST_VALID_PAYMENT:
            addresses[k][3] = total_balances[addresses_key]
            addresses[k][2] += difference
            am.main(addresses[k][0])

    with open("addresses.json", mode="w") as addresses_raw:
        json.dump(addresses, addresses_raw)
