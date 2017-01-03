from tinydb import TinyDB, Query
from .parser import get_name, get_price
from datetime import datetime
from tinyrecord import transaction
from tinydb_smartcache import SmartCacheTable

db = TinyDB('db.json')
db.table_class = SmartCacheTable
table = db.table('_default')

def init_products(products):
    print("")
    for product in products:
        Product = Query()
        if not table.search(Product.md5 == product.get("md5")):
            print(" * Found new product:", )
            url = product.get("url")
            print("   URL:", url)
            name = get_name(url)
            price = get_price(url)
            print("   Name:", name)
            print("   Price:", price)
            product.update({
                "name": name,
                "snaps": [{
                    "created_at": round(datetime.now().timestamp()),
                    "updated_at": round(datetime.now().timestamp()),
                    "price": price
                }]
            })

            with transaction(table) as tr:
                tr.insert(product)
            print("")
    print(" * Spying on", len(products), "products...")
    print("")
