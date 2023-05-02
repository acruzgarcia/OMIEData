# This is a sample Python script.
import datetime as dt
from OMIEData.DataImport.omie_energy_by_technology_importer import OMIEEnergyByTechnologyImporter
from OMIEData.Enums.all_enums import SystemType

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    dateIni = dt.datetime(2020, 6, 1)
    dateEnd = dt.datetime(2020, 7, 30)
    system_type = SystemType.SPAIN

    # This can take time, it is downloading the files from the website..
    df = OMIEEnergyByTechnologyImporter(date_ini=dateIni,
                                        date_end=dateEnd,
                                        system_type=system_type).read_to_dataframe(verbose=True)
    df.sort_values(by=['DATE', 'HOUR'], axis=0, inplace=True)
    print(df)
