
import datetime as dt
import os
import filecmp

from Downloaders.EnergyByTechnologyDownloader import EnergyByTechnologyDownloader
from Downloaders.EnergyByTechnologyDownloader import SystemType

########################################################################################################################
def test_1():

    folder = os.path.abspath('OutputTesting')
    downloader = EnergyByTechnologyDownloader(system=SystemType.IBERIAN, output_folder=folder)

    assert downloader.getCompleteURL() == \
           'https://www.omie.es/sites/default/files/dados/AGNO_YYYY/MES_MM/TXT/INT_PBC_TECNOLOGIAS_H_9_DD_MM_YYYY_DD_MM_YYYY.TXT', \
        'URL mask is not the one expected.'

########################################################################################################################

########################################################################################################################
def test_2():

    dateIni = dt.datetime(2020, 11, 13)
    dateEnd = dt.datetime(2020, 11, 13)
    folderOut = os.path.abspath('OutputTesting')
    # System 1= Spain 2= Portugal 9= Iberian Market
    downloader = EnergyByTechnologyDownloader(system=SystemType.IBERIAN, output_folder=folderOut)

    error = downloader.downloadData(dateIni=dateIni, dateEnd=dateEnd)
    assert error == 0, 'There was an error when downloading.'

    # Check it downloaded with the right name
    outputFileName = 'EnergyByTechnology_9_20201113.txt'
    assert os.path.isfile(os.path.join(folderOut, outputFileName)), \
        'The downloaded file does not have the expected name.'

    folderIn = os.path.abspath('InputTesting')
    assert filecmp.cmp(os.path.join(folderOut, outputFileName),
                       os.path.join(folderIn, outputFileName),
                       shallow=True), \
        'The content of the downloaded file is not as expected.'

    assert error == 0
########################################################################################################################
