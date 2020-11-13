import datetime as dt
from RawFilesReaders.MarginalPriceFileReader import MarginalPriceFileReader
from RawFilesReaders.MarginalPriceDumper import MarginalPriceDumper
import os
import Testing.UtilTest as UtilTest

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
def CheckCorrectValues():

    folder = os.path.abspath('InputTesting')
    filename = os.path.join(folder,'PMD_20060101.txt')

    # File contains
    #'Precio marginal (Cent/kWh);  6,694;  4,888;  4,525;  4,371;  3,870;  3,777;  3,611;  1,000;  0,500;  1,000;  1,000;\
    #  1,954;  3,755;  3,777;  3,777;  3,755;  3,755;  3,755;  4,788;  5,600;  6,725;  7,001;  6,637;  7,617;
    #' Energía en el programa resultante de la casación (MWh);  26.377;  26.070;  24.916;  23.761;  22.814;  22.116;  \
    #21.415;  20.712;  19.438;  19.699;  20.583;  21.119;  21.741;  22.264;  22.359;  21.763;  21.463;  21.610;  23.872;\
    #  24.322;  24.993;  25.064;  24.792;  25.373;'

    data = list(MarginalPriceFileReader(filename=filename).dataGenerator())

    assert UtilTest.isEqualFloat(data[0]['H7'], 36.11, tolerance=1e-3), 'Data is corrupted'
    assert UtilTest.isEqualFloat(data[1]['H9'], 19438, tolerance=1e-3), 'Data is corrupted'

########################################################################################################################

########################################################################################################################
def DumpToDataframe():

    dumper = MarginalPriceDumper(absolutePath=os.path.abspath('InputTesting'))
    df = dumper.readToDataFrame()

    # show dataframe
    #print(df)

    # 2006-1-1 file
    value = float(df.loc[(df.DATE == dt.date(2006, 1, 1)) & (df.CONCEPT == 'PRICE_SP'), 'H1'])
    assert UtilTest.isEqualFloat(value, 66.94, tolerance=1e-6), 'Data is corrupt'

    value = float(df.loc[(df.DATE == dt.date(2006, 1, 1)) & (df.CONCEPT == 'ENER_IB'), 'H23'])
    assert UtilTest.isEqualFloat(value, 24792, tolerance=1e-6), 'Data is corrupt'

    # 2009-6-1 file
    value = float(df.loc[(df.DATE == dt.date(2009, 6, 1)) & (df.CONCEPT == 'PRICE_PT'), 'H2'])
    assert UtilTest.isEqualFloat(value, 37.60, tolerance=1e-6), 'Data is corrupt'

    slice = df.loc[(df.DATE == dt.date(2009, 6, 1)) & (df.CONCEPT == 'ENER_IB'), :]
    energies = {'H1': 28325.8, 'H2': 26201.2, 'H3': 24651.6, 'H4': 23788.6, 'H5': 23565.4,
                'H6': 24149.6, 'H7': 26386.0, 'H8': 29016.5, 'H9': 33149.4, 'H10': 36289.9,
                'H11': 38527.1, 'H12': 39362.9, 'H13': 40102.1, 'H14': 39556.3, 'H15': 37944.9,
                'H16': 37503.3, 'H17': 37355.8, 'H18': 37310.8, 'H19': 36740.7, 'H20': 36079.6,
                'H21': 36029.6, 'H22': 37617.5, 'H23': 37147.9, 'H24': 33897.1}
    for k, v in energies.items():
        assert UtilTest.isEqualFloat(v, float(slice.get(k)), tolerance=1e-6), 'Data is corrupt'

    # 2020-10-22 file
    slice = df.loc[(df.DATE == dt.date(2020, 10, 22)) & (df.CONCEPT == 'ENER_IB_BILLAT'), :]
    energies = [29435.7, 27853.8, 27293.8, 26948.5, 26871.7, 27047.6, 28605.8, 31899.4, 33804.2,
                35118.1, 35916.7, 36518.3, 37036.5, 37006.9, 36251.2, 35312.6, 34689.7, 34358.7,
                33956.2, 35138.1, 37878.5, 36955.3, 33874.5, 30856.7]
    for i, v in enumerate(energies):
        assert UtilTest.isEqualFloat(energies[i], float(slice.get('H' + f'{i + 1:01}')),
                                     tolerance=1e-6), 'Data is corrupt'

    slice = df.loc[(df.DATE == dt.date(2020, 10, 22)) & (df.CONCEPT == 'PRICE_SP'), :]
    prices = [39.55, 35.00, 33.07, 32.68, 32.68, 33.08, 40.11, 47.13, 49.53,
              52.49, 52.43, 50.44, 49.08, 47.50, 46.58, 45.95, 46.11, 48.49,
              50.68, 56.63, 53.56, 49.04, 47.20, 46.30]
    for i, v in enumerate(prices):
        assert UtilTest.isEqualFloat(prices[i], float(slice.get('H' + f'{i + 1:01}')),
                                     tolerance=1e-6), 'Data is corrupt'
########################################################################################################################


# Unoffical testing ....
if __name__ == '__main__':

    # run the tests, they will fill if they do not pass
    AllKeysInDictionary()
    print('AllKeysInDictionary() passed.')

    CheckCorrectValues()
    print('DumpToDataFrame() passed.')

    DumpToDataframe()
    print('TestingDumper() passed.')
