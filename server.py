from flask import Flask, jsonify, render_template
from tinydb import TinyDB, Query
from tinyrecord import transaction

from utils.state import get_active_products
from utils.storage import init_products
from utils.spy import spy_on_products

from utils.storage import table

app = Flask(__name__, static_folder="assets", static_url_path="/assets")

active_products = get_active_products()
init_products(active_products)
spy_on_products(active_products)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    table.clear_cache()
    products = []
    for product in active_products:
        Product = Query()
        products.append(table.search(Product.md5 == product.get("md5"))[0])
    return jsonify(products)

app.run(host='0.0.0.0', port=13337)
