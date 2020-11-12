import datetime as dt
import re
import locale

####################################################################################################################
class MarginalPriceFileReader:

    filename: str

    # Private variables
    __str_line_price_old = 'Precio marginal (Cent/kWh)'
    __str_line_price_new_spain = 'Precio marginal en el sistema español (EUR/MWh)'
    __str_line_price_new_pt = 'Precio marginal en el sistema portugués (EUR/MWh)'

    __key_list_table = ['DATE','COUNTRY',
                      'H1', 'H2','H1', 'H2','H3', 'H4','H5', 'H6','H7', 'H8','H9', 'H10',
                      'H11', 'H12','H13', 'H14','H15', 'H16','H17', 'H18','H19', 'H20',
                      'H21', 'H22','H23', 'H24']

    __dateFormatInFile = '%d/%m/%Y'
    __localeInFile = "en_DK.UTF-8"

    ####################################################################################################################
    def __init__(self, filename: str):
        self.filename = filename
    ####################################################################################################################

    ####################################################################################################################
    def readPricesFile(self):

        # Method yield each dictionary one by one
        with open(self.filename, 'r') as file:

            # from first line we get the units and the price date. We just look at the date
            line = file.readline()
            matches = re.findall('\d\d/\d\d/\d\d\d\d', line)
            if not (len(matches) == 2):
                print('File ' + self.filename + ' does not have the expected format.')
            else:
                # The second date is the one we want
                dateprice = dt.datetime.strptime(matches[1],self.__dateFormatInFile)

                # Process all the lines
                while line:
                    # read following line
                    line = file.readline()
                    splits = line.split(sep=';')
                    if splits[0] == self.__str_line_price_old:
                        yield self.__processLine__(dateprice=dateprice, country='ESP', line=line, multiplier = 10.0)
                    elif splits[0] == self.__str_line_price_new_spain:
                        yield self.__processLine__(dateprice=dateprice, country='ESP', line=line, multiplier=1.0)
                    elif splits[0] == self.__str_line_price_new_pt:
                        yield self.__processLine__(dateprice=dateprice, country='PT', line=line, multiplier=1.0)

    ####################################################################################################################

    ####################################################################################################################
    def __processLine__(self, dateprice: dt.datetime, country: str, line: str, multiplier = 1.0) -> dict:

        result = dict.fromkeys(self.__key_list_table)

        splits = line.split(sep=';')
        result['DATE'] = dateprice
        result['COUNTRY'] = country

        locale.setlocale(locale.LC_NUMERIC, self.__localeInFile)
        for i in range(1, 25):
            result['H' + f'{i:01}'] = multiplier * locale.atof(splits[i])

        return result
    ####################################################################################################################

# End class GeneralOMIEDownloader
####################################################################################################################
