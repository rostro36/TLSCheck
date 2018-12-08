#most interesting part is the method "checkTLS".

import re
import requests
import time
import urllib3

http = urllib3.PoolManager()
#make it look like a Firefox query.
headers = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}


def processMain(mainList):
    #get number of all municipalities
    ALL = getAll(mainList)
    #get every entry of municipality for themselves, first is just start
    entries = re.split('<tr>\n<td', mainList)[1:]
    tlsDict = dict(
    )  #Canton->[Municipality, Canton, TLS, redirect correct, people]
    entryCounter = 0
    for municipality in entries:
        tlsEntry = processEntry(municipality)
        canton = tlsEntry[1]
        if canton in tlsDict:
            tlsDict[canton].append(tlsEntry)
        else:
            tlsDict[canton] = [tlsEntry]
        entryCounter += 1
        if entryCounter % 10 == 0:
            print('Processed ' + str(entryCounter) + ' of ' + str(ALL))
        if entryCounter == 10:
            break
        #I don't want to DoS, so I have to sleep.
        time.sleep(1)
    return tlsDict


def processEntry(municipality):
    """
    data-sort-value="Aadorf"><a href="/wiki/Aadorf" title="Aadorf">Aadorf                       </a>
    </td>
    <td><span style="display:none;">Kanton Thurgau</span><a href="/wiki/Datei:Wappen_Thurgau_matt.svg" class="image" title="Kanton Thurgau"><img alt="Kanton Thurgau" src="//upload.wikimedia.org/wikipedia/commons/thumb/7/71/Wappen_Thurgau_matt.svg/20px-Wappen_Thurgau_matt.svg.png" width="20" height="24" srcset="//upload.wikimedia.org/wikipedia/commons/thumb/7/71/Wappen_Thurgau_matt.svg/30px-Wappen_Thurgau_matt.svg.png 1.5x, //upload.wikimedia.org/wikipedia/commons/thumb/7/71/Wappen_Thurgau_matt.svg/40px-Wappen_Thurgau_matt.svg.png 2x" data-file-width="406" data-file-height="493" /></a>&#160;<a href="/wiki/Kanton_Thurgau" title="Kanton Thurgau">TG</a>
    </td>
    <td style="text-align:right;">4551
    </td>
    <td style="text-align:right;" data-sort-value="8838">8838
    </td>
    <td style="text-align:right;">19,93
    </td>
    <td style="text-align:right;">443,5
    </td></tr>
    <tr>
    <td
    """
    #get CITY
    municipality = re.split('"', municipality, maxsplit=1)[1]
    (CITY, municipality) = re.split('"', municipality, maxsplit=1)
    #get cityWikiLink
    municipality = re.split('href="', municipality, maxsplit=1)[1]
    cityWikiLink = 'https://de.wikipedia.org'
    (CITYLINK, municipality) = re.split('"', municipality, maxsplit=1)
    (TLS, REDIRECT) = checkCity(cityWikiLink + CITYLINK)
    #get Canton
    CANTON = re.split('</a>', municipality)[2][-2:]
    #get PEOPLE
    PEOPLE = ''
    municipality = re.split('data-sort-value="', municipality)[1]
    PEOPLE = re.split('"', municipality)[0]
    PEOPLE = int(PEOPLE)
    return (CITY, CANTON, TLS, REDIRECT, PEOPLE)


#get the cityLink form the cities wikipediasite
def checkCity(cityWikiLink):
    #download cityWikiLink
    try:
        r = http.request('GET', cityWikiLink)  #get the actual site
    except Exception as ex:
        print(ex)
        print('Internet not working')
        quit()
    cityWiki = r.data.decode('UTF-8')
    #city has no link
    if re.search('<td><a rel="nofollow" class="external text" href="',
                 cityWiki) is None:
        print('Municipality has no website: ' + cityWikiLink)
        return (True, True)
    cityWiki = re.split('<td><a rel="nofollow" class="external text" href="',
                        cityWiki)[1]
    cityLink = re.split('"', cityWiki)[0]
    return checkTLS(cityLink)


#checks if the city has a TLS or not.
def checkTLS(cityLink):
    #make sure all start with http-link
    if cityLink[:5] == 'https':
        cityLink = 'http' + cityLink[5:]

    (TLS, responseLink) = testLink(cityLink, True)
    #make responseLink&cityLink https
    if responseLink is not None:
        if not responseLink[:5] == 'https':
            responseLink = 'https' + responseLink[4:]
    if not cityLink[:5] == 'https':
        cityLink = 'https' + cityLink[4:]
    #check if HTTPS exists on https://cityLink or https://responseLink

    REDIRECT = testLink(cityLink, False)[0] or testLink(responseLink, False)[0]
    return (TLS, REDIRECT)


def testLink(cityLink, MODE):  #MODE==False->HTTPS, MODE==True->HTTP
    #no response from http testLink
    if cityLink is None:
        return (False, None)
    try:
        r = requests.get(
            cityLink, headers=headers, timeout=10)  #get the actual site
    except requests.exceptions.SSLError as ex:  #SSL incorrect on serverside
        if MODE:  #there are too many https sites with bad Certs
            print('SSLError: ' + cityLink)
        return (False, None)
    except requests.exceptions.ConnectionError as ex:
        if MODE:  #https doesn't exist
            print('ConnectionError: ' + cityLink)
        return (False, None)
    except requests.exceptions.Timeout as ex:
        print('Timeout: ' + cityLink)
        return (False, None)
    except Exception as ex:
        print(cityLink)
        print(ex)
        print('Internet not working!')
        quit()
    #check if TLS
    responseLink = r.url
    if responseLink[:5] == 'https':
        return (True, responseLink)
    else:
        return (False, responseLink)


def getAll(mainList):
    mainList = re.split('\(BFS\) ', mainList, maxsplit=1)[1]
    ALL = ''
    while mainList[0].isdigit():
        ALL += mainList[0]
        mainList = mainList[1:]
    return int(ALL)
