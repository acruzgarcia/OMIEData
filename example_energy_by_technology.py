# This is a sample Python script.
import datetime as dt

from OMIEData.RawFilesReaders.omie_files_reader import OMIEFilesReader
from OMIEData.Downloaders.energy_by_technology_downloader import EnergyByTechnologyDownloader
from OMIEData.Downloaders.energy_by_technology_downloader import SystemType
from OMIEData.RawFilesReaders.data_types_energy_by_technology import DataTypesEnergyByTechnologyFile
from OMIEData.RawFilesReaders.energy_by_technology_files_reader import EnergyByTechnologyHourlyFileReader

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    workingFolder = r'C:\tmp'

    # download the files
    dateIni = dt.datetime(2020, 6, 1)
    dateEnd = dt.datetime(2020, 10, 30)
    downloader = EnergyByTechnologyDownloader(SystemType.IBERIAN, output_folder=workingFolder)

    # This can take time, it is downloading the files from the website..
    error = downloader.download_data(dateIni=dateIni, dateEnd=dateEnd)

    dataTypes = [DataTypesEnergyByTechnologyFile.NUCLEAR, DataTypesEnergyByTechnologyFile.COMBINED_CYCLE]
    fileReader = EnergyByTechnologyHourlyFileReader(types=dataTypes)

    df = OMIEFilesReader(absolute_path=workingFolder,
                         file_reader=fileReader).read_to_dataframe(verbose=False)
    df.sort_values(by=['DATE', 'HOUR'], axis=0, inplace=True)
    print(df)

