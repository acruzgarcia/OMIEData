import datetime as dt
import os
import filecmp
from Downloaders.OfferAndDemandCurveDownloader import OfferAndDemandCurveDownloader

########################################################################################################################
def Test1():

    folder = os.path.abspath('OutputTesting')
    downloader = OfferAndDemandCurveDownloader(hour=1, output_folder=folder)

    assert downloader.getCompleteURL() == \
           'https://www.omie.es/sites/default/files/dados/AGNO_YYYY/MES_MM/TXT/INT_CURVA_ACUM_UO_MIB_1_1_DD_MM_YYYY_DD_MM_YYYY.TXT', \
        'URL mask is not the one expected.'
########################################################################################################################

########################################################################################################################
def Test2():

    dateIni = dt.datetime(2009, 1, 2)
    dateEnd = dt.datetime(2009, 1, 2)
    folderOut = os.path.abspath('OutputTesting')
    downloader = OfferAndDemandCurveDownloader(hour=1, output_folder=folderOut)

    error = downloader.downloadData(dateIni=dateIni, dateEnd=dateEnd)
    assert error == 0, 'There was an error when downloading.'

    # Check it downloaded with the right name
    outputFileName = 'OfferAndDemandCurve_1_20090102.txt'
    assert os.path.isfile(os.path.join(folderOut, outputFileName)), \
        'The downloaded file does not have the expected name.'

    folderIn = os.path.abspath('InputTesting')
    assert filecmp.cmp(os.path.join(folderOut, outputFileName),
                       os.path.join(folderIn, outputFileName),
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