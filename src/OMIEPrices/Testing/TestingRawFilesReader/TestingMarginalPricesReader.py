import datetime as dt
from RawFilesReaders.MarginalPriceFileReader import MarginalPriceFileReader
import os
import pandas as pd

########################################################################################################################
def AllKeysInDictionary():

    folder = os.path.abspath('InputTesting')
    filename = os.path.join(folder,'PMD_20060101.txt')
    reader = MarginalPriceFileReader(filename=filename)
    keys = reader.getKeys()

    data = list(reader.dataGenerator())

    # data is list of dictionaries
    for dictionary in data:
        for k in keys:
            assert dictionary[k], 'Key: ' + k + ' not found.'
########################################################################################################################

########################################################################################################################
def DumpToDataFrame():

    folder = os.path.abspath('InputTesting')
    filename = os.path.join(folder,'PMD_20060101.txt')
    reader = MarginalPriceFileReader(filename=filename)

    keys = reader.getKeys()
    #print(keys)
    df = pd.DataFrame(columns=keys)

    for row in reader.dataGenerator():
        #print(row)
        df.append(row, ignore_index=True)

    # show dataframe
    #print(df)
########################################################################################################################


# Unoffical testing ....
if __name__ == '__main__':

    # run the tests, they will fill if they do not pass
    AllKeysInDictionary()
    print('AllKeysInDictionary() passed.')

    DumpToDataFrame()
    print('DumpToDataFrame() passed.')

    #folder = r'F:\OMIEPrices\proj\OMIEPrices\src\OMIEPrices\TestingRawFilesReader\InputTesting'
    #reader = MarginalPriceFileReader(filename=os.path.join(folder, 'PMD_20060101.txt'))
