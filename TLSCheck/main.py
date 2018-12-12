import urllib3
from textprocess import processMain
from graph import graphMain

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#Download MainList with all municipalities
wiki = 'https://de.wikipedia.org/wiki/Liste_Schweizer_Gemeinden'
http = urllib3.PoolManager()
print('Start')
try:
    r = http.request('GET', wiki)  #get the actual site
except Exception as ex:
    print(ex)
    print('Internet not working.')
    quit()
mainList = r.data.decode('UTF-8')
print('Start processing')
tlsDict = processMain(
    mainList)  #Canton->[Municipality, TLS, redirect correct, people]
print('Start graphing')
graphMain(tlsDict)
print('Done')
