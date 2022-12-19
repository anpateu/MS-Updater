import math
import shelve
from google import Sheet
from config import Config
from api_ms import MoySkladAPI


def matrix_cena(price, stockDays):
    k_values = {
        1.10: (150000, float("inf")),
        1.15: (100000, 150000),
        1.20: (5000, 100000),
        1.30: (1000, 5000),
        1.40: (500, 1000),
        1.50: (100, 500),
        1.60: (50, 100),
        1.90: (10, 50),
        2.10: (7, 10),
        2.30: (-float("inf"), 7)
        }
    for value, price_range in k_values.items():
        if price_range[0] <= price <= price_range[1]:
            k = value
            break

    if stockDays > 90:
        k -= 0.15
    elif stockDays > 60:
        k -= 0.10
    return k

def matrix_opt(stockDays):
    k_values = {
        0.90: [180, 150],
        0.95: [120],
        0.98: [90],
        1.00: [75],
        1.05: [60],
        1.08: [45],
        1.11: [30],
        1.15: [0, float("inf")]
        }
    for value, days in k_values.items():
        if stockDays in days:
            return value

def start_update(api, meta, code, cena, opt, market, extra):
    prices = [cena * 100, opt * 100, market * 100]
    names = ['Цена продажи', 'Опт', 'Маркетплейсы']

    olds = []
    data = api.get_price(meta)
    for k in range(len(names)):
        olds.append(int(float(data['salePrices'][k]['value']/100)))

    attributes = {x['name']: x['value'] for x in data['attributes']}
    extra = int(attributes.get('Доп. наценка (скидка)', 0))
    with shelve.open('extra/extra') as shlv:
        shlv[code] = extra

    for k in range(len(names)):
        if olds[k] != prices[k]:
            api.send_price(prices[k], names[k])

def check_products(api):
    data = api.get_stocks(1, 0)
    size = int(data['meta']['size'])
    k1, k2, add = Sheet().check_table('ИП')
    for k in range(size//1000 + 1):
        data = api.get_stocks(1000, k * 1000)
        for i in range(len(data['rows'])):

            product = data['rows'][i]
            product_id = product['meta']['href'].split('/')[8]

            code = str(product['code'])
            name = str(product['name'])
            stock = int(product['stock'])
            price = round(product['price'] / 100, 2)
            stockDays = math.floor(int(product['stockDays']))

            odds = []
            odds.append(matrix_cena(price, stockDays))
            odds.append(matrix_opt(stockDays))
            odds.append(k1 if price > 5000 else k2)

            # cena = math.ceil(price * k1 + extra)
            # np_opt = math.ceil(price * k2)
            # market = math.ceil(add + (price * k3) + extra)
            #
            # while (cena % 10 != 0):
            #     cena += 1
            # if price > 0:
            #     new = update_ms(meta, code, cena, np_opt, market, extra)
            # time.sleep(2)


if __name__ == '__main__':
    api = MoySkladAPI(api_key=Config.MS_API_KEY, id_store=Config.MS_STORE_ID)
    check_products(api)