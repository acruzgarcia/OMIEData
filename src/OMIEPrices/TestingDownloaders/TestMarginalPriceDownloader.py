
import datetime as dt
import Downloaders.MarginalPriceDownloader as MarginalPriceDownloader

########################################################################################################################
def Test1():

    reader = MarginalPriceDownloader(output_folder='F:\\OMIEPrices\\DataStoreTest\\')

    assert reader.getCompleteURL() == \
           'https://www.omie.es/sites/default/files/dados/AGNO_YYYY/MES_MM/TXT/INT_PBC_EV_H_1_DD_MM_YYYY_DD_MM_YYYY.TXT'
########################################################################################################################


# Unoffical testing ....
if __name__ == '__main__':

    # run the tests, they will fill if they do not pass
    Test1()