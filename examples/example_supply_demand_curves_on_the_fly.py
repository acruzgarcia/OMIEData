# This is a sample Python script.
import datetime as dt
from OMIEData.DataImport.omie_supply_demand_curve_importer import OMIESupplyDemandCurvesImporter

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    dateIni = dt.datetime(2020, 6, 1)
    dateEnd = dt.datetime(2020, 6, 1)
    hour = 1

    # This can take time, it is downloading the files from the website..
    df = OMIESupplyDemandCurvesImporter(date_ini=dateIni, date_end=dateEnd, hour=hour).read_to_dataframe(verbose=True)
    df.sort_values(by=['DATE', 'HOUR'], axis=0, inplace=True)
    print(df)
