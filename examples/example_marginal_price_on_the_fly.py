# This is a sample Python script.
import datetime as dt
from OMIEData.DataImport.omie_marginalprice_importer import OMIEMarginalPriceFileImporter

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    import matplotlib.pyplot as plt
    from OMIEData.Enums.all_enums import DataTypeInMarginalPriceFile

    # download the files
    dateIni = dt.datetime(2020, 1, 1)
    dateEnd = dt.datetime(2022, 3, 22)

    # This can take time, it is downloading the files from the website..
    df = OMIEMarginalPriceFileImporter(date_ini=dateIni, date_end=dateEnd).read_to_dataframe(verbose=True)
    df.sort_values(by='DATE', axis=0, inplace=True)
    print(df)

    # Just spanish prices
    str_price_spain = str(DataTypeInMarginalPriceFile.PRICE_SPAIN)
    dfPrices = df[df.CONCEPT == str_price_spain]

    plt.figure()
    plt.plot(dfPrices.DATE, dfPrices.H12, label='H12')
    plt.plot(dfPrices.DATE, dfPrices.H23, label='H23')
    plt.legend()
    plt.show()
