import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()


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
        # TODO: tlsDict.append(tlsEntry)
        canton = tlsEntry[1]
        if canton in tlsDict:
            tlsDict[canton].append(tlsEntry)
        else:
            tlsDict[canton] = [tlsEntry]
        entryCounter += 1
        if entryCounter % 10 == 0:
            print('Processed ' + str(entryCounter) + ' of ' + str(ALL))
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


def checkCity(cityWikiLink):
    #download cityWikiLink
    try:
        r = http.request('GET', cityWikiLink)  #get the actual site
    except Exception as ex:
        print(ex)
        print('Internet not working')
        quit()
    cityWiki = r.data.decode('UTF-8')
    cityWiki = re.split('"nofollow" class="external text" href="', cityWiki)[1]
    cityLink = re.split('"', cityWiki)[0]
    return checkTLS(cityLink)


def checkTLS(cityLink):
    try:
        r = http.request('GET', cityLink)  #get the actual site
    except Exception as ex:
        print(ex)
        print('Internet not working!')
        quit()
    if r.geturl()[:5] == 'https':
        return (True, True)  #uses TLS and redirects correctly
    else:  #maybe just wrongly directed
        cityLink = 'https' + r.geturl()[5:]
        try:
            r = http.request('GET', cityLink)  #get the actual site
        except Exception as ex:
            #https doesnt exist
            return (False, False)
        return (True, False)


def getAll(mainList):
    mainList = re.split('\(BFS\) ', mainList, maxsplit=1)[1]
    ALL = ''
    while mainList[0].isdigit():
        ALL += mainList[0]
        mainList = mainList[1:]
    return int(ALL)
