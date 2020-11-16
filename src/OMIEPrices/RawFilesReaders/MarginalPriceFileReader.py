import datetime as dt
import re
import locale

from enum import Enum, auto

class ConceptType(Enum):

    PRICE_SPAIN = auto()
    PRICE_PORTUGAL = auto()
    ENERGY_IBERIAN = auto()
    ENERGY_IBERIAN_WITH_BILLATERAL = auto()

####################################################################################################################
class MarginalPriceFileReader:

    filename: str

    # string -> [concept , multplier]
    _dic_static_concepts_ = {'Precio marginal (Cent/kWh)': [ConceptType.PRICE_SPAIN, 10.0],
                             'Precio marginal (EUR/MWh)': [ConceptType.PRICE_SPAIN, 1.0],
                             'Precio marginal en el sistema español (Cent/kWh)': [ConceptType.PRICE_SPAIN, 10.0],
                             'Precio marginal en el sistema español (EUR/MWh)': [ConceptType.PRICE_SPAIN, 1.0],
                             'Precio marginal en el sistema portugués (Cent/kWh)': [ConceptType.PRICE_PORTUGAL, 10.0],
                             'Precio marginal en el sistema portugués (EUR/MWh)': [ConceptType.PRICE_PORTUGAL, 1.0],
                             'Demanda+bombeos (MWh)': [ConceptType.ENERGY_IBERIAN, 1.0],
                             'Energía en el programa resultante de la casación (MWh)': [ConceptType.ENERGY_IBERIAN, 1.0],
                             'Energía total del mercado Ibérico (MWh)': [ConceptType.ENERGY_IBERIAN, 1.0],
                             'Energía total con bilaterales del mercado Ibérico (MWh)': [ConceptType.ENERGY_IBERIAN_WITH_BILLATERAL, 1.0]}

    _key_list_retrieve_ = ['DATE', 'CONCEPT',
                           'H1', 'H2', 'H3', 'H4','H5', 'H6','H7', 'H8','H9','H10',
                           'H11', 'H12','H13', 'H14','H15', 'H16','H17', 'H18','H19','H20',
                           'H21', 'H22','H23', 'H24']

    _dict_concept_str_ = {ConceptType.PRICE_SPAIN: 'PRICE_SP',
                          ConceptType.PRICE_PORTUGAL: 'PRICE_PT',
                          ConceptType.ENERGY_IBERIAN: 'ENER_IB',
                          ConceptType.ENERGY_IBERIAN_WITH_BILLATERAL: 'ENER_IB_BILLAT'}

    _dateFormatInFile_ = '%d/%m/%Y'
    _localeInFile_ = "en_DK.UTF-8"

    ####################################################################################################################
    def __init__(self, filename: str):
        self.filename = filename
    ####################################################################################################################

    ####################################################################################################################
    def getKeys(self):
        return self._key_list_retrieve_
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
            date = dt.datetime.strptime(matches[1], self._dateFormatInFile_).date()

            # Process all the lines
            while line:
                # read following line
                line = file.readline()
                splits = line.split(sep=';')
                firstCol = splits[0]

                if firstCol in self._dic_static_concepts_.keys():

                    conceptType = self._dic_static_concepts_[firstCol][0]
                    units = self._dic_static_concepts_[firstCol][1]

                    yield self._processLine_(date=date,concept=conceptType, values=splits[1:], multiplier=units)

    ####################################################################################################################

    ####################################################################################################################
    def _processLine_(self, date: dt.date, concept: ConceptType, values: list, multiplier = 1.0) -> dict:

        result = dict.fromkeys(self.getKeys())
        result[self._key_list_retrieve_[0]] = date
        result[self._key_list_retrieve_[1]] = self._dict_concept_str_[concept]

        # These are the correct setting to read the files...
        locale.setlocale(locale.LC_NUMERIC, self._localeInFile_)

        for i, v in enumerate(values, start=1):
            if i > 24:
                break # Jump if 25-hour day or spaces ..
            try:
                f = multiplier * locale.atof(v)
            except:
                if i == 24:
                    # Day with 23-hours.
                    result[self._key_list_retrieve_[25]] = result[self._key_list_retrieve_[24]]
                else:
                    raise
            else:
                result[self._key_list_retrieve_[i+1]] = f

        return result
    ####################################################################################################################

# End class
####################################################################################################################
