from hashlib import md5

def get_active_products():
    file = open('parts.txt')
    urls = file.readlines()
    products = []
    for url in urls:
        url = url.strip()
        if url:
            products.append({
                "md5": md5(url.encode("utf-8")).hexdigest(),
                "url": url
            })
        else:
            print(" ! Wrong URL:", url)
    return products
