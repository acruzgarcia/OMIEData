import pandas as pd
import locale
from requests import Response
from io import BytesIO

from OMIEData.FileReaders.omie_file_reader import OMIEFileReader


class SupplyDemandCurvesReader(OMIEFileReader):

    def __init__(self):

        self._dict_column_concept = {'Fecha': 'DATE',
                                     'Hora': 'HOUR',
                                     'Pais': 'COUNTRY',
                                     'Unidad': 'UNIT',
                                     'Tipo Oferta': 'OFFER_TYPE',
                                     'Energía Compra/Venta': 'ENERGY',
                                     'Precio Compra/Venta': 'PRICE',
                                     'Ofertada (O)/Casada (C)': 'MATCHED'}

    def get_keys(self) -> list:
        return list(self._dict_column_concept.values())

    def get_data_from_response(self, response: Response) -> pd.DataFrame:

        locale.setlocale(locale.LC_NUMERIC, "en_DK.UTF-8")
        return self._get_data_from_file_like(file_like=BytesIO(response.content))

    def get_data_from_file(self, filename: str) -> pd.DataFrame:

        locale.setlocale(locale.LC_NUMERIC, "en_DK.UTF-8")
        return self._get_data_from_file_like(file_like=filename)

    def _get_data_from_file_like(self, file_like) -> pd.DataFrame:

        locale.setlocale(locale.LC_NUMERIC, "en_DK.UTF-8")
        df = pd.read_csv(file_like, sep=';', skiprows=2, header=0, encoding='latin-1', skipfooter=1, engine='python',
                         decimal=",", thousands='.')
        df = df.rename({k: v for k, v in self._dict_column_concept.items()}, axis=1)
        df = df[[x for x in self.get_keys()]]

        return df
