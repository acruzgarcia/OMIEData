import datetime as dt
import os
import filecmp
from OMIEData.Downloaders.adjustment_price_downloader import AdjustmentPriceDownloader


def test_check_url():
    assert (
        AdjustmentPriceDownloader().get_complete_url()
        == "https://www.omie.es/sites/default/files/dados/AGNO_YYYY/MES_MM/TXT/INT_MAJ_EV_H_DD_MM_YYYY_DD_MM_YYYY.TXT"
    )


def test_download_data():
    date_ini = dt.datetime(2022, 10, 30)
    date_end = dt.datetime(2022, 10, 30)

    folder_out = os.path.join(os.path.dirname(__file__), "OutputTesting")
    error = AdjustmentPriceDownloader().download_data(
        date_ini=date_ini, date_end=date_end, output_folder=folder_out
    )
    assert error == 0, "There was an error when downloading."

    # Check it downloaded with the right name
    output_file_name = "PMD_20221030.txt"
    assert os.path.isfile(
        os.path.join(folder_out, output_file_name)
    ), "The downloaded file does not have the expected name."

    folder_in = os.path.join(os.path.dirname(__file__), "InputTesting")
    assert filecmp.cmp(
        os.path.join(folder_out, output_file_name),
        os.path.join(folder_in, output_file_name),
        shallow=True,
    ), "The content of the downloaded file is not as expected."

    assert error == 0


def test_3():
    date_ini = dt.datetime(2022, 10, 30)
    date_end = dt.datetime(2022, 10, 31)

    for response in AdjustmentPriceDownloader().url_responses(
        date_ini=date_ini, date_end=date_end
    ):
        assert response


def run_all_tests():
    import warnings

    test_functions = [test_check_url, test_download_data, test_3]
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=FutureWarning)
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        for test_func in test_functions:
            try:
                test_func()
            except (AssertionError, UnicodeDecodeError, TypeError, IndexError) as e:
                print(f"{test_func.__name__} failed: {e}")
                raise e


if __name__ == "__main__":
    run_all_tests()
