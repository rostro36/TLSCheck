# TLSCheck for Swiss municipality websites.
### Prerequisites
The Checker is written in Python 3 and uses the [requests library](http://docs.python-requests.org/en/master/ "requests") for checking the websites and the [matplotlib library ](https://matplotlib.org/ "matplotlib")to draw the graph.
### Input
This program takes the links to municipial websites of Switzerland from [wikipedia](https://de.wikipedia.org/wiki/Liste_Schweizer_Gemeinden "wikipedia") and checks if they use TLS.
### Output
The checker puts out two .csv-files.
One named municipalities(DATE).csv, which contains every municipality/city and a record for it.
The record looks like this:
Municipality,Canton,TLS,correct redirect,people
The other is named cantons(DATE).csv.
The record looks like this:
Canton,TLSNormal,RedirectNormal,AllNominal,TLSPeople,RedirectPeople,AllPeople
It also puts out an image where the values for each canton are plotted out.
