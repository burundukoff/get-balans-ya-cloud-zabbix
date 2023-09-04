#!/usr/bin/env -S python3 -u
import requests
from sys import argv

url_iam = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
url_balans ='https://billing.api.cloud.yandex.net/billing/v1/billingAccounts' 
iam_token = ''


def get_iam(url_iam, api_token):
    param = {'yandexPassportOauthToken':api_token}
    response = requests.post(url_iam, json=param)
    if response.status_code == 200:
        json_response = response.json()
        iam_token = json_response.get('iamToken')
        return iam_token
    else:
        return response.status_code
    
def get_balans(url_balans, iam_token):
    headers = {'Authorization': f"Bearer {iam_token}"}
    response = requests.get(url_balans, headers=headers)
    if response.status_code == 200:
        json_response = response.json()
        balance = json_response.get('billingAccounts')
        balance = round(float(balance[0].get('balance')))
        return balance
    else:
        return response.status_code

if len(argv) <= 1:
    print('required parameters are missing')
else:
    api_token  = argv[1]
    iam_token = get_iam(url_iam, api_token)
    balans = get_balans(url_balans, iam_token)
    print(balans)

