import datetime as dt
from RawFilesReaders.MarginalPriceFileReader import MarginalPriceFileReader
import os
import filecmp

########################################################################################################################
def AllKeysInDictionary():

    folder = os.path.abspath('InputTesting')
    filename = os.path.join(folder,'PMD_20060101.txt')
    reader = MarginalPriceFileReader(filename=filename)

    prices = list(reader.pricesGenerator())

    keys = ['DATE', 'COUNTRY',
            'H1', 'H2', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10',
            'H11', 'H12', 'H13', 'H14', 'H15', 'H16', 'H17', 'H18', 'H19', 'H20',
            'H21', 'H22', 'H23', 'H24']

    for dictionary in prices:
        thekeys = list(dictionary.keys())
        for k in keys:
            assert dictionary[k], 'Key: ' + k + ' not found.'

########################################################################################################################

# Unoffical testing ....
if __name__ == '__main__':

    # run the tests, they will fill if they do not pass
    AllKeysInDictionary()
    print('Test1() passed.')