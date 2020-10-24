# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests as req
import datetime as dt

url1= 'https://www.omie.es/sites/default/files/dados/'
url_ano = 'AGNO_YYYY'
url_mes = '/MES_MM/TXT/'
url_name = 'INT_PBC_EV_H_1_DD_MM_YYYY_DD_MM_YYYY.TXT'

rootfolder = 'F:\\OMIEPrices\\'
storefolder = 'DataStoreTest\\PreciosMD\\'
outputfilename = rootfolder + storefolder + 'PrecioMD_OMIE_YYYYMMDD.txt'

url_total = url1 + url_ano + url_mes + url_name

dateIni = dt.datetime(2003,1,1)
dateend = dt.datetime(2004,12,31)

dtaux = dateIni
while (dtaux <= dateend):

    dd = f'{dtaux.day:02}'
    mm = f'{dtaux.month:02}'
    yyyy = f'{dtaux.year:04}'

    urlaux = url_total
    urlaux = urlaux.replace('DD', dd)
    urlaux = urlaux.replace('MM', mm)
    urlaux = urlaux.replace('YYYY', yyyy)

    print('Downloading ' + urlaux + ' ...')
    request = req.get(urlaux, allow_redirects=True)
    fileaux = outputfilename
    fileaux = fileaux.replace('DD', dd)
    fileaux = fileaux.replace('MM', mm)
    fileaux = fileaux.replace('YYYY', yyyy)
    f = open(fileaux, 'wb').write(request.content)

    dtaux = dtaux + dt.timedelta(days=+1)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Do nothing






