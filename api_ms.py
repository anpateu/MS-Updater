import requests
import json


class MoySkladAPI:
    def __init__(self, api_key, id_store):
        self.headers = {
            "Authorization": f"Basic {api_key}"
            }
        self.id_store = id_store

    def get_price(self, product_id):
        endpoint = f"https://online.moysklad.ru/api/remap/1.2/entity/product/{product_id}"
        response = requests.get(endpoint, headers=self.headers, data=json.dumps({}))
        return response.json()

    def get_stocks(self, limit, offset):
        store = f"https://online.moysklad.ru/api/remap/1.2/entity/store/{self.id_store}"
        endpoint = (
            "https://online.moysklad.ru/api/remap/1.2/report/stock/all?"
            "quantityMode=positiveOnly&"
            "filter=store={store}&"
            "limit={limit}&"
            "offset={offset}"
        )
        endpoint = endpoint.format(store=store, limit=limit, offset=offset)
        response = requests.get(endpoint, headers=self.headers, data=json.dumps({}))
        return response.json()

    def send_price(self, price, name):
        endpoint = ""
        body_price = {
            "salePrices": [{
                "value": price,
                "priceType": name
                }]
            }
        response = requests.put(endpoint, headers=self.headers, body=json.dumps(body_price))
        return response.json()
