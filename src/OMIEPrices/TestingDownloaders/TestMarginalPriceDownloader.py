
import datetime as dt
import os
from Downloaders.MarginalPriceDownloader import MarginalPriceDownloader

########################################################################################################################
def Test1():

    folder = os.path.abspath('OutputTesting')
    reader = MarginalPriceDownloader(output_folder=folder)

    assert reader.getCompleteURL() == \
           'https://www.omie.es/sites/default/files/dados/AGNO_YYYY/MES_MM/TXT/INT_PBC_EV_H_1_DD_MM_YYYY_DD_MM_YYYY.TXT'
########################################################################################################################

########################################################################################################################
def Test2():

    dateIni = dt.datetime(2009, 1, 1)
    dateEnd = dt.datetime(2009, 1, 2)
    folder = os.path.abspath('OutputTesting')
    downloader = MarginalPriceDownloader(output_folder=folder)

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