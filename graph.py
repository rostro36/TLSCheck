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
            #write national
            valuesPlot['CH'] = [
                nationalTLSNormal, nationalRedirectNormal, nationalAll,
                nationalTLSPeople, nationalRedirectPeople, nationalPeople
            ]
            canWriter.writerow([
                'CH', nationalTLSNormal, nationalRedirectNormal, nationalAll,
                nationalTLSPeople, nationalRedirectPeople, nationalPeople
            ])
    #sort iranalphabetical for better reading
    valuesKeys = sorted(valuesPlot, reverse=True)

    return (valuesPlot, valuesKeys)


def plot(valuesPlot, valuesKeys):
    print('Start plotting.')
    #prepare nominal values, sort by cantons
    valueCantons = valuesKeys
    valueTLSNormal = [valuesPlot[cantons][0] for cantons in valuesKeys]
    valueRedirectNormal = [valuesPlot[cantons][1] for cantons in valuesKeys]
    valueAllNormal = [valuesPlot[cantons][2] for cantons in valuesKeys]
    valueNothingNormal = [
        valueAllNormal[it] - valueRedirectNormal[it] - valueTLSNormal[it]
        for it in range(len(valueAllNormal))
    ]

    #prepare People values, by cantons
    valueTLSPeople = [valuesPlot[cantons][3] for cantons in valuesKeys]
    valueRedirectPeople = [valuesPlot[cantons][4] for cantons in valuesKeys]
    valueAllPeople = [valuesPlot[cantons][5] for cantons in valuesKeys]
    valueNothingPeople = [
        valueAllPeople[it] - valueRedirectPeople[it] - valueTLSPeople[it]
        for it in range(len(valueAllPeople))
    ]
    #nominal subplot
    plt.subplot(2, 1, 1)
    plt.title('TLS in municipalities nominal')
    plt.ylabel('Cantons')
    plt.xticks([it * 10 for it in range(11)])
    plt.yticks(range(len(valueCantons)), valueCantons)
    pRedirectN = plt.barh(
        range(len(valueCantons)), [
            valueRedirectNormal[it] * 100 / valueAllNormal[it]
            for it in range(len(valueAllNormal))
        ],
        color='ForestGreen')
    pTLSN = plt.barh(
        range(len(valueCantons)), [
            valueTLSNormal[it] * 100 / valueAllNormal[it]
            for it in range(len(valueAllNormal))
        ],
        left=[
            valueRedirectNormal[it] * 100 / valueAllNormal[it]
            for it in range(len(valueRedirectNormal))
        ],
        color='Gold')
    pNothingN = plt.barh(
        range(len(valueCantons)), [
            valueNothingNormal[it] * 100 / valueAllNormal[it]
            for it in range(len(valueAllNormal))
        ],
        left=[
            100 - (valueNothingNormal[it] * 100 / valueAllNormal[it])
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
    plt.xticks([it * 10 for it in range(11)])
    plt.yticks(range(len(valueCantons)), valueCantons)

    pRedirectP = plt.barh(
        range(len(valueCantons)), [
            valueRedirectPeople[it] * 100 / valueAllPeople[it]
            for it in range(len(valueAllPeople))
        ],
        color='ForestGreen')
    pTLSP = plt.barh(
        range(len(valueCantons)), [
            valueTLSPeople[it] * 100 / valueAllPeople[it]
            for it in range(len(valueAllPeople))
        ],
        left=[
            valueRedirectPeople[it] * 100 / valueAllPeople[it]
            for it in range(len(valueRedirectPeople))
        ],
        color='Gold')
    pNothingP = plt.barh(
        range(len(valueCantons)), [
            valueNothingPeople[it] * 100 / valueAllPeople[it]
            for it in range(len(valueAllPeople))
        ],
        left=[
            100 - (valueNothingPeople[it] * 100 / valueAllPeople[it])
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
