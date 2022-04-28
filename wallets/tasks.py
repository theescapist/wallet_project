from models import Currency
import urllib.request, json
from celery import Celery

CURRENCY_URL = "https://www.cbr-xml-daily.ru/daily_json.js"


def currency_sync():
    currencies_list = Currency.objects.all()
    response = urllib.request.urlopen(CURRENCY_URL)
    currency_data = json.loads(response.read().decode())
    for currency in currencies_list:
        if currency.code != 'RUB':
            new_ratio = currency_data['Valute'][currency.code]['Value']
            currency.ratio = new_ratio
            currency.save() #прописать атомарную транзакцию


currency_sync_app = Celery('tasks', broker='redis://guest@localhost//')


@currency_sync_app.task
def get_new_currency():
    currency_sync()
