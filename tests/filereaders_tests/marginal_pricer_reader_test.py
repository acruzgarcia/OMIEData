import datetime as dt
import numpy as np
import os

from OMIEData.FileReaders.marginal_price_file_reader import MarginalPriceFileReader
from OMIEData.DataImport.omie_data_importer_from_folder import (
    OMIEDataImporterFromFolder,
)
from OMIEData.Enums.all_enums import DataTypeInMarginalPriceFile
import pandas as pd


def is_equal_float(x1: float, x2: float, tolerance=1e-4):
    return np.abs(x1 - x2) < tolerance


def test_all_keys_in_df():
    folder = os.path.join(os.path.dirname(__file__), "InputTesting")
    filename = os.path.join(folder, "PMD_20060101.txt")

    reader = MarginalPriceFileReader()
    keys = reader.get_keys()
    df = reader.get_data_from_file(filename=filename)

    # data is list of dictionaries
    columns = df.columns.to_list()
    for k in keys:
        assert k in columns, "Key: " + k + " not found."


def test_check_correct_values():
    folder = os.path.join(os.path.dirname(__file__), "InputTesting")
    filename = os.path.join(folder, "PMD_20060101.txt")

    # File contains
    #'Precio marginal (Cent/kWh);  6,694;  4,888;  4,525;  4,371;  3,870;  3,777;  3,611;  1,000;  0,500;  1,000;  1,000;\
    #  1,954;  3,755;  3,777;  3,777;  3,755;  3,755;  3,755;  4,788;  5,600;  6,725;  7,001;  6,637;  7,617;
    #' Energía en el programa resultante de la casación (MWh);  26.377;  26.070;  24.916;  23.761;  22.814;  22.116;  \
    # 21.415;  20.712;  19.438;  19.699;  20.583;  21.119;  21.741;  22.264;  22.359;  21.763;  21.463;  21.610;  23.872;\
    #  24.322;  24.993;  25.064;  24.792;  25.373;'

    data = MarginalPriceFileReader().get_data_from_file(filename=filename)

    assert is_equal_float(
        data.iloc[0]["H7"], 36.11, tolerance=1e-3
    ), "Data is corrupted"
    assert is_equal_float(
        data.iloc[1]["H9"], 19438, tolerance=1e-3
    ), "Data is corrupted"


def test_dump_to_dataframe(verbose=False):
    folder = os.path.join(os.path.dirname(__file__), "InputTesting")
    file_reader = MarginalPriceFileReader()
    dumper = OMIEDataImporterFromFolder(absolute_path=folder, file_reader=file_reader)
    df = dumper.read_to_dataframe()

    # show dataframe
    if verbose:
        print(df)

    # 2006-1-1 file
    value = float(
        df.loc[
            (df.DATE == dt.date(2006, 1, 1))
            & (df.CONCEPT == str(DataTypeInMarginalPriceFile.PRICE_SPAIN)),
            "H1",
        ]
    )
    assert is_equal_float(value, 66.94, tolerance=1e-6), "Data is corrupt"

    value = float(
        df.loc[
            (df.DATE == dt.date(2006, 1, 1))
            & (df.CONCEPT == str(DataTypeInMarginalPriceFile.ENERGY_IBERIAN)),
            "H23",
        ]
    )
    assert is_equal_float(value, 24792, tolerance=1e-6), "Data is corrupt"

    # 2009-6-1 file
    value = float(
        df.loc[
            (df.DATE == dt.date(2009, 6, 1))
            & (df.CONCEPT == str(DataTypeInMarginalPriceFile.PRICE_PORTUGAL)),
            "H2",
        ]
    )
    assert is_equal_float(value, 37.60, tolerance=1e-6), "Data is corrupt"

    slice = df.loc[
        (df.DATE == dt.date(2009, 6, 1))
        & (df.CONCEPT == str(DataTypeInMarginalPriceFile.ENERGY_IBERIAN)),
        :,
    ]
    energies = {
        "H1": 28325.8,
        "H2": 26201.2,
        "H3": 24651.6,
        "H4": 23788.6,
        "H5": 23565.4,
        "H6": 24149.6,
        "H7": 26386.0,
        "H8": 29016.5,
        "H9": 33149.4,
        "H10": 36289.9,
        "H11": 38527.1,
        "H12": 39362.9,
        "H13": 40102.1,
        "H14": 39556.3,
        "H15": 37944.9,
        "H16": 37503.3,
        "H17": 37355.8,
        "H18": 37310.8,
        "H19": 36740.7,
        "H20": 36079.6,
        "H21": 36029.6,
        "H22": 37617.5,
        "H23": 37147.9,
        "H24": 33897.1,
    }
    for k, v in energies.items():
        assert is_equal_float(v, float(slice.get(k)), tolerance=1e-6), "Data is corrupt"

    # 2020-10-22 file
    slice = df.loc[
        (df.DATE == dt.date(2020, 10, 22))
        & (
            df.CONCEPT
            == str(DataTypeInMarginalPriceFile.ENERGY_IBERIAN_WITH_BILLATERAL)
        ),
        :,
    ]
    energies = [
        29435.7,
        27853.8,
        27293.8,
        26948.5,
        26871.7,
        27047.6,
        28605.8,
        31899.4,
        33804.2,
        35118.1,
        35916.7,
        36518.3,
        37036.5,
        37006.9,
        36251.2,
        35312.6,
        34689.7,
        34358.7,
        33956.2,
        35138.1,
        37878.5,
        36955.3,
        33874.5,
        30856.7,
    ]
    for i, v in enumerate(energies):
        assert is_equal_float(
            energies[i], float(slice.get("H" + f"{i + 1:01}")), tolerance=1e-6
        ), "Data is corrupt"

    slice = df.loc[
        (df.DATE == dt.date(2020, 10, 22))
        & (df.CONCEPT == str(DataTypeInMarginalPriceFile.PRICE_SPAIN)),
        :,
    ]
    prices = [
        39.55,
        35.00,
        33.07,
        32.68,
        32.68,
        33.08,
        40.11,
        47.13,
        49.53,
        52.49,
        52.43,
        50.44,
        49.08,
        47.50,
        46.58,
        45.95,
        46.11,
        48.49,
        50.68,
        56.63,
        53.56,
        49.04,
        47.20,
        46.30,
    ]
    for i, v in enumerate(prices):
        assert is_equal_float(
            prices[i], float(slice.get("H" + f"{i + 1:01}")), tolerance=1e-6
        ), "Data is corrupt"


def test_day_with_23_hours():
    folder = os.path.join(os.path.dirname(__file__), "InputTesting")
    filename = os.path.join(folder, "PrecioMD_OMIE_20200329.txt")

    # File contains
    #';1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20;21;22;23;
    # Precio marginal (Cent/kWh);  2,002;  1,762;  1,562;  1,527;  1,482;  1,475;  1,762;  2,149;  4,167;  4,340;  \
    # 4,276;  4,276;  3,500;  3,585;  3,200;  3,300;  3,400;  2,192;  3,300;  5,000;  4,426;  4,197;  3,673;  4,340;
    # Demanda+bombeos (MWh);  23.669;  21.263;  19.804;  19.187;  18.774;  18.666;  20.321;  22.565;  24.720;  25.838;  \
    # 26.405;  26.603;  26.194;  25.455;  23.956;  24.020;  24.041;  24.599;  26.224;  28.132;  27.617;  26.571;  \
    # 24.909;  24.664;
    # ;;;;;;;;;;;;;;;;;;;;;;;;;'

    df = MarginalPriceFileReader().get_data_from_file(filename=filename)
    assert pd.isna(df.iloc[0]["H24"]), "H24 should be NaN."


def test_day_with_25_hours():
    folder = os.path.join(os.path.dirname(__file__), "InputTesting")
    filename = os.path.join(folder, "PrecioMD_OMIE_20223010.txt")

    # File contains
    #';1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20;21;22;23;24;25;
    # ;;;;;;;;;;;;;;;;;;;;;;;;;'

    df = MarginalPriceFileReader().get_data_from_file(filename=filename)
    assert not pd.isna(df.iloc[0]["H25"]), "H24 should not be NaN."


def test_20030802():
    folder = os.path.join(os.path.dirname(__file__), "InputTesting")
    filename = os.path.join(folder, "PMD_20030802.txt")

    # File contains
    # ;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20;21;22;23;24;
    # Precio marginal (Cent/kWh);  4,553;  3,700;  2,955;  2,607;  2,406;  2,206;  2,089;  2,089;  2,647;  3,956;  \
    # 4,662;  4,934;  5,096;  5,149;  5,000;  4,934;  4,900;  4,908;  4,908;  4,908;  4,800;  5,149;  5,309;  4,934;
    # Demanda+bombeos (MWh);  24.623;  22.721;  22.019;  21.657;  21.307;  20.919;  20.989;  20.889;  21.350;  22.025;\
    # 24.378;  25.414;  25.873;  25.947;  25.103;  24.215;  23.711;  23.506;  23.437;  23.406;  23.543;  24.854;  \
    # 25.507;  24.181;
    # ;;;;;;;;;;;;;;;;;;;;;;;;
    input = MarginalPriceFileReader().get_data_from_file(filename=filename)
    concepts = list(input["CONCEPT"])

    assert (
        str(DataTypeInMarginalPriceFile.ENERGY_IBERIAN) in concepts
    ), "{} has to be one of the concepts read".format(
        DataTypeInMarginalPriceFile.ENERGY_IBERIAN
    )
    assert (
        str(DataTypeInMarginalPriceFile.PRICE_SPAIN) in concepts
    ), "{} has to be one of the concepts read".format(
        DataTypeInMarginalPriceFile.PRICE_SPAIN
    )


def test_20040101():
    folder = os.path.join(os.path.dirname(__file__), "InputTesting")
    filename = os.path.join(folder, "PMD_20040101.txt")

    # File contains
    # OMEL - Mercado de electricidad;Fecha Emisión :31/12/2003 - 10:23;;01/01/2004;Precio del mercado diario (cent/kWh)\
    # ;;;;
    #
    # ;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20;21;22;23;24;
    # Precio marginal (Cent/kWh);  2,899;  2,823;  2,548;  2,300;  1,654;  1,468;  1,454;  1,167;  0,757;  0,287;  \
    # 1,001;  0,937;  1,127;  1,217;  1,197;  1,012;  0,917;  1,022;  1,468;  2,101;  2,101;  2,300;  2,101;  2,300;
    # Demanda+bombeos (MWh);  21.704;  20.248;  18.415;  16.699;  15.449;  14.677;  14.539;  14.390;  14.596;  14.739;\
    # 14.908;  16.360;  16.826;  16.855;  17.001;  16.914;  16.666;  17.398;  18.787;  20.146;  20.512;  20.935;\
    # 20.381;  20.493;
    # ;;;;;;;;;;;;;;;;;;;;;;;;;
    #

    df = MarginalPriceFileReader().get_data_from_file(filename=filename)

    prices = [
        10 * x
        for x in [
            2.899,
            2.823,
            2.548,
            2.300,
            1.654,
            1.468,
            1.454,
            1.167,
            0.757,
            0.287,
            1.001,
            0.937,
            1.127,
            1.217,
            1.197,
            1.012,
            0.917,
            1.022,
            1.468,
            2.101,
            2.101,
            2.300,
            2.101,
            2.300,
        ]
    ]

    for row in df.itertuples():
        if row.CONCEPT == str(DataTypeInMarginalPriceFile.PRICE_SPAIN):
            for i, v in enumerate(prices):
                assert is_equal_float(prices[i], float(row[i + 3]), tolerance=1e-6), (
                    "Data is corrupt: " + row.CONCEPT + " (H" + f"{i + 1:01})"
                )


def test_20040101_from_response():
    # File contains
    # OMEL - Mercado de electricidad;Fecha Emisión :31/12/2003 - 10:23;;01/01/2004;Precio del mercado diario (cent/kWh)\
    # ;;;;
    #
    # ;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20;21;22;23;24;
    # Precio marginal (Cent/kWh);  2,899;  2,823;  2,548;  2,300;  1,654;  1,468;  1,454;  1,167;  0,757;  0,287;  \
    # 1,001;  0,937;  1,127;  1,217;  1,197;  1,012;  0,917;  1,022;  1,468;  2,101;  2,101;  2,300;  2,101;  2,300;
    # Demanda+bombeos (MWh);  21.704;  20.248;  18.415;  16.699;  15.449;  14.677;  14.539;  14.390;  14.596;  14.739;\
    # 14.908;  16.360;  16.826;  16.855;  17.001;  16.914;  16.666;  17.398;  18.787;  20.146;  20.512;  20.935;\
    # 20.381;  20.493;
    # ;;;;;;;;;;;;;;;;;;;;;;;;;
    #

    prices = [
        10 * x
        for x in [
            2.899,
            2.823,
            2.548,
            2.300,
            1.654,
            1.468,
            1.454,
            1.167,
            0.757,
            0.287,
            1.001,
            0.937,
            1.127,
            1.217,
            1.197,
            1.012,
            0.917,
            1.022,
            1.468,
            2.101,
            2.101,
            2.300,
            2.101,
            2.300,
        ]
    ]

    from OMIEData.Downloaders.marginal_price_downloader import MarginalPriceDownloader

    responses = list(
        MarginalPriceDownloader().url_responses(
            date_ini=dt.date(2004, 1, 1), date_end=dt.date(2004, 1, 1)
        )
    )

    df = MarginalPriceFileReader().get_data_from_response(response=responses[0])

    for row in df.itertuples():
        if row.CONCEPT == str(DataTypeInMarginalPriceFile.PRICE_SPAIN):
            for i, v in enumerate(prices):
                assert is_equal_float(prices[i], float(row[i + 3]), tolerance=1e-6), (
                    "Data is corrupt: " + row.CONCEPT + " (H" + f"{i + 1:01})"
                )


def run_all_tests():
    import warnings

    test_functions = [
        test_all_keys_in_df,
        test_check_correct_values,
        test_dump_to_dataframe,
        test_day_with_23_hours,
        test_20030802,
        test_20040101,
    ]
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=FutureWarning)
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        for test_func in [test_functions]:
            try:
                test_func()
            except (AssertionError, UnicodeDecodeError, TypeError, IndexError) as e:
                print(f"{test_func.__name__} failed: {e}")
                raise e


if __name__ == "__main__":
    run_all_tests()
