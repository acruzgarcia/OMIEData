# This is a sample Python script.
import matplotlib.pyplot as plt
import datetime as dt

from OMIEData.DataImport.omie_data_importer_from_folder import OMIEDataImporterFromFolder
from OMIEData.Downloaders.marginal_price_downloader import MarginalPriceDownloader
from OMIEData.FileReaders.marginal_price_file_reader import MarginalPriceFileReader
from OMIEData.FileReaders.data_types_marginal_price_file import DataTypesMarginalPriceFile

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    workingFolder = r'C:\tmp'

    # download the files
    dateIni = dt.datetime(2012, 3, 11)
    dateEnd = dt.datetime(2012, 12, 31)

    # This can take time, it is downloading the files from the website..
    error = MarginalPriceDownloader().download_data(date_ini=dateIni, date_end=dateEnd, output_folder=workingFolder)

    dataTypes = [DataTypesMarginalPriceFile.PRICE_SPAIN, DataTypesMarginalPriceFile.ENERGY_IBERIAN]
    fileReader = MarginalPriceFileReader(types=dataTypes)
    df = OMIEDataImporterFromFolder(absolute_path=workingFolder,
                                    file_reader=fileReader).read_to_dataframe(verbose=False)
    df.sort_values(by='DATE', axis=0, inplace=True)
    print(df)

    # Just spanish prices
    plt.figure()
    str_price_spain = str(DataTypesMarginalPriceFile.PRICE_SPAIN)
    dfPrices = df[df.CONCEPT == str_price_spain]

    plt.plot(dfPrices.DATE, dfPrices.H12)
    plt.plot(dfPrices.DATE, dfPrices.H23)
    plt.show()

    plt.figure()
    str_energy_ib = str(DataTypesMarginalPriceFile.ENERGY_IBERIAN)
    dfEnergy = df[df.CONCEPT == str_energy_ib]
    plt.plot(dfEnergy.DATE, dfEnergy.H12)
    plt.show()
