
import datetime as dt
import os
import filecmp
from OMIEData.Downloaders.MarginalPriceDownloader import MarginalPriceDownloader

########################################################################################################################
def test_1():

    folder = os.path.abspath('OutputTesting')
    reader = MarginalPriceDownloader(output_folder=folder)

    assert reader.getCompleteURL() == \
           'https://www.omie.es/sites/default/files/dados/AGNO_YYYY/MES_MM/TXT/INT_PBC_EV_H_1_DD_MM_YYYY_DD_MM_YYYY.TXT'
########################################################################################################################

########################################################################################################################
def test_2():

    dateIni = dt.datetime(2009, 6, 1)
    dateEnd = dt.datetime(2009, 6, 1)
    folderOut = os.path.abspath('OutputTesting')
    downloader = MarginalPriceDownloader(output_folder=folderOut)

    error = downloader.downloadData(dateIni=dateIni, dateEnd=dateEnd)
    assert error == 0, 'There was an error when downloading.'

    # Check it downloaded with the right name
    outputFileName = 'PMD_20090601.txt'
    assert os.path.isfile(os.path.join(folderOut, outputFileName)), \
        'The downloaded file does not have the expected name.'

    folderIn = os.path.abspath('InputTesting')
    assert filecmp.cmp(os.path.join(folderOut, outputFileName),
                       os.path.join(folderIn, outputFileName),
                       shallow=True), \
        'The content of the downloaded file is not as expected.'

    assert error == 0
########################################################################################################################
