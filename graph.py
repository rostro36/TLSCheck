import matplotlib.pyplot as plt
import csv
import time


def graphMain(tlsDict):
    (valuesPlot, valuesKeys) = format(tlsDict)
    plot(valuesPlot, valuesKeys)


def format(tlsDict):
    print('Start formatting.')
    #tlsDict == Canton->[Municipality,canton, HTTP, HTTPS, people]
    valuesPlot = dict(
    )  #canton ->[TLSNormal,RedirectNormal,All,TLSPeople,RedirectPeople,AllPeople]
    #setup national
    nationalAll = 0
    nationalPeople = 0
    nationalTLSNormal = 0
    nationalTLSPeople = 0
    nationalRedirectNormal = 0
    nationalRedirectPeople = 0
    #get DATE to give csv files a date.
    DATE = time.strftime("%Y-%m-%d")
    munFile = open('municipalities' + DATE + '.csv', 'w', newline='')
    canFile = open('cantons' + DATE + '.csv', 'w', newline='')
    munWriter = csv.writer(munFile)
    canWriter = csv.writer(canFile)
    munWriter.writerow(
        ['Municipality', 'Canton', 'HTTP', 'HTTPS', 'people'])
    canWriter.writerow([
        'Canton', 'HTTPNominal', 'HTTPSNominal', 'AllNominal', 'HTTPPeople',
        'HTTPSPeople', 'AllPeople'
    ])
    for canton in tlsDict:
        #setup canton
        TLSNormal = 0
        RedirectNormal = 0
        All = 0
        TLSPeople = 0  #just TLS
        RedirectPeople = 0  #also correct redirect
        AllPeople = 0
        for cityRecord in tlsDict[
                canton]:  #[Municipality,canton,  HTTP, HTTPS, people]
            #count canton
            All += 1
            cityPeople = cityRecord[4]
            AllPeople += cityPeople
            #write city to municipality csv
            munWriter.writerow(cityRecord)
            if cityRecord[2] == True:  #good TLS&redirect
                RedirectNormal += 1
                RedirectPeople += cityPeople
            elif cityRecord[3] == True:  #good TLS&bad redirect
                TLSNormal += 1
                TLSPeople += cityPeople
            else:
                pass  #they have nothing
        #write values to plotdict
        valuesPlot[canton] = [
            TLSNormal, RedirectNormal, All, TLSPeople, RedirectPeople,
            AllPeople
        ]
        #write to cantons csv
        canWriter.writerow([
            canton, TLSNormal, RedirectNormal, All, TLSPeople, RedirectPeople,
            AllPeople
        ])
        #update national
        nationalAll += All
        nationalPeople += AllPeople
        nationalTLSNormal += TLSNormal
        nationalTLSPeople += TLSPeople
        nationalRedirectNormal += RedirectNormal
        nationalRedirectPeople += RedirectPeople
    #write national in valuesPlot
    valuesPlot['CH'] = [
        nationalTLSNormal, nationalRedirectNormal, nationalAll,
        nationalTLSPeople, nationalRedirectPeople, nationalPeople
    ]
    canWriter.writerow([
        'CH', nationalTLSNormal, nationalRedirectNormal, nationalAll,
        nationalTLSPeople, nationalRedirectPeople, nationalPeople
    ])
    #sort iralphabetical for better reading
    valuesKeys = sorted(valuesPlot, reverse=True)

    return (valuesPlot, valuesKeys)


def plot(valuesPlot, valuesKeys):
    print('Start plotting.')
    #prepare nominal values, sort by cantons, make it percent already
    valueCantons = valuesKeys
    valueAllNormal = {
        cantons: valuesPlot[cantons][2]
        for cantons in valuesKeys
    }
    valueTLSNormal = {
        it: valuesPlot[it][0] * 100 / valueAllNormal[it]
        for it in valueCantons
    }
    valueRedirectNormal = {
        it: valuesPlot[it][1] * 100 / valueAllNormal[it]
        for it in valueCantons
    }
    valueNothingNormal = {
        it: 100 - valueRedirectNormal[it] - valueTLSNormal[it]
        for it in valueCantons
    }

    #prepare People values, by cantons
    valueAllPeople = {
        cantons: valuesPlot[cantons][5]
        for cantons in valuesKeys
    }
    valueTLSPeople = {
        it: valuesPlot[it][3] * 100 / valueAllPeople[it]
        for it in valueCantons
    }
    valueRedirectPeople = {
        it: valuesPlot[it][4] * 100 / valueAllPeople[it]
        for it in valueCantons
    }
    valueNothingPeople = {
        it: 100 - valueRedirectPeople[it] - valueTLSPeople[it]
        for it in valueCantons
    }
    #nominal subplot
    plt.subplot(2, 1, 1)
    plt.title('TLS in municipalities nominal')
    plt.ylabel('Cantons')
    plt.xticks([it * 10 for it in range(11)])
    plt.yticks([1.2 * x for x in range(len(valueCantons))], valueCantons)

    #plot in municipalites without TLS, Redirect and those who are good.
    pRedirectN = plt.barh([1.2 * x for x in range(len(valueCantons))],
                          list(valueRedirectNormal.values()),
                          color='ForestGreen')
    pTLSN = plt.barh([1.2 * x for x in range(len(valueCantons))],
                     list(valueTLSNormal.values()),
                     left=list(valueRedirectNormal.values()),
                     color='Gold')
    pNothingN = plt.barh(
        [1.2 * x for x in range(len(valueCantons))],
        list(valueNothingNormal.values()),
        left=[100 - valueNothingNormal[it] for it in valueNothingNormal],
        color='Crimson')
    plt.legend((pRedirectN[0], pTLSN[0], pNothingN[0]),
               ('Good', 'bad Redirect', 'Nothing'),
               bbox_to_anchor=(1.04, 0.5),
               loc='center left')
    #per capita sub plot
    plt.subplot(2, 1, 2)
    plt.title('TLS in municipalities per capita')
    plt.ylabel('Cantons')
    #make the ticks on the sides/names of cantons
    plt.xticks([it * 10 for it in range(11)])
    plt.yticks([1.2 * x for x in range(len(valueCantons))], valueCantons)

    #plot in municipalites without TLS, Redirect and those who are good.
    pRedirectP = plt.barh([1.2 * x for x in range(len(valueCantons))],
                          list(valueRedirectPeople.values()),
                          color='ForestGreen')
    pTLSP = plt.barh([1.2 * x for x in range(len(valueCantons))],
                     list(valueTLSPeople.values()),
                     left=list(valueRedirectPeople.values()),
                     color='Gold')
    pNothingP = plt.barh(
        [1.2 * x for x in range(len(valueCantons))],
        list(valueNothingPeople.values()),
        left=[100 - valueNothingPeople[it] for it in valueNothingPeople],
        color='Crimson')
    plt.legend((pRedirectP[0], pTLSP[0], pNothingP[0]),
               ('Good', 'bad Redirect', 'Nothing'),
               bbox_to_anchor=(1.04, 0.5),
               loc='center left')
    #save and show
    plt.tight_layout()
    plt.savefig('graphTLS.png', dpi='figure', bbox_inches='tight')
    plt.show()
