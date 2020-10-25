
import datetime as dt
from Downloaders.MarginalPriceDownloader import MarginalPriceDownloader

########################################################################################################################
def Test1():

    reader = MarginalPriceDownloader(output_folder='F:\\OMIEPrices\\DataStoreTest\\')

    assert reader.getCompleteURL() == \
           'https://www.omie.es/sites/default/files/dados/AGNO_YYYY/MES_MM/TXT/INT_PBC_EV_H_1_DD_MM_YYYY_DD_MM_YYYY.TXT'
########################################################################################################################

########################################################################################################################
def Test2():

    dateIni = dt.datetime(2009, 1, 1)
    dateEnd = dt.datetime(2009, 1, 2)
    downloader = MarginalPriceDownloader(output_folder='F:\\OMIEPrices\\DataStoreTest\\')

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