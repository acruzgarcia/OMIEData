import datetime as dt
import re
from babel.numbers import parse_decimal, NumberFormatError
import pandas as pd
import numpy as np

from requests import Response
from OMIEData.Enums.all_enums import DataTypeInMarginalPriceFile, Frequency
from OMIEData.FileReaders.omie_file_reader import OMIEFileReader


class MarginalPriceFileReader(OMIEFileReader):

    # Static or class variables
    __dic_static_concepts__ = {
        'Precio marginal (Cent/kWh)':
            [DataTypeInMarginalPriceFile.PRICE_SPAIN, 10.0],
        'Precio marginal (EUR/MWh)':
            [DataTypeInMarginalPriceFile.PRICE_SPAIN, 1.0],
        'Precio marginal en el sistema español (Cent/kWh)':
            [DataTypeInMarginalPriceFile.PRICE_SPAIN, 10.0],
        'Precio marginal en el sistema español (EUR/MWh)':
            [DataTypeInMarginalPriceFile.PRICE_SPAIN, 1.0],
        'Precio marginal en el sistema portugués (Cent/kWh)':
            [DataTypeInMarginalPriceFile.PRICE_PORTUGAL, 10.0],
        'Precio marginal en el sistema portugués (EUR/MWh)':
            [DataTypeInMarginalPriceFile.PRICE_PORTUGAL, 1.0],
        'Demanda+bombeos (MWh)':
            [DataTypeInMarginalPriceFile.ENERGY_IBERIAN, 1.0],
        'Energía en el programa resultante de la casación (MWh)':
            [DataTypeInMarginalPriceFile.ENERGY_IBERIAN, 1.0],
        'Energía total del mercado Ibérico (MWh)':
            [DataTypeInMarginalPriceFile.ENERGY_IBERIAN, 1.0],
        'Energía total con bilaterales del mercado Ibérico (MWh)':
            [DataTypeInMarginalPriceFile.ENERGY_IBERIAN_WITH_BILLATERAL, 1.0]}

    __key_list_retrieve__ = ['DATE', 'CONCEPT',
                             'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10',
                             'H11', 'H12', 'H13', 'H14', 'H15', 'H16', 'H17', 'H18', 'H19', 'H20',
                             'H21', 'H22', 'H23', 'H24', 'H25']

    __dateFormatInFile__ = '%d/%m/%Y'
    __localeInFile__ = "en_DK.UTF-8"
    __quarters_per_hour__ = 4

    def __init__(self, types=None, frequency: Frequency = Frequency.HOURLY,
                 derive_hourly_from_quarters: bool = False):
        self.conceptsToLoad = [v for v in DataTypeInMarginalPriceFile] if not types else types
        self.frequency = frequency
        self.derive_hourly_from_quarters = derive_hourly_from_quarters

    def get_keys(self):
        if self.frequency == Frequency.QUARTERLY:
            return ['DATE', 'CONCEPT'] + [f'H{i}' for i in range(1, 101)]
        return MarginalPriceFileReader.__key_list_retrieve__

    @staticmethod
    def _is_quarter_hour(text: str) -> bool:
        return 'H1Q1' in text

    def get_data_from_response(self, response: Response) -> pd.DataFrame:
        return self._read(response.text, source=response.url)

    def get_data_from_file(self, filename: str) -> pd.DataFrame:
        with open(filename, 'r', encoding='latin-1') as file:
            text = file.read()
        return self._read(text, source=filename)

    def _read(self, text: str, source: str) -> pd.DataFrame:
        res = pd.DataFrame(columns=self.get_keys())

        lines = text.split("\n")
        matches = re.findall(r'\d\d/\d\d/\d\d\d\d', lines.pop(0))
        if len(matches) != 2:
            print('Source ' + str(source) + ' does not have the expected format.')
            return res

        # The second date is the one we want
        date = dt.datetime.strptime(matches[1], self.__dateFormatInFile__).date()
        is_quarter = self._is_quarter_hour(text)

        if self.frequency == Frequency.QUARTERLY and not is_quarter:
            return res
        if self.frequency == Frequency.HOURLY and is_quarter and not self.derive_hourly_from_quarters:
            return res

        for line in lines:
            splits = line.split(sep=';')
            concept = self.__dic_static_concepts__.get(splits[0])
            if concept is None:
                continue
            concept_type, units = concept
            if concept_type not in self.conceptsToLoad:
                continue
            dico = self._process_line(date=date, concept=concept_type, values=splits[1:],
                                      is_quarter=is_quarter, multiplier=units)
            res = pd.concat([res, pd.DataFrame([dico])], ignore_index=True)

        return res

    def _process_line(self, date: dt.date, concept: DataTypeInMarginalPriceFile,
                      values: list, is_quarter: bool, multiplier=1.0) -> dict:

        result = dict.fromkeys(self.get_keys())
        result['DATE'] = date
        result['CONCEPT'] = str(concept)

        parsed = []
        for v in values:
            if v.strip() == '':
                continue
            try:
                parsed.append(multiplier * float(parse_decimal(v, locale=self.__localeInFile__)))
            except (NumberFormatError, ValueError):
                parsed.append(np.nan)

        if is_quarter and self.frequency == Frequency.HOURLY:
            parsed = self._quarters_to_hourly(parsed)

        for i, value in enumerate(parsed, start=1):
            result[f'H{i}'] = value

        return result

    @classmethod
    def _quarters_to_hourly(cls, values: list) -> list:
        step = cls.__quarters_per_hour__
        hourly = []
        for start in range(0, len(values), step):
            block = [x for x in values[start:start + step]
                     if not (isinstance(x, float) and np.isnan(x))]
            hourly.append(float(np.mean(block)) if block else np.nan)
        return hourly
