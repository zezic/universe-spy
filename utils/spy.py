from time import sleep
from datetime import datetime
from threading import Thread
from tinydb import TinyDB, Query
from tinyrecord import transaction
from termcolor import colored
from random import randint
import os

from .parser import get_price
from .storage import table

INTERVAL = 360  # seconds

config = open(os.path.join("config.txt"))
settings = config.readlines()
for setting in settings:
    if "INTERVAL" in setting:
        setting = setting.split("=")[1].strip()
        INTERVAL = int(setting)


def spy_on_product(product):

    Product = Query()
    product_data = table.search(Product.md5 == product.get("md5"))[0]

    snaps = product_data.get("snaps")
    last_snap = product_data.get("snaps")[-1]
    old_price = last_snap.get("price")
    elapsed_time = round(datetime.now().timestamp()) - last_snap.get("updated_at")
    if elapsed_time >= INTERVAL:
        new_price = get_price(product_data.get("url"))
        print(" * Checking {}: ".format(product_data.get("name")), end="")
        if new_price != old_price:
            if new_price > old_price:
                print(colored("price {2} from {0} to {1}.".format(
                    old_price, new_price, ("raised" if new_price > old_price else "dropped")
                    ), "red" if new_price > old_price else "green"))
            snaps.append({
                "created_at": round(datetime.now().timestamp()),
                "updated_at": round(datetime.now().timestamp()),
                "price": new_price
            })
        else:
            snaps[-1].update({
                "updated_at": round(datetime.now().timestamp())
            })
            print("price still at {0}.".format(old_price))
        with transaction(table) as tr:
            tr.update({"snaps": snaps}, Product.md5 == product.get("md5"))
    else:
        time_left = INTERVAL - elapsed_time + randint(60, 120)
        print(" * {0} seconds until next check for {1}".format(time_left, product_data.get("name")))
        sleep(time_left)
    spy_on_product(product)

def spy_on_products(products):
    for product in products:
        thread = Thread(target=spy_on_product, args=(product,))
        thread.start()
