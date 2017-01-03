from flask import Flask, jsonify, render_template
from tinydb import TinyDB, Query

from utils.state import get_active_products
from utils.storage import init_products
from utils.spy import spy_on_products

app = Flask(__name__, static_folder="assets", static_url_path="/assets")
db = TinyDB('db.json')

active_products = get_active_products()
init_products(db, active_products)
spy_on_products(active_products)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    db.table("_default").clear_cache()
    products = []
    for product in active_products:
        Product = Query()
        products.append(db.search(Product.md5 == product.get("md5"))[0])
    return jsonify(products)

app.run(host='0.0.0.0', port=13337)
