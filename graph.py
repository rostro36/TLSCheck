import matplotlib.pyplot as plt
import csv


def graphMain(tlsDict):
    (valuesPlot, valuesKeys) = format(tlsDict)
    plot(valuesPlot, valuesKeys)


def format(tlsDict):
    print('Start formatting.')
    #tlsDict == Canton->[Municipality,canton, TLS, redirect correct, people]
    valuesPlot = dict(
    )  #canton ->[TLSNormal,RedirectNormal,All,TLSPeople,RedirectPeople,AllPeople]
    #setup national
    nationalAll = 0
    nationalPeople = 0
    nationalTLSNormal = 0
    nationalTLSPeople = 0
    nationalRedirectNormal = 0
    nationalRedirectPeople = 0
    with open('municipalities.csv', 'w', newline='') as munFile:
        with open('cantons.csv', 'w', newline='') as canFile:
            munWriter = csv.writer(munFile)
            canWriter = csv.writer(canFile)
            munWriter.writerow([
                'Municipality', 'Canton', 'TLS', 'correct redirect', 'people'
            ])
            canWriter.writerow([
                'Canton', 'TLSNormal', 'RedirectNormal', 'AllNominal',
                'TLSPeople', 'RedirectPeople', 'AllPeople'
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
                        canton]:  #[Municipality,canton,  TLS, redirect correct, people]
                    #count canton
                    All += 1
                    cityPeople = cityRecord[4]
                    AllPeople += cityPeople
                    #write city to municipality csv
                    munWriter.writerow(cityRecord)
                    if cityRecord[3] == True:  #good TLS&redirect
                        RedirectNormal += 1
                        RedirectPeople += cityPeople
                    elif cityRecord[2] == True:  #good TLS&bad redirect
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
                    canton, TLSNormal, RedirectNormal, All, TLSPeople,
                    RedirectPeople, AllPeople
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
    valueAllNormal = [valuesPlot[cantons][2] for cantons in valuesKeys]
    valueTLSNormal = [
        valuesPlot[it][0] * 100 / valueAllNormal[it]
        for it in range(len(valueAllNormal))
    ]
    valueRedirectNormal = [
        valuesPlot[it][1] * 100 / valueAllNormal[it]
        for it in range(len(valueAllNormal))
    ]
    valueNothingNormal = [
        100 - valueRedirectNormal[it] - valueTLSNormal[it]
        for it in range(len(valueAllNormal))
    ]

    #prepare People values, by cantons
    valueAllPeople = [valuesPlot[cantons][5] for cantons in valuesKeys]
    valueTLSPeople = [
        valuesPlot[it][3] * 100 / valueAllPeople[it]
        for it in range(len(valueAllPeople))
    ]
    valueRedirectPeople = [
        valuesPlot[it][4] * 100 / valueAllPeople[it]
        for it in range(len(valueAllPeople))
    ]
    valueNothingNormal = [
        100 - valueRedirectPeople[it] - valueTLSPeople[it]
        for it in range(len(valueAllPeople))
    ]
    #nominal subplot
    plt.subplot(2, 1, 1)
    plt.title('TLS in municipalities nominal')
    plt.ylabel('Cantons')
    plt.xticks([it * 10 for it in range(11)])
    plt.yticks([1.2 * x for x in range(len(valueCantons))], valueCantons)

    #plot in municipalites without TLS, Redirect and those who are good.
    pRedirectN = plt.barh([1.2 * x for x in range(len(valueCantons))],
                          valueRedirectNormal,
                          color='ForestGreen')
    pTLSN = plt.barh([1.2 * x for x in range(len(valueCantons))],
                     valueTLSNormal,
                     left=valueRedirectNormal,
                     color='Gold')
    pNothingN = plt.barh([1.2 * x for x in range(len(valueCantons))],
                         valueNothingNormal,
                         left=[
                             100 - valueNothingNormal[it]
                             for it in range(len(valueNothingNormal))
                         ],
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
                          valueRedirectPeople,
                          color='ForestGreen')
    pTLSP = plt.barh([1.2 * x for x in range(len(valueCantons))],
                     valueTLSPeople,
                     left=valueRedirectPeople,
                     color='Gold')
    pNothingP = plt.barh([1.2 * x for x in range(len(valueCantons))],
                         valueNothingPeople,
                         left=[
                             100 - valueNothingPeople[it]
                             for it in range(len(valueNothingNormal))
                         ],
                         color='Crimson')
    plt.legend((pRedirectP[0], pTLSP[0], pNothingP[0]),
               ('Good', 'bad Redirect', 'Nothing'),
               bbox_to_anchor=(1.04, 0.5),
               loc='center left')
    #save and show
    plt.tight_layout()
    plt.savefig('graphTLS.png', dpi='figure', bbox_inches='tight')
    plt.show()
