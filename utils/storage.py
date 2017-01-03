from tinydb import Query
from .parser import get_name, get_price
from datetime import datetime

def init_products(db, products):
    db.table("_default").clear_cache()
    print("")
    for product in products:
        Product = Query()
        if not db.search(Product.md5 == product.get("md5")):
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
            db.insert(product)
            print("")
    print(" * Spying on", len(products), "products...")
    print("")
