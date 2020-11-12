
import datetime as dt
from Downloaders.GeneralOMIEDownloader import GeneralOMIEDownloader
import os
import filecmp

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
           'https://www.omie.es/sites/default/files/dados/AGNO_YYYY/MES_MM/TXT/INT_PBC_EV_H_1_DD_MM_YYYY_DD_MM_YYYY.TXT', \
        'URL mask is not the one expected.'
########################################################################################################################

########################################################################################################################
def Test2():

    # This test is insufficient
    # We need to download the file independently

    # Testing
    url_ano = 'AGNO_YYYY'
    url_mes = '/MES_MM/TXT/'
    url_name = 'INT_PBC_EV_H_1_DD_MM_YYYY_DD_MM_YYYY.TXT'

    url1 = url_ano + url_mes + url_name
    folderOut = os.path.abspath('OutputTesting')
    downloader = GeneralOMIEDownloader(url_mask=url1,
                                       output_folder=folderOut,
                                       output_mask='PMD_YYYYMMDD.txt')

    dateIni = dt.datetime(2006,1,1)
    dateEnd = dt.datetime(2006,1,1)

    error = downloader.downloadData(dateIni=dateIni, dateEnd=dateEnd)
    assert error == 0, 'There was an error when downloading.'

    # Check it downloaded with the right name
    assert os.path.isfile(os.path.join(folderOut, 'PMD_20060301.txt')),\
        'The downloaded file does not have the expected name.'

    folderIn = os.path.abspath('InputTesting')
    assert filecmp.cmp(os.path.join(folderOut,'PMD_20060101.txt'),
                       os.path.join(folderIn,'PMD_20060101.txt'),
                       shallow=True), \
        'The content of the downloaded file is not as expected.'

########################################################################################################################

# Unoffical testing ....
if __name__ == '__main__':

    # run the tests, they will fill if they do not pass
    Test1()
    print('Test1() passed.')
    Test2()
    print('Test2() passed.')