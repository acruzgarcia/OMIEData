
import datetime as dt
from OMIEData.Downloaders.general_omie_downloader import GeneralOMIEDownloader
import os
import filecmp


def test_1():

    # Testing PMDs
    url_ano = 'AGNO_YYYY'
    url_mes = '/MES_MM/TXT/'
    url_name = 'INT_PBC_EV_H_1_DD_MM_YYYY_DD_MM_YYYY.TXT'

    url1 = url_ano + url_mes + url_name
    downloader = GeneralOMIEDownloader(url_mask=url1,
                                       output_mask='PMD_YYYYMMDD.txt')

    assert downloader.get_complete_url() == \
           'https://www.omie.es/sites/default/files/dados/AGNO_YYYY/MES_MM/TXT/INT_PBC_EV_H_1_DD_MM_YYYY_DD_MM_YYYY.TXT', \
        'URL mask is not the one expected.'


def test_2():

    # This test is insufficient
    # We need to download the file independently

    # Testing
    url_ano = 'AGNO_YYYY'
    url_mes = '/MES_MM/TXT/'
    url_name = 'INT_PBC_EV_H_1_DD_MM_YYYY_DD_MM_YYYY.TXT'

    url1 = url_ano + url_mes + url_name

    downloader = GeneralOMIEDownloader(url_mask=url1,
                                       output_mask='PMD_YYYYMMDD.txt')

    date_ini = dt.datetime(2006, 1, 1)
    date_end = dt.datetime(2006, 1, 1)

    folder_out = os.path.join(os.path.dirname(__file__), 'OutputTesting')
    error = downloader.download_data(date_ini=date_ini, date_end=date_end, output_folder=folder_out)
    assert error == 0, 'There was an error when downloading.'

    # Check it downloaded with the right name
    assert os.path.isfile(os.path.join(folder_out, 'PMD_20060101.txt')),\
        'The downloaded file does not have the expected name.'

    folder_in = os.path.join(os.path.dirname(__file__), 'InputTesting')
    assert filecmp.cmp(os.path.join(folder_out, 'PMD_20060101.txt'),
                       os.path.join(folder_in, 'PMD_20060101.txt'),
                       shallow=True), \
        'The content of the downloaded file is not as expected.'
