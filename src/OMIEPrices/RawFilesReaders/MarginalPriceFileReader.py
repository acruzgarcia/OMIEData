import datetime as dt
import re
import locale

####################################################################################################################
class MarginalPriceFileReader:

    filename: str

    # Private variables
    __str_line_price_old__cE__ = 'Precio marginal (Cent/kWh)'
    __str_line_price_old__E__ = 'Precio marginal (EUR/MWh)'
    __str_line_price_new_spain_cE__ = 'Precio marginal en el sistema español (Cent/kWh)'
    __str_line_price_new_spain_E__ = 'Precio marginal en el sistema español (EUR/MWh)'
    __str_line_price_new_pt__cE__ = 'Precio marginal en el sistema portugués (Cent/kWh)'
    __str_line_price_new_pt__E__ = 'Precio marginal en el sistema portugués (EUR/MWh)'

    __key_list_table__ = ['DATE', 'COUNTRY',
                      'H1', 'H2','H1', 'H2','H3', 'H4','H5', 'H6','H7', 'H8','H9', 'H10',
                      'H11', 'H12','H13', 'H14','H15', 'H16','H17', 'H18','H19', 'H20',
                      'H21', 'H22','H23', 'H24']

    __dateFormatInFile__ = '%d/%m/%Y'
    __localeInFile__ = "en_DK.UTF-8"

    ####################################################################################################################
    def __init__(self, filename: str):
        self.filename = filename
    ####################################################################################################################

    ####################################################################################################################
    def getPriceKeys(self, filename: str):
        return self.__key_list_table__

    ####################################################################################################################

    ####################################################################################################################
    def pricesGenerator(self):

        # Method yield each dictionary one by one
        file = open(self.filename, 'r')

        # from first line we get the units and the price date. We just look at the date
        line = file.readline()
        matches = re.findall('\d\d/\d\d/\d\d\d\d', line)
        if not (len(matches) == 2):
            print('File ' + self.filename + ' does not have the expected format.')
        else:
            # The second date is the one we want
            dateprice = dt.datetime.strptime(matches[1], self.__dateFormatInFile__)

            # Process all the lines
            while line:
                # read following line
                line = file.readline()
                splits = line.split(sep=';')
                if splits[0] == self.__str_line_price_old__cE__:
                    yield self.__processLine__(dateprice=dateprice, country='ESP', line=line, multiplier=10.0)
                if splits[0] == self.__str_line_price_old__E__:
                    yield self.__processLine__(dateprice=dateprice, country='ESP', line=line, multiplier=1.0)
                elif splits[0] == self.__str_line_price_new_spain_cE__:
                    yield self.__processLine__(dateprice=dateprice, country='ESP', line=line, multiplier=10.0)
                elif splits[0] == self.__str_line_price_new_spain_E__:
                    yield self.__processLine__(dateprice=dateprice, country='ESP', line=line, multiplier=1.0)
                elif splits[0] == self.__str_line_price_new_pt__cE__:
                    yield self.__processLine__(dateprice=dateprice, country='PT', line=line, multiplier=10.0)
                elif splits[0] == self.__str_line_price_new_pt__E__:
                    yield self.__processLine__(dateprice=dateprice, country='PT', line=line, multiplier=1.0)

    ####################################################################################################################

    ####################################################################################################################
    def __processLine__(self, dateprice: dt.datetime, country: str, line: str, multiplier = 1.0) -> dict:

        result = dict.fromkeys(self.__key_list_table__)

        splits = line.split(sep=';')
        result['DATE'] = dateprice
        result['COUNTRY'] = country

        locale.setlocale(locale.LC_NUMERIC, self.__localeInFile__)
        for i in range(1, 25):
            result['H' + f'{i:01}'] = multiplier * locale.atof(splits[i])

        return result
    ####################################################################################################################

# End class GeneralOMIEDownloader
####################################################################################################################
