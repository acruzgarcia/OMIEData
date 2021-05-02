# This is a sample Python script.
import datetime as dt

from OMIEData.DataImport.omie_data_importer_from_folder import OMIEDataImporterFromFolder
from OMIEData.Downloaders.energy_by_technology_downloader import EnergyByTechnologyDownloader
from OMIEData.Downloaders.energy_by_technology_downloader import SystemType
from OMIEData.FileReaders.data_types_energy_by_technology import DataTypesEnergyByTechnologyFile
from OMIEData.FileReaders.energy_by_technology_files_reader import EnergyByTechnologyHourlyFileReader

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # download the files
    dateIni = dt.datetime(2020, 6, 1)
    dateEnd = dt.datetime(2020, 10, 30)
    downloader = EnergyByTechnologyDownloader(SystemType.IBERIAN)

    # This can take time, it is downloading the files from the website..
    workingFolder = r'C:\tmp'
    error = downloader.download_data(date_ini=dateIni, date_end=dateEnd, output_folder=workingFolder)

    dataTypes = [DataTypesEnergyByTechnologyFile.NUCLEAR, DataTypesEnergyByTechnologyFile.COMBINED_CYCLE]
    fileReader = EnergyByTechnologyHourlyFileReader(types=dataTypes)

    df = OMIEDataImporterFromFolder(absolute_path=workingFolder,
                                    file_reader=fileReader).read_to_dataframe(verbose=False)
    df.sort_values(by=['DATE', 'HOUR'], axis=0, inplace=True)
    print(df)
