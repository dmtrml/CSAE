import requests
from requests.auth import HTTPBasicAuth
import time

headers = {
'Device-Id': 'noneOrRealId',
'Device-OS': 'Adnroid 5.1',
'Version': '2',
'ClientVersion': '1.4.4.1',
'Host': 'proverkacheka.nalog.ru:9999',
'Connection': 'Keep-Alive',
'User-Agent': 'okhttp/3.0.1'

}

s = requests.Session()
#r = s.post('https://proverkacheka.nalog.ru:9999/v1/mobile/users/login', auth=HTTPBasicAuth('+79776494088', '181218'))
x = requests.get('https://proverkacheka.nalog.ru:9999/v1/inns/*/kkts/*/fss/9289000100022002/tickets/46853?fiscalSign=2408338133&sendToEmail=no', auth=HTTPBasicAuth('+79776494088', '181218'), headers=headers)
#time.sleep(2)
#y = requests.get('https://proverkacheka.nalog.ru:9999/v1/inns/*/kkts/*/fss/9289000100022002/tickets/46853?fiscalSign=2408338133&sendToEmail=no', auth=HTTPBasicAuth('+79776494088', '181218'), headers=headers)
#result = requests.get('https://proverkacheka.nalog.ru:9999/v1/mobile/users/login')


#r = s.post('https://proverkacheka.nalog.ru:9999/v1/mobile/users/login', data={'phone':'+79776494088', 'password':'181218'})
#r = s.get('https://dnevnik.ru/user')
x_json = x.json()
items = x_json['document']['receipt']['items']
print(items)
#print(y.text)