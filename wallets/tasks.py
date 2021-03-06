# from models import Currency
# import urllib.request, json
# from celery.decorators import periodic_task
# from celery.task.schedules import crontab
#
# CURRENCY_URL = "https://www.cbr-xml-daily.ru/daily_json.js"
#
# @periodic_task(run_every=(crontab(days='*/1')), name="currency_sync", ignore_result=True)
# def currency_sync():
#     currencies_list = Currency.objects.all()
#     response = urllib.request.urlopen(CURRENCY_URL)
#     currency_data = json.loads(response.read().decode())
#     for currency in currencies_list:
#         if currency.code != 'RUB':
#             new_ratio = currency_data['Valute'][currency.code]['Value']
#             currency.ratio = new_ratio
#             currency.save()
