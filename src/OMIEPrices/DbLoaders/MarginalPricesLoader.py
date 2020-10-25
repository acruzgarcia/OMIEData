import sqlite3 as sqlite3
import datetime as dt
import fnmatch
import re
import os
import locale

####################################################################################################################
class MarginalPricesLoader:

    sqlite_conn: sqlite3.Connection
    folder_name: str
    file_mask: str

    str_line_price_old = 'Precio marginal (Cent/kWh)'
    str_line_price_new_spain = 'Precio marginal en el sistema español (EUR/MWh)'
    str_line_price_new_pt = 'Precio marginal en el sistema portugués (EUR/MWh)'

    key_list_table = ['DATE','COUNTRY',
                      'H1', 'H2','H1', 'H2','H3', 'H4','H5', 'H6','H7', 'H8','H9', 'H10',
                      'H11', 'H12','H13', 'H14','H15', 'H16','H17', 'H18','H19', 'H20',
                      'H21', 'H22','H23', 'H24']

    dateFormatInFile = '%d/%m/%Y'
    localeInFile = "en_DK.UTF-8"

    ####################################################################################################################
    def __init__(self, sqlitedb_name: str, folder_name: str, file_mask: str):
        self.folder_name = folder_name
        self.file_mask = file_mask

        # Do the conection with the DB
        self.sqlite_conn = sqlite3.connect(sqlitedb_name)
    ####################################################################################################################

    ####################################################################################################################
    def processFile(self, filename: str) -> list:

        # dictionary of dictionaries
        result = list()

        with open(filename, 'r') as file:
            # from first line we get the units and the price date.
            line = file.readline()
            matches = re.findall('\d\d/\d\d/\d\d\d\d', line)
            if not (len(matches) == 2):
                print('File ' + filename + ' does not have the expected format.')
                return result
            else:
                # The second date is the one we want
                dateprice = dt.datetime.strptime(matches[1],self.dateFormatInFile)

                # Process all the lines
                while line:
                    # read following line
                    line = file.readline()
                    splits = line.split(sep=';')
                    if splits[0] == self.str_line_price_old:
                        res = self.processLine(dateprice=dateprice, country='ESP', line=line, multiplier = 10.0)
                        result.append(res)
                    elif splits[0] == self.str_line_price_new_spain:
                        res = self.processLine(dateprice=dateprice, country='ESP', line=line, multiplier=1.0)
                        result.append(res)
                    elif splits[0] == self.str_line_price_new_pt:
                        res = self.processLine(dateprice=dateprice, country='PT', line=line, multiplier=1.0)
                        result.append(res)

        return result
    ####################################################################################################################

    ####################################################################################################################
    def processLine(self, dateprice: dt.datetime, country: str, line: str, multiplier = 1.0) -> dict:

        result = dict.fromkeys(self.key_list_table)

        splits = line.split(sep=';')
        result['DATE'] = dateprice
        result['COUNTRY'] = country

        locale.setlocale(locale.LC_NUMERIC, self.localeInFile)
        for i in range(1, 25):
            result['H' + f'{i:01}'] = multiplier * locale.atof(splits[i])

        return result
    ####################################################################################################################

    ####################################################################################################################
    def loadDataIntoDB(self) -> int:

        # Get the files in self.folder_name that matches the pattern
        mask = self.file_mask.replace('DD','*').replace('MM','*').replace('YYYYY','*')
        files = [f for f in os.listdir(self.folder_name) if fnmatch.fnmatch(f,mask)]

        # Process every file matching the criteria
        for f in files:
            lt = self.processFile(filename=f)

            for elem in lt:
                # Insert into table
                print(elem)
        return 0

# End class GeneralOMIEDownloader
####################################################################################################################
