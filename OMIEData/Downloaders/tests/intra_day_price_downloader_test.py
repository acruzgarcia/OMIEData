
import datetime as dt
import os
import filecmp
from OMIEData.Downloaders.intra_day_price_downloader import IntraDayPriceDownloader


def test_1():

    assert IntraDayPriceDownloader(session=2).get_complete_url() == \
           'https://www.omie.es/sites/default/files/dados/AGNO_YYYY/MES_MM/TXT/INT_PIB_EV_H_1_2_DD_MM_YYYY_DD_MM_YYYY.TXT', \
        'URL mask is not the one expected.'


def test_2():

    date_ini = dt.datetime(2009, 1, 3)
    date_end = dt.datetime(2009, 1, 3)
    downloader = IntraDayPriceDownloader(session=2)

    folder_out = os.path.abspath('OutputTesting')
    error = downloader.download_data(date_ini=date_ini, date_end=date_end, output_folder=folder_out)
    assert error == 0, 'There was an error when downloading.'

    # Check it downloaded with the right name
    output_file_name = 'PrecioIntra_2_20090103.txt'
    assert os.path.isfile(os.path.join(folder_out, output_file_name)), \
        'The downloaded file does not have the expected name.'

    folder_in = os.path.abspath('InputTesting')
    assert filecmp.cmp(os.path.join(folder_out, output_file_name),
                       os.path.join(folder_in, output_file_name),
                       shallow=True), \
        'The content of the downloaded file is not as expected.'
