import os

import numpy as np
import pandas as pd

from OMIEData.Enums.all_enums import DataTypeInMarginalPriceFile, Frequency
from OMIEData.FileReaders.marginal_price_file_reader import MarginalPriceFileReader
from OMIEData.FileReaders.energy_by_technology_files_reader import (
    EnergyByTechnologyHourlyFileReader,
)

FOLDER = os.path.join(os.path.dirname(__file__), "InputTesting")
MARGINAL_QUARTER = "PrecioMD_OMIE_20251015.txt"   # post-cutover, 96 quarter periods
MARGINAL_HOURLY = "PMD_20060101.txt"              # pre-cutover, 24 hourly periods
ENERGY_QUARTER = "EnergyByTechnology_9_20251015.TXT"   # post-cutover, 96 rows
ENERGY_PERIODO_HOURLY = "EnergyByTechnology_9_20250915.TXT"  # pre-cutover, 'Periodo', 24 rows

TOL = 1e-4


def _price_spain(df: pd.DataFrame) -> pd.Series:
    return df.loc[df.CONCEPT == str(DataTypeInMarginalPriceFile.PRICE_SPAIN)].iloc[0]


def test_marginal_quarter_96():
    df = MarginalPriceFileReader(frequency=Frequency.QUARTERLY).get_data_from_file(
        os.path.join(FOLDER, MARGINAL_QUARTER)
    )
    assert "H96" in df.columns, "quarterly output must expose all 96 periods"
    row = _price_spain(df)
    assert abs(row["H1"] - 118.28) < TOL   # first quarter (H1Q1)
    assert not pd.isna(row["H96"])         # last quarter present, not truncated


def test_marginal_quarter_precutover():
    df = MarginalPriceFileReader(frequency=Frequency.QUARTERLY).get_data_from_file(
        os.path.join(FOLDER, MARGINAL_HOURLY)
    )
    assert len(df) == 0, "no quarter-hour data exists before 2025-10-01"


def test_marginal_hourly_mean():
    df = MarginalPriceFileReader(
        frequency=Frequency.HOURLY, derive_hourly_from_quarters=True
    ).get_data_from_file(os.path.join(FOLDER, MARGINAL_QUARTER))
    row = _price_spain(df)
    # H1 is the mean of the first four quarters (118.28, 117.8, 115.01, 113.07)
    assert abs(row["H1"] - 116.04) < TOL
    assert "H26" not in df.columns


def test_marginal_hourly_optin():
    df = MarginalPriceFileReader(frequency=Frequency.HOURLY).get_data_from_file(
        os.path.join(FOLDER, MARGINAL_QUARTER)
    )
    assert len(df) == 0, "post-cutover hourly needs explicit derive_hourly_from_quarters"


def test_marginal_hourly_native():
    df = MarginalPriceFileReader().get_data_from_file(os.path.join(FOLDER, MARGINAL_HOURLY))
    row = _price_spain(df)
    assert abs(row["H1"] - 66.94) < TOL   # backward-compatible historical behavior


def test_energy_quarter_96():
    df = EnergyByTechnologyHourlyFileReader(frequency=Frequency.QUARTERLY).get_data_from_file(
        os.path.join(FOLDER, ENERGY_QUARTER)
    )
    assert len(df) == 96
    assert "QUARTER" in df.columns
    assert list(df.columns).count("QUARTER") == 1
    assert len(df.columns) == len(set(df.columns))
    assert abs(df.iloc[0]["NUCLEAR"] - 4906.9) < TOL


def test_energy_hourly_mean():
    df = EnergyByTechnologyHourlyFileReader(
        frequency=Frequency.HOURLY, derive_hourly_from_quarters=True
    ).get_data_from_file(os.path.join(FOLDER, ENERGY_QUARTER))
    assert len(df) == 24
    assert "QUARTER" not in df.columns
    assert abs(df.iloc[0]["NUCLEAR"] - 4906.9) < TOL   # mean of 4 identical quarters


def test_energy_hourly_optin():
    df = EnergyByTechnologyHourlyFileReader(frequency=Frequency.HOURLY).get_data_from_file(
        os.path.join(FOLDER, ENERGY_QUARTER)
    )
    assert len(df) == 0


def test_energy_periodo():
    # OMIE renamed 'Hora' -> 'Periodo'; this hourly file must still parse (independent fix).
    df = EnergyByTechnologyHourlyFileReader().get_data_from_file(
        os.path.join(FOLDER, ENERGY_PERIODO_HOURLY)
    )
    assert len(df) == 24
    assert "HOUR" in df.columns
    assert abs(df.iloc[0]["NUCLEAR"] - 6451.0) < TOL
