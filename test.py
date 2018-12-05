import urllib3
import requests

headers = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}
wiki = 'https://www.' + 'aarau' + '.ch/'
print('spu')
try:
    r = requests.get(wiki, headers=headers, timeout=10)  #get the actual site
except requests.exceptions.SSLError as ex:
    print('SSLError')
    r = requests.Response(url='123')
except requests.exceptions.Timeout as ex:
    print(ex)
    r = requests.Response()
    r.url = wiki
except requests.exceptions.ConnectionError() as ex:
    print('ayoo')
    print(ex)
    quit()
except Exception as ex:
    print(ex)
    quit()
print(r.url)
print('done')

cityLink = 'http://www.stadt-zuerich.ch/portal'
if cityLink[:5] == 'https':
    cityLink = 'http' + cityLink[5:]
print(cityLink)
