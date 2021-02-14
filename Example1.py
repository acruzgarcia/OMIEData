# This is a sample Python script.
import matplotlib.pyplot as plt
import datetime as dt

from OMIEData.RawFilesReaders.OMIEFilesReader import OMIEFilesReader
from OMIEData.Downloaders.MarginalPriceDownloader import MarginalPriceDownloader
from OMIEData.RawFilesReaders.MarginalPriceFileReader import MarginalPriceFileReader
from OMIEData.RawFilesReaders.EnergyDataTypes import EnergyDataType


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    workingFolder = r'C:\tmp'

    # download the files
    dateIni = dt.datetime(2012, 3, 11)
    dateEnd = dt.datetime(2012, 12, 31)
    downloader = MarginalPriceDownloader(output_folder=workingFolder)
    #error = downloader.downloadData(dateIni=dateIni, dateEnd=dateEnd)

    df = OMIEFilesReader(absolutePath=workingFolder,
                         fileReader=MarginalPriceFileReader()).readToDataFrame(verbose=False)
    df.sort_values(by='DATE', axis=0, inplace=True)
    print(df)

    # Just spanish prices
    str_price_spain = str(EnergyDataType.PRICE_SPAIN)
    dfPrices = df[df.CONCEPT == str_price_spain]

    plt.plot(dfPrices.DATE, dfPrices.H12)
    plt.plot(dfPrices.DATE, dfPrices.H23)
    plt.show()

    str_energy_ib = str(EnergyDataType.ENERGY_IBERIAN)
    dfEnergy = df[df.CONCEPT == str_energy_ib]
    plt.plot(dfEnergy.DATE, dfEnergy.H12)
    plt.show()

    plt.hist(dfPrices.H12, bins=50)
