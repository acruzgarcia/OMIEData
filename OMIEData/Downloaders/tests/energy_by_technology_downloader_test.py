
import datetime as dt
import os
import filecmp

from OMIEData.Downloaders.energy_by_technology_downloader import EnergyByTechnologyDownloader
from OMIEData.Downloaders.energy_by_technology_downloader import SystemType


def test_1():

    folder = os.path.abspath('OutputTesting')
    downloader = EnergyByTechnologyDownloader(system=SystemType.IBERIAN)

    assert downloader.get_complete_url() == \
           'https://www.omie.es/sites/default/files/dados/AGNO_YYYY/MES_MM/TXT/INT_PBC_TECNOLOGIAS_H_9_DD_MM_YYYY_DD_MM_YYYY.TXT', \
        'URL mask is not the one expected.'


def test_2():

    dateIni = dt.datetime(2020, 11, 13)
    dateEnd = dt.datetime(2020, 11, 13)
    folderOut = os.path.abspath('OutputTesting')
    # System 1= Spain 2= Portugal 9= Iberian Market
    downloader = EnergyByTechnologyDownloader(system=SystemType.IBERIAN)

    error = downloader.download_data(date_ini=dateIni, date_end=dateEnd, output_folder=folderOut)
    assert error == 0, 'There was an error when downloading.'

    # Check it downloaded with the right name
    output_file_name = 'EnergyByTechnology_9_20201113.txt'
    assert os.path.isfile(os.path.join(folderOut, output_file_name)), \
        'The downloaded file does not have the expected name.'

    folder_in = os.path.abspath('InputTesting')
    assert filecmp.cmp(os.path.join(folderOut, output_file_name),
                       os.path.join(folder_in, output_file_name),
                       shallow=True), \
        'The content of the downloaded file is not as expected.'

    assert error == 0
