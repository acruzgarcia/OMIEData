
import datetime as dt
import os
import filecmp
from OMIEData.Downloaders.marginal_price_downloader import MarginalPriceDownloader


def test_check_url():

    assert MarginalPriceDownloader().get_complete_url() == \
           'https://www.omie.es/sites/default/files/dados/AGNO_YYYY/MES_MM/TXT/INT_PBC_EV_H_1_DD_MM_YYYY_DD_MM_YYYY.TXT'


def test_download_data():

    date_ini = dt.datetime(2009, 6, 1)
    date_end = dt.datetime(2009, 6, 1)

    folder_out = os.path.join(os.path.dirname(__file__), 'OutputTesting')
    error = MarginalPriceDownloader().download_data(date_ini=date_ini, date_end=date_end, output_folder=folder_out)
    assert error == 0, 'There was an error when downloading.'

    # Check it downloaded with the right name
    output_file_name = 'PMD_20090601.txt'
    assert os.path.isfile(os.path.join(folder_out, output_file_name)), \
        'The downloaded file does not have the expected name.'

    folder_in = os.path.join(os.path.dirname(__file__), 'InputTesting')
    assert filecmp.cmp(os.path.join(folder_out, output_file_name),
                       os.path.join(folder_in, output_file_name),
                       shallow=True), \
        'The content of the downloaded file is not as expected.'

    assert error == 0


def test_3():

    date_ini = dt.datetime(2009, 6, 1)
    date_end = dt.datetime(2009, 7, 1)

    for response in MarginalPriceDownloader().url_responses(date_ini=date_ini, date_end=date_end):
        assert response
