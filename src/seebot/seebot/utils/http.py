import requests
import json

class httpUtil:
    def post(url, param=None, headers=None):
        if headers is None:
            headers = {}
        headers.setdefault("Content-Type", "application/json")
        res = requests.post(url=url, data=json.dumps(param), headers=headers)
        return res

    def get(url, headers=None):
        if headers is None:
            headers = {}
        res = requests.get(url=url, headers=headers)
        return res