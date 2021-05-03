import datetime as dt

from OMIEData.DataImport.omie_data_importer_from_responses import OMIEDataImporterFromResponses
from OMIEData.Downloaders.energy_by_technology_downloader import EnergyByTechnologyDownloader
from OMIEData.FileReaders.energy_by_technology_files_reader import EnergyByTechnologyHourlyFileReader
from OMIEData.Downloaders.energy_by_technology_downloader import SystemType


class OMIEEnergyByTechnologyImporter(OMIEDataImporterFromResponses):

    def __init__(self, date_ini: dt.date, date_end: dt.date, system_type: SystemType):

        super().__init__(date_ini=date_ini,
                         date_end=date_end,
                         file_downloader=EnergyByTechnologyDownloader(system=system_type),
                         file_reader=EnergyByTechnologyHourlyFileReader())
