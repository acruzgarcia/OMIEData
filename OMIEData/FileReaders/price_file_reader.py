import datetime as dt
import re
import locale
import pandas as pd

from requests import Response
from OMIEData.FileReaders.data_types_marginal_price_file import DataTypesMarginalPriceFile
from OMIEData.FileReaders.omie_file_reader import OMIEFileReader


class PriceFileReader(OMIEFileReader):

    # Static or class variables
    __dic_static_concepts__ = {
        'Precio marginal (Cent/kWh)':
            [DataTypesMarginalPriceFile.PRICE_SPAIN, 10.0],
        'Precio marginal (EUR/MWh)':
            [DataTypesMarginalPriceFile.PRICE_SPAIN, 1.0],
        'Precio marginal en el sistema español (Cent/kWh)':
            [DataTypesMarginalPriceFile.PRICE_SPAIN, 10.0],
        'Precio marginal en el sistema español (EUR/MWh)':
            [DataTypesMarginalPriceFile.PRICE_SPAIN, 1.0],
        'Precio marginal en el sistema portugués (Cent/kWh)':
            [DataTypesMarginalPriceFile.PRICE_PORTUGAL, 10.0],
        'Precio marginal en el sistema portugués (EUR/MWh)':
            [DataTypesMarginalPriceFile.PRICE_PORTUGAL, 1.0],
        'Demanda+bombeos (MWh)':
            [DataTypesMarginalPriceFile.ENERGY_IBERIAN, 1.0],
        'Energía en el programa resultante de la casación (MWh)':
            [DataTypesMarginalPriceFile.ENERGY_IBERIAN, 1.0],
        'Energía total del mercado Ibérico (MWh)':
            [DataTypesMarginalPriceFile.ENERGY_IBERIAN, 1.0],
        'Energía total con bilaterales del mercado Ibérico (MWh)':
            [DataTypesMarginalPriceFile.ENERGY_IBERIAN_WITH_BILLATERAL, 1.0]}

    __key_list_retrieve__ = ['DATE', 'CONCEPT',
                             'H1', 'H2', 'H3', 'H4','H5', 'H6','H7', 'H8','H9','H10',
                             'H11', 'H12','H13', 'H14','H15', 'H16','H17', 'H18','H19','H20',
                             'H21', 'H22','H23', 'H24']

    __dateFormatInFile__ = '%d/%m/%Y'
    __localeInFile__ = "en_DK.UTF-8"

    def __init__(self, types=None):
        self.conceptsToLoad = [v for v in DataTypesMarginalPriceFile] if not types else types

    def get_keys(self):
        return PriceFileReader.__key_list_retrieve__

    def get_data_from_response(self, response: Response) -> pd.DataFrame:

        res = pd.DataFrame(columns=self.get_keys())

        # from first line we get the units and the price date. We just look at the date
        lines = response.text.split("\n")
        matches = re.findall('\d\d/\d\d/\d\d\d\d', lines.pop(0))
        if not (len(matches) == 2):
            print('Response ' + response.url + ' does not have the expected format.')
        else:
            # The second date is the one we want
            date = dt.datetime.strptime(matches[1], PriceFileReader.__dateFormatInFile__).date()

            # Process all the lines

            while lines:
                # read following line
                line = lines.pop(0)
                splits = line.split(sep=';')
                first_col = splits[0]

                if first_col in PriceFileReader.__dic_static_concepts__.keys():
                    concept_type = PriceFileReader.__dic_static_concepts__[first_col][0]

                    if concept_type in self.conceptsToLoad:
                        units = PriceFileReader.__dic_static_concepts__[first_col][1]

                        dico = self._process_line(date=date, concept=concept_type, values=splits[1:], multiplier=units)
                        res = res.append(dico, ignore_index=True)

            return res

    def get_data_from_file(self, filename: str) -> pd.DataFrame:

        # Method yield each dictionary one by one
        res = pd.DataFrame(columns=self.get_keys())
        file = open(filename, 'r')

        # from first line we get the units and the price date. We just look at the date
        line = file.readline()
        matches = re.findall('\d\d/\d\d/\d\d\d\d', line)
        if not (len(matches) == 2):
            print('File ' + filename + ' does not have the expected format.')
        else:
            # The second date is the one we want
            date = dt.datetime.strptime(matches[1], PriceFileReader.__dateFormatInFile__).date()

            # Process all the lines
            while line:
                # read following line
                line = file.readline()
                splits = line.split(sep=';')
                first_col = splits[0]

                if first_col in PriceFileReader.__dic_static_concepts__.keys():
                    concept_type = PriceFileReader.__dic_static_concepts__[first_col][0]

                    if concept_type in self.conceptsToLoad:
                        units = PriceFileReader.__dic_static_concepts__[first_col][1]

                        dico = self._process_line(date=date, concept=concept_type, values=splits[1:], multiplier=units)
                        res = res.append(dico, ignore_index=True)

            return res

    def _process_line(self, date: dt.date, concept: DataTypesMarginalPriceFile, values: list, multiplier=1.0) -> dict:

        keylist = PriceFileReader.__key_list_retrieve__

        result = dict.fromkeys(self.get_keys())
        result[keylist[0]] = date
        result[keylist[1]] = str(concept)

        # These are the correct setting to read the files...
        locale.setlocale(locale.LC_NUMERIC, PriceFileReader.__localeInFile__)

        for i, v in enumerate(values, start=1):
            if i > 24:
                break # Jump if 25-hour day or spaces ..
            try:
                f = multiplier * locale.atof(v)
            except:
                if i == 24:
                    # Day with 23-hours.
                    result[keylist[25]] = result[keylist[24]]
                else:
                    raise
            else:
                result[keylist[i + 1]] = f

        return result
