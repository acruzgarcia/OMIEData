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

    # Possible lines to recognize
    # Prices
    _str_line_price_old_cE_ = 'Precio marginal (Cent/kWh)'
    _str_line_price_old_E_ = 'Precio marginal (EUR/MWh)'
    _str_line_price_new_spain_cE_ = 'Precio marginal en el sistema español (Cent/kWh)'
    _str_line_price_new_spain_E_ = 'Precio marginal en el sistema español (EUR/MWh)'
    _str_line_price_new_pt_cE_ = 'Precio marginal en el sistema portugués (Cent/kWh)'
    _str_line_price_new_pt_E_ = 'Precio marginal en el sistema portugués (EUR/MWh)'

    # Energy
    _str_line_energy_old_ = 'Energía en el programa resultante de la casación (MWh)'
    _str_line_energy_new_iber_ = 'Energía total del mercado Ibérico (MWh)'
    _str_line_energy_new_iber_with_bilaterals_ = 'Energía total con bilaterales del mercado Ibérico (MWh)'

    _key_list_retrieve_ = ['DATE', 'CONCEPT',
                       'H1', 'H2', 'H3', 'H4','H5', 'H6','H7', 'H8','H9','H10',
                       'H11', 'H12','H13', 'H14','H15', 'H16','H17', 'H18','H19','H20',
                       'H21', 'H22','H23', 'H24']

    _dict_concept_str = {ConceptType.PRICE_SPAIN: 'PRICE_SP',
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

                if firstCol == self._str_line_price_old_cE_:
                    yield self._processLine_(date=date, concept=ConceptType.PRICE_SPAIN, line=line, multiplier=10.0)
                if firstCol == self._str_line_price_old_E_:
                    yield self._processLine_(date=date, concept=ConceptType.PRICE_SPAIN, line=line, multiplier=1.0)
                elif firstCol == self._str_line_price_new_spain_cE_:
                    yield self._processLine_(date=date, concept=ConceptType.PRICE_SPAIN, line=line, multiplier=10.0)
                elif firstCol == self._str_line_price_new_spain_E_:
                    yield self._processLine_(date=date, concept=ConceptType.PRICE_SPAIN, line=line, multiplier=1.0)
                elif firstCol == self._str_line_price_new_pt_cE_:
                    yield self._processLine_(date=date, concept=ConceptType.PRICE_PORTUGAL, line=line, multiplier=10.0)
                elif firstCol == self._str_line_price_new_pt_E_:
                    yield self._processLine_(date=date, concept=ConceptType.PRICE_PORTUGAL, line=line, multiplier=1.0)
                elif firstCol == self._str_line_energy_old_:
                    yield self._processLine_(date=date, concept=ConceptType.ENERGY_IBERIAN, line=line, multiplier=1.0)
                elif firstCol == self._str_line_energy_new_iber_:
                    yield self._processLine_(date=date, concept=ConceptType.ENERGY_IBERIAN, line=line, multiplier=1.0)
                elif firstCol == self._str_line_energy_new_iber_with_bilaterals_:
                    yield self._processLine_(date=date, concept=ConceptType.ENERGY_IBERIAN_WITH_BILLATERAL, line=line,
                                             multiplier=1.0)
    ####################################################################################################################

    ####################################################################################################################
    def _processLine_(self, date: dt.date, concept: ConceptType, line: str, multiplier = 1.0) -> dict:

        result = dict.fromkeys(self.getKeys())
        result['DATE'] = date
        result['CONCEPT'] = self._dict_concept_str[concept]

        # These are the correct setting to read the files...
        locale.setlocale(locale.LC_NUMERIC, self._localeInFile_)

        splits = line.split(sep=';')
        splits = splits[1:] # first split contains the description
        for i, v in enumerate(splits, start=1):
            if i > 24:
                # Jump if 25-hour day or spaces ..
                break
            try:
                f = multiplier * locale.atof(v)
            except:
                if i == 24:
                    # Day with 23-hours.
                    result['H24'] = result['H23']
                else:
                    raise
            else:
                result['H' + f'{i:01}'] = f

        return result
    ####################################################################################################################

# End class
####################################################################################################################
