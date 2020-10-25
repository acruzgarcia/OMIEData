
import datetime as dt
from Downloaders.GeneralOMIEDownloader import GeneralOMIEDownloader
import os

########################################################################################################################
def Test1():

    # Testing PMDs
    url_ano = 'AGNO_YYYY'
    url_mes = '/MES_MM/TXT/'
    url_name = 'INT_PBC_EV_H_1_DD_MM_YYYY_DD_MM_YYYY.TXT'

    folder = os.path.abspath('OutputTesting')
    url1 = url_ano + url_mes + url_name
    downloader = GeneralOMIEDownloader(url_mask=url1,
                                       output_folder=folder,
                                       output_mask='PMD_YYYYMMDD.txt')

    assert downloader.getCompleteURL() == \
           'https://www.omie.es/sites/default/files/dados/AGNO_YYYY/MES_MM/TXT/INT_PBC_EV_H_1_DD_MM_YYYY_DD_MM_YYYY.TXT'
########################################################################################################################

########################################################################################################################
def Test2():

    # Testing
    url_ano = 'AGNO_YYYY'
    url_mes = '/MES_MM/TXT/'
    url_name = 'INT_PBC_EV_H_1_DD_MM_YYYY_DD_MM_YYYY.TXT'

    url1 = url_ano + url_mes + url_name
    folder = os.path.abspath('OutputTesting')
    downloader = GeneralOMIEDownloader(url_mask=url1,
                                       output_folder=folder,
                                       output_mask='PMD_YYYYMMDD.txt')

    dateIni = dt.datetime(2006,1,1)
    dateEnd = dt.datetime(2006,1,31)
    error = downloader.downloadData(dateIni=dateIni, dateEnd=dateEnd)

    assert error == 0
########################################################################################################################

# Unoffical testing ....
if __name__ == '__main__':

    # run the tests, they will fill if they do not pass
    Test1()
    print('Test1() passed.')
    Test2()
    print('Test2() passed.')