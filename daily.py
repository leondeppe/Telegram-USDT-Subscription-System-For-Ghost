import json
import schedule
from time import sleep
import remove_members as rm
import polygon as pg


def daily_removal():
    with open("addresses.json", mode="r") as addresses_raw:
        addresses = json.load(addresses_raw)
    
    for k, v in addresses.items():
        if v[2] > 0:
            addresses[k][2] -= 1
            if addresses[k][2] == 0:
                # remove email
                rm.main(v[0])

    with open("addresses.json", mode="w") as addresses_raw:
        json.dump(addresses, addresses_raw)


schedule.every().day.at("00:00").do(daily_removal)

while True:
    schedule.run_pending()
    pg.check_payments()
    sleep(1)
