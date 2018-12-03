import urllib3
import requests

#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
retries = urllib3.Retry(connect=1000, read=1000, redirect=1000)
headers = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}
http = urllib3.PoolManager(retries=retries)
wiki = 'www.fiesch.com/'
print('spu')
try:
    r = http.request('GET', wiki)  #get the actual site
except requests.exceptions.SSLError as ex:
    print('fu arosa')
    r = requests.Response(url='123')
    r.url
except Exception as ex:
    print(ex)
print(r.geturl())
print('done')
