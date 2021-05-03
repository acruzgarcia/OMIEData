# This is a sample Python script.
import datetime as dt
from OMIEData.DataImport.omie_marginalprice_importer import OMIEMarginalPriceImporter

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # download the files
    dateIni = dt.datetime(2012, 3, 11)
    dateEnd = dt.datetime(2012, 4, 15)

    # This can take time, it is downloading the files from the website..
    df = OMIEMarginalPriceImporter(date_ini=dateIni, date_end=dateEnd).read_to_dataframe(verbose=False)
    df.sort_values(by='DATE', axis=0, inplace=True)
    print(df)
