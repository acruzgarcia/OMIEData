import datetime as dt
from RawFilesReaders.MarginalPriceFileReader import MarginalPriceFileReader
import os
import filecmp

########################################################################################################################
def Test1():

    folderOut = os.path.abspath('OutputTesting')
    filename = os.path.join(folderOut, 'PMD_20090601.txt')
    reader = MarginalPriceFileReader(filename=filename)

    out = reader.readPricesFile()
########################################################################################################################

# Unoffical testing ....
if __name__ == '__main__':

    # run the tests, they will fill if they do not pass
    Test1()
    print('Test1() passed.')