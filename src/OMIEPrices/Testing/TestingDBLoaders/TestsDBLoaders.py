import os
from DbLoaders.MarginalPricesLoader import MarginalPricesLoader

########################################################################################################################
def Test1():

    # Testing PMDs
    #folder = os.path.abspath('InputForTesting')
    folder = 'F:\\OMIEPrices\\proj\\OMIEPrices\\src\\OMIEPrices\\TestingDBLoaders\\InputForTesting'
    mask = 'PMD_YYYYMMDD.txt'
    file = 'PMD_20060120.txt'

    databasename = os.path.join(folder, 'TestDatabase.db')
    loader = MarginalPricesLoader(sqlitedb_name=databasename,
                                  folder_name=folder,
                                  file_mask=mask)

    r = loader.processFile(filename=os.path.join(folder,file))




########################################################################################################################


# Unoffical testing ....
if __name__ == '__main__':

    # run the tests, they will fill if they do not pass
    Test1()
