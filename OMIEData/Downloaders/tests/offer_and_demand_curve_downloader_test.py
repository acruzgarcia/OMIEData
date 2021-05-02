import datetime as dt
import os
import filecmp
from OMIEData.Downloaders.offer_and_demand_curve_downloader import OfferAndDemandCurveDownloader


def test_1():

    assert OfferAndDemandCurveDownloader(hour=1).get_complete_url() == \
           'https://www.omie.es/sites/default/files/dados/AGNO_YYYY/MES_MM/TXT/INT_CURVA_ACUM_UO_MIB_1_1_DD_MM_YYYY_DD_MM_YYYY.TXT', \
        'URL mask is not the one expected.'


def test_2():

    date_ini = dt.datetime(2009, 1, 2)
    date_end = dt.datetime(2009, 1, 2)

    folder_out = os.path.abspath('OutputTesting')
    error = OfferAndDemandCurveDownloader(hour=1).download_data(date_ini=date_ini,
                                                                date_end=date_end,
                                                                output_folder=folder_out)
    assert error == 0, 'There was an error when downloading.'

    # Check it downloaded with the right name
    output_file_name = 'OfferAndDemandCurve_1_20090102.txt'
    assert os.path.isfile(os.path.join(folder_out, output_file_name)), \
        'The downloaded file does not have the expected name.'

    folder_in = os.path.abspath('InputTesting')
    assert filecmp.cmp(os.path.join(folder_out, output_file_name),
                       os.path.join(folder_in, output_file_name),
                       shallow=True), \
        'The content of the downloaded file is not as expected.'
