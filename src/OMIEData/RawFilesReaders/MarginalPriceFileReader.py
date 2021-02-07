import datetime as dt
import re
import locale
from enum import Enum, auto

########################################################################################################################
from typing import List

class EnergyDataType(Enum):

    PRICE_SPAIN = auto()
    PRICE_PORTUGAL = auto()
    ENERGY_IBERIAN = auto()
    ENERGY_IBERIAN_WITH_BILLATERAL = auto()

    __dict_concept_str__ = {PRICE_SPAIN: 'PRICE_SP',
                            PRICE_PORTUGAL: 'PRICE_PT',
                            ENERGY_IBERIAN: 'ENER_IB',
                            ENERGY_IBERIAN_WITH_BILLATERAL: 'ENER_IB_BILLAT'}

    def __str__(self):
        return self.__dict_concept_str__[self.value]
########################################################################################################################


########################################################################################################################
class MarginalPriceFileReader:

    # Static or class variables
    __dic_static_concepts__ = {'Precio marginal (Cent/kWh)': [EnergyDataType.PRICE_SPAIN, 10.0],
                               'Precio marginal (EUR/MWh)': [EnergyDataType.PRICE_SPAIN, 1.0],
                               'Precio marginal en el sistema español (Cent/kWh)': [EnergyDataType.PRICE_SPAIN, 10.0],
                               'Precio marginal en el sistema español (EUR/MWh)': [EnergyDataType.PRICE_SPAIN, 1.0],
                               'Precio marginal en el sistema portugués (Cent/kWh)': [EnergyDataType.PRICE_PORTUGAL, 10.0],
                               'Precio marginal en el sistema portugués (EUR/MWh)': [EnergyDataType.PRICE_PORTUGAL, 1.0],
                               'Demanda+bombeos (MWh)': [EnergyDataType.ENERGY_IBERIAN, 1.0],
                               'Energía en el programa resultante de la casación (MWh)': [EnergyDataType.ENERGY_IBERIAN, 1.0],
                               'Energía total del mercado Ibérico (MWh)': [EnergyDataType.ENERGY_IBERIAN, 1.0],
                               'Energía total con bilaterales del mercado Ibérico (MWh)': [EnergyDataType.ENERGY_IBERIAN_WITH_BILLATERAL, 1.0]}

    __key_list_retrieve__ = ['DATE', 'CONCEPT',
                             'H1', 'H2', 'H3', 'H4','H5', 'H6','H7', 'H8','H9','H10',
                             'H11', 'H12','H13', 'H14','H15', 'H16','H17', 'H18','H19','H20',
                             'H21', 'H22','H23', 'H24']

    __dateFormatInFile__ = '%d/%m/%Y'
    __localeInFile__ = "en_DK.UTF-8"

    __all_types__ = [EnergyDataType.PRICE_SPAIN, EnergyDataType.PRICE_PORTUGAL,
                     EnergyDataType.ENERGY_IBERIAN, EnergyDataType.ENERGY_IBERIAN_WITH_BILLATERAL]

    ####################################################################################################################
    def __init__(self, filename: str, types=None):
        self.filename = filename
        self.conceptsToLoad = MarginalPriceFileReader.__all_types__ if not types else types
    ####################################################################################################################

    ####################################################################################################################
    @staticmethod
    def getKeys():
        return MarginalPriceFileReader.__key_list_retrieve__
    ####################################################################################################################

    ####################################################################################################################
    def dataGenerator(self):

        # Method yield each dictionary one by one
        file = open(self.filename, 'r')

        # from first line we get the units and the price date. We just look at the date
        line = file.readline()
        matches = re.findall('\d\d/\d\d/\d\d\d\d', line)
        if not (len(matches) == 2):
            print('File ' + self.filename + ' does not have the expected format.')
        else:
            # The second date is the one we want
            date = dt.datetime.strptime(matches[1], MarginalPriceFileReader.__dateFormatInFile__).date()

            # Process all the lines
            while line:
                # read following line
                line = file.readline()
                splits = line.split(sep=';')
                firstCol = splits[0]

                if firstCol in MarginalPriceFileReader.__dic_static_concepts__.keys():
                    conceptType = MarginalPriceFileReader.__dic_static_concepts__[firstCol][0]

                    if conceptType in self.conceptsToLoad:
                        units = MarginalPriceFileReader.__dic_static_concepts__[firstCol][1]

                        yield MarginalPriceFileReader.__processLine__(
                            date=date, concept=conceptType, values=splits[1:], multiplier=units)
    ####################################################################################################################

    ####################################################################################################################
    @staticmethod
    def __processLine__(date: dt.date, concept: EnergyDataType, values: list, multiplier=1.0) -> dict:

        keylist = MarginalPriceFileReader.__key_list_retrieve__

        result = dict.fromkeys(MarginalPriceFileReader.getKeys())
        result[keylist[0]] = date
        result[keylist[1]] = str(concept)

        # These are the correct setting to read the files...
        locale.setlocale(locale.LC_NUMERIC, MarginalPriceFileReader.__localeInFile__)

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
    ####################################################################################################################

# End class
####################################################################################################################
