# This is a sample Python script.
from RawFilesReaders.MarginalPriceReader import MarginalPriceReader
from Downloaders.MarginalPriceDownloader import MarginalPriceDownloader
import matplotlib.pyplot as plt
import datetime as dt
import os

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    isDownloaded = True
    workingFolder = r'F:\OMIEPrices\DataStore\PreciosMD'

    # download the files
    if not isDownloaded:

        dateIni = dt.datetime(2000, 1, 1)
        dateEnd = dt.datetime(2014, 12, 31)
        downloader = MarginalPriceDownloader(output_folder=workingFolder)
        error = downloader.downloadData(dateIni=dateIni, dateEnd=dateEnd)

    df = MarginalPriceReader(absolutePath=workingFolder).readToDataFrame(verbose=False)
    df.sort_values(by='DATE',axis=0, inplace=True)
    print(df)

    # Just spanish prices
    dfPrices = df[df.CONCEPT == 'PRICE_SP']
    dfEnergy = df[df.CONCEPT == 'ENER_IB']

    plt.plot(dfPrices.DATE, dfPrices.H12)
    plt.plot(dfPrices.DATE, dfPrices.H23)
    plt.show()

    plt.plot(dfEnergy.DATE, dfEnergy.H12)
    plt.show()

    plt.hist(dfPrices.H12, bins=50)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
