
import datetime as dt
import os
import filecmp

from Downloaders.EnergyByTechnologyDownloader import EnergyByTechnologyDownloader
from Downloaders.MarginalPriceDownloader import MarginalPriceDownloader

########################################################################################################################
def Test1():

    folder = os.path.abspath('OutputTesting')
    reader = EnergyByTechnologyDownloader(output_folder=folder)

    assert reader.getCompleteURL() == \
           'https://www.omie.es/sites/default/files/dados/AGNO_YYYY/MES_MM/TXT/INT_PBC_TECNOLOGIAS_H_9_DD_MM_YYYY_DD_MM_YYYY.TXT'
########################################################################################################################

########################################################################################################################
def Test2():

    dateIni = dt.datetime(2020, 11, 13)
    dateEnd = dt.datetime(2020, 11, 13)
    folderOut = os.path.abspath('OutputTesting')
    downloader = EnergyByTechnologyDownloader(output_folder=folderOut)

    error = downloader.downloadData(dateIni=dateIni, dateEnd=dateEnd)
    assert error == 0, 'There was an error when downloading.'

    # Check it downloaded with the right name
    outputFileName = 'EnergyByTechnology_20201113.txt'
    assert os.path.isfile(os.path.join(folderOut, outputFileName)), \
        'The downloaded file does not have the expected name.'

    folderIn = os.path.abspath('InputTesting')
    assert filecmp.cmp(os.path.join(folderOut, outputFileName),
                       os.path.join(folderIn, outputFileName),
                       shallow=True), \
        'The content of the downloaded file is not as expected.'

    assert error == 0
########################################################################################################################

# Unoffical testing ....
if __name__ == '__main__':

    # run the tests, they will fill if they do not pass
    Test1()
    print('Test1() passed.')
    Test2()
    print('Test2() passed.')