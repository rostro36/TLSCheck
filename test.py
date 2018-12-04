import urllib3
import requests

#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
retries = urllib3.Retry(connect=1000, read=1000, redirect=1000)
headers = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}
http = urllib3.PoolManager(retries=retries)
wiki = 'http://www.fiesch.com/'
print('spu')
try:
    r = requests.get(wiki, headers=headers, timeout=10)  #get the actual site
except requests.exceptions.SSLError as ex:
    print('fu arosa')
    r = requests.Response(url='123')
except requests.exceptions.Timeout as ex:
    print(ex)
    r = requests.Response()
    r.url = wiki
except Exception as ex:
    print(ex)
print(r.url)
print('done')
