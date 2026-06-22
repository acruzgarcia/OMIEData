import unicodedata
from io import BytesIO

import pandas as pd
from requests import Response

from OMIEData.FileReaders.omie_file_reader import OMIEFileReader
from OMIEData.Enums.all_enums import TechnologyType


def _strip_accents(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    )


class EnergyByTechnologyHourlyFileReader(OMIEFileReader):

    def __init__(self, types=None):

        self.conceptsToLoad = [v for v in TechnologyType] if not types else types

        self._dict_column_concept = {'Fecha': 'DATE',
                                     'Hora': 'HOUR',
                                     'Periodo': 'HOUR',
                                     'CARBÓN': 'COAL',
                                     'FUEL-GAS': 'FUEL_GAS',
                                     'AUTOPRODUCTOR': 'SELF_PRODUCER',
                                     'NUCLEAR': 'NUCLEAR',
                                     'HIDRÁULICA': 'HYDRO',
                                     'CICLO COMBINADO': 'COMBINED_CYCLE',
                                     'EÓLICA': 'WIND',
                                     'SOLAR TÉRMICA': 'THERMAL_SOLAR',
                                     'SOLAR FOTOVOLTAICA': 'PHOTOVOLTAIC_SOLAR',
                                     'COGENERACIÓN/RESIDUOS/MINI HIDRA': 'RESIDUALS',
                                     'IMPORTACIÓN INTER.': 'IMPORT',
                                     'IMPORTACIÓN INTER. SIN MIBEL': 'IMPORT_WITHOUT_MIBEL',
                                     'ALMACENAMIENTO': 'STORAGE',
                                     'HIBRIDACIÓN': 'HYBRIDIZATION'}

    def get_keys(self) -> list:

        key_list_retrieve = ['DATE', 'HOUR']
        key_list_retrieve.extend([str(v) for v in self.conceptsToLoad])
        return key_list_retrieve

    def get_data_from_response(self, response: Response) -> pd.DataFrame:
        return self._get_data_from_file_like(file_like=BytesIO(response.content))

    def get_data_from_file(self, filename: str) -> pd.DataFrame:
        return self._get_data_from_file_like(file_like=filename)

    def _get_data_from_file_like(self, file_like) -> pd.DataFrame:

        df = pd.read_csv(file_like, sep=';', skiprows=2, header=0, encoding='latin-1', skipfooter=1,
                         engine='python', decimal=",", thousands='.')
        df = df.loc[:, ~df.columns.str.startswith("Unnamed")]

        norm_mapping = {_strip_accents(k).lower(): v for k, v in self._dict_column_concept.items()}
        rename_map = {}
        for col in df.columns:
            col_norm = _strip_accents(col.strip()).lower()
            if col_norm in norm_mapping:
                rename_map[col] = norm_mapping[col_norm]
        df = df.rename(columns=rename_map)

        expected = [k for k in self.get_keys() if k in df.columns]
        for extra in ("STORAGE", "HYBRIDIZATION"):
            if extra in df.columns and extra not in expected:
                expected.append(extra)
        df = df[expected]

        return df
