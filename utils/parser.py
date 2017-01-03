import requests
from lxml import html

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0'
}

def get_product_html(url):
    r = requests.get(url, headers=headers)
    tree = html.fromstring(r.content)
    return tree

def get_price(url):
    tree = get_product_html(url)

    price_text = tree.xpath('//font[@class="oldpricebolditalic"]/text()')[0]
    price_digits = price_text.split("\xa0")[0]
    price_digits = price_digits.replace(" ", "")
    price = int(price_digits)

    return price

def get_name(url):
    tree = get_product_html(url)

    name = tree.xpath('//h1[@class="producttitle fn"]/text()')[0]
    name = " ".join(name.split(" ")[:3])
    return name

# get_price("https://www.computeruniverse.ru/products/90668943/manli-geforce-gtx1070-ultimate.asp")
